#!/usr/bin/env python3
"""Seam blend for overlapping MiniMax H3 windows at 768 × 432.

Uses the overlaps so the tone steps at the cuts disappear. Needs only numpy and
ffmpeg. The windows themselves are untouched.

For each cut c between window A (before) and window B (after), inside the overlap
[s0, s1] both windows rendered the same frames. Per frame g, a per-channel tone
curve C_AB(g) (A->B) is estimated by quantile matching over a +-HALF-frame pool of
same-frame pairs; C_BA is its inverse. With a smoothstep ramp r(g) from 0 at s0 to
1 at s1:

    A'(g) = lerp(identity, C_AB, r)(A)
    B'(g) = lerp(C_BA, identity, r)(B)

so both sides reach the same intermediate tone at the cut and each window returns
to its own tone at the overlap ends. A short pixel dissolve over D frames centred
on the cut then mixes A' and B'. Geometry is assumed already matched in the
windows; no warp or retime is applied.
"""
import argparse, hashlib, json, os, shutil, subprocess
from pathlib import Path
import numpy as np

W, H = 768, 432
Q = np.linspace(0, 100, 257)


def ffmpeg():
    exe = shutil.which('ffmpeg')
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def decode(path):
    raw = subprocess.run(
        [ffmpeg(), '-v', 'error', '-i', str(path), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def encode(frames, path, args):
    p = subprocess.Popen(
        [ffmpeg(), '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
         '-s', f'{W}x{H}', '-r', '24', '-i', '-', *args, str(path)],
        stdin=subprocess.PIPE,
    )
    for f in frames:
        p.stdin.write(np.ascontiguousarray(f).tobytes())
    p.stdin.close()
    assert p.wait() == 0, path


def curve(src, dst):
    """Monotone per-channel LUT (3, 256) mapping src tone onto dst."""
    lut = np.empty((3, 256), np.float64)
    for ch in range(3):
        qs = np.percentile(src[..., ch], Q)
        qd = np.percentile(dst[..., ch], Q)
        qs = np.maximum.accumulate(qs + np.arange(len(qs)) * 1e-6)
        lut[ch] = np.maximum.accumulate(np.interp(np.arange(256), qs, qd))
    return lut


def invert(lut):
    return np.stack([
        np.interp(np.arange(256), lut[ch] + np.arange(256) * 1e-6, np.arange(256.0))
        for ch in range(3)
    ])


def apply(img, lut):
    return np.stack([lut[ch][img[..., ch]] for ch in range(3)], -1)


def smooth(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def blend(windows, cuts, half, dissolve):
    """windows: {name: (start_global, frames)}; cuts: [(c, A, B)]."""
    get = lambda w, g: windows[w][1][g - windows[w][0]]
    last = lambda w: windows[w][0] + len(windows[w][1]) - 1
    owner = {}
    order = [cuts[0][1]] + [b for _, _, b in cuts]
    bounds = [windows[order[0]][0]] + [c + 1 for c, _, _ in cuts] + [last(order[-1]) + 1]
    for w, a, b in zip(order, bounds[:-1], bounds[1:]):
        for g in range(a, b):
            owner[g] = w
    out = {g: get(owner[g], g) for g in owner}
    report = []
    for c, A, B in cuts:
        s0, s1 = windows[B][0], last(A)
        crop = (slice(8, H - 8, 3), slice(8, W - 8, 3))
        for g in range(s0, s1 + 1):
            pool = range(max(s0, g - half), min(s1, g + half) + 1)
            cab = curve(
                np.stack([get(A, k)[crop] for k in pool]),
                np.stack([get(B, k)[crop] for k in pool]),
            )
            cba = invert(cab)
            ident = np.tile(np.arange(256.0), (3, 1))
            r = smooth((g - s0) / (s1 - s0))
            a2 = apply(get(A, g), (1 - r) * ident + r * cab)
            b2 = apply(get(B, g), (1 - r) * cba + r * ident)
            lo, hi = c - dissolve // 2 + 1, c + dissolve - dissolve // 2
            m = smooth((g - lo + 1) / (dissolve + 1)) if lo <= g <= hi else (0.0 if g <= c else 1.0)
            out[g] = np.clip(np.rint((1 - m) * a2 + m * b2), 0, 255).astype(np.uint8)
        report.append({
            'cut': [c, c + 1], 'A': A, 'B': B, 'overlap': [s0, s1],
            'dissolve_frames': [lo, hi],
            'ramp_at_cut': round(float(smooth((c - s0) / (s1 - s0))), 3),
        })
    return out, report


def metrics(seq, cuts):
    Y = lambda f: (f[40:392, 150:610].astype(np.float64) @ [0.2126, 0.7152, 0.0722])
    d = lambda i: np.abs(Y(seq[i]) - Y(seq[i - 1])).mean()
    res = {}
    for c, _, _ in cuts:
        i = c
        res[f'{c}|{c + 1}'] = {
            'pop_ratio': round(float(
                d(i) / np.mean([d(k) for k in (i - 3, i - 2, i - 1, i + 1, i + 2, i + 3)])
            ), 2),
            'luma_step_5f': round(float(
                np.mean([Y(seq[k]).mean() for k in range(i, i + 5)]) -
                np.mean([Y(seq[k]).mean() for k in range(i - 5, i)])
            ), 1),
        }
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--window', action='append', required=True, help='NAME:START_GLOBAL:SUBDIR')
    ap.add_argument('--cut', action='append', required=True, help='C:A:B')
    ap.add_argument('--half', type=int, default=12)
    ap.add_argument('--dissolve', type=int, default=12)
    ap.add_argument('--label', default='stairs')
    a = ap.parse_args()
    inp = Path(os.environ.get('CWC_INPUT_DIR', '.'))
    outd = Path(os.environ.get('CWC_OUTPUT_DIR', 'out'))
    outd.mkdir(parents=True, exist_ok=True)
    windows, src = {}, {}
    for spec in a.window:
        name, start, sub = spec.split(':')
        path = next((inp / sub).glob('*.mp4'))
        src[name] = {'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        windows[name] = (int(start), decode(path))
    cuts = [(int(c), A, B) for c, A, B in (s.split(':') for s in a.cut)]
    out, report = blend(windows, cuts, a.half, a.dissolve)
    blended = [out[g] for g in sorted(out)]
    hard = []
    order = [cuts[0][1]] + [b for _, _, b in cuts]
    bounds = [windows[order[0]][0]] + [c + 1 for c, _, _ in cuts]
    for g in sorted(out):
        w = order[max(i for i, b in enumerate(bounds) if g >= b)]
        hard.append(windows[w][1][g - windows[w][0]])
    master = outd / f'{a.label}_seamblend_f0001_f{len(blended):04d}_24fps_768x432_ffv1.mkv'
    review = outd / f'{a.label}_seamblend_f0001_f{len(blended):04d}_24fps_768x432.mp4'
    encode(blended, master, ['-c:v', 'ffv1', '-level', '3', '-pix_fmt', 'rgb24'])
    encode(blended, review, [
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '4',
        '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    ])
    rec = {
        'schema': 'stairs_seam_blend_v1',
        'sources': src,
        'windows': {k: [v[0], v[0] + len(v[1]) - 1] for k, v in windows.items()},
        'params': {'half_pool': a.half, 'dissolve': a.dissolve},
        'cuts': report,
        'frames': len(blended),
        'metrics_hardcut': metrics(hard, cuts),
        'metrics_blend': metrics(blended, cuts),
        'outputs': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (master, review)},
    }
    (outd / f'{a.label}_seam_blend_receipt.json').write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec['metrics_hardcut']), json.dumps(rec['metrics_blend']))


if __name__ == '__main__':
    main()
