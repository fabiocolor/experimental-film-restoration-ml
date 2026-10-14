#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from typing import Any


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
PREFERRED_KONTEXT_RESOLUTIONS = [
    (672, 1568),
    (688, 1504),
    (720, 1456),
    (752, 1392),
    (800, 1328),
    (832, 1248),
    (880, 1184),
    (944, 1104),
    (1024, 1024),
    (1104, 944),
    (1184, 880),
    (1248, 832),
    (1328, 800),
    (1392, 752),
    (1456, 720),
    (1504, 688),
    (1568, 672),
]


def load_pillow():
    try:
        from PIL import Image, ImageDraw, ImageOps
    except (ImportError, ModuleNotFoundError) as exc:
        raise SystemExit(
            "This script requires Pillow. Run it with the same Python environment used for "
            "scripts/run_prompt_experiment.py, or install Pillow into the active environment."
        ) from exc
    return Image, ImageDraw, ImageOps


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_path(path_value: str | Path, base_dir: Path | None = None) -> Path:
    raw = Path(path_value)
    if raw.is_absolute():
        return raw.resolve()
    base = base_dir or repo_root()
    return (base / raw).resolve()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Path(filesystem_path(path)).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def filesystem_path(path: Path) -> str:
    """Return a Windows extended-length path for APIs that still hit MAX_PATH."""
    raw = str(path.resolve())
    if os.name != "nt" or raw.startswith("\\\\?\\"):
        return raw
    if raw.startswith("\\\\"):
        return "\\\\?\\UNC\\" + raw[2:]
    return "\\\\?\\" + raw


def path_is_file(path: Path) -> bool:
    try:
        return Path(filesystem_path(path)).is_file()
    except OSError:
        return False


def image_file(path: Path) -> bool:
    return path_is_file(path) and path.suffix.lower() in IMAGE_EXTS


def find_single_output(run_dir: Path) -> Path | None:
    if not run_dir.is_dir():
        return None
    candidates = [
        p
        for p in run_dir.rglob("*")
        if image_file(p)
        and "thumb" not in p.name.lower()
        and "contact_sheet" not in p.name.lower()
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda p: (p.stat().st_mtime, str(p)))
    return candidates[-1]


def composite_source_luma_with_result_chroma(
    source_path: Path,
    result_path: Path,
    output_path: Path,
    chroma_crop_box: list[int] | None = None,
    geometry_mode: str = "flux-kontext-inverse",
    flux_kontext_crop_box: list[int] | None = None,
    flux_kontext_x_offset: int = 0,
    flux_kontext_y_offset: int = 0,
    flux_kontext_border_fill: str = "source",
    output_crop_box: list[int] | None = None,
    shadow_chroma_mode: str = "none",
    shadow_luma_start: int = 24,
    shadow_luma_end: int = 80,
    shadow_min_generated_weight: float = 0.15,
) -> dict[str, Any]:
    Image, ImageDraw, ImageOps = load_pillow()
    source = Image.open(filesystem_path(source_path)).convert("RGB")
    result = Image.open(filesystem_path(result_path)).convert("RGB")
    if chroma_crop_box:
        result = result.crop(tuple(int(value) for value in chroma_crop_box))

    source_y, source_cb, source_cr = source.convert("YCbCr").split()
    if geometry_mode == "flux-kontext-inverse":
        result_cb, result_cr = inverse_flux_kontext_chroma_to_source(
            source,
            result,
            crop_box=tuple(int(value) for value in flux_kontext_crop_box) if flux_kontext_crop_box else None,
            x_offset=flux_kontext_x_offset,
            y_offset=flux_kontext_y_offset,
            border_fill=flux_kontext_border_fill,
        )
    else:
        if result.size != source.size:
            result = result.resize(source.size, resample=Image.Resampling.LANCZOS)
        _, result_cb, result_cr = result.convert("YCbCr").split()
    shadow_metrics = apply_shadow_chroma_gate(
        source_y,
        source_cb,
        source_cr,
        result_cb,
        result_cr,
        mode=shadow_chroma_mode,
        luma_start=shadow_luma_start,
        luma_end=shadow_luma_end,
        min_generated_weight=shadow_min_generated_weight,
    )
    composite = Image.merge("YCbCr", (source_y, result_cb, result_cr)).convert("RGB")
    if output_crop_box:
        composite = composite.crop(tuple(int(value) for value in output_crop_box))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    composite.save(filesystem_path(output_path))
    return shadow_metrics


def clamp_int(value: int, low: int, high: int) -> int:
    return min(max(int(value), low), high)


def apply_shadow_chroma_gate(
    source_y,
    source_cb,
    source_cr,
    result_cb,
    result_cr,
    *,
    mode: str,
    luma_start: int,
    luma_end: int,
    min_generated_weight: float,
) -> dict[str, Any]:
    """Limit generated chroma in low-confidence shadows using original source luma."""
    if mode == "none":
        return {"shadow_chroma_mode": "none"}
    if mode not in {"neutral", "source"}:
        raise ValueError(f"Unsupported shadow chroma mode: {mode}")

    Image, _, _ = load_pillow()
    luma_start = clamp_int(luma_start, 0, 255)
    luma_end = clamp_int(luma_end, 0, 255)
    if luma_end <= luma_start:
        raise ValueError("--shadow-luma-end must be greater than --shadow-luma-start")
    min_generated_weight = min(max(float(min_generated_weight), 0.0), 1.0)

    if mode == "neutral":
        base_cb = Image.new("L", result_cb.size, 128)
        base_cr = Image.new("L", result_cr.size, 128)
    else:
        base_cb = source_cb
        base_cr = source_cr

    weight_lut: list[int] = []
    for value in range(256):
        if value <= luma_start:
            weight = min_generated_weight
        elif value >= luma_end:
            weight = 1.0
        else:
            t = (value - luma_start) / (luma_end - luma_start)
            smooth = t * t * (3.0 - 2.0 * t)
            weight = min_generated_weight + (1.0 - min_generated_weight) * smooth
        weight_lut.append(round(weight * 255))

    generated_weight = source_y.point(weight_lut, "L")
    gated_cb = Image.composite(result_cb, base_cb, generated_weight)
    gated_cr = Image.composite(result_cr, base_cr, generated_weight)
    result_cb.paste(gated_cb)
    result_cr.paste(gated_cr)

    histogram = source_y.histogram()
    total = max(sum(histogram), 1)
    deep_shadow_pixels = sum(histogram[: luma_start + 1])
    transition_pixels = sum(histogram[luma_start + 1 : luma_end])
    return {
        "shadow_chroma_mode": mode,
        "shadow_luma_start": luma_start,
        "shadow_luma_end": luma_end,
        "shadow_min_generated_weight": min_generated_weight,
        "deep_shadow_ratio": deep_shadow_pixels / total,
        "transition_shadow_ratio": transition_pixels / total,
    }


def flux_kontext_target_size(source_size: tuple[int, int]) -> tuple[int, int]:
    source_w, source_h = source_size
    source_aspect = source_w / source_h
    _, width, height = min(
        (abs(source_aspect - width / height), width, height)
        for width, height in PREFERRED_KONTEXT_RESOLUTIONS
    )
    return width, height


def flux_kontext_source_crop(
    source_size: tuple[int, int],
    target_size: tuple[int, int],
    *,
    x_offset: int = 0,
    y_offset: int = 0,
) -> tuple[int, int, int, int]:
    source_w, source_h = source_size
    target_w, target_h = target_size
    old_aspect = source_w / source_h
    new_aspect = target_w / target_h
    x = 0
    y = 0
    if old_aspect > new_aspect:
        x = round((source_w - source_w * (new_aspect / old_aspect)) / 2)
    elif old_aspect < new_aspect:
        y = round((source_h - source_h * (old_aspect / new_aspect)) / 2)
    crop_w = source_w - x * 2
    crop_h = source_h - y * 2
    x = min(max(x + int(x_offset), 0), source_w - crop_w)
    y = min(max(y + int(y_offset), 0), source_h - crop_h)
    return x, y, x + crop_w, y + crop_h


def inverse_flux_kontext_chroma_to_source(
    source,
    result,
    *,
    crop_box: tuple[int, int, int, int] | None = None,
    x_offset: int = 0,
    y_offset: int = 0,
    border_fill: str = "source",
):
    Image, _, _ = load_pillow()
    source_w, source_h = source.size
    target_size = flux_kontext_target_size(source.size)
    if crop_box is None:
        crop_box = flux_kontext_source_crop(source.size, target_size, x_offset=x_offset, y_offset=y_offset)
    crop_w = crop_box[2] - crop_box[0]
    crop_h = crop_box[3] - crop_box[1]

    _, result_cb, result_cr = result.convert("YCbCr").split()
    cb_crop = result_cb.resize((crop_w, crop_h), resample=Image.Resampling.LANCZOS)
    cr_crop = result_cr.resize((crop_w, crop_h), resample=Image.Resampling.LANCZOS)

    if border_fill == "edge":
        source_cb = edge_extend_channel(cb_crop, source.size, crop_box)
        source_cr = edge_extend_channel(cr_crop, source.size, crop_box)
    else:
        _, source_cb, source_cr = source.convert("YCbCr").split()
    source_cb.paste(cb_crop, (crop_box[0], crop_box[1]))
    source_cr.paste(cr_crop, (crop_box[0], crop_box[1]))
    return source_cb, source_cr


def edge_extend_channel(channel, canvas_size: tuple[int, int], crop_box: tuple[int, int, int, int]):
    Image, _, _ = load_pillow()
    canvas_w, canvas_h = canvas_size
    left, top, right, bottom = crop_box
    canvas = Image.new("L", canvas_size)
    canvas.paste(channel, (left, top))
    if top > 0:
        canvas.paste(channel.crop((0, 0, channel.width, 1)).resize((channel.width, top)), (left, 0))
    if bottom < canvas_h:
        canvas.paste(
            channel.crop((0, channel.height - 1, channel.width, channel.height)).resize((channel.width, canvas_h - bottom)),
            (left, bottom),
        )
    if left > 0:
        canvas.paste(canvas.crop((left, 0, left + 1, canvas_h)).resize((left, canvas_h)), (0, 0))
    if right < canvas_w:
        canvas.paste(canvas.crop((right - 1, 0, right, canvas_h)).resize((canvas_w - right, canvas_h)), (right, 0))
    return canvas


def make_panel(image_path: Path, label: str, panel_size: tuple[int, int]):
    Image, ImageDraw, ImageOps = load_pillow()
    label_h = 34
    image = Image.open(filesystem_path(image_path)).convert("RGB")
    thumb = ImageOps.contain(image, panel_size)
    canvas = Image.new("RGB", (panel_size[0], panel_size[1] + label_h), (20, 20, 20))
    x = (panel_size[0] - thumb.width) // 2
    y = label_h + (panel_size[1] - thumb.height) // 2
    canvas.paste(thumb, (x, y))
    draw = ImageDraw.Draw(canvas)
    draw.text((10, 10), label[:42], fill=(238, 238, 238))
    return canvas


def make_contact_sheet(rows: list[dict[str, str]], output_path: Path) -> None:
    Image, ImageDraw, ImageOps = load_pillow()
    if not rows:
        return
    panel_size = (320, 220)
    columns = [
        ("source_path", "source"),
        ("control_image_path", "control"),
        ("result_path", "inference"),
        ("composite_path", "source-luma composite"),
    ]
    columns = [column for column in columns if any(row.get(column[0]) for row in rows)]
    row_h = panel_size[1] + 34
    sheet = Image.new("RGB", (panel_size[0] * len(columns), row_h * len(rows)), (12, 12, 12))
    for row_index, row in enumerate(rows):
        for col_index, (key, label) in enumerate(columns):
            if not row.get(key):
                continue
            panel = make_panel(Path(row[key]), f"{row['subject_id']} / {label}", panel_size)
            sheet.paste(panel, (col_index * panel_size[0], row_index * row_h))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(filesystem_path(output_path))


def iter_manifest_entries(manifest: dict[str, Any], experiment_dir: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for prompt_result in manifest.get("prompt_results") or []:
        prompt = prompt_result.get("prompt") or {}
        prompt_id = str(prompt.get("id") or "prompt")
        prompt_label = str(prompt.get("label") or prompt_id)
        for entry in prompt_result.get("entries") or []:
            generation = entry.get("generation") or {}
            output_image = generation.get("output_image_path") or entry.get("result_image_path")
            if not output_image:
                planned = entry.get("planned_run_dir")
                output_path = find_single_output(resolve_path(planned, experiment_dir)) if planned else None
            else:
                output_path = resolve_path(output_image, experiment_dir)
            if not output_path or not path_is_file(output_path):
                continue
            control_image = entry.get("control_image_path") or (entry.get("generation") or {}).get("control_image_path")
            source_luma_path = entry.get("source_luma_path") or entry.get("sourceLumaPath") or entry["input_path"]
            entries.append(
                {
                    "prompt_id": prompt_id,
                    "prompt_label": prompt_label,
                    "subject_id": str(entry.get("subject_id") or output_path.stem),
                    "source_path": resolve_path(source_luma_path, experiment_dir),
                    "proxy_input_path": resolve_path(entry["input_path"], experiment_dir),
                    "control_image_path": resolve_path(control_image, experiment_dir) if control_image else None,
                    "control_type": entry.get("control_type") or (entry.get("generation") or {}).get("control_type"),
                    "result_path": output_path,
                    "chroma_crop_box": entry.get("chroma_crop_box") or entry.get("chromaCropBox"),
                }
            )
    return entries


def write_review_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    fields = [
        "subject_id",
        "prompt_id",
        "control_image_path",
        "control_type",
        "composite_path",
        "diffusion_output_path",
        "chroma_usable",
        "source_luma_preserved",
        "registration_ok",
        "chroma_edges_bleed",
        "hue_or_saturation_issue",
        "accept_for_next_phase",
        "notes",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(filesystem_path(output_path), "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def build_from_manifest(
    experiment_dir: Path,
    output_dir: Path,
    geometry_mode: str,
    *,
    flux_kontext_crop_box: list[int] | None = None,
    flux_kontext_x_offset: int = 0,
    flux_kontext_y_offset: int = 0,
    flux_kontext_border_fill: str = "source",
    output_crop_box: list[int] | None = None,
    shadow_chroma_mode: str = "none",
    shadow_luma_start: int = 24,
    shadow_luma_end: int = 80,
    shadow_min_generated_weight: float = 0.15,
) -> dict[str, Any]:
    manifest_path = experiment_dir / "experiment_manifest.json"
    manifest = load_json(manifest_path)
    rows: list[dict[str, str]] = []
    by_prompt: dict[str, list[dict[str, str]]] = {}

    for item in iter_manifest_entries(manifest, experiment_dir):
        prompt_id = item["prompt_id"]
        subject_id = item["subject_id"]
        composite_path = output_dir / prompt_id / f"{subject_id}_source_luma_result_chroma.png"
        shadow_metrics = composite_source_luma_with_result_chroma(
            item["source_path"],
            item["result_path"],
            composite_path,
            chroma_crop_box=item.get("chroma_crop_box"),
            geometry_mode=geometry_mode,
            flux_kontext_crop_box=flux_kontext_crop_box,
            flux_kontext_x_offset=flux_kontext_x_offset,
            flux_kontext_y_offset=flux_kontext_y_offset,
            flux_kontext_border_fill=flux_kontext_border_fill,
            output_crop_box=output_crop_box,
            shadow_chroma_mode=shadow_chroma_mode,
            shadow_luma_start=shadow_luma_start,
            shadow_luma_end=shadow_luma_end,
            shadow_min_generated_weight=shadow_min_generated_weight,
        )
        row = {
            "subject_id": subject_id,
            "prompt_id": prompt_id,
            "prompt_label": item["prompt_label"],
            "source_path": str(item["source_path"]),
            "proxy_input_path": str(item["proxy_input_path"]),
            "control_image_path": str(item["control_image_path"]) if item.get("control_image_path") else "",
            "control_type": str(item.get("control_type") or ""),
            "result_path": str(item["result_path"]),
            "diffusion_output_path": str(item["result_path"]),
            "composite_path": str(composite_path),
            "chroma_crop_box": item.get("chroma_crop_box") or "",
            "flux_kontext_crop_box": flux_kontext_crop_box or "",
            "output_crop_box": output_crop_box or "",
            "shadow_chroma_mode": shadow_chroma_mode,
            "shadow_chroma_metrics": shadow_metrics,
        }
        rows.append(row)
        by_prompt.setdefault(prompt_id, []).append(row)

    for prompt_id, prompt_rows in by_prompt.items():
        make_contact_sheet(prompt_rows, output_dir / "contact_sheets" / f"{prompt_id}_source_inference_composite.png")
    write_review_csv(rows, output_dir / "chroma_luma_composite_review.csv")

    payload = {
        "experiment_dir": str(experiment_dir),
        "output_dir": str(output_dir),
        "color_space": "YCbCr",
        "method": "source Y channel plus diffusion-result Cb/Cr channels",
        "geometry_mode": geometry_mode,
        "flux_kontext_crop_box": flux_kontext_crop_box,
        "flux_kontext_x_offset": flux_kontext_x_offset,
        "flux_kontext_y_offset": flux_kontext_y_offset,
        "flux_kontext_border_fill": flux_kontext_border_fill,
        "output_crop_box": output_crop_box,
        "shadow_chroma_mode": shadow_chroma_mode,
        "shadow_luma_start": shadow_luma_start,
        "shadow_luma_end": shadow_luma_end,
        "shadow_min_generated_weight": shadow_min_generated_weight,
        "count": len(rows),
        "rows": rows,
    }
    write_json(output_dir / "chroma_luma_composite_manifest.json", payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build source-luma/result-chroma composites for color-recovery benchmark review."
    )
    parser.add_argument(
        "--experiment-dir",
        type=Path,
        required=True,
        help="Prompt experiment directory containing experiment_manifest.json.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory. Defaults to <experiment-dir>/chroma_luma_composites.",
    )
    parser.add_argument(
        "--geometry-mode",
        choices=["resize", "flux-kontext-inverse"],
        default="flux-kontext-inverse",
        help=(
            "How to map diffusion chroma into source-luma space. Defaults to the inverse "
            "Flux/Kontext geometry path used by Qwen Image Edit; use resize only for explicit diagnostics."
        ),
    )
    parser.add_argument("--flux-kontext-x-offset", type=int, default=0)
    parser.add_argument("--flux-kontext-y-offset", type=int, default=0)
    parser.add_argument(
        "--flux-kontext-crop-box",
        nargs=4,
        type=int,
        help=(
            "Explicit source-space crop box x0 y0 x1 y1 used to inverse-map the Qwen/Flux output. "
            "Use this for measured geometry solutions that include scale as well as translation."
        ),
    )
    parser.add_argument("--flux-kontext-border-fill", choices=["source", "edge"], default="source")
    parser.add_argument(
        "--output-crop-box",
        nargs=4,
        type=int,
        help=(
            "Optional final crop box x0 y0 x1 y1 applied after source-Y/result-CbCr compositing. "
            "Useful when source/control were padded before inference and the review artifact should return to content size."
        ),
    )
    parser.add_argument(
        "--shadow-chroma-mode",
        choices=["none", "neutral", "source"],
        default="none",
        help=(
            "Limit generated chroma in low-luma source regions. `neutral` blends shadows toward neutral Cb/Cr; "
            "`source` blends toward the source frame's original Cb/Cr. Default preserves legacy behavior."
        ),
    )
    parser.add_argument(
        "--shadow-luma-start",
        type=int,
        default=24,
        help="Source-luma value at or below which generated chroma is most limited.",
    )
    parser.add_argument(
        "--shadow-luma-end",
        type=int,
        default=80,
        help="Source-luma value at or above which generated chroma is fully used.",
    )
    parser.add_argument(
        "--shadow-min-generated-weight",
        type=float,
        default=0.15,
        help="Generated-chroma weight in deepest shadows when shadow chroma limiting is enabled.",
    )
    args = parser.parse_args()

    experiment_dir = args.experiment_dir.resolve()
    if not path_is_file(experiment_dir / "experiment_manifest.json"):
        raise FileNotFoundError(f"Missing experiment_manifest.json in {experiment_dir}")
    output_dir = (args.output_dir or (experiment_dir / "chroma_luma_composites")).resolve()
    payload = build_from_manifest(
        experiment_dir,
        output_dir,
        args.geometry_mode,
        flux_kontext_crop_box=args.flux_kontext_crop_box,
        flux_kontext_x_offset=args.flux_kontext_x_offset,
        flux_kontext_y_offset=args.flux_kontext_y_offset,
        flux_kontext_border_fill=args.flux_kontext_border_fill,
        output_crop_box=args.output_crop_box,
        shadow_chroma_mode=args.shadow_chroma_mode,
        shadow_luma_start=args.shadow_luma_start,
        shadow_luma_end=args.shadow_luma_end,
        shadow_min_generated_weight=args.shadow_min_generated_weight,
    )
    print(json.dumps({"output_dir": payload["output_dir"], "count": payload["count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
