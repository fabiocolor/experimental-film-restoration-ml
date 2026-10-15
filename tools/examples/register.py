"""Line the result up with the source before a comparison video is built.

A source clip and a result clip rarely sit on the same pixels: the result may be a different size, carry a
few pixels of border, or start a frame or two later. measure() samples both clips, finds the frame offset
and the affine map between them, and returns a result crop and start time that land on the source exactly.

    sc, rc, res_start, report = measure(src, sc, res, rc, start, dur, fps)

sc / rc are (x, y, w, h) crops in each clip's own pixels. Luminance is what gets matched (a recovered
shot keeps the scan's brightness), so a faded source and a colour result still register.
"""
import cv2
import numpy as np

WORK_W = 960


def _open(path):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError(f'cannot open {path}')
    return cap, cap.get(cv2.CAP_PROP_FPS), int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


def _grab(cap, idx):
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, idx))
    ok, f = cap.read()
    return cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) if ok else None


def _prep(g, crop, size):
    x, y, w, h = crop
    g = g[y:y + h, x:x + w]
    g = cv2.resize(g, size, interpolation=cv2.INTER_AREA).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), 1.0)
    return g


def _edges(g):
    e = np.sqrt(cv2.Sobel(g, cv2.CV_32F, 1, 0) ** 2 + cv2.Sobel(g, cv2.CV_32F, 0, 1) ** 2)
    return (e - e.mean()).astype(np.float32)


def _response(a, b, win):
    return cv2.phaseCorrelate(_edges(a), _edges(b), win)[1]


def measure(src, sc, res, rc, start, dur, fps=None, samples=9, max_k=8):
    """Returns (src_crop, res_crop, res_start, report). res_start is in seconds in the result clip."""
    cs, fs, ns = _open(src)
    cr, fr, nr = _open(res)
    fps = fps or fs
    size = (WORK_W, int(round(WORK_W * sc[3] / sc[2])) // 2 * 2)
    win = cv2.createHanningWindow(size, cv2.CV_32F)
    i0 = int(round(start * fs))
    j0 = int(round(start * fr))
    n = int(dur * fs)
    rel = np.linspace(max_k + 1, max(max_k + 2, n - max_k - 2), samples).astype(int)
    # 1. frame offset: the k for which res[j0 + t*fr/fs + k] best matches src[i0 + t]
    ks = []
    pairs = []
    for t in rel:
        a = _grab(cs, i0 + t)
        if a is None:
            continue
        a = _prep(a, sc, size)
        best = None
        jb = j0 + int(round(t * fr / fs))
        for k in range(-max_k, max_k + 1):   # max_k=0 locks the timing (source and result from the same file)
            b = _grab(cr, jb + k)
            if b is None:
                continue
            r = _response(a, _prep(b, rc, size), win)
            if best is None or r > best[1]:
                best = (k, r, b)
        ks.append(best[0])
        pairs.append((a, _prep(best[2], rc, size)))
    k = int(np.median(ks))
    half = len(ks) // 2
    drift = int(np.median(ks[half:]) - np.median(ks[:half])) if len(ks) > 3 else 0
    # 2. affine map src_work -> res_work (ECC), averaged over the samples that converge
    warps = []
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    for a, b in pairs:
        W = np.eye(2, 3, dtype=np.float32)
        try:
            # coarse first at quarter size, then full
            a4, b4 = cv2.resize(a, None, fx=0.25, fy=0.25), cv2.resize(b, None, fx=0.25, fy=0.25)
            cv2.findTransformECC(a4, b4, W, cv2.MOTION_AFFINE, crit, None, 5)
            W[:, 2] *= 4
            cv2.findTransformECC(a, b, W, cv2.MOTION_AFFINE, crit, None, 5)
            warps.append(W.copy())
        except cv2.error:
            pass
    if not warps:
        raise RuntimeError('ECC did not converge on any sample')
    W = np.median(np.stack(warps), axis=0)
    # 3. the src crop's corners, mapped into the result clip's own pixels
    def to_res(px, py):
        wx, wy = W @ np.array([px, py, 1.0])
        return rc[0] + wx * rc[2] / size[0], rc[1] + wy * rc[3] / size[1]
    x0, y0 = to_res(0, 0)
    x1, y1 = to_res(size[0], size[1])
    # if the result does not hold the whole source crop, keep the part both have: shrink the source crop too
    RW, RH = int(cr.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cr.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cx0, cy0, cx1, cy1 = max(0.0, x0), max(0.0, y0), min(float(RW), x1), min(float(RH), y1)
    new_sc = sc
    if (cx0, cy0, cx1, cy1) != (x0, y0, x1, y1):
        fx, fy = sc[2] / (x1 - x0), sc[3] / (y1 - y0)   # result px -> source px along each axis (affine, near-axis-aligned)
        sx0, sy0 = sc[0] + (cx0 - x0) * fx, sc[1] + (cy0 - y0) * fy
        sx1, sy1 = sc[0] + (cx1 - x0) * fx, sc[1] + (cy1 - y0) * fy
        new_sc = (int(round(sx0)), int(round(sy0)), int(round(sx1 - sx0)) // 2 * 2, int(round(sy1 - sy0)) // 2 * 2)
    new_rc = (int(round(cx0)), int(round(cy0)), int(round(cx1 - cx0)) // 2 * 2, int(round(cy1 - cy0)) // 2 * 2)
    res_start = (j0 + k) / fr
    report = dict(k=k, drift=drift, ks=ks, warp=W.round(4).tolist(), sc_in=sc, sc_out=new_sc, rc_in=rc, rc_out=new_rc,
                  res_start=round(res_start, 4), fps_src=fs, fps_res=fr, ecc_ok=len(warps))
    cs.release(); cr.release()
    return new_sc, new_rc, res_start, report


if __name__ == '__main__':
    import sys, json
    src, res = sys.argv[1], sys.argv[2]
    sc = tuple(int(v) for v in sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] != '-' else None
    rc = tuple(int(v) for v in sys.argv[4].split(',')) if len(sys.argv) > 4 and sys.argv[4] != '-' else None
    start = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    dur = float(sys.argv[6]) if len(sys.argv) > 6 else 5.0
    c, f, n = _open(src)
    w, h = int(c.get(3)), int(c.get(4))
    sc = sc or (0, 0, w, h)
    c2, _, _ = _open(res)
    rc = rc or (0, 0, int(c2.get(3)), int(c2.get(4)))
    print(json.dumps(measure(src, sc, res, rc, start, dur)[3], indent=1))
