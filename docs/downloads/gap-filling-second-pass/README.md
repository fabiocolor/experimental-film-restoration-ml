---
layout: default
title: "Download: Healing Second Pass"
parent: "Diffusion Healing"
nav_order: 90
permalink: /downloads/gap-filling-second-pass/
---

# Diffusion healing: the second pass

The last step of the flute players shot on the diffusion healing page. The first pass (MiniMax H3, with the film's own drumming kept where H3 couldn't follow it) leaves two kinds of picture side by side. A light Wan VACE pass makes them consistent without changing geometry or motion.

On the example files it matches the approved result to ΔE 0.9 on average, and each window to ΔE 0.6 or better, below the visible threshold. Source, first pass, models and approval are in the [record]({{ '/records/wong-flute-players/' | relative_url }}).

## What you need

- ComfyUI with the built-in Wan nodes. No custom nodes.
- Models, all public:
  - [`wan2.1_vace_14B_fp16.safetensors`](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/blob/main/split_files/diffusion_models/wan2.1_vace_14B_fp16.safetensors) (diffusion_models)
  - [`umt5_xxl_fp8_e4m3fn_scaled.safetensors`](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/blob/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors) (text_encoders)
  - [`wan_2.1_vae.safetensors`](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/blob/main/split_files/vae/wan_2.1_vae.safetensors) (vae)
- Python 3.10+ with `numpy` and `opencv-python`, and `ffmpeg` on your path, for the seam blend.

## Steps

1. **Second pass.** Load `graph/second_pass_vace_refine_ui.json` (laid out, with notes on what the pass does and what should and should not change; `second_pass_vace_refine.json` is the same graph in API format), point the Load Video node at one 81-frame window of your first pass, and run. It encodes the window as the starting point and samples at denoise 0.30 (seed 0, 30 steps, CFG 4.5), with the same window as the VACE control. Run it once for each window. Each window overlaps the next by 30 frames.
2. **Pack each window.** The graph saves PNG frames. Pack each window losslessly, for example `ffmpeg -framerate 24 -i second_pass_%05d_.png -c:v ffv1 -pix_fmt bgr0 W1.mkv`.
3. **Seam blend.** `INPUT_DIR=<folder with W1.mkv W2.mkv W3.mkv> OUTPUT_DIR=out python tools/run_blend_example.py`. It uses the overlaps to remove the tone steps at the cuts. For your own shot, change the windows and cuts in `run_blend_example.py`.

The prompt in the graph describes this shot. Write your own for your footage, and keep the last sentence: it asks the model to keep every person, hand, prop and movement exactly as they are.

## Example

`example/` has the three first-pass windows of the flute players shot (frames 0–80, 51–131 and 102–182, 768 × 560). The approved result is the reconstruction video on the diffusion healing page.

The larger example files are hosted outside the repository. Download them into `example/` before you start:

- [`first_pass_frames_0_80.mp4`](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/first_pass_frames_0_80.mp4)
- [`first_pass_frames_102_182.mp4`](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/first_pass_frames_102_182.mp4)
- [`first_pass_frames_51_131.mp4`](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/first_pass_frames_51_131.mp4)

## Comfy Cloud

The graph uses only built-in nodes and standard Wan 2.1 files, so it should run on Comfy Cloud. It has not been tested there yet.
