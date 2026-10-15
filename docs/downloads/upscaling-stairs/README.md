---
layout: default
title: "Download: Reconstruction Stairs Kit"
parent: "Diffusion Reconstruction"
nav_order: 1
permalink: /downloads/upscaling-stairs/
---

# Diffusion reconstruction stairs kit: overlapping H3 windows and seam blend

How the stairs shot on the diffusion reconstruction page was made. MiniMax H3 rebuilds the shot in overlapping sections at 768 × 432, because the model can only do about ten seconds at a time, and a light seam blend removes the tone steps at the cuts.

On the four example windows, the seam blend matches the published result to ΔE 1.07 on average, which is smaller than you can see. The hybrid step gives identical pixels. Source and models are in the [record]({{ '/records/el-tinterillo-stairs/' | relative_url }}).

## What you need

- ComfyUI with the built-in MiniMax H3 reference-to-video nodes for the four window graphs. No custom nodes.
- Models, all public:
  - [`minimax_h3_ref2va_pruned_int8_convrot.safetensors`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors) (diffusion_models)
  - [`qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors) (text_encoders; needs an NVIDIA Blackwell GPU)
  - [`minimax_h3_video_vae_fp16.safetensors`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/vae/minimax_h3_video_vae_fp16.safetensors) and [`minimax_h3_audio_vae_fp32.safetensors`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/vae/minimax_h3_audio_vae_fp32.safetensors) (vae)
- Python 3.10+ with `numpy` and `opencv-python`, and `ffmpeg` on your path, for the hybrid and the seam blend.

## Steps

1. **Hybrid and median carrier.** For each reference frame, run

   `python tools/make_hybrid.py --scan FG_01.00000200.png --telecine-dir BG_01/ --frame 200 --last-frame 624 --out hybrids/`

   The 16mm frame is median-filtered (23 px) and reduced to 240 × 135 for the full canvas: the median takes out the damage, and most of the detail with it, leaving the geometry of the shot for the model to follow. The closest telecine frame within ±12 frames is registered into it, tone-matched and feathered in. If the registration doesn't line up, choose another frame. On frame 200 of the stairs shot this gives the same pixels as the published hybrid.
2. **Reference still.** Give an image generator the hybrid (Image 1) and one finished still from the shot (Image 2, look only) with the prompt in `reference/reference_prompt.txt`; replace `{FRAME}` and `{CONTENT}`. The stills used for the published shot were made with ChatGPT image generation, which is not an open model, so this step cannot be repeated exactly. Check each still against its hybrid and throw out any where people or architecture have moved; the still sets the look, and the model will follow its geometry too. The stills used are in `example/`.
3. **Generate each window.** Load one of the `_ui.json` graphs in `graphs/` (laid out, with notes on what the window does and what should and should not happen; the matching `.json` without the suffix is the same graph in API format), point it at the matching `example/` source MP4 and three reference stills, and run. The graphs are for this stairs shot: w1 (frames 1–243), w2b (128–370), w3b (300–542) and w3 (382–624). Start each section in a calm passage; the model gets lost if it starts in the middle of a movement. The kit already includes the four H3 windows used for the check (`example/w1.mp4` and so on), so you can skip steps 1–3 if you only want to try the join.
4. **Seam blend.** From this folder:

   `INPUT_DIR=example OUTPUT_DIR=out python tools/run_blend_example.py`

   It uses the overlaps to remove the tone steps at cuts 200, 340 and 400 (half-pool 12, dissolve 12). The windows don't always agree with each other, so the join is made where they do and dissolved over a few frames. For your own shot, change the windows and cuts in `run_blend_example.py`.

## Example

`example/` has the four source windows, their reference stills, and the four H3 windows for the stairs shot. The published result is the stairs video on the diffusion reconstruction page.

The larger example files are hosted outside the repository. Download them into `example/` before you start:

- [`w1.mp4`](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/w1.mp4)
- [`w1_source.mp4`](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/w1_source.mp4)
- [`w2b.mp4`](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/w2b.mp4)
- [`w2b_source.mp4`](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/w2b_source.mp4)
- [`w3.mp4`](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/w3.mp4)
- [`w3_source.mp4`](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/w3_source.mp4)
- [`w3b_source.mp4`](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/w3b_source.mp4)

## Comfy Cloud

The graphs are standard ComfyUI JSON. The kit hasn't been tried on Comfy Cloud yet.
