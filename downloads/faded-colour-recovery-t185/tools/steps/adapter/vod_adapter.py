"""Shot extension: gate-passing registered H3 frames teach a small
shot-local Temporal CbCr adapter, which then colours every frame of the cut-to-cut clip.

Inputs ($CWC_INPUT_DIR): source/<proxy>.mkv (clip, half-size working media), artifacts/donors/teacher_targets.npz (exact
trainer-space targets for every carrier frame) and artifacts/donors/registration_report.json from the FADED preview stage.
Code: vendored pinned trainer (train_adapter.py sha 99798ac5..., fullframe.py) plus adapter_spec.json.

Teachers: the admitted carrier frames named in adapter_spec.json (luma-gate-passing; automatic in the demo app, a
recorded delegated decision in research runs). Each target is used as its exact hash-verified bytes (source Y +
registered H3 CbCr). Contiguous runs shorter than the sequence length are dropped (no gaps, zero weights or substitution).
One contiguous block is held out for checkpoint selection (lowest held-out prediction MAE, T161 rule).
Inference: fresh temporal state at clip frame 0, carried across the whole clip. Output: source Y + adapter CbCr.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import torch

sys.path.insert(0, os.environ.get("CWC_EXPERIMENT_CODE_DIR") or str(Path(__file__).parent))
import train_adapter  # noqa: E402

LUMA = np.array([.2126, .7152, .0722], np.float32)


def sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def decode_rgb(path, size=None):
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                      "-of", "json", str(path)], capture_output=True, text=True, check=True).stdout)["streams"][0]
    w, h = size if size else (int(info["width"]), int(info["height"]))
    vf = f"scale={w}:{h}:flags=area,format=rgb24" if size else "format=rgb24"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-an", "-vf", vf, "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


# Trainer colour space (BT.601 full range, CbCr centred on 0.5), exactly as base_r2 / train_adapter.
def trainer_ycbcr(rgb):
    x = rgb.astype(np.float32) / 255
    y = .299 * x[..., 0] + .587 * x[..., 1] + .114 * x[..., 2]
    return y, np.stack([.5 + (x[..., 2] - y) * .564, .5 + (x[..., 0] - y) * .713], -1)


def trainer_rgb(y, cbcr):
    cb, cr = cbcr[..., 0] - .5, cbcr[..., 1] - .5
    out = np.clip(np.stack([y + 1.403 * cr, y - .344 * cb - .714 * cr, y + 1.773 * cb], -1), 0, 1)
    return np.clip(np.rint(out * 255), 0, 255).astype(np.uint8)


# Delivery colour space (BT.709 full range), as the FADED source-Y composite.
def ycc709(rgb):
    x = rgb.astype(np.float32) / 255.
    y = x @ LUMA
    return y, np.stack([(x[..., 2] - y) / 1.8556, (x[..., 0] - y) / 1.5748], -1)


def rgb709(y, c):
    return np.clip(np.rint(np.stack([y + 1.5748 * c[..., 1], y - .1873 * c[..., 0] - .4681 * c[..., 1], y + 1.8556 * c[..., 0]], -1) * 255),
                   0, 255).astype(np.uint8)


def guided(guide, src, r, eps):
    box = lambda v: cv2.boxFilter(v, -1, (2 * r + 1, 2 * r + 1), normalize=True, borderType=cv2.BORDER_REFLECT)
    mi, mp = box(guide), box(src)
    a = (box(guide * src) - mi * mp) / (box(guide * guide) - mi * mi + eps)
    return box(a) * guide + box(mp - a * mi)


def composite(source_rgb, c_small):
    y, _ = ycc709(source_rgb)
    h, w = y.shape
    r = max(2, int(round(6 * w / 960)))
    c = np.stack([guided(y, cv2.resize(c_small[..., k], (w, h), interpolation=cv2.INTER_CUBIC), r, 2e-3) for k in range(2)], -1)
    return rgb709(y, c)


class Encoder:
    def __init__(self, path, size, fps, crf=14):
        w, h = size
        self.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                                      "-an", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                                      "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-movflags", "+faststart", str(path)],
                                     stdin=subprocess.PIPE)

    def write(self, frame):
        self.proc.stdin.write(np.ascontiguousarray(frame).tobytes())

    def close(self):
        self.proc.stdin.close()
        assert self.proc.wait() == 0


def label(img, text):
    out = img.copy()
    scale = max(.5, img.shape[1] / 1400)
    for colour, thick in (((0, 0, 0), 4), ((255, 255, 255), 1)):
        cv2.putText(out, text, (12, int(30 * scale) + 6), cv2.FONT_HERSHEY_SIMPLEX, scale, colour, thick, cv2.LINE_AA)
    return out


def side_by_side(left, right, height=540):
    fit = lambda im: cv2.resize(im, (int(round(im.shape[1] * height / im.shape[0] / 2)) * 2, height), interpolation=cv2.INTER_AREA)
    return np.hstack([label(fit(left), "ORIGINAL"), label(fit(right), "RECOVERED (automatic)")])


def runs_of(frames):
    runs, cur = [], []
    for f in sorted(frames):
        if cur and f != cur[-1] + 1:
            runs.append(cur)
            cur = []
        cur.append(f)
    return runs + ([cur] if cur else [])


def split_runs(passed, seq):
    """Train/validation runs: contiguous, each >= seq frames, disjoint. One held-out block for checkpoint selection."""
    runs = [r for r in runs_of(passed) if len(r) >= seq]
    assert runs, "no contiguous gate-passing run long enough to teach"
    longest = max(runs, key=len)
    if len(longest) >= 3 * seq:
        m = longest[0] + (len(longest) - seq) // 2
        rest = [r for r in runs if r is not longest]
        train = rest + [[f for f in longest if f < m], [f for f in longest if f >= m + seq]]
        val = [list(range(m, m + seq))]
        holdout = True
    elif len(runs) > 1:
        val = [min(runs, key=len)]
        train = [r for r in runs if r is not val[0]]
        holdout = True
    else:  # one short run: no honest holdout; monitor on the training run and keep the final epoch
        train, val, holdout = runs, runs, False
    return train, val, holdout


def main():
    I, O = Path(os.environ["CWC_INPUT_DIR"]), Path(os.environ["CWC_OUTPUT_DIR"])
    O.mkdir(exist_ok=True)
    spec = json.loads((Path(os.environ["CWC_EXPERIMENT_CODE_DIR"]) / "adapter_spec.json").read_text())
    start = time.time()
    (src,) = list((I / "source").glob("*.mkv"))
    targets_path, report_path = I / "artifacts/donors/teacher_targets.npz", I / "artifacts/donors/registration_report.json"
    assert sha(src) == spec["source_sha256"] and sha(targets_path) == spec["targets_sha256"] and sha(report_path) == spec["report_sha256"]
    report = json.loads(report_path.read_text())
    W, H = spec["canvas"]
    seq, cs, fps = spec["sequence_length"], spec["context_start"], spec["fps"]

    source = decode_rgb(src)
    assert len(source) == spec["frame_count"]
    small = np.stack([cv2.resize(f, (W, H), interpolation=cv2.INTER_AREA) for f in source])
    bundle = np.load(targets_path)
    exact = {int(f): bundle["targets"][k] for k, f in enumerate(bundle["clip_frames"])}
    assert bundle["targets"].shape[1:3] == (H, W)

    # Trainer input: source recentred by one shot-wide CbCr constant (T179-T182 procedure).
    conv = [trainer_ycbcr(f) for f in small]
    offset = np.mean([c.reshape(-1, 2).astype(np.float64).mean(0) for _, c in conv], axis=0) - .5
    inputs = np.stack([trainer_rgb(y, c - offset.astype(np.float32)) for y, c in conv])
    gate = {r["clip_frame"]: r["after"]["pass"] for r in report["rows"]}
    targets = {}
    for t in spec["teachers"]:
        f = int(t["frame"])
        assert gate[f], f"frame {f} failed the luma gate"
        assert hashlib.sha256(np.ascontiguousarray(exact[f]).tobytes()).hexdigest() == t["target_sha256"], f"target {f} bytes differ"
        targets[f] = exact[f]
    train, val, holdout = split_runs(sorted(targets), seq)
    used = {f for run in train + val for f in run}
    targets = {f: v for f, v in targets.items() if f in used}

    data = Path.cwd() / "vod_dataset"
    shots = []
    for split, group in (("train", train), ("val", val)):
        for k, run in enumerate(group):
            name = f"vod_{split}_{k:02d}"
            p = data / "shots" / name
            p.mkdir(parents=True, exist_ok=True)
            np.save(p / "source_rgb.npy", inputs[run])
            np.save(p / "target_rgb.npy", np.stack([targets[f] for f in run]))
            np.save(p / "confidence.npy", np.full((len(run), H, W), 255, np.uint8))
            np.save(p / "frame_weights.npy", np.ones(len(run), np.float32))
            np.save(p / "frame_numbers.npy", np.array(run, np.int32))
            shots.append({"shot": name, "split": split, "frame_count": len(run), "regime": 1, "frames": [run[0], run[-1]], "gap_frames": []})
    manifest = {"schema": "faded_vod_adapter_dataset_v1", "generated_teacher_distillation": True, "generated_teacher_is_ground_truth": False,
                "source_y_authoritative": True, "canvas": [W, H], "fps": fps, "source_sha256": spec["source_sha256"],
                "input_chroma_recentring_offset_trainer_space": offset.tolist(), "shots": shots}
    (data / "dataset_manifest.json").write_text(json.dumps(manifest, indent=1))

    train_adapter.make_review_artifacts = lambda *a, **kw: {}
    tdir = Path.cwd() / "vod_training"
    sys.argv = ["train_adapter.py", "--dataset-dir", str(data), "--output-dir", str(tdir), "--sequence-length", str(seq), "--train-stride", "1",
                "--eval-stride", "4", "--batch-size", "2", "--base-channels", "24", "--epochs", str(spec["epochs"]), "--max-eval-windows", "0",
                "--generated-targets", "--target-provenance",
                "FADED T183 VOD: registered H3 ControlNet CbCr on source Y, automatic luma-gate admission; distillation target, not ground truth",
                "--fps", str(int(round(fps)))]
    train_adapter.main()
    ckpt = tdir / "checkpoints" / ("best.pt" if holdout else "latest.pt")
    device = torch.device("cuda")
    ck = torch.load(ckpt, map_location=device, weights_only=False)
    model = train_adapter.TemporalCbCrAdapter(24).to(device)
    model.load_state_dict(ck["model"])
    model.eval()
    fit_seconds = time.time() - start

    h, w = source.shape[1:3]
    enc = Encoder(O / "full_recovered.mp4", (w, h), fps)
    sbs0 = side_by_side(source[0], source[0])
    enc_sbs = Encoder(O / "full_side_by_side.mp4", (sbs0.shape[1], sbs0.shape[0]), fps, crf=18)
    state, stats, prev, thumbs = None, [], None, []
    gain = float(spec.get("chroma_gain", 1.0))
    with torch.inference_mode():
        for i in range(len(source)):
            x = torch.from_numpy(inputs[i].copy()).permute(2, 0, 1).float().div(255)[None, None].to(device)
            p, _, state = model.forward_with_state(x, state)
            pred = p[0, 0].permute(1, 2, 0).float().cpu().numpy()
            pred = .5 + (pred - .5) * gain
            c_small = ycc709(trainer_rgb(conv[i][0], pred))[1]
            frame = composite(source[i], c_small)
            enc.write(frame)
            enc_sbs.write(side_by_side(source[i], frame))
            cur = c_small
            stats.append({"clip_frame": i, "teacher": i in targets, "chroma_radius_mean": float(np.hypot(cur[..., 0], cur[..., 1]).mean()),
                          "chroma_step_mae": None if prev is None else float(np.abs(cur - prev).mean())})
            prev = cur
            thumbs.append(frame)
            if i in (0, len(source) // 4, len(source) // 2, 3 * len(source) // 4, len(source) - 1):
                cv2.imwrite(str(O / f"full_frame_clip{i:03d}.jpg"), cv2.cvtColor(np.hstack([source[i], frame]), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])
    enc.close()
    enc_sbs.close()
    tw = 320
    th = int(round(h * tw / w))
    for first in range(0, len(thumbs), 32):
        chunk = list(range(first, min(first + 32, len(thumbs))))
        sheet = np.zeros(((len(chunk) + 3) // 4 * (th + 22), 4 * tw, 3), np.uint8)
        for k, i in enumerate(chunk):
            x, y = k % 4 * tw, k // 4 * (th + 22)
            sheet[y + 22:y + 22 + th, x:x + tw] = cv2.resize(thumbs[i], (tw, th), interpolation=cv2.INTER_AREA)
            tag = "teacher" if i in targets else ("H3, not teacher" if cs <= i < cs + report["context_frames"] else "outside H3")
            cv2.putText(sheet, f"clip {i} {tag}", (x + 4, y + 16), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imwrite(str(O / f"full_sheet_{first:03d}.jpg"), cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
    for name in ("metrics.jsonl", "training_summary.json", "run_manifest.json"):
        if (tdir / name).exists():
            (O / name).write_bytes((tdir / name).read_bytes())
    summary = {"schema": "faded_vod_adapter_v1", "admission": spec.get("admission"), "teacher_frames": sorted(targets), "teacher_count": len(targets),
               "train_runs": [[r[0], r[-1]] for r in train], "val_runs": [[r[0], r[-1]] for r in val], "holdout": holdout,
               "checkpoint": ckpt.name, "checkpoint_epoch": int(ck["epoch"]), "best_val_prediction_mae": float(ck.get("best_val", float("nan"))),
               "epochs": spec["epochs"], "canvas": [W, H], "clip_frames": len(source), "context_start": cs, "context_frames": report["context_frames"],
               "chroma_gain": gain, "fit_seconds": fit_seconds, "wall_seconds": time.time() - start, "gpu": torch.cuda.get_device_name(device),
               "trainer_sha256": sha(Path(train_adapter.__file__)), "full_recovered_sha256": sha(O / "full_recovered.mp4"),
               "full_side_by_side_sha256": sha(O / "full_side_by_side.mp4"),
               "chroma_step_mae_mean": float(np.mean([s["chroma_step_mae"] for s in stats[1:]])), "per_frame": stats}
    (O / "adapter_summary.json").write_text(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
