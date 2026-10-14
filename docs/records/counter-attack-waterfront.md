---
layout: default
title: "Counter Attack, waterfront"
parent: "Example Records"
nav_order: 2
permalink: /records/counter-attack-waterfront/
---

# Counter Attack (1976), waterfront: record

| | |
| --- | --- |
| Source | A faded film copy of *Counter Attack* (反击, 1976), unbalanced, faded to magenta-red. Source frames 17804–18141 (338 frames), 1920 × 1440, 30 fps. No colour reference survives. |
| Route | MiniMax H3 with three reference stills for the whole shot (three sections, stitched in their overlaps). On 30 frames of hand movement (17946–17959 and 17996–18011), where H3 lost registration, the colour was replaced with an independent TeleStyle pass on the same shot. The scan's own luma is kept on every frame. No masks. |
| Models | H3: [`minimax_h3_ref2va_int8_convrot`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_ref2va_int8_convrot.safetensors), [`qwen3vl_32b_minimax_h3_nvfp4_awq`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors), [`minimax_h3_video_vae_fp16`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/vae/minimax_h3_video_vae_fp16.safetensors). TeleStyle: [`qwen_image_edit_2511_fp8mixed`](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/blob/main/split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors) with the TeleStyle LoRA. |
| Settings | Repair weight 1.0 with a 2-frame ramp at each end. The TeleStyle frames were reused from an earlier run on the same shot; no new inference for the final assembly. |
| Approval | Fabio accepted the shot and promoted the method on 9 August 2026. |
| Method record | SHA-256 `a76a53b432e7e9b844f9ad91bea357cc28857f6946f3b9af99dbe101d2afdcc7` (research repository). H3 base video SHA-256 `51214a94c6a3d6796a7a3fc1fa6b9b227edb64742d053a15c6198c06782eec6f`. |
| Colour check | Red, green and blue all present: median score 3.52 across the shot, 6.21 on the frame shown (R 29.5, G 19.0, B 6.2). |
| Reproduction | Not yet. The H3 and TeleStyle graphs, the reference stills and the source frames are not published, and the run has not been repeated from public files. |

The still on the [colour recovery page]({{ '/colour-recovery/' | relative_url }}) is frame 160 of the shot (source frame 17964). The source panel comes from an earlier comparison of the same shot, so the framing differs slightly.
