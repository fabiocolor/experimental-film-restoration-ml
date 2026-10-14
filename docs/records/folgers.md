---
layout: default
title: "Folgers"
parent: "Example Records"
nav_order: 3
permalink: /records/folgers/
---

# Folgers (1970s commercial): record

The reference shot for the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}). It is the only balanced-source example that has been reproduced end to end. It is not used as a showcase image: the result has too little blue (colour score 0.07, pass mark 3).

| | |
| --- | --- |
| Source | One shot from a compilation of 1970s commercials, balanced before recovery. 135 frames, 1024 × 768. |
| Route | Palette still (Qwen Image Edit 2511) → MiniMax H3 with the Fun ControlNet → Temporal CbCr adapter → surviving-colour step. |
| Graphs | `1_palette_still_fp8mixed_local.json`, `2_h3_fun_controlnet_local.json`, in the kit. |
| Models | Listed with links in the [kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}#what-you-need). |
| Settings | Palette still: seed 0, 4 steps (Lightning LoRA). The adapter and respect settings are in `tools/steps/*/\*_spec.json`. |
| Approval | Fabio approved the shot (T185 route). |

## Reproduction (ΔE against the approved result)

| Stage | ΔE | Result |
| --- | --- | --- |
| Palette still | 0.61 | Pass |
| MiniMax H3 | 1.34 | Pass |
| Temporal CbCr adapter | 1.20 | Pass |
| Surviving-colour step | 0 (identical) | Pass |
