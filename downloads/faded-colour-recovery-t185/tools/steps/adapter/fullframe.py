"""Full-frame transforms and verified original-Y assembly.

No spatial selection, padding, cropping, confidence arrays or edge weighting.
The final FFV1 stream keeps source Y samples and source raster/subsampling.
The RGB MP4 produced by the runner is review-only.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

import cv2
import numpy as np

WIDTH, HEIGHT = 320, 224
# Subsampling and bit depth; fail closed on undeclared pixel formats.
FORMATS = {
    "yuv444p": (1, 1, 8), "yuv422p": (2, 1, 8), "yuv420p": (2, 2, 8),
    "yuv444p10le": (1, 1, 10), "yuv422p10le": (2, 1, 10), "yuv420p10le": (2, 2, 10),
}


def process_options():
    return {"creationflags": 0x08000000} if os.name == "nt" else {}


def prepare_rgb(rgb):
    return cv2.resize(rgb, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)


def inverse_chroma(cbcr, width, height):
    if cbcr.shape != (HEIGHT, WIDTH, 2):
        raise ValueError("Expected complete model-resolution CbCr raster")
    return cv2.resize(cbcr, (width, height), interpolation=cv2.INTER_LINEAR)


def probe(path):
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe is required (install it with ffmpeg)")
    return json.loads(subprocess.check_output([
        ffprobe, "-v", "error", "-select_streams", "v:0", "-show_streams",
        "-show_frames", "-show_entries",
        "stream=width,height,pix_fmt,avg_frame_rate,r_frame_rate,time_base,sample_aspect_ratio,color_range,color_space,color_transfer,color_primaries:frame=best_effort_timestamp",
        "-of", "json", str(path),
    ], **process_options()))


def timestamps(info):
    timebase = Fraction(info["streams"][0]["time_base"])
    return [int(frame["best_effort_timestamp"]) * timebase for frame in info["frames"]]


def probe_source(path, contract, teacher=False):
    info = probe(path)
    stream = info["streams"][0]
    if [stream["width"], stream["height"]] != list(contract["resolution"]):
        raise ValueError("Source and teacher must have identical native raster geometry")
    if len(info["frames"]) != int(contract["frames"]):
        raise ValueError("Decoded frame count differs from exact source contract")
    fps = Fraction(str(contract["fps"]))
    if fps != 24 or Fraction(stream["r_frame_rate"]) != fps:
        raise ValueError("This reviewed profile requires the unchanged 24 fps source clock")
    pts = timestamps(info)
    if not pts or pts[0] != 0 or any(b <= a for a, b in zip(pts, pts[1:])):
        raise ValueError("Requires zero-start, strictly increasing source timestamps")
    # Container ticks may quantize 24fps (e.g. Matroska milliseconds).
    tick = Fraction(stream["time_base"])
    if any(abs(pts[i] - Fraction(i, 1) / fps) > tick for i in range(len(pts))):
        raise ValueError("Variable frame timing is unsupported; never retime it")
    if not teacher and stream["pix_fmt"] not in FORMATS:
        raise ValueError("Unsupported original-Y pixel format: " + stream["pix_fmt"])
    return info


def read_exact(stream, size):
    blocks = []
    remaining = size
    while remaining:
        data = stream.read(remaining)
        if not data:
            raise RuntimeError("Truncated native frame stream")
        blocks.append(data)
        remaining -= len(data)
    return b"".join(blocks)


def raw_decoder(ffmpeg, path, pixel_format):
    return subprocess.Popen([
        ffmpeg, "-nostdin", "-v", "error", "-i", str(path), "-map", "0:v:0",
        "-vsync", "0", "-f", "rawvideo", "-pix_fmt", pixel_format, "pipe:1",
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, **process_options())


def exact_source_y_assembly(ffmpeg, source, chroma_path, output, contract):
    info = probe_source(source, contract)
    stream = info["streams"][0]
    width, height = stream["width"], stream["height"]
    pixel_format = stream["pix_fmt"]
    sx, sy, bits = FORMATS[pixel_format]
    cw, ch = (width + sx - 1) // sx, (height + sy - 1) // sy
    dtype = np.dtype("u1" if bits == 8 else "<u2")
    y_bytes = width * height * dtype.itemsize
    chroma_bytes = cw * ch * dtype.itemsize
    frame_bytes = y_bytes + 2 * chroma_bytes
    count = int(contract["frames"])
    if Path(chroma_path).stat().st_size != count * width * height * 2 * 4:
        raise ValueError("Predicted chroma count/geometry differs from exact source")
    sar = stream.get("sample_aspect_ratio", "1:1")
    if sar in ("N/A", "0:1"):
        sar = "1:1"
    output_path = Path(output)
    tmp_path = output_path.with_name(output_path.name + ".nosar.tmp.mkv")
    # Encode FFV1 with NO video filtergraph and NO color_* flags on the encode.
    # Some Windows ffmpeg 8.x builds inserts swscale/Y drift when either
    # `-vf setsar` or color_* options ride on the raw→FFV1 encode; Linux often does not.
    # SAR + color metadata are applied metadata-only via a later -c copy remux.
    command = [ffmpeg, "-nostdin", "-v", "error", "-y", "-f", "rawvideo",
               "-pixel_format", pixel_format, "-video_size", f"{width}x{height}",
               "-framerate", "24", "-i", "pipe:0",
               "-vsync", "0", "-c:v", "ffv1", "-level", "3", "-pix_fmt", pixel_format,
               str(tmp_path)]
    decoder = raw_decoder(ffmpeg, source, pixel_format)
    encoder = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, **process_options())
    y_hash = hashlib.sha256()
    try:
        with Path(chroma_path).open("rb") as chroma:
            for _ in range(count):
                raw = read_exact(decoder.stdout, frame_bytes)
                original_y = raw[:y_bytes]
                y_hash.update(original_y)
                prediction = np.frombuffer(read_exact(chroma, width * height * 8), dtype="<f4").reshape(height, width, 2)
                if not np.isfinite(prediction).all():
                    raise ValueError("Nonfinite predicted chroma")
                reduced = cv2.resize(prediction, (cw, ch), interpolation=cv2.INTER_AREA)
                if stream.get("color_range") == "pc":
                    quantized = np.rint(np.clip(reduced, 0, 1) * ((1 << bits) - 1)).astype(dtype)
                else:
                    factor = 1 << (bits - 8)
                    quantized = np.rint(16 * factor + np.clip(reduced, 0, 1) * 224 * factor).astype(dtype)
                encoder.stdin.write(original_y)
                encoder.stdin.write(quantized[..., 0].tobytes())
                encoder.stdin.write(quantized[..., 1].tobytes())
        if decoder.stdout.read(1):
            raise ValueError("Source has extra frames")
        decoder.stdout.close()
        encoder.stdin.close()
        for process in (decoder, encoder):
            error = process.stderr.read()
            if process.wait() != 0:
                raise RuntimeError(error.decode(errors="replace")[-2000:])
        # Metadata-only remux: -c copy -sar W:H plus preserved color_* (never on encode).
        remux_cmd = [
            ffmpeg, "-nostdin", "-v", "error", "-y", "-i", str(tmp_path),
            "-c", "copy", "-sar", sar,
        ]
        for field, option in [("color_range", "-color_range"), ("color_space", "-colorspace"),
                              ("color_transfer", "-color_trc"), ("color_primaries", "-color_primaries")]:
            value = stream.get(field)
            if value and value not in ("unknown", "unspecified"):
                remux_cmd += [option, value]
        remux_cmd += [str(output_path)]
        remux = subprocess.run(remux_cmd, capture_output=True, **process_options())
        if remux.returncode != 0:
            raise RuntimeError(remux.stderr.decode(errors="replace")[-2000:])
    finally:
        for process in (decoder, encoder):
            if process.poll() is None:
                process.kill()
                process.wait()
        try:
            tmp_path.unlink(missing_ok=True)
        except TypeError:
            if tmp_path.exists():
                tmp_path.unlink()
    result = probe_source(output, contract)
    out_stream = result["streams"][0]
    if timestamps(info) != timestamps(result):
        raise ValueError("Output PTS differ from source; exact timing is unsupported for this container")
    if out_stream.get("sample_aspect_ratio", "1:1") != sar or out_stream["pix_fmt"] != pixel_format:
        raise ValueError("Output sample geometry or native pixel format changed")
    verify = raw_decoder(ffmpeg, output, pixel_format)
    output_hash = hashlib.sha256()
    try:
        for _ in range(count):
            output_hash.update(read_exact(verify.stdout, frame_bytes)[:y_bytes])
        if verify.stdout.read(1):
            raise ValueError("Output has extra frames")
        error = verify.stderr.read()
        if verify.wait() != 0:
            raise RuntimeError(error.decode(errors="replace")[-2000:])
    finally:
        if verify.poll() is None:
            verify.kill()
            verify.wait()
    if y_hash.digest() != output_hash.digest():
        # Strict gate retained; emit frame-level ΔY diagnostics before raise.
        diag = _exact_y_mismatch_diagnostics(
            ffmpeg, source, output, pixel_format, frame_bytes, y_bytes, count, dtype)
        payload = {
            "error": "Exact original-Y sample verification failed",
            "source_y_sha256": y_hash.hexdigest(),
            "output_y_sha256": output_hash.hexdigest(),
            **diag,
        }
        print(json.dumps(payload, sort_keys=True), flush=True)
        raise ValueError(json.dumps(payload, sort_keys=True))
    return {"status": "verified", "source_y_sha256": y_hash.hexdigest(),
            "output_y_sha256": output_hash.hexdigest(), "timestamps_exact": True,
            "frames": count, "resolution": [width, height], "pixel_format": pixel_format,
            "sample_aspect_ratio": sar, "codec": "ffv1", "audio": "not_in_this_video_only_assembly"}


def _exact_y_mismatch_diagnostics(ffmpeg, source, output, pixel_format, frame_bytes, y_bytes, count, dtype):
    """Compare source vs output Y planes; return first mismatch index and abs-ΔY stats."""
    src_dec = raw_decoder(ffmpeg, source, pixel_format)
    out_dec = raw_decoder(ffmpeg, output, pixel_format)
    first = None
    max_abs = 0
    abs_sum = 0.0
    sample_count = 0
    try:
        for index in range(count):
            src_y = np.frombuffer(read_exact(src_dec.stdout, frame_bytes)[:y_bytes], dtype=dtype)
            out_y = np.frombuffer(read_exact(out_dec.stdout, frame_bytes)[:y_bytes], dtype=dtype)
            # Promote to int32 so 10-bit unsigned differences stay exact.
            delta = out_y.astype(np.int32) - src_y.astype(np.int32)
            abs_delta = np.abs(delta)
            frame_max = int(abs_delta.max()) if abs_delta.size else 0
            if frame_max:
                if first is None:
                    first = index
                if frame_max > max_abs:
                    max_abs = frame_max
            abs_sum += float(abs_delta.sum())
            sample_count += int(abs_delta.size)
        for process in (src_dec, out_dec):
            process.stdout.close()
            process.stderr.read()
            process.wait()
    finally:
        for process in (src_dec, out_dec):
            if process.poll() is None:
                process.kill()
                process.wait()
    mean_abs = (abs_sum / sample_count) if sample_count else 0.0
    return {
        "first_mismatched_frame": first,
        "max_abs_delta_y": max_abs,
        "mean_abs_delta_y": mean_abs,
        "y_sample_count": sample_count,
    }
