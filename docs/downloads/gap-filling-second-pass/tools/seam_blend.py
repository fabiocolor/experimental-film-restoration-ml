#!/usr/bin/env python3
"""Seam blend for overlapping generated windows: use the overlaps so the tone steps at the cuts disappear.
Needs only numpy and ffmpeg. The windows themselves are untouched.

For each cut c between window A (before) and window B (after), inside the overlap [s0, s1] both windows
rendered the same frames.  Per frame g, a per-channel tone curve C_AB(g) (A->B) is estimated by quantile
matching over a +-HALF-frame pool of same-frame pairs; C_BA is its inverse.  With a smoothstep ramp r(g)
from 0 at s0 to 1 at s1:
    A'(g) = lerp(identity, C_AB, r)(A)       B'(g) = lerp(C_BA, identity, r)(B)
so both sides reach the same intermediate tone at the cut and each window returns to its own tone at the
overlap ends (identity).  A short pixel dissolve over D frames centred on the cut then mixes A' and B'.
Geometry was matched in-inference (Q46); no warp, retime or other repair is applied.
"""
import argparse, hashlib, json, os, shutil, subprocess
from pathlib import Path
import numpy as np

W, H = 768, 432
PX0, PX1 = 88, 680   # picture columns; r16 'full560' layout: whole 768x560 picture (set in main)
Q = np.linspace(0, 100, 257)


def ffmpeg():
    exe = shutil.which('ffmpeg')
    if exe: return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def decode(path, canvas_h=H):
    """r12: windows rendered on a 768x448 canvas (8 px bars) are cropped back to the 768x432 layout; no resampling."""
    raw = subprocess.run([ffmpeg(), '-v', 'error', '-i', str(path), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         check=True, capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, canvas_h, W, 3)
    pad = (canvas_h - H) // 2
    return fr[:, pad:pad + H]


def encode(frames, path, args):
    p = subprocess.Popen([ffmpeg(), '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', '24', '-i', '-', *args, str(path)], stdin=subprocess.PIPE)
    for f in frames: p.stdin.write(np.ascontiguousarray(f).tobytes())
    p.stdin.close(); assert p.wait() == 0, path


def curve(src, dst):
    """Monotone per-channel LUT (3, 256) mapping src tone distribution onto dst (same-frame pairs pooled)."""
    lut = np.empty((3, 256), np.float64)
    for ch in range(3):
        qs = np.percentile(src[..., ch], Q); qd = np.percentile(dst[..., ch], Q)
        qs = np.maximum.accumulate(qs + np.arange(len(qs)) * 1e-6)
        lut[ch] = np.maximum.accumulate(np.interp(np.arange(256), qs, qd))
    return lut


def invert(lut):
    return np.stack([np.interp(np.arange(256), lut[ch] + np.arange(256) * 1e-6, np.arange(256.0)) for ch in range(3)])


def apply(img, lut):
    return np.stack([lut[ch][img[..., ch]] for ch in range(3)], -1)


def smooth(x):
    x = np.clip(x, 0.0, 1.0); return x * x * (3 - 2 * x)


def blend(windows, cuts, half, dissolve):
    """windows: {name: (start_global, frames)}; cuts: [(c, A, B)]; returns {g: uint8 frame} for every owned g."""
    get = lambda w, g: windows[w][1][g - windows[w][0]]
    last = lambda w: windows[w][0] + len(windows[w][1]) - 1
    owner = {}
    order = [cuts[0][1]] + [b for _, _, b in cuts]
    bounds = [windows[order[0]][0]] + [c + 1 for c, _, _ in cuts] + [last(order[-1]) + 1]
    for w, a, b in zip(order, bounds[:-1], bounds[1:]):
        for g in range(a, b): owner[g] = w
    out = {g: get(owner[g], g) for g in owner}   # uint8; only overlap frames are recomputed
    report = []
    for c, A, B in cuts:
        s0, s1 = windows[B][0], last(A)
        crop = (slice(8, H - 8, 3), slice(PX0 + 8, PX1 - 8, 3))   # tone statistics on a 1/9 pixel lattice
        for g in range(s0, s1 + 1):
            pool = range(max(s0, g - half), min(s1, g + half) + 1)
            cab = curve(np.stack([get(A, k)[crop] for k in pool]), np.stack([get(B, k)[crop] for k in pool]))
            cba = invert(cab); ident = np.tile(np.arange(256.0), (3, 1))
            r = smooth((g - s0) / (s1 - s0))
            a2 = apply(get(A, g), (1 - r) * ident + r * cab)
            b2 = apply(get(B, g), (1 - r) * cba + r * ident)
            lo, hi = c - dissolve // 2 + 1, c + dissolve - dissolve // 2
            m = smooth((g - lo + 1) / (dissolve + 1)) if lo <= g <= hi else (0.0 if g <= c else 1.0)
            out[g] = np.clip(np.rint((1 - m) * a2 + m * b2), 0, 255).astype(np.uint8)
        report.append({'cut': [c, c + 1], 'A': A, 'B': B, 'overlap': [s0, s1], 'dissolve_frames': [lo, hi],
                       'ramp_at_cut': round(float(smooth((c - s0) / (s1 - s0))), 3)})
    return out, report


def metrics(seq, cuts):
    Y = lambda f: (f[20:H - 20, PX0 + 20:PX1 - 20].astype(np.float64) @ [0.2126, 0.7152, 0.0722])
    d = lambda i: np.abs(Y(seq[i]) - Y(seq[i - 1])).mean()
    res = {}
    for c, _, _ in cuts:
        i = c + 1  # seq index i holds shot frame i (0-based), so d(c+1) = |F(c+1) - F(c)|
        res[f'{c}|{c + 1}'] = {'pop_ratio': round(float(d(i) / np.mean([d(k) for k in (i - 3, i - 2, i - 1, i + 1, i + 2, i + 3)])), 2),
                               'luma_step_5f': round(float(np.mean([Y(seq[k]).mean() for k in range(i, i + 5)]) -
                                                           np.mean([Y(seq[k]).mean() for k in range(i - 5, i)])), 1)}
    return res


def main():
    global H, PX0, PX1
    ap = argparse.ArgumentParser()
    ap.add_argument('--window', action='append', required=True, help='NAME:START:FILE:NFRAMES[:CANVAS_H]')
    ap.add_argument('--cut', action='append', required=True, help='C:A:B')
    ap.add_argument('--half', type=int, default=12); ap.add_argument('--dissolve', type=int, default=12)
    ap.add_argument('--label', default='q47'); ap.add_argument('--canvas-height', type=int, default=H)
    ap.add_argument('--layout', default='pillar592', choices=['pillar592', 'full560'])
    a = ap.parse_args()
    if a.layout == 'full560': H, PX0, PX1 = 560, 0, 768
    inp = Path(os.environ.get('INPUT_DIR') or os.environ.get('CWC_INPUT_DIR', '.'))
    outd = Path(os.environ.get('OUTPUT_DIR') or os.environ.get('CWC_OUTPUT_DIR', 'out'))
    outd.mkdir(parents=True, exist_ok=True)
    windows, src = {}, {}
    for spec in a.window:
        name, start, fname, n, *ch = spec.split(':')
        path = next(inp.rglob(fname)); src[name] = {'file': fname, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        fr = decode(path, int(ch[0]) if ch else a.canvas_height); assert len(fr) >= int(n), (name, len(fr)); windows[name] = (int(start), fr[:int(n)])
    cuts = [(int(c), A, B) for c, A, B in (s.split(':') for s in a.cut)]
    out, report = blend(windows, cuts, a.half, a.dissolve)
    blended = [out[g] for g in sorted(out)]
    hard = []
    order = [cuts[0][1]] + [b for _, _, b in cuts]; bounds = [windows[order[0]][0]] + [c + 1 for c, _, _ in cuts]
    for g in sorted(out):
        w = order[max(i for i, b in enumerate(bounds) if g >= b)]; hard.append(windows[w][1][g - windows[w][0]])
    master = outd / f'{a.label}_seamblend_{len(blended)}f_24fps_{PX1 - PX0}x{H}_ffv1.mkv'
    review = outd / f'{a.label}_seamblend_{len(blended)}f_24fps_{PX1 - PX0}x{H}.mp4'
    hardv = outd / f'{a.label}_hardcut_{len(blended)}f_24fps_{PX1 - PX0}x{H}_ffv1.mkv'
    pic = lambda fs: [f[:, PX0:PX1] for f in fs]
    global W
    W0 = W; W = PX1 - PX0
    encode(pic(blended), master, ['-c:v', 'ffv1', '-level', '3', '-pix_fmt', 'rgb24'])
    encode(pic(blended), review, ['-c:v', 'libx264', '-preset', 'slow', '-crf', '4', '-pix_fmt', 'yuv420p', '-movflags', '+faststart'])
    encode(pic(hard), hardv, ['-c:v', 'ffv1', '-level', '3', '-pix_fmt', 'rgb24'])
    W = W0
    rec = {'schema': 'q47_seam_blend_v1', 'sources': src, 'windows': {k: [v[0], v[0] + len(v[1]) - 1] for k, v in windows.items()},
           'params': {'half_pool': a.half, 'dissolve': a.dissolve}, 'cuts': report, 'frames': len(blended),
           'metrics_hardcut': metrics(hard, cuts), 'metrics_blend': metrics(blended, cuts),
           'outputs': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (master, review, hardv)}}
    (outd / f'{a.label}_seam_blend_receipt.json').write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec['metrics_hardcut']), json.dumps(rec['metrics_blend']))


if __name__ == '__main__':
    main()
