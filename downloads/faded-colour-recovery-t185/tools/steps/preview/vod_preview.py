"""One-shot preview: bounded same-frame registration of H3 to its carrier, luma gate, source-Y composite.

Registration is the T181 h3_register procedure (DIS-medium carrier-Y -> H3-Y, Gaussian sigma 8, clip +/-4 px,
whole-frame remap, same frame only). The preview composites exact proxy source Y with registered H3 CbCr over the
interior ownership span (carrier minus edge_trim frames at each end; H3 context edges are least reliable).
Registration, gate results and teacher targets are reported for every carrier frame.
"""
import json
import os
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, os.environ["CWC_EXPERIMENT_CODE_DIR"])
from vod_color import Encoder, composite, contact_sheets, decode_rgb, measure, sha, side_by_side, teacher_target, ycc  # noqa: E402
import hashlib  # noqa: E402


def main():
    I, O = Path(os.environ["CWC_INPUT_DIR"]), Path(os.environ["CWC_OUTPUT_DIR"])
    O.mkdir(exist_ok=True)
    spec = json.loads((Path(os.environ["CWC_EXPERIMENT_CODE_DIR"]) / "preview_spec.json").read_text())
    (src,) = list((I / "source").glob("*.mkv"))
    car, h3 = I / "artifacts/donors/context.mp4", I / "artifacts/donors" / spec["h3_filename"]
    assert sha(src) == spec["source_sha256"] and sha(car) == spec["carrier_sha256"] and sha(h3) == spec["h3_sha256"]
    cw, ch = spec["h3_canvas"]
    cs, n, fps = spec["context_start"], spec["context_frames"], spec["fps"]
    source = decode_rgb(src)
    carrier, gen = decode_rgb(car, (cw, ch)), decode_rgb(h3, (cw, ch))
    assert len(carrier) == len(gen) == n, (len(carrier), len(gen))

    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    gx, gy = np.meshgrid(np.arange(cw, dtype=np.float32), np.arange(ch, dtype=np.float32))
    enc_reg = Encoder(O / "registered_h3.mkv", (cw, ch), 24, crf=4, pix_fmt="yuv444p", preset="slow")
    h, w = source.shape[1:3]
    enc_prev = Encoder(O / "preview_recovered.mp4", (w, h), fps, crf=14)
    sbs0 = side_by_side(source[0], source[0])
    enc_sbs = Encoder(O / "preview_side_by_side.mp4", (sbs0.shape[1], sbs0.shape[0]), fps, crf=18)
    aw, ah = spec["adapter_canvas"]
    trim = int(spec.get("edge_trim", 0))
    rows, thumbs, caps, targets = [], [], [], []
    for i in range(n):
        sy = ycc(carrier[i])[0]
        gy0, _ = ycc(gen[i])
        before = measure(sy, gy0)
        flow = dis.calc(np.clip(sy * 255, 0, 255).astype(np.uint8), np.clip(gy0 * 255, 0, 255).astype(np.uint8), None)
        flow = np.clip(cv2.GaussianBlur(flow, (0, 0), 8), -4, 4)
        reg = cv2.remap(gen[i], gx + flow[..., 0], gy + flow[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        gy1, gc1 = ycc(reg)
        after = measure(sy, gy1)
        mags = np.linalg.norm(flow, axis=-1)
        enc_reg.write(reg)
        targets.append(teacher_target(cv2.resize(source[cs + i], (aw, ah), interpolation=cv2.INTER_AREA),
                                      cv2.resize(reg, (aw, ah), interpolation=cv2.INTER_AREA)))
        frame = composite(source[cs + i], gc1)
        if trim <= i < n - trim:
            enc_prev.write(frame)
            enc_sbs.write(side_by_side(source[cs + i], frame))
        rows.append({"carrier_frame": i, "clip_frame": cs + i, "before": before, "after": after,
                     "flow_p50": float(np.percentile(mags, 50)), "flow_p95": float(np.percentile(mags, 95)), "flow_max": float(mags.max()),
                     "chroma_radius_mean": float(np.hypot(gc1[..., 0], gc1[..., 1]).mean()),
                     "target_sha256": hashlib.sha256(np.ascontiguousarray(targets[-1]).tobytes()).hexdigest()})
        thumbs.append(frame)
        caps.append(f"clip {cs + i} {'PASS' if after['pass'] else 'fail'} {after['shift_magnitude']:.1f}/{after['tile_shift_p90'] or -1:.1f}px")
        if i in (0, n // 4, n // 2, 3 * n // 4, n - 1):
            cv2.imwrite(str(O / f"preview_frame_clip{cs + i:03d}.jpg"), cv2.cvtColor(np.hstack([source[cs + i], frame]), cv2.COLOR_RGB2BGR),
                        [cv2.IMWRITE_JPEG_QUALITY, 93])
    for e in (enc_reg, enc_prev, enc_sbs):
        e.close()
    contact_sheets(thumbs, caps, O, "preview_sheet")
    # Exact adapter teacher targets (uint8 RGB, trainer space) for every carrier frame; admission chooses among them.
    stack = np.stack(targets)
    np.savez_compressed(O / "teacher_targets.npz", targets=stack, clip_frames=np.arange(cs, cs + n, dtype=np.int32))
    contact_sheets(list(stack), [f"target clip {cs + i} {'PASS' if rows[i]['after']['pass'] else 'fail'}" for i in range(n)], O, "teacher_board", per_sheet=24, cols=4)
    passed = [r["clip_frame"] for r in rows if r["after"]["pass"]]
    report = {"schema": "faded_vod_registration_v1", "source_sha256": spec["source_sha256"], "carrier_sha256": spec["carrier_sha256"],
              "h3_sha256": spec["h3_sha256"], "registered_sha256": sha(O / "registered_h3.mkv"), "context_start": cs, "context_frames": n,
              "procedure": "DIS-medium same-frame, gaussian sigma 8, clip +/-4 px, whole-frame remap; no masks",
              "gate": "luma only: global <= 1.5 px and tile p90 <= 2.5 px (T180/T181 measurement)",
              "passed_clip_frames": passed, "pass_count": len(passed), "preview_sha256": sha(O / "preview_recovered.mp4"),
              "teacher_targets_sha256": sha(O / "teacher_targets.npz"), "adapter_canvas": [aw, ah], "edge_trim": trim,
              "preview_clip_frames": [cs + trim, cs + n - trim - 1],
              "target_rule": "trainer-space RGB: source Y + registered H3 CbCr composed on source Y (BT.709), area-resized to the adapter canvas",
              "side_by_side_sha256": sha(O / "preview_side_by_side.mp4"), "rows": rows}
    (O / "registration_report.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
