---
layout: default
title: "Reptilicus, beach"
parent: "Example Records"
nav_order: 1
permalink: /records/reptilicus-beach/
---

# Reptilicus (1961), beach: record

The home-page example. It was made with an earlier single-frame route and is kept because the result holds up. The current route for unbalanced sources is the one used for [Counter Attack]({{ '/records/counter-attack-waterfront/' | relative_url }}).

| | |
| --- | --- |
| Source | *Reptilicus* trailer, from a 35mm trailer reel scan posted publicly on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps). 2048 × 1556, 24 fps, 2,941 frames. Sampled frame 25 of 80 (beach, woman). Unbalanced, faded to magenta. |
| Route | Earlier single-frame route: Qwen Image Edit 2509 with a Canny edge control and a blurred colour chart as the reference, then the scan's own luma composited under the result. |
| Model | [`qwen_image_edit_2509_fp8_e4m3fn.safetensors`](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/blob/main/split_files/diffusion_models/qwen_image_edit_2509_fp8_e4m3fn.safetensors) |
| Reference | Belak colour patch chart, reduced to 32 px, resized back with bicubic and blurred (Gaussian 18). No people or scene content. |
| Settings | Seed 0, CFG 1.0. |
| Approval | Shown at SEAPAVAA 2026; kept by Fabio as the home-page example (October 2026). |
| Reproduction | No kit. The five stages are published below so the result can be checked. |

## Published files (SHA-256)

| Stage | File | SHA-256 |
| --- | --- | --- |
| Source | [`01_source…png`]({{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/01_source_reptilicus_tlr_000025-40689881.png' | relative_url }}) | `0be51b934eaab6144b8d7f344522791205c91f7f1e42c7639537d3a23bace25f` |
| Edge control | [`02_control…png`]({{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/02_control_reptilicus_tlr_05_beach_woman_canny-73d21cd9.png' | relative_url }}) | `350a6b4b0126fabd3c8774b0a4183b93fd1ce45c9ef7de6c066f3a59d90ee83d` |
| Reference | [`03_reference…png`]({{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/03_reference_Belak_Color_Patch_Chart_softblur_32-9142a789.png' | relative_url }}) | `d1718cfe9837039a5ef38d2e0db2de030986345ffed85b0f338eeee62edd24cd` |
| Model output | [`04_inference…png`]({{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/04_inference_frame_000000_seed_0_cfg_1.000_Belak-0c1f0329.png' | relative_url }}) | `02b699058ba44211e2403a32832d22ee098111929e91f6f5eeb209c05a462ec0` |
| Final composite | [`05_final_composite…png`]({{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/05_final_composite_reptilicus_tlr_05_beach_woman_source-38de94d1.png' | relative_url }}) | `75078fbcdc93323260508fe1286f798c8962039d2788dc3c816d7f791733168b` |
