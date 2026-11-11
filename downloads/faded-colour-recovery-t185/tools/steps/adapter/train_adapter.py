#!/usr/bin/env python3
"""Train/evaluate T115 v0: a compact ConvLSTM residual-CbCr adapter."""

from __future__ import annotations

import argparse
import contextlib
import json
import math
import random
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import cv2
except ImportError:  # Inference-only runtimes do not need the contact-sheet dependency.
    cv2 = None
import numpy as np
import torch
from fullframe import process_options
from torch import Tensor, nn
from torch.utils.data import DataLoader, Dataset, RandomSampler, Subset


EXPERIMENT_ID = "SHOT0001-T115-TEMPORAL-CBCR-ADAPTER-V0"
JOURNAL_CODE = "EXP-20260720-MIX-TMP-FRONTIER-T115CBCRV0"


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def rgb_to_ycbcr(rgb: Tensor) -> tuple[Tensor, Tensor]:
    red, green, blue = rgb.unbind(dim=-3)
    y = 0.299 * red + 0.587 * green + 0.114 * blue
    cb = 0.5 + (blue - y) * 0.564
    cr = 0.5 + (red - y) * 0.713
    return y.unsqueeze(-3), torch.stack((cb, cr), dim=-3).clamp(0.0, 1.0)


def ycbcr_to_rgb(y: Tensor, cbcr: Tensor) -> Tensor:
    cb = cbcr.select(-3, 0) - 0.5
    cr = cbcr.select(-3, 1) - 0.5
    yy = y.select(-3, 0)
    red = yy + 1.403 * cr
    blue = yy + 1.773 * cb
    green = yy - 0.344 * cb - 0.714 * cr
    return torch.stack((red, green, blue), dim=-3).clamp(0.0, 1.0)


def sobel_edges(y: Tensor) -> Tensor:
    shape = y.shape
    flat = y.reshape(-1, 1, shape[-2], shape[-1])
    kernel_x = torch.tensor(
        [[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]],
        device=y.device,
        dtype=y.dtype,
    ).reshape(1, 1, 3, 3)
    kernel_y = kernel_x.transpose(-1, -2)
    gx = torch.nn.functional.conv2d(flat, kernel_x, padding=1)
    gy = torch.nn.functional.conv2d(flat, kernel_y, padding=1)
    edge = torch.sqrt(gx.square() + gy.square() + 1e-6).clamp(0.0, 1.0)
    return edge.reshape(*shape)


@dataclass(frozen=True)
class WindowRef:
    shot_index: int
    start: int


class FrontierTemporalDataset(Dataset[dict[str, Tensor]]):
    def __init__(
        self,
        dataset_dir: Path,
        split: str,
        sequence_length: int,
        stride: int,
        augment: bool,
        shot_filter: set[str] | None = None,
    ) -> None:
        self.dataset_dir = dataset_dir
        self.manifest = json.loads((dataset_dir / "dataset_manifest.json").read_text(encoding="utf-8"))
        self.sequence_length = sequence_length
        self.augment = augment
        self.shots = [
            row
            for row in self.manifest["shots"]
            if (row["split"] == split or split == "all") and (not shot_filter or row["shot"] in shot_filter)
        ]
        self.windows: list[WindowRef] = []
        for shot_index, shot in enumerate(self.shots):
            count = int(shot["frame_count"])
            if count < sequence_length:
                continue
            for start in range(0, count - sequence_length + 1, stride):
                self.windows.append(WindowRef(shot_index, start))
        self._arrays: dict[str, dict[str, np.ndarray]] = {}
        if not self.windows:
            raise ValueError(f"No {split} windows of length {sequence_length}")

    def __len__(self) -> int:
        return len(self.windows)

    def _shot_arrays(self, shot_name: str) -> dict[str, np.ndarray]:
        if shot_name not in self._arrays:
            root = self.dataset_dir / "shots" / shot_name
            self._arrays[shot_name] = {
                "source": np.load(root / "source_rgb.npy", mmap_mode="r"),
                "target": np.load(root / "target_rgb.npy", mmap_mode="r"),
                "weights": np.load(root / "frame_weights.npy", mmap_mode="r"),
                "frames": np.load(root / "frame_numbers.npy", mmap_mode="r"),
            }
        return self._arrays[shot_name]

    def __getitem__(self, index: int) -> dict[str, Tensor]:
        ref = self.windows[index]
        shot = self.shots[ref.shot_index]
        arrays = self._shot_arrays(shot["shot"])
        slc = slice(ref.start, ref.start + self.sequence_length)
        source = np.array(arrays["source"][slc], copy=True)
        target = np.array(arrays["target"][slc], copy=True)
        weights = np.array(arrays["weights"][slc], copy=True)
        frames = np.array(arrays["frames"][slc], copy=True)
        if self.augment and random.random() < 0.5:
            source = source[:, :, ::-1].copy()
            target = target[:, :, ::-1].copy()
        return {
            "source_rgb": torch.from_numpy(source).permute(0, 3, 1, 2).float().div_(255.0),
            "target_rgb": torch.from_numpy(target).permute(0, 3, 1, 2).float().div_(255.0),
            "frame_weights": torch.from_numpy(weights).float(),
            "frame_numbers": torch.from_numpy(frames.astype(np.int64)),
            "shot_index": torch.tensor(ref.shot_index, dtype=torch.int64),
        }


class ConvBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, stride: int = 1) -> None:
        super().__init__()
        groups = max(1, min(8, out_channels // 4))
        self.net = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, stride=stride, padding=1),
            nn.GroupNorm(groups, out_channels),
            nn.SiLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.GroupNorm(groups, out_channels),
            nn.SiLU(inplace=True),
        )

    def forward(self, value: Tensor) -> Tensor:
        return self.net(value)


class ConvLSTMCell(nn.Module):
    def __init__(self, channels: int) -> None:
        super().__init__()
        self.channels = channels
        self.gates = nn.Conv2d(channels * 2, channels * 4, 3, padding=1)

    def forward(self, value: Tensor, state: tuple[Tensor, Tensor] | None) -> tuple[Tensor, Tensor]:
        if state is None:
            hidden = torch.zeros_like(value)
            cell = torch.zeros_like(value)
        else:
            hidden, cell = state
        forget, update, output, candidate = self.gates(torch.cat((value, hidden), dim=1)).chunk(4, dim=1)
        cell = torch.sigmoid(forget + 1.0) * cell + torch.sigmoid(update) * torch.tanh(candidate)
        hidden = torch.sigmoid(output) * torch.tanh(cell)
        return hidden, cell


class TemporalCbCrAdapter(nn.Module):
    def __init__(self, base_channels: int = 24, max_residual: float = 0.35) -> None:
        super().__init__()
        self.max_residual = max_residual
        self.enc0 = ConvBlock(5, base_channels)
        self.enc1 = ConvBlock(base_channels, base_channels * 2, stride=2)
        self.enc2 = ConvBlock(base_channels * 2, base_channels * 4, stride=2)
        self.temporal = ConvLSTMCell(base_channels * 4)
        self.dec1 = ConvBlock(base_channels * 6, base_channels * 2)
        self.dec0 = ConvBlock(base_channels * 3, base_channels)
        self.head = nn.Conv2d(base_channels, 2, 3, padding=1)

    def forward_with_state(
        self,
        source_rgb: Tensor,
        state: tuple[Tensor, Tensor] | None = None,
    ) -> tuple[Tensor, Tensor, tuple[Tensor, Tensor]]:
        batch, frames, _, height, width = source_rgb.shape
        source_y, source_cbcr = rgb_to_ycbcr(source_rgb)
        edge = sobel_edges(source_y)
        model_input = torch.cat((source_rgb, source_y, edge), dim=2).reshape(batch * frames, 5, height, width)
        skip0 = self.enc0(model_input)
        skip1 = self.enc1(skip0)
        encoded = self.enc2(skip1).reshape(batch, frames, -1, height // 4, width // 4)
        temporal_values: list[Tensor] = []
        for frame_index in range(frames):
            state = self.temporal(encoded[:, frame_index], state)
            temporal_values.append(state[0])
        assert state is not None
        temporal = torch.stack(temporal_values, dim=1).reshape(batch * frames, -1, height // 4, width // 4)
        up1 = torch.nn.functional.interpolate(temporal, size=skip1.shape[-2:], mode="bilinear", align_corners=False)
        decoded1 = self.dec1(torch.cat((up1, skip1), dim=1))
        up0 = torch.nn.functional.interpolate(decoded1, size=skip0.shape[-2:], mode="bilinear", align_corners=False)
        decoded0 = self.dec0(torch.cat((up0, skip0), dim=1))
        residual = torch.tanh(self.head(decoded0)).reshape(batch, frames, 2, height, width) * self.max_residual
        prediction = (source_cbcr + residual).clamp(0.0, 1.0)
        return prediction, residual, state

    def forward(self, source_rgb: Tensor) -> tuple[Tensor, Tensor]:
        prediction, residual, _ = self.forward_with_state(source_rgb)
        return prediction, residual


def compute_losses(
    model: TemporalCbCrAdapter,
    batch: dict[str, Tensor],
    temporal_weight: float,
    smoothness_weight: float,
    nochange_weight: float,
) -> tuple[Tensor, dict[str, Tensor], dict[str, Tensor]]:
    source = batch["source_rgb"]
    target = batch["target_rgb"]
    source_y, source_cbcr = rgb_to_ycbcr(source)
    _, target_cbcr = rgb_to_ycbcr(target)
    prediction, residual = model(source)

    clamp_frames = []
    for frame_index in range(source_cbcr.shape[1]):
        first = max(0, frame_index - 1)
        last = min(source_cbcr.shape[1], frame_index + 2)
        clamp_frames.append(source_cbcr[:, first:last].median(dim=1).values)
    temporal_clamp = torch.stack(clamp_frames, dim=1)

    reconstruction = torch.abs(prediction - target_cbcr).mean()
    if prediction.shape[1] > 1:
        pred_steps = prediction[:, 1:] - prediction[:, :-1]
        target_steps = target_cbcr[:, 1:] - target_cbcr[:, :-1]
        temporal = torch.abs(pred_steps - target_steps).mean()
    else:
        temporal = reconstruction.new_zeros(())
    dx = torch.abs(prediction[..., :, 1:] - prediction[..., :, :-1])
    dy = torch.abs(prediction[..., 1:, :] - prediction[..., :-1, :])
    smoothness = 0.5 * (dx.mean() + dy.mean())
    # Uniform residual regularization replaces the legacy selected-pixel term.
    nochange = torch.abs(residual).mean()
    total = reconstruction + temporal_weight * temporal + smoothness_weight * smoothness + nochange_weight * nochange
    metrics = {
        "loss": total.detach(),
        "reconstruction": reconstruction.detach(),
        "temporal": temporal.detach(),
        "smoothness": smoothness.detach(),
        "nochange": nochange.detach(),
        "source_mae": torch.abs(source_cbcr - target_cbcr).mean().detach(),
        "temporal_clamp_mae": torch.abs(temporal_clamp - target_cbcr).mean().detach(),
        "prediction_mae": reconstruction.detach(),
    }
    tensors = {
        "source_y": source_y.detach(),
        "source_cbcr": source_cbcr.detach(),
        "target_cbcr": target_cbcr.detach(),
        "prediction": prediction.detach(),
    }
    return total, metrics, tensors


def aggregate_metrics(rows: Iterable[dict[str, float]]) -> dict[str, float]:
    materialized = list(rows)
    keys = sorted({key for row in materialized for key in row})
    return {key: float(np.mean([row[key] for row in materialized if key in row])) for key in keys}


def tensor_metrics(metrics: dict[str, Tensor]) -> dict[str, float]:
    return {key: float(value.float().cpu()) for key, value in metrics.items()}


@torch.no_grad()
def evaluate(
    model: TemporalCbCrAdapter,
    loader: DataLoader[dict[str, Tensor]],
    device: torch.device,
    args: argparse.Namespace,
) -> tuple[dict[str, float], tuple[dict[str, Tensor], dict[str, Tensor]] | None]:
    model.eval()
    rows = []
    review = None
    for index, cpu_batch in enumerate(loader):
        batch = {key: value.to(device, non_blocking=True) for key, value in cpu_batch.items()}
        with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=args.amp and device.type == "cuda"):
            _, metrics, tensors = compute_losses(
                model, batch, args.temporal_weight, args.smoothness_weight, args.nochange_weight
            )
        rows.append(tensor_metrics(metrics))
        if review is None:
            review = (cpu_batch, {key: value.cpu() for key, value in tensors.items()})
        if args.max_eval_batches and index + 1 >= args.max_eval_batches:
            break
    return aggregate_metrics(rows), review


def make_review_artifacts(
    review: tuple[dict[str, Tensor], dict[str, Tensor]], output_dir: Path, epoch: int, fps: int
) -> dict[str, str]:
    cpu_batch, tensors = review
    source = cpu_batch["source_rgb"][0]
    source_y = tensors["source_y"][0]
    source_cbcr = tensors["source_cbcr"][0]
    target_cbcr = tensors["target_cbcr"][0]
    prediction = tensors["prediction"][0]
    baseline_rgb = ycbcr_to_rgb(source_y, source_cbcr)
    target_rgb = ycbcr_to_rgb(source_y, target_cbcr)
    predicted_rgb = ycbcr_to_rgb(source_y, prediction)
    rows = []
    frames = []
    for frame_index in range(source.shape[0]):
        tiles = [source[frame_index], baseline_rgb[frame_index], predicted_rgb[frame_index], target_rgb[frame_index]]
        tile_np = [(item.permute(1, 2, 0).numpy() * 255.0).clip(0, 255).astype(np.uint8) for item in tiles]
        row = np.concatenate(tile_np, axis=1)
        cv2.putText(
            row,
            "source RGB | source-Y/source-CbCr | source-Y/predicted-CbCr | source-Y/target-CbCr",
            (8, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (255, 255, 0),
            1,
            cv2.LINE_AA,
        )
        rows.append(row)
        frames.append(tile_np[2])
    review_dir = output_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    sheet_path = review_dir / f"epoch_{epoch:03d}_contact_sheet.jpg"
    sheet = np.concatenate(rows, axis=0)
    cv2.imwrite(str(sheet_path), cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    video_path = review_dir / f"epoch_{epoch:03d}_prediction.mp4"
    height, width = frames[0].shape[:2]
    process = subprocess.Popen(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{width}x{height}",
            "-r",
            str(fps),
            "-i",
            "pipe:0",
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(video_path),
        ],
        stdin=subprocess.PIPE,
        **process_options(),
    )
    assert process.stdin is not None
    for frame in frames:
        process.stdin.write(frame.tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("FFmpeg could not create review MP4")
    return {"contact_sheet": str(sheet_path), "prediction_video": str(video_path)}


def limited_subset(dataset: Dataset[Any], maximum: int, seed: int) -> Dataset[Any]:
    if not maximum or len(dataset) <= maximum:
        return dataset
    generator = torch.Generator().manual_seed(seed)
    indices = torch.randperm(len(dataset), generator=generator)[:maximum].tolist()
    return Subset(dataset, indices)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument(
        "--eval-dataset-dir",
        help="Optional separate dataset cache for validation; defaults to --dataset-dir.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--sequence-length", type=int, default=8)
    parser.add_argument("--train-stride", type=int, default=4)
    parser.add_argument("--eval-stride", type=int, default=8)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--base-channels", type=int, default=24)
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--temporal-weight", type=float, default=0.25)
    parser.add_argument("--smoothness-weight", type=float, default=0.015)
    parser.add_argument("--nochange-weight", type=float, default=0.05)
    parser.add_argument("--max-train-windows", type=int, default=0)
    parser.add_argument("--max-eval-windows", type=int, default=128)
    parser.add_argument("--steps-per-epoch", type=int, default=0)
    parser.add_argument("--max-eval-batches", type=int, default=0)
    parser.add_argument("--overfit-shot", action="append", default=[])
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--seed", type=int, default=115)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--amp", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--resume")
    parser.add_argument(
        "--generated-targets",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Record whether the supervised targets are generated/derived rather than true photographed ground truth.",
    )
    parser.add_argument(
        "--target-provenance",
        default="",
        help="Human-readable target provenance recorded in the run manifest.",
    )
    parser.add_argument("--fps", type=int, default=24)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    device = torch.device(args.device)
    dataset_dir = Path(args.dataset_dir).resolve()
    eval_dataset_dir = Path(args.eval_dataset_dir).resolve() if args.eval_dataset_dir else dataset_dir
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    shot_filter = {item.upper() for item in args.overfit_shot} or None
    train_split = "all" if shot_filter else "train"
    eval_split = "all" if shot_filter else "val"
    train_data = FrontierTemporalDataset(
        dataset_dir, train_split, args.sequence_length, args.train_stride, True, shot_filter
    )
    eval_data = FrontierTemporalDataset(
        eval_dataset_dir, eval_split, args.sequence_length, args.eval_stride, False, shot_filter
    )
    train_data_limited = limited_subset(train_data, args.max_train_windows, args.seed)
    eval_data_limited = limited_subset(eval_data, args.max_eval_windows, args.seed + 1)
    sampler = None
    if args.steps_per_epoch:
        sampler = RandomSampler(
            train_data_limited,
            replacement=True,
            num_samples=args.steps_per_epoch * args.batch_size,
            generator=torch.Generator().manual_seed(args.seed),
        )
    train_loader = DataLoader(
        train_data_limited,
        batch_size=args.batch_size,
        shuffle=sampler is None,
        sampler=sampler,
        num_workers=args.num_workers,
        pin_memory=device.type == "cuda",
    )
    eval_loader = DataLoader(
        eval_data_limited,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=device.type == "cuda",
    )

    model = TemporalCbCrAdapter(args.base_channels).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    scaler = torch.amp.GradScaler("cuda", enabled=args.amp and device.type == "cuda")
    start_epoch = 1
    best_val = math.inf
    if args.resume:
        checkpoint = torch.load(args.resume, map_location=device, weights_only=False)
        model.load_state_dict(checkpoint["model"])
        optimizer.load_state_dict(checkpoint["optimizer"])
        for parameter_group in optimizer.param_groups:
            parameter_group["lr"] = args.learning_rate
            parameter_group["weight_decay"] = args.weight_decay
        start_epoch = int(checkpoint["epoch"]) + 1
        best_val = float(checkpoint.get("best_val", math.inf))

    manifest = {
        "experiment_id": EXPERIMENT_ID,
        "journal_code": JOURNAL_CODE,
        "created_unix": time.time(),
        "script": "scripts/train_t115_temporal_cbcr_adapter.py",
        "dataset_dir": str(dataset_dir),
        "eval_dataset_dir": str(eval_dataset_dir),
        "output_dir": str(output_dir),
        "device": str(device),
        "gpu": torch.cuda.get_device_name(device) if device.type == "cuda" else None,
        "torch_version": torch.__version__,
        "parameters": vars(args),
        "model_parameters": sum(parameter.numel() for parameter in model.parameters()),
        "windows": {"train": len(train_data_limited), "eval": len(eval_data_limited)},
        "policy": {
            "source_y_authoritative": True,
            "prediction": "residual CbCr",
            "generated_targets": bool(args.generated_targets),
            "target_provenance": args.target_provenance or None,
            "alignment_changes": False,
        },
    }
    manifest["parameters"]["dataset_dir"] = str(dataset_dir)
    manifest["parameters"]["output_dir"] = str(output_dir)
    write_json(output_dir / "run_manifest.json", manifest)

    metrics_path = output_dir / "metrics.jsonl"
    checkpoints = output_dir / "checkpoints"
    checkpoints.mkdir(parents=True, exist_ok=True)
    started = time.time()
    for epoch in range(start_epoch, args.epochs + 1):
        model.train()
        train_rows = []
        for cpu_batch in train_loader:
            batch = {key: value.to(device, non_blocking=True) for key, value in cpu_batch.items()}
            optimizer.zero_grad(set_to_none=True)
            autocast = torch.autocast(
                device_type=device.type, dtype=torch.float16, enabled=args.amp and device.type == "cuda"
            )
            with autocast:
                loss, metrics, _ = compute_losses(
                    model, batch, args.temporal_weight, args.smoothness_weight, args.nochange_weight
                )
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            train_rows.append(tensor_metrics(metrics))
        train_metrics = aggregate_metrics(train_rows)
        val_metrics, review = evaluate(model, eval_loader, device, args)
        improved = val_metrics["prediction_mae"] < best_val
        best_val = min(best_val, val_metrics["prediction_mae"])
        checkpoint = {
            "epoch": epoch,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "best_val": best_val,
            "args": vars(args),
        }
        torch.save(checkpoint, checkpoints / "latest.pt")
        if improved:
            torch.save(checkpoint, checkpoints / "best.pt")
        review_paths = make_review_artifacts(review, output_dir, epoch, args.fps) if review else {}
        row = {
            "epoch": epoch,
            "train": train_metrics,
            "val": val_metrics,
            "best_val": best_val,
            "improved": improved,
            "review": review_paths,
            "elapsed_seconds": time.time() - started,
        }
        with metrics_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")
        print(json.dumps(row), flush=True)
    summary = {
        "status": "completed",
        "epochs": args.epochs,
        "best_val_prediction_mae": best_val,
        "latest_checkpoint": str(checkpoints / "latest.pt"),
        "best_checkpoint": str(checkpoints / "best.pt"),
        "duration_seconds": time.time() - started,
    }
    write_json(output_dir / "training_summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
