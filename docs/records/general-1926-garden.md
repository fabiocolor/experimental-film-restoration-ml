---
layout: default
title: "The General, garden and train"
parent: "Example Records"
nav_order: 20
permalink: /records/general-1926-garden/
---

# The General (1926), garden and train: record

| | |
| --- | --- |
| Source | *The General* (1926, Buster Keaton and Clyde Bruckman). Two shots of 124 frames each: Annabelle reads in the garden; the locomotive below the pines, with a pan. |
| Where it came from | Published 1926, US public domain. [archive.org `the-general-1926-remux-1080p-dts-hd-ma-51-x264`](https://archive.org/details/the-general-1926-remux-1080p-dts-hd-ma-51-x264), a copy of a restoration Blu-ray, marked Public Domain Mark 1.0 by the uploader. Only the 1926 picture is used; the restoration's own work, the score and the upload's provenance are not cleared. |
| Route | Garden: one Qwen Image Edit 2511 colour frame from the shot (frame 62), placed on the source picture → base MiniMax H3 (no ControlNet) as a colour donor → the source luminance kept byte-exact, colour from the donor. Train: the same route with three anchors from the shot, start, middle and end of the pan, through multi-image H3, after a first pass left faults in the trees. Whole frame, no masks, no local fixes. |
| Models | [`qwen_image_edit_2511_fp8mixed`](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/blob/main/split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors); [MiniMax H3](https://huggingface.co/Comfy-Org/MiniMax-H3) ref2va, int8 with the NVFP4 text encoder [`qwen3vl_32b_minimax_h3_nvfp4_awq`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors) and [`minimax_h3_video_vae_fp16`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/vae/minimax_h3_video_vae_fp16.safetensors). |
| Settings | Qwen: 4 steps, CFG 1, Euler/simple, seed 0. H3: 768 × 576, 124 frames, 20 steps, res_multistep/simple, seed 0. Temporal carry 0.5. |
| Approval | Both shots approved by Fabio on 25 September 2026; the garden with the note that more complex movement and subjects are the next test, the train at its third version. |
| Reproduction | Not yet. The graphs, prompts and colour frames are in the private black-and-white colourization research repository and have not been run again from public files. |

On the site: the garden reveal (5 seconds) heads the [black-and-white colourization page]({{ '/black-and-white-colourization/' | relative_url }}), the train is its first side-by-side video and the home page's fifth reveal. The original is on the left, the result on the right.

The dress, book and rose colours are an interpretation, not historical fact.
