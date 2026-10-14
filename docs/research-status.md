---
layout: default
title: Where the Research Stands
nav_order: 7
permalink: /research-status/
---


# Where the research stands

Status as of October 2026, after SEAPAVAA in June and FIAT/IFTA in October: what works, what does not yet, and what can be reproduced.

The most reliable approach this year has been to keep the film's own picture and use the model only for what is missing: colour, a gap or detail. Each shot needs several iterations, and a restorer makes the decisions.

## 1. Faded colour recovery

**What works now**

- **Balanced sources.** One palette still from the scan's luma, carried through the shot with MiniMax H3, the Fun ControlNet and the Temporal CbCr adapter, then checked so the red-green colour that survived is never flipped or weakened. Tested on four shots from one source so far, at reduced resolution.
- **Unbalanced sources, single frames.** Qwen Image Edit 2511, guided by an edge map and a softly blurred colour chart, gives useful colour on most faded material, with every frame reviewed.
- **Unbalanced sources, whole shots.** Frames from H3 or TeleStyle that pass review become teachers for the Temporal CbCr adapter, which fills in the rest of the shot.

**What does not work yet**

- Frames coloured one at a time flicker.
- A picture used as the colour guide leaks into the shot; a plain colour chart avoids that.
- The video models see a reduced picture, around 768 × 432, about ten seconds at a time. Tiling keeps more detail, but the colour drifts between tiles.
- Hard motion and a broken cadence still leave some tint, as in the *Counter Attack* crowd shot.
- One 11-second shot with TeleStyle took around four hours.
- The target is for at least three out of four new shots to work on the first pass. This has not been reached yet.

**What you can try today:** the [single-frame kit]({{ '/downloads/colour-recovery-single-frame/' | relative_url }}) (one faded frame to one colour frame, in ComfyUI locally or in Comfy Cloud, no Python) and the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}) (a whole shot, end to end). See [Faded Colour Recovery]({{ '/colour-recovery/' | relative_url }}).

## 2. Temporal CbCr

With a historical reference (a DVD, a telecine, another print), a small model learns the colour from matching frames, as on *Frontier Experience* (the adapter, from a telecine) and *Candy Candy* (CopyCat, from a DVD). *Frontier Experience* is the only example completed with the adapter from a historical reference so far. With a synthetic reference, the frames a person approves teach the adapter: on a choir shot from *Unman, Wittering and Zigo*, about a hundred frames became teachers and training took about a minute and a half.

**What you can try today:** the Nuke template for CopyCat, from the [releases page](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest), with the [CopyCat workflow]({{ '/copycat-workflow/' | relative_url }}) guide. The adapter code is in the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}). See [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}).

## 3. Diffusion healing

When frames are missing or the whole shot has decayed, the surviving picture in other elements is used first, and only what is missing is generated, guided by the surrounding movement. On the decayed 16mm Wong flute players shot, the film's own drumming was kept where generation could not follow it. The picture is soft, and the fastest strikes still show unnatural movement.

**What you can try today:** the [second-pass kit]({{ '/downloads/gap-filling-second-pass/' | relative_url }}). See [Diffusion Healing]({{ '/diffusion-healing/' | relative_url }}).

## 4. Diffusion reconstruction

For films beyond repair. On *El Tinterillo*, a 16mm print and a telecine were combined, the result was cleaned with a median filter to get a rough outline, and MiniMax H3 was guided with a synthetic reference. The result has a synthetic look, and small faces and lip movement are still a problem.

**What you can try today:** the [stairs kit]({{ '/downloads/upscaling-stairs/' | relative_url }}). See [Diffusion Reconstruction]({{ '/diffusion-reconstruction/' | relative_url }}).

## 5. Black-and-white colourization

Colour for orthochromatic and panchromatic film, inferred from the recorded greyscale and the stock's spectral response. Fifteen shots are approved; seven public-domain ones are shown on the site; skin on the earliest shots and some foliage are still open. See [Black-and-White Colourization]({{ '/black-and-white-colourization/' | relative_url }}).

## What can be reproduced

Every example on the site has a [record]({{ '/records/' | relative_url }}) of its source, route, models, settings and approval, and the [download kits]({{ '/downloads/' | relative_url }}) reproduce four of them from the published files and say how closely (ΔE against the approved result). The graphs use built-in ComfyUI nodes only, with the model file names, prompt, seed, steps, cfg and sampler in the graph itself, and ComfyUI writes the whole graph into every PNG it saves. That makes a run repeatable on another machine to within the models' own run-to-run variation, which is small at a fixed seed but not zero.

## Comfy Cloud

The two still-frame graphs (the single-frame kit and the balanced kit's palette still) open and run in Comfy Cloud as they are, with the bf16 Qwen Image Edit model from Cloud's own library. The published recipe uses the fp8mixed model, which has to be imported from Hugging Face (Creator plan or higher); the bf16 model gives a visibly different colour on some surfaces (ΔE 2.67 on the palette still). The video steps (MiniMax H3, Wan VACE) and the Python steps run locally.

## Next steps

- One app that runs the current colour route on new shots.
- The healing and reconstruction routes as self-contained ComfyUI graphs beyond the published second-pass and window kits.

## Hardware

| | Still frames (Qwen Image Edit 2511) | Shots (MiniMax H3, Wan VACE, the adapter) | CopyCat in Nuke |
| --- | --- | --- | --- |
| GPU | NVIDIA, 8 GB of VRAM or more with the fp8mixed model (ComfyUI keeps the rest in system RAM); 16 GB or more keeps the 20 GB model on the card | NVIDIA, 16 GB of VRAM or more; 24 GB (RTX 3090/4090) or 32 GB (RTX 5090) for the H3 route at 768 × 576 | Foundry lists the requirements for each edition of Nuke |
| System RAM | 32 GB or more | 64 GB recommended | |
| Storage | About 31 GB of models (20.5 GB model, 9.4 GB text encoder, 254 MB VAE, 850 MB LoRA) | A further 40–60 GB for H3, its text encoder, VAEs and the ControlNet; Wan VACE 14B adds 32 GB | |
| Apple Silicon | The bf16 model (41 GB) runs on a Mac with 64 GB of unified memory or more; the fp8 versions do not | Not tested | |
| Time | Under a minute a frame at 4 steps on a recent card | H3 with the ControlNet: 20–45 minutes per 124-frame section at 768 × 576; the adapter trains in about 90 seconds on an RTX 5090 | |

Software: ComfyUI (current release; every graph here uses built-in nodes only), Python 3.10 or newer with OpenCV, NumPy, Pillow and PyTorch for the Python steps, and ffmpeg. The exact model files, with links and hashes on Hugging Face, are listed on each kit page.

## Models and licences

| Model | Publisher | Licence on the model card |
|---|---|---|
| [Qwen Image Edit 2509 and 2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) | Qwen team, Alibaba | Apache-2.0 |
| [Qwen Image Edit Lightning LoRAs](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning) | LightX2V | Apache-2.0 |
| [TeleStyle V2](https://huggingface.co/Tele-AI/TeleStyleV2) | TeleAI | Apache-2.0 |
| [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) | MiniMax | MiniMax H3 Community License Agreement. The card has an application form for the USA, the EU, the UK and South Korea, so it's worth checking the terms where you are. |
| [Fun ControlNet for H3](https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union) | Alibaba PAI | See the model card |

## A note on "approved"

Approved means the whole shot was reviewed at full size and accepted as a research result. Colour that survived in the scan is evidence. Colour the model filled in is an interpretation the film can't confirm.

The examples on these pages are research tests: faded trailers from a 35mm trailer reel scan posted publicly on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps), and copies of other films used in the research. The films belong to their rights holders.
