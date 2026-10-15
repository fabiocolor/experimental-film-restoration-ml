---
layout: default
title: "Downloads"
nav_order: 5.5
permalink: /downloads/
---

# Download kits

Each kit reproduces a published example from the files on this site, and says how closely. The ComfyUI graphs use built-in nodes only; where a step is Python, the script is included. The models are public and listed with links on each kit page.

ΔE is the average CIEDE2000 colour difference against the approved result; 1.5 is the pass mark used here, and about 2.3 is the smallest difference most viewers can see.

| Kit | Area | What it does | Runs on | Checked against the approved result |
| --- | --- | --- | --- | --- |
| [Single-frame kit]({{ '/downloads/colour-recovery-single-frame/' | relative_url }}) | Faded colour recovery | One faded frame to one colour frame, composite included, no Python | ComfyUI, local or Comfy Cloud | Sampler identical to the research graph; core-node rerun mean ΔE 1.89 to the approved still |
| [Balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}) | Faded colour recovery | A balanced shot end to end: palette still, H3 with the Fun ControlNet, Temporal CbCr adapter, surviving-colour step | ComfyUI + Python, NVIDIA GPU; the palette still also in Comfy Cloud | Every stage within ΔE 1.5 (0.61, 1.34, 1.20, identical) |
| [Healing second-pass kit]({{ '/downloads/gap-filling-second-pass/' | relative_url }}) | Diffusion healing | The Wan VACE refinement pass and the seam blend on the Wong flute players shot | ComfyUI + Python, NVIDIA GPU | ΔE 0.9 |
| [Stairs kit]({{ '/downloads/upscaling-stairs/' | relative_url }}) | Diffusion reconstruction | The four MiniMax H3 windows and the seam blend of the *El Tinterillo* stairs shot | ComfyUI + Python, NVIDIA GPU | Hybrid identical; seam blend ΔE 1.07 |
| [Nuke template](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest) | Temporal CbCr | The CopyCat colour-recovery template for Nuke Non-Commercial or Indie, with the [workflow guide]({{ '/copycat-workflow/' | relative_url }}) | Nuke | Used on the *Candy Candy* example |

## What is not published yet

- The first pass of the healing route (the H3 storyboard step), and the full reconstruction route beyond the stairs windows.
- The black-and-white colourization route. Its examples are on the site; the graphs follow once the stock models are settled.
- The *Knights of the Trail* material, shown by courtesy of the George Eastman Museum, is not offered for download.
- Any trained weights: each Temporal CbCr adapter is trained for one shot in minutes, so the code is published, not the weights.

## Comfy Cloud

Comfy Cloud runs the single-frame graph and the palette-still graph as they are, with the bf16 model from its own library. The published recipe uses the fp8mixed model, which has to be imported from Hugging Face (Creator plan or higher). The video steps (MiniMax H3, Wan VACE) and the Python steps run locally.

## Hardware

See [What is possible now]({{ '/research-status/' | relative_url }}#hardware) for what each area needs.
