---
layout: default
title: Where the Research Stands
nav_order: 7
permalink: /research-status/
---


# Where the research stands

Where things are in October 2026, after SEAPAVAA in June and FIAT/IFTA in October: what works, what doesn't yet, and what you can try.

What has worked best this year is keeping the film's own picture and letting the model add only what's missing: the colour, a gap or the detail. It takes patience, and a restorer still makes the calls.

## 1. Faded colour recovery

**What works now**

- **Balanced sources.** One palette still from the scan's luma, carried through the shot with MiniMax H3, the Fun ControlNet and the Temporal CbCr adapter, then checked so the red-green colour that survived is never flipped or weakened. Tested on four shots from one source so far, at reduced resolution.
- **Unbalanced sources, single frames.** Qwen Image Edit 2511, guided by an edge map and a softly blurred colour chart, gives useful colour on most faded material, with every frame reviewed.
- **Unbalanced sources, whole shots.** Frames from H3 or TeleStyle that pass review become teachers for the Temporal CbCr adapter, which fills in the rest of the shot.

**What still doesn't**

- Frames coloured one at a time flicker.
- A picture used as the colour guide leaks into the shot; a plain colour chart avoids that.
- The video models see a reduced picture, around 768 × 432, about ten seconds at a time. Tiling keeps more detail, but the colour drifts between tiles.
- Hard motion and a broken cadence still leave some tint, as in the *Counter Attack* crowd shot.
- One 11-second shot with TeleStyle took around four hours.
- I'd like at least three out of four new shots to work on the first pass. I'm not there yet.

**What you can try today:** the [download kit for balanced sources]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}). See [Faded Colour Recovery]({{ '/colour-recovery/' | relative_url }}).

## 2. Temporal CbCr

With a historical reference (a DVD, a telecine, another print), a small model learns the colour from matching frames, as on *Candy Candy*. With a synthetic reference, the frames a person approves teach the adapter, as on *Unman, Wittering and Zigo*, where about a hundred frames became teachers and training took about a minute and a half.

**What you can try today:** the Nuke template for CopyCat, from the [releases page](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/latest), with the [CopyCat workflow]({{ '/copycat-workflow/' | relative_url }}) guide. The adapter isn't public yet. See [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}).

## 3. Diffusion healing

When frames are gone or the whole shot has decayed, I first use whatever survives in the other elements, then generate only what's missing, guided by the movement around it. On the decayed 16mm Wong flute players shot, I kept the film's own drumming where generation couldn't follow it. The picture is softer than I'd like, and the fastest strikes still move oddly.

**What you can try today:** the [second-pass kit]({{ '/downloads/gap-filling-second-pass/' | relative_url }}). See [Diffusion Healing]({{ '/diffusion-healing/' | relative_url }}).

## 4. Diffusion reconstruction

For films beyond repair. On *El Tinterillo* I combined a 16mm print and a telecine, cleaned the result with a median filter to get a rough outline, and guided MiniMax H3 with a synthetic reference. The result has a synthetic look, and small faces and lip movement are still a problem.

**What you can try today:** the [stairs kit]({{ '/downloads/upscaling-stairs/' | relative_url }}). See [Diffusion Reconstruction]({{ '/diffusion-reconstruction/' | relative_url }}).

## 5. Black-and-white colourization

Colour for orthochromatic and panchromatic film, inferred from the recorded greyscale and the stock's spectral response. Fifteen public-domain shots are done; skin on the earliest shots and some foliage are still open. See [Black-and-White Colourization]({{ '/black-and-white-colourization/' | relative_url }}).

## What's next

- One app that runs the current colour route on new shots, and a cleaner ComfyUI version someone else can run on their own machine.
- A few of the best examples as ComfyUI Cloud workflows, so you can try them without your own GPU. Not ready yet.

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
| [Fun ControlNet for H3](https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union) | Alibaba PAI | See the model card |

## A note on "approved"

Approved means I watched the whole shot at full size and accepted it as a research result. Colour that survived in the scan is evidence. Colour the model filled in is an interpretation the film can't confirm.

The examples on these pages are my research tests: faded trailers from a 35mm trailer reel scan posted publicly on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps), and copies of other films I worked with. The films belong to their rights holders.
