"""Preparation: neutral source-Y H3 carrier, source merged-Canny control, palette frame, input sheets.

Carrier: 124 real consecutive clip frames, source Y only (CbCr neutral), area-resized to the H3 canvas, 24 fps CFR.
Control: T181 canny_control recipe (median5 + CLAHE 2.0/8x8 + Canny 40/120 L2, 4 px border masked) on the carrier.
No reversal, padding, duplication, interpolation or retiming.
"""
import json
import os
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, os.environ["CWC_EXPERIMENT_CODE_DIR"])
from vod_color import Encoder, contact_sheets, decode_rgb, probe, sha, ycc  # noqa: E402


def merged_canny(gray):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    edges = cv2.Canny(clahe.apply(cv2.medianBlur(gray, 5)), 40, 120, L2gradient=True) > 0
    edges[:4] = edges[-4:] = False
    edges[:, :4] = edges[:, -4:] = False
    return edges


def main():
    I, O = Path(os.environ["CWC_INPUT_DIR"]), Path(os.environ["CWC_OUTPUT_DIR"])
    O.mkdir(exist_ok=True)
    spec = json.loads((Path(os.environ["CWC_EXPERIMENT_CODE_DIR"]) / "prep_spec.json").read_text())
    (src,) = list((I / "source").glob("*.mkv"))
    assert sha(src) == spec["source_sha256"]
    info = probe(src)
    frames = decode_rgb(src)
    assert len(frames) == spec["frame_count"], (len(frames), spec["frame_count"])
    cw, ch = spec["h3_canvas"]
    cs, n = spec["context_start"], spec["context_frames"]
    assert 0 <= cs and cs + n <= len(frames)

    carrier, control = O / "context.mp4", O / "control.mp4"
    enc_c, enc_k = Encoder(carrier, (cw, ch), 24, crf=10, preset="medium"), Encoder(control, (cw, ch), 24, crf=8, preset="slow")
    density = []
    for i in range(cs, cs + n):
        y, _ = ycc(frames[i])
        g = np.clip(np.rint(cv2.resize(y, (cw, ch), interpolation=cv2.INTER_AREA) * 255), 0, 255).astype(np.uint8)
        enc_c.write(np.repeat(g[..., None], 3, 2))
        e = merged_canny(g)
        density.append(float(e.mean()))
        enc_k.write(np.repeat((e[..., None] * 255).astype(np.uint8), 3, 2))
    enc_c.close()
    enc_k.close()
    for path in (carrier, control):
        p = probe(path)
        assert int(p["nb_read_frames"]) == n and p["avg_frame_rate"] == "24/1", p

    pi = spec["palette_index"]
    cv2.imwrite(str(O / "palette_frame.png"), cv2.cvtColor(frames[pi], cv2.COLOR_RGB2BGR))
    caps = [f"clip {i}{' H3' if cs <= i < cs + n else ''}{' PALETTE' if i == pi else ''}" for i in range(len(frames))]
    contact_sheets(list(frames), caps, O, "inputs")
    receipt = {"schema": "faded_vod_prepare_v1", "source_sha256": spec["source_sha256"], "source_probe": info, "clip_frames": len(frames),
               "context_start": cs, "context_frames": n, "h3_canvas": [cw, ch], "carrier_sha256": sha(carrier), "control_sha256": sha(control),
               "palette_index": pi, "palette_frame_sha256": sha(O / "palette_frame.png"), "control_edge_density": density,
               "transformation": "carrier = BT.709 source Y of real consecutive clip frames, neutral CbCr, area resize, 24fps CFR; no reversal/padding/retiming",
               "control_recipe": "median5 CLAHE2 Canny40/120 L2 on carrier Y, 4px border masked"}
    (O / "prep_receipt.json").write_text(json.dumps(receipt, indent=1))


if __name__ == "__main__":
    main()
