---
layout: default
title: Where Things Stand
nav_order: 7
permalink: /research-status/
---


# Where things stand

October 2026, after SEAPAVAA in June and FIAT/IFTA in São Paulo. The short version: if you keep the film's own picture and use a model only for what is missing, every kind of loss tried this year has come back on at least one whole shot, and most on several. What it takes is time, passes and someone reviewing, not a breakthrough that hasn't happened yet. Area by area, what works, what doesn't, and what you can run yourself.

## 1. Faded colour recovery

Whole shots with hard motion, at the scan's full resolution: a crowd with a fast pan (385 frames), a ballroom with a moving camera (254 frames at 2048 × 1556), a quarry in six sections (681 frames), a waterfront with fast hands, all from the same faded copy of *Counter Attack*, and the balanced-source route end to end on a commercial. One colour frame checked at full size, MiniMax H3 with the Fun ControlNet to carry it through the shot, the frames that pass review teaching the Temporal CbCr adapter, and the adapter colouring every frame. Only the colour is taken; brightness, grain and damage stay the scan's.

Some shots still need a second pass. The target is three out of four new shots right first time, and it is close but not there. Deep shadows keep a tint on the hardest shots. The video models see a reduced picture, about 768 × 576 and ten seconds at a time, which is why shots are done in sections and why you waste inference. And the colour is an interpretation unless a surviving reference confirms it.

You can run the [single-frame kit]({{ '/downloads/colour-recovery-single-frame/' | relative_url }}) (one faded frame to one colour frame, in Comfy Cloud or locally, no Python) and the palette still from the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}) without a GPU. The rest of the balanced kit does a whole shot end to end on a local card. See [faded colour recovery]({{ '/colour-recovery/' | relative_url }}).

## 2. Temporal CbCr

With a historical reference (a DVD, a telecine, another print) a small model learns the colour from the matching frames: *Candy Candy* from a PAL DVD, *Frontier Experience* from a telecine. With a synthetic reference, about a hundred reviewed frames teach the adapter, which trains in 90 seconds and colours the rest of the shot: *Unman, Wittering and Zigo*. The adapter is the finishing step of the whole-shot colour results above, and it has done a 25-minute film.

Lining up a historical reference is still partly by hand, and a synthetic reference is only as good as the frames that get through review. New examples are being made and will be added to the page.

The Nuke template for CopyCat is on the [releases page](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest), with the [CopyCat workflow]({{ '/copycat-workflow/' | relative_url }}) guide; the adapter code is in the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}). See [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}).

## 3. Diffusion healing

Nitrate decay healed on a whole shot of *Knights of the Trail*: in the 18 damaged frames the actor stays the film's and only the ruined background is generated, the other 206 frames are untouched, and every generated pixel is on record. A 16mm reversal shot with the emulsion breaking up across the whole frame (the Wong flute players) healed from one storyboard sheet, with the film's own drumming kept. A fifteen-frame hole in a camera negative (*Poison Pen*, 1939), with the sound running on, is being filled with the actors' movement tracked across the gap.

The healed shots are at working size (640 × 512, 768 × 560); the pass at the scan's full resolution is a separate step. The Wong shot stops at a good result at working size, to be finished with conventional restoration. The fastest, thinnest movement, a drumstick, is still better kept from the film than generated. And none of it is one click.

You can run the [second-pass kit]({{ '/downloads/gap-filling-second-pass/' | relative_url }}). See [diffusion healing]({{ '/diffusion-healing/' | relative_url }}).

## 4. Diffusion reconstruction

A whole reel of *El Tinterillo*, a film that survives only as a heavily damaged 16mm print and a soft telecine, rebuilt shot by shot to one look: the stairs (624 frames) and three more shots of 410, 422 and 176 frames with the same method. The last still has its lip movement to do. The result is labelled as a reconstruction, with detail the film no longer holds.

Small faces and lips are the limit, because the model works at 768 × 432; the next pass targets articulation. Video upscalers, Wan VACE driven by the source and a CopyCat detail model were all tried on this material and dropped.

You can run the [stairs kit]({{ '/downloads/upscaling-stairs/' | relative_url }}). See [diffusion reconstruction]({{ '/diffusion-reconstruction/' | relative_url }}).

## 5. Black-and-white colourization

Fifteen shots finished, whole shots at full resolution with the original brightness untouched, the colour fitted to the stock that recorded the film: *The General* (a garden scene and a pan on a locomotive) and six other public-domain films of the 1920s.

Skin on the earliest shots, some foliage, and soft, low-detail sources are the weak points. More complex movement and subjects are the next tests. The palettes are interpretations, and the route is not published yet.

See [black-and-white colourization]({{ '/black-and-white-colourization/' | relative_url }}).

## What can be reproduced

Every example on the site has a [record]({{ '/records/' | relative_url }}) of its source, route, models and settings, and the [download kits]({{ '/downloads/' | relative_url }}) reproduce four of them from the published files and say how closely (ΔE against the published result). Every graph is published laid out with notes that say what the step does and what should and should not happen on the footage, and as the API-format prompt the server runs. The graphs use built-in ComfyUI nodes only. The model file names, prompt, seed, steps, cfg and sampler are in the graph itself, and ComfyUI writes the whole graph into every PNG it saves, so a run is repeatable on another machine to within the models' own run-to-run variation, which is small at a fixed seed but not zero.

## Comfy Cloud

Not everyone has a GPU, so the two still-frame graphs (the single-frame kit and the balanced kit's palette still) open and run in Comfy Cloud as they are, with the bf16 Qwen Image Edit model from Cloud's own library. The published recipe uses the fp8mixed model, which has to be imported from Hugging Face (Creator plan or higher), and the bf16 model gives a visibly different colour on some surfaces (ΔE 2.67 on the palette still). The video steps (MiniMax H3, Wan VACE) and the Python steps run locally.

## Next

The original-resolution pass for the healed shots, starting with *Knights of the Trail*. Lips on the *El Tinterillo* reel. One app that runs the current colour route on new shots, which is possible now but still needs too many decisions to be left alone. And the healing and reconstruction routes as self-contained graphs, beyond the second-pass and window kits that are published.

## Hardware

| | Still frames (Qwen Image Edit 2511) | Shots (MiniMax H3, Wan VACE, the adapter) | CopyCat in Nuke |
| --- | --- | --- | --- |
| GPU | NVIDIA, 8 GB of VRAM or more with the fp8mixed model (ComfyUI keeps the rest in system RAM); 16 GB or more keeps the 20 GB model on the card | NVIDIA, 16 GB of VRAM or more; 24 GB (RTX 3090/4090) or 32 GB (RTX 5090) for the H3 route at 768 × 576 | Foundry lists the requirements for each edition of Nuke |
| System RAM | 32 GB or more | 64 GB recommended | |
| Storage | About 31 GB of models (20.5 GB model, 9.4 GB text encoder, 254 MB VAE, 850 MB LoRA) | A further 40–60 GB for H3, its text encoder, VAEs and the ControlNet; Wan VACE 14B adds 32 GB | |
| Apple Silicon | The bf16 model (41 GB) runs on a Mac with 64 GB of unified memory or more; the fp8 versions do not | Not tested | |
| Time | Under a minute a frame at 4 steps on a recent card | H3 with the ControlNet: 20–45 minutes per 124-frame section at 768 × 576; the adapter trains in about 90 seconds on an RTX 5090 | |

Software: ComfyUI (current release; every graph here uses built-in nodes only), Python 3.10 or newer with OpenCV, NumPy, Pillow and PyTorch for the Python steps, and ffmpeg. The exact model files, with links and hashes on Hugging Face, are listed on each kit page. There is no free compute: a local card costs money up front and electricity after, and cloud inference costs per run and can't be iterated on the way a film needs. This research runs on local cards because iteration is the whole job.

## Models and licences

| Model | Publisher | Licence on the model card |
|---|---|---|
| [Qwen Image Edit 2509 and 2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) | Qwen team, Alibaba | Apache-2.0 |
| [Qwen Image Edit Lightning LoRAs](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning) | LightX2V | Apache-2.0 |
| [TeleStyle V2](https://huggingface.co/Tele-AI/TeleStyleV2) | TeleAI | Apache-2.0 |
| [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) | MiniMax | MiniMax H3 Community License Agreement. The card has an application form for the USA, the EU, the UK and South Korea, so it's worth checking the terms where you are. |
| [Fun ControlNet for H3](https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union) | Alibaba PAI | See the model card |
| [Wan 2.1 VACE 14B](https://github.com/ali-vilab/VACE) | Wan team, Alibaba | Apache-2.0 |

## A note on the results

Everything on this site was reviewed at full size before it was published. Colour that survived in the scan is evidence. Colour the model filled in is an interpretation the film can't confirm. Generated picture is an inference, and the records say where it is.

The examples on these pages are research tests: faded trailers from a 35mm trailer reel scan posted publicly on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps), public-domain films, copies of other films used in the research, and material shown by courtesy of the George Eastman Museum. The films belong to their rights holders.
