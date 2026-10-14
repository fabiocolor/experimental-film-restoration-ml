---
layout: default
title: "The General, garden"
parent: "Example Records"
nav_order: 20
permalink: /records/general-1926-garden/
---

# The General, garden (1926): record

| | |
| --- | --- |
| Source | *The General* (1926, Buster Keaton and Clyde Bruckman). Annabelle reads in the garden. 124 frames. |
| Where it came from | Published 1926, US public domain. [archive.org `the-general-1926-remux-1080p-dts-hd-ma-51-x264`](https://archive.org/details/the-general-1926-remux-1080p-dts-hd-ma-51-x264), a copy of a restoration Blu-ray, marked Public Domain Mark 1.0 by the uploader. Only the 1926 picture is used; the restoration's own work, the score and the upload's provenance are not cleared. |
| Route | Earlier route. One Qwen Image Edit 2511 colour frame from the shot (frame 62), placed on the source picture → base MiniMax H3 (no ControlNet) as a colour donor → the source luminance kept byte-exact, colour from the donor. Whole frame, no masks. |
| Models | [`qwen_image_edit_2511_fp8mixed`](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/blob/main/split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors); [MiniMax H3](https://huggingface.co/Comfy-Org/MiniMax-H3) ref2va, int8 with the NVFP4 text encoder [`qwen3vl_32b_minimax_h3_nvfp4_awq`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors) and [`minimax_h3_video_vae_fp16`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/vae/minimax_h3_video_vae_fp16.safetensors). |
| Settings | Qwen: 4 steps, CFG 1, Euler/simple, seed 0. H3: 768 × 576, 124 frames, 20 steps, res_multistep/simple, seed 0. Temporal carry 0.5. |
| Approval | Approved by Fabio in the Review Hub on 25 September 2026. |
| Reproduction | Not yet. The graphs, prompts and colour frames are in the private black-and-white colourization research repository and have not been run again from public files. |

The still on the [black-and-white colourization page]({{ '/black-and-white-colourization/' | relative_url }}) is frame 62 of the shot: the original on the left, the result on the right.

The dress, book and rose colours are an interpretation, not historical fact.
