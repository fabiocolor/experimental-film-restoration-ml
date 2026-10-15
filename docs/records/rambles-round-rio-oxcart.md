---
layout: default
title: "Rambles 'Round Rio, ox cart"
parent: "Example Records"
nav_order: 26
permalink: /records/rambles-round-rio-oxcart/
---

# Rambles 'Round Rio, ox cart (1921): record

| | |
| --- | --- |
| Source | *Rambles 'Round Rio* (1921), non-fiction. An ox cart on a hillside road. Scan frames 1330–1453. |
| Where it came from | US public domain (published before 1931). Prelinger Archives print, scanned by Internet Archive at 4096 × 3072, 16 fps. The item carries no licence URL. [archive.org `200626_Rambles_Round_Rio`](https://archive.org/details/200626_Rambles_Round_Rio). |
| Route | Qwen Image Edit 2511 colour frames from the shot itself (frames 8, 62 and 116), placed on the source picture → MiniMax H3 with the Fun ControlNet (merged Canny control) as a colour donor → colour rebuilt so the chosen stock would record exactly the greyscale on the film. Whole frame, no masks. |
| Models | [`qwen_image_edit_2511_fp8mixed`](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/blob/main/split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors); [MiniMax H3](https://huggingface.co/Comfy-Org/MiniMax-H3) ref2va, int8 with the NVFP4 text encoder [`qwen3vl_32b_minimax_h3_nvfp4_awq`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors) and [`minimax_h3_video_vae_fp16`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/vae/minimax_h3_video_vae_fp16.safetensors); [`MiniMax-H3-Fun-Controlnet-Union`](https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/blob/main/MiniMax-H3-Fun-Controlnet-Union.safetensors). |
| Settings | Stock reading: Eastman orthochromatic cine negative with a K-2 filter, daylight, linear R, G, B weights 0.026, 0.759, 0.215, chosen once for the film. Qwen: 4 steps, CFG 1, Euler/simple, seed 0. H3: 768 × 576, 124 frames mapped 1:1, 20 steps, res_multistep/simple, seed 0, control strength 1.0. |
| Approval | Approved by Fabio on 11 October 2026 (third version; the two earlier stock readings were approved with notes). |
| Reproduction | Not yet. The graphs, prompts and colour frames are in the private black-and-white colourization research repository and have not been run again from public files. |

The still on the [black-and-white colourization page]({{ '/black-and-white-colourization/' | relative_url }}) is frame 62 of the shot: the original on the left, the result on the right.
