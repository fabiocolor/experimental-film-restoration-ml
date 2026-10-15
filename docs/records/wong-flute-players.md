---
layout: default
title: "Wong flute players"
parent: "Example Records"
nav_order: 7
permalink: /records/wong-flute-players/
---

# Wong flute players: record

| | |
| --- | --- |
| Source | A decayed 16mm shot from the Wong Rengifo collection, 183 frames, 24 fps. |
| Route | 1. One storyboard sheet of restored keyframes. 2. MiniMax H3 across the shot, guided by the sheet. 3. In about 8% of the frame, following the drummer's hands and beater, the film's own luma with the restored colour. 4. A low-denoise Wan VACE pass over the assembly, in three 81-frame windows, then a seam blend. |
| Models | H3: [`minimax_h3_ref2va_int8_convrot`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_ref2va_int8_convrot.safetensors), [`qwen3vl_32b_minimax_h3_nvfp4_awq`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors). Second pass: [`wan2.1_vace_14B_fp16`](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/blob/main/split_files/diffusion_models/wan2.1_vace_14B_fp16.safetensors), [`umt5_xxl_fp8_e4m3fn_scaled`](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/blob/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors), [`wan_2.1_vae`](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/blob/main/split_files/vae/wan_2.1_vae.safetensors). |
| Settings | Second pass: denoise 0.30, seed 0, 30 steps, CFG 4.5; windows 0–80, 51–131, 102–182. |
| Finished | 11 October 2026, at working size; work continues on a version that heals the original scan. |
| Reproduction | Second pass and seam blend: ΔE 0.9 on average, 0.6 or better per window (the [kit]({{ '/downloads/gap-filling-second-pass/' | relative_url }})). The first pass (steps 1–3) is described here but its graph is not yet published. |
