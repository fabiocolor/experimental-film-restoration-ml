---
layout: default
title: "Reptilicus, office"
parent: "Example Records"
nav_order: 4
permalink: /records/reptilicus-office/
---

# Reptilicus (1961), office: record

| | |
| --- | --- |
| Source | *Reptilicus* trailer, from the same archive.org [trailer reel scan](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps). One shot of 253 frames, 2048 × 1556, 24 fps. Unbalanced, faded to magenta. SHA-256 `6e7f39f2ace0cf51ae557e8375f9ba6a5d6eb010393d8815ca8ac20ec91247d5`. |
| Route | Synthetic reference. MiniMax H3 and TeleStyle made candidate frames from one approved palette frame (frame 48). Frames that passed review taught the Temporal CbCr adapter. H3 colour was used directly only on frames 24–74, faded in over 24–31 and out over 68–74. The scan's own luma, timing and audio are kept. No masks. |
| Models | H3: [`minimax_h3_ref2va_int8_convrot`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_ref2va_int8_convrot.safetensors), [`qwen3vl_32b_minimax_h3_nvfp4_awq`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors). TeleStyle: [`qwen_image_edit_2511_fp8mixed`](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/blob/main/split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors). Adapter: the code in the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}) (`tools/steps/adapter/`), trained on this shot only. |
| Approval | Fabio approved the complete shot on 24 September 2026. Approved file SHA-256 `f31696525e6b5d73f79354d941780f66ece259c9ebb0e1691d3e9a3709801465`. |
| Colour check | Red, green and blue all present on the frame shown (frame 66: R 17.5, G 7.4, B 4.7; score 4.72). Median over the shot 0.79. |
| Reproduction | Not yet. The candidate frames, teacher list and adapter settings for this shot are not published. |
