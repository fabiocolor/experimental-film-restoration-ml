---
layout: default
title: What Is Possible Now
nav_order: 7
permalink: /research-status/
---


# What is possible now

Status in October 2026, after SEAPAVAA in June and FIAT/IFTA in October. The short version: with the film's own picture kept and a model used only for what is missing, every kind of loss tried this year has been recovered on at least one whole shot, and most on several. What it takes is time, passes and a restorer's review, not a wall. Below, area by area: what is done, what is still open, and what can be reproduced.

## 1. Faded colour recovery

**Done.** Whole shots with hard motion, at the scan's full resolution: a crowd with a fast pan (385 frames), a ballroom with a moving camera (254 frames at 2048 × 1556), a quarry in six sections (681 frames), a waterfront with fast hands (all three from the same faded copy of *Counter Attack*), and the balanced-source route end to end on a commercial. From one approved colour frame, MiniMax H3 with the Fun ControlNet carries the colour through the shot, the frames that pass review teach the Temporal CbCr adapter, and the adapter colours every frame consistently. Only the colour is taken; brightness, grain and damage stay the scan's.

**Open.** Some shots still need a second pass; the target of three out of four new shots right first time is close but not reached. Deep shadows keep a tint on the hardest shots. The video models see a reduced picture (about 768 × 576, ten seconds at a time), which is why shots are done in sections. The colour is an interpretation unless a surviving reference confirms it.

**Try it.** The [single-frame kit]({{ '/downloads/colour-recovery-single-frame/' | relative_url }}) (one faded frame to one colour frame, in Comfy Cloud or locally, no Python) and the balanced palette still from the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}) are the two graphs anyone can run; the rest of the balanced kit does a whole shot, end to end, on a local card. See [faded colour recovery]({{ '/colour-recovery/' | relative_url }}).

## 2. Temporal CbCr

**Done.** With a historical reference (a DVD, a telecine, another print) a small model learns the colour from matching frames: *Candy Candy* from a PAL DVD, *Frontier Experience* from a telecine. With a synthetic reference, about a hundred approved frames teach the adapter, which trains in 90 seconds and colours the rest of the shot: *Unman, Wittering and Zigo*. The adapter is the finishing step of the whole-shot colour results above.

**Open.** Lining up a historical reference is still partly done by hand. A synthetic reference is only as good as the frames a person approves.

**Try it.** The Nuke template for CopyCat, from the [releases page](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest), with the [CopyCat workflow]({{ '/copycat-workflow/' | relative_url }}) guide; the adapter code is in the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}). See [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}).

## 3. Diffusion healing

**Done.** Nitrate decay healed on a whole shot of *Knights of the Trail*: in the 18 damaged frames the actor stays the film's and only the ruined background is generated; the other 206 frames are untouched, and every generated pixel is on record. A 16mm reversal shot with the emulsion breaking up across the whole frame (the Wong flute players) healed from one storyboard sheet, with the film's own drumming kept. A 15-frame hole in a camera negative (*Poison Pen*, 1939), with the sound running on, is being filled with the actors' movement tracked across the gap.

**Open.** The healed shots are approved at working size (640 × 512, 768 × 560); the pass at the scan's full resolution is a separate step. The Wong shot stops at a good result at working size, to be finished together with conventional restoration. The fastest, thinnest movement (a drumstick) is still better kept from the film than generated.

**Try it.** The [second-pass kit]({{ '/downloads/gap-filling-second-pass/' | relative_url }}). See [diffusion healing]({{ '/diffusion-healing/' | relative_url }}).

## 4. Diffusion reconstruction

**Done.** A whole reel of *El Tinterillo*, a film that survives only as a heavily damaged 16mm print and a soft telecine, rebuilt shot by shot to one look: the stairs (624 frames) and three more shots of 410, 422 and 176 frames, the last approved with notes, all with the same method. The result is labelled as a reconstruction, with detail the film no longer holds.

**Open.** Small faces and lip movement, because the models work at 768 × 432; the next pass targets articulation. Video upscalers, Wan VACE driven by the source, and a CopyCat detail model were tried and dropped for this material.

**Try it.** The [stairs kit]({{ '/downloads/upscaling-stairs/' | relative_url }}). See [diffusion reconstruction]({{ '/diffusion-reconstruction/' | relative_url }}).

## 5. Black-and-white colourization

**Done.** Fifteen shots approved, whole shots at full resolution with the original brightness untouched, the colour fitted to the stock that recorded the film: *The General* (a garden scene and a pan on a locomotive) and six other public-domain films of the 1920s.

**Open.** Skin on the earliest shots, some foliage, and soft, low-detail sources, which give the model too little to work from. More complex movement and subjects are the next tests. The palettes are interpretations.

See [black-and-white colourization]({{ '/black-and-white-colourization/' | relative_url }}).

## What can be reproduced

Every example on the site has a [record]({{ '/records/' | relative_url }}) of its source, route, models, settings and approval, and the [download kits]({{ '/downloads/' | relative_url }}) reproduce four of them from the published files and say how closely (ΔE against the approved result). Every graph is published laid out with notes that say what it does and what should and should not happen on the footage, and as the API-format prompt the server runs. The graphs use built-in ComfyUI nodes only, with the model file names, prompt, seed, steps, cfg and sampler in the graph itself, and ComfyUI writes the whole graph into every PNG it saves. That makes a run repeatable on another machine to within the models' own run-to-run variation, which is small at a fixed seed but not zero.

## Comfy Cloud

The two still-frame graphs (the single-frame kit and the balanced kit's palette still) open and run in Comfy Cloud as they are, with the bf16 Qwen Image Edit model from Cloud's own library. The published recipe uses the fp8mixed model, which has to be imported from Hugging Face (Creator plan or higher); the bf16 model gives a visibly different colour on some surfaces (ΔE 2.67 on the palette still). The video steps (MiniMax H3, Wan VACE) and the Python steps run locally.

## Next steps

- The original-resolution pass for the healed shots, and the first full-resolution Knights of the Trail shot.
- Lip articulation on the *El Tinterillo* reel.
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
| [Wan 2.1 VACE 14B](https://github.com/ali-vilab/VACE) | Wan team, Alibaba | Apache-2.0 |

## A note on "approved"

Approved means the whole shot was reviewed at full size and accepted as a research result. Colour that survived in the scan is evidence. Colour the model filled in is an interpretation the film can't confirm. Generated picture is an inference, and the records say where it is.

The examples on these pages are research tests: faded trailers from a 35mm trailer reel scan posted publicly on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps), public-domain films, copies of other films used in the research, and material shown by courtesy of the George Eastman Museum. The films belong to their rights holders.
