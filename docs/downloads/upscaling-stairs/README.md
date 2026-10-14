---
layout: default
title: "Download: Reconstruction Stairs Kit"
parent: "Diffusion Reconstruction"
nav_order: 1
permalink: /downloads/upscaling-stairs/
---

# Diffusion reconstruction stairs kit: overlapping H3 windows and seam blend

This is the method behind the stairs shot on the diffusion reconstruction page. MiniMax H3 rebuilds the shot in overlapping sections at 768 × 432, then a light seam blend removes the tone steps at the cuts.

I checked the seam blend against the result I approved: run on the four example windows below, it matches mine to an average colour difference of ΔE 1.07 (you can't see it).

## What you need

- ComfyUI with MiniMax Hailuo / H3 reference-to-video nodes for the four window graphs.
- Python 3.10+ with `numpy`, and `ffmpeg` on your path, for the seam blend.

## Steps

1. **Generate each window.** Load one of the graphs in `graphs/`, point it at the matching `example/` source MP4 and three reference stills, and run. The graphs are for this stairs shot: w1 (frames 1–243), w2b (128–370), w3b (300–542) and w3 (382–624). Keep a calm start for each section. The kit already includes the four H3 windows I used for the check (`example/w1.mp4` and so on), so you can skip this step if you only want to try the join.
2. **Seam blend.** From this folder:

   `INPUT_DIR=example OUTPUT_DIR=out python tools/run_blend_example.py`

   It uses the overlaps to remove the tone steps at cuts 200, 340 and 400 (half-pool 12, dissolve 12). For your own shot, change the windows and cuts in `run_blend_example.py`.

## Example

`example/` has the four source windows, their reference stills, and the four H3 windows for the stairs shot. The result I approved is the stairs video on the diffusion reconstruction page.

The larger example files are hosted outside the repository. Download them into `example/` before you start:

- [`w1.mp4`](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/w1.mp4)
- [`w1_source.mp4`](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/w1_source.mp4)
- [`w2b.mp4`](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/w2b.mp4)
- [`w2b_source.mp4`](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/w2b_source.mp4)
- [`w3.mp4`](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/w3.mp4)
- [`w3_source.mp4`](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/w3_source.mp4)
- [`w3b_source.mp4`](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/w3b_source.mp4)

## Comfy Cloud

The graphs are ordinary ComfyUI JSON. I haven't run this kit on Comfy Cloud yet.
