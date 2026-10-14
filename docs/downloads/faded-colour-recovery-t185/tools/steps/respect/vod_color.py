"""Shared helpers for video on demand: decode/encode, BT.709 Y/CbCr, luma gate, source-Y composite.

The luma gate is the T180/T181 measurement (global phase correlation <=1.5 px and 3x3 tile p90 <=2.5 px),
generalized from the fixed 768x576 canvas to any H3 canvas. Chroma never gates.
"""
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

LUMA = np.array([.2126, .7152, .0722], np.float32)


def sha(path) -> str:
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def probe(path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                          "stream=width,height,pix_fmt,nb_read_frames,avg_frame_rate,color_space,color_range,color_transfer,color_primaries",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)["streams"][0]


def decode_rgb(path, size=None) -> np.ndarray:
    """Decode every frame to uint8 RGB (optionally area-resized to size=(w, h))."""
    info = probe(path)
    w, h = (size if size else (int(info["width"]), int(info["height"])))
    vf = f"scale={w}:{h}:flags=area,format=rgb24" if size else "format=rgb24"
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-an", "-vf", vf, "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(out, np.uint8).reshape(-1, h, w, 3)


def ycc(rgb):
    """Full-range BT.709 Y and (Cb, Cr) in [-0.5, 0.5] from uint8 RGB."""
    x = rgb.astype(np.float32) / 255.
    y = x @ LUMA
    return y, np.stack([(x[..., 2] - y) / 1.8556, (x[..., 0] - y) / 1.5748], -1)


def rgb(y, c) -> np.ndarray:
    return np.clip(np.rint(np.stack([y + 1.5748 * c[..., 1], y - .1873 * c[..., 0] - .4681 * c[..., 1], y + 1.8556 * c[..., 0]], -1) * 255),
                   0, 255).astype(np.uint8)


def guided(guide, src, r, eps):
    box = lambda v: cv2.boxFilter(v, -1, (2 * r + 1, 2 * r + 1), normalize=True, borderType=cv2.BORDER_REFLECT)
    mi, mp = box(guide), box(src)
    a = (box(guide * src) - mi * mp) / (box(guide * guide) - mi * mi + eps)
    return box(a) * guide + box(mp - a * mi)


def upsample_chroma(c_small, y_full):
    """Guided chroma upsample to the source-Y grid (base_r2 recipe: radius scales with size, eps 2e-3)."""
    h, w = y_full.shape
    r = max(2, int(round(6 * w / 960)))
    return np.stack([guided(y_full, cv2.resize(c_small[..., k], (w, h), interpolation=cv2.INTER_CUBIC), r, 2e-3) for k in range(2)], -1)


def composite(source_rgb, c_small):
    """Final frame = exact source Y + recovered CbCr (no masks, no regional compositing)."""
    y, _ = ycc(source_rgb)
    return rgb(y, upsample_chroma(c_small.astype(np.float32), y))


def measure(sy, gy) -> dict:
    """T180 inspect_h3_worker luma-only registration measurement on an arbitrary canvas."""
    h, w = sy.shape
    win = cv2.createHanningWindow((w, h), cv2.CV_32F)
    (dx, dy), _ = cv2.phaseCorrelate(sy.astype(np.float32).copy(), gy.astype(np.float32).copy(), win)
    th, tw = h // 3, w // 3
    tiles = []
    for yy in (0, th, 2 * th):
        for xx in (0, tw, 2 * tw):
            aa = sy[yy:yy + th, xx:xx + tw].astype(np.float32).copy()
            bb = gy[yy:yy + th, xx:xx + tw].astype(np.float32).copy()
            if aa.std() < .03:
                continue
            (tx, ty), rr = cv2.phaseCorrelate(aa, bb, cv2.createHanningWindow((tw, th), cv2.CV_32F))
            if rr >= .3:
                tiles.append(float(np.hypot(tx, ty)))
    p90 = float(np.percentile(tiles, 90)) if tiles else None
    mag = float(np.hypot(dx, dy))
    return {"shift_magnitude": mag, "tile_shift_p90": p90, "tile_count": len(tiles),
            "pass": mag <= 1.5 and p90 is not None and p90 <= 2.5}


class Encoder:
    def __init__(self, path, size, fps, *, crf=16, pix_fmt="yuv420p", preset="medium", codec="libx264"):
        w, h = size
        self.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                                      "-an", "-c:v", codec, "-preset", preset, "-crf", str(crf), "-pix_fmt", pix_fmt,
                                      "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                                      "-movflags", "+faststart", str(path)], stdin=subprocess.PIPE)

    def write(self, frame):
        self.proc.stdin.write(np.ascontiguousarray(frame).tobytes())

    def close(self):
        self.proc.stdin.close()
        assert self.proc.wait() == 0


def label(img, text):
    out = img.copy()
    scale = max(.5, img.shape[1] / 1400)
    cv2.putText(out, text, (12, int(30 * scale) + 6), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(out, text, (12, int(30 * scale) + 6), cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), 1, cv2.LINE_AA)
    return out


def side_by_side(left, right, height=540):
    def fit(im):
        w = int(round(im.shape[1] * height / im.shape[0] / 2)) * 2
        return cv2.resize(im, (w, height), interpolation=cv2.INTER_AREA)
    return np.hstack([label(fit(left), "ORIGINAL"), label(fit(right), "RECOVERED (automatic)")])


def contact_sheets(frames, captions, out_dir, prefix, per_sheet=32, cols=4, thumb_w=320):
    th = int(round(frames[0].shape[0] * thumb_w / frames[0].shape[1]))
    for first in range(0, len(frames), per_sheet):
        chunk = list(range(first, min(first + per_sheet, len(frames))))
        rows = (len(chunk) + cols - 1) // cols
        sheet = np.zeros((rows * (th + 22), cols * thumb_w, 3), np.uint8)
        for k, i in enumerate(chunk):
            x, y = k % cols * thumb_w, k // cols * (th + 22)
            sheet[y + 22:y + 22 + th, x:x + thumb_w] = cv2.resize(frames[i], (thumb_w, th), interpolation=cv2.INTER_AREA)
            cv2.putText(sheet, captions[i], (x + 4, y + 16), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imwrite(str(Path(out_dir) / f"{prefix}_{first:03d}.jpg"), cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])


# Temporal CbCr trainer colour space (BT.601 full range, CbCr centred on 0.5), identical to the sister trainer.
def trainer_ycbcr(rgb_u8):
    x = rgb_u8.astype(np.float32) / 255
    y = .299 * x[..., 0] + .587 * x[..., 1] + .114 * x[..., 2]
    return y, np.stack([.5 + (x[..., 2] - y) * .564, .5 + (x[..., 0] - y) * .713], -1)


def trainer_rgb(y, cbcr):
    cb, cr = cbcr[..., 0] - .5, cbcr[..., 1] - .5
    out = np.clip(np.stack([y + 1.403 * cr, y - .344 * cb - .714 * cr, y + 1.773 * cb], -1), 0, 1)
    return np.clip(np.rint(out * 255), 0, 255).astype(np.uint8)


def teacher_target(source_small, generated_small):
    """Adapter target: source Y (trainer space) + generated CbCr composed on source Y in BT.709 (T181 prepare_dataset rule)."""
    y709, _ = ycc(source_small)
    composed = rgb(y709, ycc(generated_small)[1])
    return trainer_rgb(trainer_ycbcr(source_small)[0], trainer_ycbcr(composed)[1])
