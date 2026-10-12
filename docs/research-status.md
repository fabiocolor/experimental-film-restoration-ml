---
layout: default
title: Where the Research Stands
nav_order: 1
permalink: /research-status/
---

<p class="eyebrow">October 2026</p>

# Where the research stands

This is where my research is in October 2026, after SEAPAVAA in June and FIAT/IFTA in October: what works, what doesn't yet, and what you can try yourself. The examples are on the [FIAT/IFTA 2026 companion]({{ '/fiat-ifta-2026-companion/' | relative_url }}) and the [SEAPAVAA 2026 companion]({{ '/seapavaa-2026-companion/' | relative_url }}).

Looking back at this year, what has worked best is keeping the original picture of the film and letting the model add only what's missing: the colour, a gap, a word. None of it is one click, though. It takes a lot of patience, and it's always a restorer who decides what's acceptable and who says what was generated.

## Colour with a reference: CopyCat in Nuke

This is where I started, and it's still my baseline. You train a small model for each film from matching frames of two copies: the damaged scan as the source, and a better copy as the result you want. So it needs that better copy to learn from.

The Nuke template runs locally in Nuke Non-Commercial or Nuke Indie, with your own footage. You use it to build a small dataset for each shot and train CopyCat on it. You can get it from the [releases page](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/latest), and the [CopyCat workflow guide]({{ '/copycat-workflow/' | relative_url }}) walks through the steps.

## Colour without a reference: Qwen Image Edit

When there's no better copy, I create what I call a synthetic reference: an approved colour frame for each shot. For that I use Qwen Image Edit, running in ComfyUI.

**What works now**

- **Single frames.** Qwen Image Edit 2511, guided by an edge map of the frame and a softly blurred colour chart, gives useful colour on all kinds of faded material. Someone still has to review every frame, and the colour is an interpretation.
- **Whole shots.** The frames only agree with each other when the whole shot is guided by an approved reference. Three routes have worked for me:
  - TeleStyle, a LoRA for Qwen Image Edit, which copies one approved reference onto every frame.
  - MiniMax H3 with Alibaba's Fun ControlNet for H3, which uses the edges of every frame to keep the geometry.
  - The Temporal CbCr adapter, a small model I built. You keep the frames that pass review (I call them teachers), and the adapter learns the colour of that one shot from them and fills in the rest. On the choir scene from *Unman, Wittering and Zigo*, about a hundred frames became teachers, and training took about a minute and a half.

  Each of these worked on the shots where I tested them, which isn't the same as working on every shot.

**What still doesn't**

- **Semantic contamination.** If you use a leader lady as the reference, she ends up in the shot. A plain colour chart, softly blurred, avoids that.
- **Frame by frame.** Each frame is a fair interpretation on its own, but together they flicker.
- **Resolution and length.** The video models see a reduced picture, around 768 × 432, about ten seconds at a time. Tiling keeps more detail, but the colour drifts between tiles and you get seams.
- **Hard motion and broken cadence.** My best result on a fast crowd shot still has some tint in the shadows, because the copy had a broken cadence.
- **Time.** One 11-second shot with TeleStyle took around four hours.
- **New shots.** I'd like at least three out of four new shots to work on the first pass. I'm not there yet.

**What I'm working on**

- One app that runs the current route on new shots (H3 with the Fun ControlNet, then the Temporal CbCr adapter), instead of one experiment at a time.
- Tests on scans I've balanced by hand first.
- A cleaner ComfyUI version that someone else can run on their own machine.

**What I'd like to do next**

- Make a few workflows from the best examples usable on ComfyUI Cloud, so you can try them without setting up your own GPU. That's a goal for now, not something that's ready.

**What you can try today**

- The single-frame workflow, on the [Qwen Image Edit workflow page]({% link qwen-color-recovery-app.md %}). It's a snapshot of the research, so expect it to change.
- The whole-shot routes aren't on this site yet. They still depend on my own job system and on the adapter, which isn't public.
- The example workflows from SEAPAVAA and FIAT/IFTA exist, but they need more work before someone else can use them.
- The Qwen Image Edit workflow can run on ComfyUI Cloud, but I haven't tested that route properly for restoration work.

## Rebuilding picture: diffusion upscaling and reconstruction

The second half of the FIAT/IFTA talk was about the picture itself.

- **Diffusion upscaling.** When every frame of the surviving element is damaged, there's nothing left to borrow. I combined a 16mm print and a telecine, cleaned the result with a median filter to get a rough outline, and guided MiniMax H3 with a synthetic reference. The result has a synthetic look, and I wouldn't call it proper film restoration myself. Small faces and lip movement are still a problem.
- **Diffusion reconstruction.** When frames are completely gone, I first use whatever survives in the other elements, and then generate only inside the gap, guided by the movement around it (Wan VACE 14B, with pose control). The tests are at reduced resolution so far.

I don't have examples of these two that I can show publicly yet, and the workflows aren't public either.

## Hardware

- A modern NVIDIA GPU.
- 8 GB of VRAM or more for still frames, with the fp8 or GGUF versions of Qwen Image Edit.
- 16 GB or more for video.
- On a Mac with Apple Silicon, the bf16 version of Qwen Image Edit 2509 runs, but the fp8 versions don't.
- For CopyCat, Foundry lists the requirements for each edition of Nuke.

## Models and licences

| Model | Publisher | Licence on the model card |
|---|---|---|
| [Qwen Image Edit 2509 and 2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) | Qwen team, Alibaba | Apache-2.0 |
| [Qwen Image Edit Lightning LoRAs](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning) | LightX2V | Apache-2.0 |
| [TeleStyle V2](https://huggingface.co/Tele-AI/TeleStyleV2) | TeleAI | Apache-2.0 |
| [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) | MiniMax | MiniMax H3 Community License Agreement. The card has an application form for the USA, the EU, the UK and South Korea, so it's worth checking the terms where you are. |
| Fun ControlNet for H3 | Alibaba PAI | See the model card |

## A note on "approved"

When I say I approved a result, I mean I watched the whole shot at full size and accepted it as a research result for that shot. It doesn't mean the colour is historically accurate. Colour made without a reference is always an interpretation.

The examples on these pages are faded trailers from a 35mm trailer reel scan posted publicly on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps). The trailers belong to their rights holders.
