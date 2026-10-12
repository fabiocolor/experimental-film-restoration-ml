---
layout: default
title: Where the Research Stands
nav_order: 1
permalink: /research-status/
---

<p class="eyebrow">October 2026</p>

# Where the research stands

This page sums up my research as of October 2026, after SEAPAVAA (June) and FIAT/IFTA (October). It covers what works, what doesn't yet, and what you can actually reproduce. For the examples themselves, see the [FIAT/IFTA 2026 companion]({{ '/fiat-ifta-2026-companion/' | relative_url }}) and the [SEAPAVAA 2026 companion]({{ '/seapavaa-2026-companion/' | relative_url }}).

What has worked best this year is keeping the original picture of the film and letting the model add only what is missing: the colour, a gap, a word. None of these workflows is one click. It's always a restorer who decides what is acceptable and who says what was generated.

## Colour recovery with a reference (CopyCat in Nuke)

This is where the research started, and it's still my baseline. You train a small model for each film, using matching frames from two copies: the damaged scan as the source and a better copy as the ground truth. It needs that better copy to learn from.

**What you can use.** A Nuke template, available for **Nuke Non-Commercial** (`.nknc`) and **Nuke Indie** (`.nkind`) from the [releases page](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/latest). Be clear about what it is:

- It's a template that you run **locally**, in your own copy of Nuke, **with your own footage**. You use it to build a dataset for each shot and train CopyCat on it.
- **There is no cloud version** of the Nuke workflow, and no hosted service.
- It doesn't include footage, trained models or references. Those come from your project.

The [CopyCat workflow guide]({{ '/copycat-workflow/' | relative_url }}) explains the steps.

## Colour recovery without a reference (Qwen Image Edit)

When there's no better copy, I create what I call a synthetic reference: an approved colour frame for each shot. The main model is Qwen Image Edit, run in ComfyUI.

**What works now**

- **Single frames.** Qwen Image Edit 2511, guided by an edge map of the source and a softly blurred colour chart, gives useful colour on varied faded material. A person still needs to review every frame, and the colour is an interpretation.
- **Whole shots, with approved references.** The frames only agree with each other when the whole shot is guided by an approved reference:
  - TeleStyle, a LoRA for Qwen Image Edit, copying one approved reference onto every frame.
  - MiniMax H3 with Alibaba's Fun ControlNet for H3, using the edges of every frame to keep the geometry.
  - The Temporal CbCr adapter, a small model I built. It learns the colour of one shot from the frames that passed review (the teachers) and fills in the rest. On the *Unman, Wittering and Zigo* choir shot, about a hundred frames became teachers and training took about a minute and a half.

  Each of these worked on specific shots that I reviewed at full size. That isn't proof that they work on every shot.

**What still fails or is limited**

- **Semantic contamination.** A leader lady used as a reference ends up in the shot. A plain, blurred colour chart avoids it.
- **Frame by frame doesn't hold.** Each frame is a fair interpretation on its own, but together they flicker.
- **Resolution and length.** The video models see a reduced picture, around 768 × 432, and about ten seconds at a time. Tiling keeps more detail, but the colour drifts between tiles and you get seams.
- **Hard motion and broken cadence.** The best *Counter Attack* result still has some tint in the shadows, because the source had a broken cadence.
- **Time.** An 11-second shot with TeleStyle took around four hours.
- **Generalisation.** My target is at least 75% acceptable first-pass recovery on new shots. I haven't shown that yet.

**What I'm working on now**

- One app that runs the current route, H3 with the Fun ControlNet followed by the Temporal CbCr adapter, on new shots, instead of one experiment at a time.
- Tests on sources that were balanced by hand first.
- A cleaner, self-contained ComfyUI version that someone else can run.

**What you can reproduce**

- The **single-frame workflow** is on the [Qwen Image Edit workflow page]({% link qwen-color-recovery-app.md %}). It's a research snapshot, not a finished tool.
- The **whole-shot routes** aren't reproducible from this site yet. They depend on my own job system and on the Temporal CbCr adapter, which isn't public yet.
- The **example workflows** from SEAPAVAA and FIAT/IFTA exist, but they aren't fully usable yet.
- **ComfyUI Cloud.** The Qwen Image Edit workflow can technically run on ComfyUI Cloud, but I haven't validated that route professionally.

## Diffusion upscaling and diffusion reconstruction

The second half of the FIAT/IFTA talk was about rebuilding picture, not colour.

- **Diffusion upscaling.** When every frame of the surviving element is damaged, there's nothing left to borrow. On *El Tinterillo* I combined a 16mm print and a telecine, cleaned the result with a median filter to get a rough outline, and guided MiniMax H3 with a synthetic reference. The result has a synthetic look. I wouldn't call it proper film restoration myself, and lip movement on small faces is still a problem.
- **Diffusion reconstruction.** When frames are completely missing, I first use what survives in other elements, then generate only inside the gap. On *Knight of the Trail* (1915), with elements from the George Eastman Museum, I registered a nitrate print and a diacetate safety copy, mapped which element survives frame by frame, and used masked reconstruction (Wan VACE 14B, with pose control) only where neither survives. The work at the original resolution is still open.

These projects aren't public as workflows yet.

## Hardware

- A modern **NVIDIA** GPU.
- **8 GB** of VRAM or more for still frames, using the fp8 or GGUF versions of Qwen Image Edit.
- **16 GB** or more for video.
- On Apple Silicon, the bf16 version of Qwen Image Edit 2509 runs, but the fp8 checkpoints don't.
- For CopyCat, see Foundry's own requirements for your edition of Nuke.

## Models and licences

| Model | Publisher | Licence (per the model card) |
|---|---|---|
| [Qwen Image Edit 2509 and 2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) | Qwen team, Alibaba | Apache-2.0 |
| [Qwen Image Edit Lightning LoRAs](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning) | LightX2V | Apache-2.0 |
| [TeleStyle V2](https://huggingface.co/Tele-AI/TeleStyleV2) | TeleAI | Apache-2.0 |
| [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) | MiniMax | MiniMax H3 Community License Agreement. There's an application form for the USA, EU, UK and South Korea, so check the terms for your country. |
| Fun ControlNet for H3 | Alibaba PAI | Check the model card |

## How to read my results

When I say a result was "approved", I mean I watched the whole shot at full size and accepted it as a research result for that shot. It doesn't mean the method is ready for production work, or that the colour is historically accurate. Colour made without a reference is always an interpretation.

The images and clips on these pages are for viewing. The film material belongs to its owners, and credit isn't permission to reuse it.
