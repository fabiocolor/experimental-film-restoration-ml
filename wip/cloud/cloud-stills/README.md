# Cloud stills check (14 Oct 2026) — not pushed

Published source: fabiocolor/experimental-film-restoration-ml @750a391, release examples-2026-10.

## Balanced (T185 palette still) — `balanced/1_palette_still_fp8mixed_cloud.json`
- Identical to published `docs/downloads/faded-colour-recovery-t185/graphs/1_palette_still_fp8mixed_local.json` (API-format JSON; ComfyUI/Cloud can open it, but it has no layout).
- Nodes: all core (LoadImage, UNETLoader, CLIPLoader, VAELoader, LoraLoaderModelOnly, TextEncodeQwenImageEditPlus, FluxKontextImageScale, FluxKontextMultiReferenceLatentMethod, ModelSamplingAuraFlow, CFGNorm, ComfySwitchNode, Primitive*, KSampler, VAEEncode/Decode, SaveImage). No local paths.
- Inputs: example/source_y.png, release faded_frame.png, example/canny.png (upload into nodes 41, 83, 171).
- Local repro via CWC comfyui_graph_v1 (job 7f77ae74…): raw output → tools/composite_still.py → vs example/palette.png: mean ΔE76 0.614 (p95 1.89). PASS (record says 0.61).
- Cloud: text encoder, VAE, Lightning LoRA are in Cloud's library. qwen_image_edit_2511_fp8mixed is NOT → must be imported from HF (Creator plan+). bf16 (in library, free tier) gave ΔE 2.67 earlier → fails bar. int8_convrot (in library) untested (CWC job queued, no worker).
- Final step (composite on source luma, flux-kontext inverse, shadow envelope) is local Python; no core-node equivalent that would match.

## Unbalanced
- No unbalanced still workflow is published on main (the Qwen app page now redirects to /colour-recovery/). Only a screenshot + PNGs on the SEAPAVAA companion page.
- Candidate: Clara Anchor (proven single-frame recipe: fp8mixed, Lightning 4-step, cfg 0.9, seed 0, Canny 80/160, Belak softblur chart) on Counter Attack waterfront, approved still = seapavaa2026/originals/fanji_waterfront_top3/04_clara_anchor.png.
  - `unbalanced/1_clara_anchor_still_fp8mixed_api.json` (core nodes only). CWC run 1886aab9: raw vs approved mean ΔE76 1.89 (p95 4.13). FAIL vs 1.5 bar, visually very close.
  - Rerun with published 03_control.png queued (job d8cd5edc…).
- `faded-qwen-2511-cloud-composite-app_stock_nodes_ui.json` = old SEAPAVAA-era app (Lightning off, 40 steps, bf16, generic prompt). Superseded; don't publish.
