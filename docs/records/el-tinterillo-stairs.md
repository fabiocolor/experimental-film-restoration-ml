---
layout: default
title: "El Tinterillo, the reel"
parent: "Example Records"
nav_order: 8
permalink: /records/el-tinterillo-stairs/
---

# El Tinterillo, the stairs and the reel: record

| | |
| --- | --- |
| Source | *El Tinterillo*, a black-and-white film. A heavily damaged 16mm print and a cleaner, cropped telecine of the same shot, both as 1920 × 1080 Rec.709 frames. 624 frames, 24 fps. |
| Route | 1. Hybrid: the 16mm frame, median-filtered, for the full canvas, with the registered telecine inside it. 2. One reference still per section, made from the hybrid with an image generator and checked for geometry. 3. MiniMax H3 in four overlapping windows (w1 1–243, w2b 128–370, w3b 300–542, w3 382–624) at 768 × 432. 4. Seam blend at cuts 200, 340 and 400. |
| Models | [`minimax_h3_ref2va_pruned_int8_convrot`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors), [`qwen3vl_32b_minimax_h3_nvfp4_awq`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors), [`minimax_h3_video_vae_fp16`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/vae/minimax_h3_video_vae_fp16.safetensors), [`minimax_h3_audio_vae_fp32`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/vae/minimax_h3_audio_vae_fp32.safetensors). The reference stills were made with ChatGPT image generation, which is not an open model. |
| Finished | 26 September 2026, the complete stairs shot. |

## The reel

The stairs shot set the look; the other shots of the reel followed the same route with the stairs as the look reference, in overlapping windows of about ten seconds joined with a short tone blend, all at 768 × 432 and 24 fps.

| Shot | Frames | Finished |
| --- | --- | --- |
| FG02, the young man at the door | 410 | 26 September 2026 |
| FG03, the man with glasses | 176 | The look is there; the lip movement is the next target |
| FG04, the young man across the desk | 422 | 26 September 2026 |

The side-by-side videos on the [diffusion full reconstruction page]({{ '/diffusion-full-reconstruction/' | relative_url }}) show 9 seconds from the middle of each shot: the 16mm print on the left, the reconstruction on the right.

## Reproduction

| Step | Check | Result |
| --- | --- | --- |
| 1. Hybrid (`tools/make_hybrid.py`) | Frame 200 rebuilt from the original frames | Identical pixels (ΔE 0) |
| 2. Reference stills | Closed image model; the prompt is published, the result cannot be repeated exactly | Stills published in the kit |
| 3. H3 windows | Not re-run | The four windows used are published |
| 4. Seam blend | Against the published result | ΔE 1.07 |
