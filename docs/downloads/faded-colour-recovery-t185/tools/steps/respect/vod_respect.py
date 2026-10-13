"""Surviving-dye respect (v2): the recovery may add to the surviving red-green record, never flip or weaken it.

Model (2026-10-13): in a faded, later neutralized print the magenta dye (green record) survives best, the cyan dye (red
record) partly, the yellow dye (blue record) is mostly gone; the yellow-blue axis is largely a copy of the other two.
v1 (gain fitted to the recovery) imported the reference's saturation and amplified grain; v2 uses no gain.

  axes          a = R - G (surviving red-green), b = B - (R+G)/2 (yellow-blue, mostly lost); Y = source Y exactly
  tone level    per frame, per luma bin median of a (source and recovery separately), smoothed over time
  deviations    u = filtered source a - source tone level (surviving local colour); v = recovered a - recovered tone level
  object scale  optional: subtract a reliability-weighted Gaussian low-pass of u (sigma object_scale_sigma px at 1024 width)
  respect       where |u| > tau (3x the frame's grain level): v' = u if v disagrees in sign, else the stronger of u and v;
                elsewhere v' = v (no surviving information above grain: the reference is free)
  final         a = recovered tone level + v'; b = recovered b

No inference, masks or shapes. Inputs: source/<proxy>.mkv and artifacts/recovered/<full_recovered>.mp4 (same clip frames).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, os.environ["CWC_EXPERIMENT_CODE_DIR"])
from vod_color import Encoder, contact_sheets, probe, sha  # noqa: E402

LUMA = np.array([.2126, .7152, .0722], np.float32)
BINS = 16


def frames(path, fmt, dtype, scale):
    info = probe(path)
    w, h = int(info["width"]), int(info["height"])
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-an", "-f", "rawvideo", "-pix_fmt", fmt, "-"], stdout=subprocess.PIPE)
    size = w * h * 3 * np.dtype(dtype).itemsize
    while True:
        buf = proc.stdout.read(size)
        if len(buf) < size:
            break
        yield np.frombuffer(buf, dtype).reshape(h, w, 3).astype(np.float32) / scale
    proc.wait()


def opponent(rgb):
    y = rgb @ LUMA
    return y, rgb[..., 0] - rgb[..., 1], rgb[..., 2] - (rgb[..., 0] + rgb[..., 1]) / 2


def compose(y, a, b):
    g = y - .2487 * a - .0722 * b
    return np.stack([g + a, g, g + a / 2 + b], -1)


def median5(a, passes):
    """Iterated 5 px median on 16-bit a (thin R/G registration fringes and grain; OpenCV 16-bit median is limited to 5 px)."""
    m = np.clip((a + 1) * 32767.5, 0, 65535).astype(np.uint16)
    for _ in range(passes):
        m = cv2.medianBlur(m, 5)
    return m.astype(np.float32) / 32767.5 - 1


def guided(guide, src, r, eps):
    box = lambda v: cv2.boxFilter(v, -1, (2 * r + 1, 2 * r + 1), normalize=True, borderType=cv2.BORDER_REFLECT)
    mi, mp = box(guide), box(src)
    a = (box(guide * src) - mi * mp) / (box(guide * guide) - mi * mi + eps)
    return box(a) * guide + box(mp - a * mi)


def reliability(y):
    s = lambda e0, e1, v: np.clip((v - e0) / (e1 - e0), 0, 1)
    return s(.03, .10, y) * (1 - s(.90, .97, y))


def tone_levels(y, a, mask):
    idx = np.minimum((y * BINS).astype(int), BINS - 1)
    out = np.full(BINS, np.nan, np.float32)
    for bi in range(BINS):
        m = mask & (idx == bi)
        if m.sum() > 200:
            out[bi] = np.median(a[m])
    ok = ~np.isnan(out)
    return np.interp(np.arange(BINS), np.flatnonzero(ok), out[ok]).astype(np.float32) if ok.any() else np.zeros(BINS, np.float32)


def smooth_time(rows, sig):
    kern = np.exp(-.5 * (np.arange(-3 * sig, 3 * sig + 1) / sig) ** 2); kern /= kern.sum()
    pad = np.pad(rows, ((3 * sig, 3 * sig), (0, 0)), mode="edge")
    return np.stack([np.convolve(pad[:, i], kern, mode="valid") for i in range(rows.shape[1])], 1)


def step_series(path, size):
    prev, vals = None, []
    for f in frames(path, "rgb24", np.uint8, 255.):
        _, a, b = opponent(cv2.resize(f, size, interpolation=cv2.INTER_AREA))
        if prev is not None:
            vals.append(float(np.abs(a - prev[0]).mean() + np.abs(b - prev[1]).mean()))
        prev = (a, b)
    return {"mean": float(np.mean(vals)), "p95": float(np.percentile(vals, 95)), "max": float(np.max(vals))}


def main():
    I, O = Path(os.environ["CWC_INPUT_DIR"]), Path(os.environ["CWC_OUTPUT_DIR"])
    O.mkdir(exist_ok=True)
    spec = json.loads((Path(os.environ["CWC_EXPERIMENT_CODE_DIR"]) / "respect_spec.json").read_text())
    (src,) = list((I / "source").glob("*.mkv"))
    (rec,) = list((I / "artifacts/recovered").glob("*.mp4"))
    assert sha(src) == spec["source_sha256"] and sha(rec) == spec["recovered_sha256"]
    passes, gr, tau_k, sig = spec["median_passes"], spec["guided_radius"], spec["tau_sigma"], spec["tone_temporal_sigma"]

    # Pass 1 (quarter size): tone levels of source and recovery per frame, and the frame's grain level of the surviving deviation.
    ls, lr, grain = [], [], []
    for s_rgb, r_rgb in zip(frames(src, "rgb48le", np.uint16, 65535.), frames(rec, "rgb24", np.uint8, 255.)):
        q = lambda x: cv2.resize(x, (x.shape[1] // 4, x.shape[0] // 4), interpolation=cv2.INTER_AREA)
        ys, as_, _ = opponent(q(s_rgb)); _, ar, _ = opponent(q(r_rgb))
        mask = reliability(ys) > .99
        af = median5(as_, 1)
        ls.append(tone_levels(ys, af, mask)); lr.append(tone_levels(ys, ar, mask))
        hp = af - cv2.GaussianBlur(af, (0, 0), 2)
        grain.append(float(1.4826 * np.median(np.abs(hp[mask] - np.median(hp[mask])))))
    n = len(ls)
    assert n == spec["frame_count"], (n, spec["frame_count"])
    ls_s, lr_s = smooth_time(np.stack(ls), sig), smooth_time(np.stack(lr), sig)
    grain_shot = float(np.median(grain)) * 2  # quarter-size noise underestimates full-size grain after the same filter chain
    centres = (np.arange(BINS) + .5) / BINS

    # Pass 2 (full proxy size).
    first = probe(src); W, H = int(first["width"]), int(first["height"])
    enc = Encoder(O / "respect.mp4", (W, H), spec["fps"], crf=14)
    sbs = Encoder(O / "respect_compare.mp4", (W // 2 * 3, H // 2), spec["fps"], crf=16)
    sheet_r, sheet_c, stats = [], [], []
    for t, (s_rgb, r_rgb) in enumerate(zip(frames(src, "rgb48le", np.uint16, 65535.), frames(rec, "rgb24", np.uint8, 255.))):
        ys, as_, _ = opponent(s_rgb)
        _, ar, br = opponent(r_rgb)
        rel = reliability(ys)
        u = guided(ys, median5(as_, passes) - np.interp(ys, centres, ls_s[t]), gr, 2e-3)
        if spec.get("object_scale_sigma"):  # drop wall/gradient-scale red-green (cast, uneven fading); keep object-scale pieces
            sg = spec["object_scale_sigma"] * W / 1024
            wmask = cv2.GaussianBlur(rel, (0, 0), sg) + 1e-4
            u = u - cv2.GaussianBlur(u * rel, (0, 0), sg) / wmask
        tone_r = np.interp(ys, centres, lr_s[t])
        v = ar - tone_r
        tau = max(tau_k * grain_shot, spec["tau_floor"])
        informative = (np.abs(u) > tau) & (rel > .5)
        agree = np.sign(u) == np.sign(v)
        stronger = np.where(np.abs(v) > np.abs(u), v, u)
        vp = np.where(informative, np.where(agree, stronger, u), v)
        # soft transition at the threshold and in unreliable tones avoids switching edges
        wgt = np.clip((np.abs(u) - tau) / tau, 0, 1) * rel
        vf = v + wgt * (vp - v)
        out = np.clip(np.rint(compose(ys, tone_r + vf, br) * 255), 0, 255).astype(np.uint8)
        enc.write(out)
        rec8 = np.clip(np.rint(r_rgb * 255), 0, 255).astype(np.uint8)
        changed = np.abs(vf - v) > .01
        stats.append({"frame": t, "informative_fraction": float(informative.mean()),
                      "contradicted_before": float((informative & ~agree).mean()), "changed_fraction": float(changed.mean()),
                      "mean_abs_change": float(np.abs(vf - v).mean())})
        sheet_r.append(cv2.resize(out, (W // 4, H // 4), interpolation=cv2.INTER_AREA))
        sheet_c.append(cv2.resize(rec8, (W // 4, H // 4), interpolation=cv2.INTER_AREA))
        half = lambda x: cv2.resize(x, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
        src8 = np.clip(np.rint(s_rgb * 255), 0, 255).astype(np.uint8)
        strip = [half(src8), half(rec8), half(out)]
        for img, txt in zip(strip, ["SOURCE", "CURRENT (reference only)", "SURVIVING DYES RESPECTED"]):
            cv2.putText(img, txt, (10, H // 2 - 12), 0, .55, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(img, txt, (10, H // 2 - 12), 0, .55, (255, 255, 255), 1, cv2.LINE_AA)
        sbs.write(np.hstack(strip))
        if t in spec["matched_frames"]:
            cmap = np.zeros_like(src8); cmap[changed & (vf > v)] = (255, 60, 60); cmap[changed & (vf < v)] = (60, 255, 60)
            diag = half((rec8 * .35 + cmap * .65).astype(np.uint8))
            cv2.putText(diag, "where survival changed the result (red=redder, green=greener)", (10, H // 2 - 12), 0, .45, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imwrite(str(O / f"matched_{t:03d}.jpg"), cv2.cvtColor(np.vstack([np.hstack(strip[:2]), np.hstack([strip[2], diag])]), cv2.COLOR_RGB2BGR),
                        [cv2.IMWRITE_JPEG_QUALITY, 92])
    enc.close(); sbs.close()
    contact_sheets(sheet_r, [f"clip {i} respect" for i in range(n)], O, "sheet_respect")
    contact_sheets(sheet_c, [f"clip {i} current" for i in range(n)], O, "sheet_current")
    q = (W // 4, H // 4)
    receipt = {"schema": "t185_surviving_dye_respect_v2", "source_sha256": spec["source_sha256"], "recovered_sha256": spec["recovered_sha256"],
               "frame_count": n, "grain_level": grain_shot, "tau": max(tau_k * grain_shot, spec["tau_floor"]), "params": spec,
               "respect_sha256": sha(O / "respect.mp4"), "compare_sha256": sha(O / "respect_compare.mp4"),
               "opponent_step": {"respect": step_series(O / "respect.mp4", q), "current": step_series(rec, q)},
               "means": {k: float(np.mean([r[k] for r in stats])) for k in stats[0] if k != "frame"}, "per_frame": stats, "recipe": __doc__}
    (O / "respect_receipt.json").write_text(json.dumps(receipt, indent=1))


if __name__ == "__main__":
    main()
