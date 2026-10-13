---
layout: default
title: Qwen Image Edit Workflow
parent: Open-Weight Color Recovery
nav_order: 1
grand_parent: Colour Recovery
---

# Qwen Image Edit Colour Recovery Workflow

I've taken down the single-frame workflow that used to be here. It was an earlier version of the research, and this site only offers what I'm using now and can reproduce.

The current route is for pre-balanced footage: one palette still made from the scan's own brightness, with the faded frame as a hint of which hue each object had, carried through the shot and then checked against the colour that survived in the scan. You can download it now: the [faded colour recovery kit for pre-balanced scans](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/tree/main/docs/downloads/faded-colour-recovery-t185) has the ComfyUI graphs, the Python steps and a README that walks through one shot. I re-ran each step from the kit against a shot I approved, and the results match to within a colour difference you can't see (average ΔE 1.34 or less). The Comfy Cloud version of the palette still hasn't been tested yet. For the wider picture, see [where the research stands]({{ '/research-status/' | relative_url }}).

| File | What it is |
|---|---|
| [`1_palette_still_fp8mixed_local.json`]({{ '/downloads/faded-colour-recovery-t185/graphs/1_palette_still_fp8mixed_local.json' | relative_url }}) | The palette still, for your own computer. |
| [`1_palette_still_bf16_cloud.json`]({{ '/downloads/faded-colour-recovery-t185/graphs/1_palette_still_bf16_cloud.json' | relative_url }}) | The same graph with the bf16 model, for Comfy Cloud. Not tested on Cloud yet. |
| [`2_h3_fun_controlnet_local.json`]({{ '/downloads/faded-colour-recovery-t185/graphs/2_h3_fun_controlnet_local.json' | relative_url }}) | The shot with MiniMax H3 and the Fun ControlNet, for your own computer. |
| [Python steps and README](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/tree/main/docs/downloads/faded-colour-recovery-t185) | Preparing the shot, lining up H3 with the film, the Temporal CbCr adapter and the respect step. |
