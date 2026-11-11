---
layout: default
title: Where Things Stand
nav_order: 7
permalink: /research-status/
---


# Where things stand

Updated 11 November 2026. These are scoped research results and open questions. A demonstrated shot does not establish a reliable default for new footage, an integrated app workflow or a finished restoration.

## 1. Faded colour recovery

Whole shots with hard motion, at the scan's full resolution: a crowd with a fast pan (385 frames), a ballroom with a moving camera (254 frames at 2048 × 1556), a quarry in six sections (681 frames), a waterfront with fast hands, all from the same faded copy of *Counter Attack*, and the balanced-source route end to end on a commercial. One colour frame checked at full size, MiniMax H3 with the Fun ControlNet (a merged-Canny control) to carry it through the shot, the frames that pass review teaching the Temporal CbCr adapter, and the adapter colouring every frame. Only the colour is taken; brightness, grain and damage stay the scan's.

**Geometry control.** Hard Canny is the default: an aligned binary hard-Canny edge map given to Qwen Image Edit as one of its input images. It is soft conditioning, not a ControlNet, and it holds the geometry without adding meaning of its own to the colour. A real ControlNet model (the H3 Fun ControlNet used in the whole-shot examples) and the final step that lays the colour onto the scan's brightness are separate things. Whether the H3 step's merged-Canny control counts as hard Canny is still open.

The generic balanced-source route still falls short of its preregistered three-in-four target: an interim reading of the 34-shot test in late October had 25 shots workable, and the owner's rating is still outstanding. Later development trials improved the results, but operational retries and choosing a different second pass for each shot must not be counted as a uniformly successful first pass. Owner ratings and normal-speed review remain separate from frame-sheet assessments. A clean palette still can become wrong object colour in the video; returning the balanced input unchanged is not colour recovery. Dark footage and short-shot teacher admission remain important limits. The video models see a reduced picture, about 768 × 576 and ten seconds at a time; inference and full-resolution finishing need separate checks. Colour is an interpretation unless surviving evidence confirms it.

You can run the [single-frame kit]({{ '/downloads/colour-recovery-single-frame/' | relative_url }}) (one faded frame to one colour frame, in Comfy Cloud or locally, no Python) and the palette still from the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}) without a GPU. The rest of the balanced kit does a whole shot end to end on a local card. See [faded colour recovery]({{ '/colour-recovery/' | relative_url }}).

## 2. Temporal CbCr

With a historical reference (a DVD, a telecine, another print) a small model learns the colour from the matching frames: *Candy Candy* from a PAL DVD, *Frontier Experience* from a telecine. With a synthetic reference, about a hundred reviewed frames teach the adapter, which trains in 90 seconds and colours the rest of the shot: *Unman, Wittering and Zigo*. The adapter is the finishing step of the whole-shot colour results above, and it has been run over a 25-minute film; a shot-by-shot review of that run is not recorded yet.

Automatic alignment now has recorded tests for leaders, reframing, cadence changes and incomplete reference windows; finding the matching material in a whole reference film is still incomplete. Alignment alone does not qualify a teacher. Reference balance, missing picture coverage and full-frame training statistics can all affect the learned colour. Metrics against a changed teacher are not directly comparable, and full-size playback remains necessary.

The Nuke template for CopyCat is on the [releases page](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest), with the [CopyCat workflow]({{ '/copycat-workflow/' | relative_url }}) guide; the adapter code is in the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}). See [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}).

## 3. Diffusion healing

Nitrate decay healed on a whole shot of *Knights of the Trail*: in the 18 damaged frames the actor stays the film's and only the ruined background is generated, the other 206 frames are untouched, and every generated pixel is on record. A fifteen-frame hole in a camera negative (*Poison Pen*, 1939), with the sound running on, was filled with the actors' movement tracked across the gap; those tests were closed on 28 September at test scope and are not shown here. Healing tests on a public-domain nitrate title were paused on 25 October, when testing moved into the research application.

The healed shot is at working size (640 × 512); the pass at the scan's full resolution is a separate step. And none of it is one click.

See [diffusion healing]({{ '/diffusion-healing/' | relative_url }}).

## 4. Diffusion Full Reconstruction

Shots from a reel of *El Tinterillo*, a film that survives only as a heavily damaged 16mm print and a soft telecine, rebuilt one by one to one look. Five shots have the owner's decision at the model's 768 × 432 working size: the stairs (624 frames) and two others approved, and two more approved with notes. Lip movement is still to do. The result is labelled as a reconstruction, with detail the film no longer holds. The Wong flute players, a 16mm reversal shot with the emulsion breaking up across the whole frame, was regenerated from one storyboard sheet with the film's own drumming kept; it is parked at working size (768 × 560), to be finished with conventional restoration, and the fastest, thinnest movement, a drumstick, is still better kept from the film than generated.

Small faces and lip performance remain unresolved at the tested 768 × 432 size. A codec diagnostic retained mouth motion, so the evidence does not establish resolution as the sole cause; executable conditioning still needs investigation. Video upscalers, Wan VACE driven by the source and a CopyCat detail model were all tried on this material and dropped.

You can run the [stairs kit]({{ '/downloads/upscaling-stairs/' | relative_url }}) and the Wong shot's [second-pass kit]({{ '/downloads/gap-filling-second-pass/' | relative_url }}). See [diffusion full reconstruction]({{ '/diffusion-full-reconstruction/' | relative_url }}).

## 5. Black-and-white colourization

Fifteen stock-route research shots have recorded results; the four 1920s fiction shots among them were made at half the scan's size, and their full-resolution pass is still to do. The colour frames were carried by H3 with the Fun ControlNet's merged-Canny control; the route has not yet been run with the hard-Canny default. Exact-source-brightness colourization and stock-response reconstruction are different output contracts: the latter may change brightness to match the stock response. Examples include *The General* (a garden scene and a pan on a locomotive) and six other public-domain films of the 1920s.

Known-colour tests distinguish a useful stock constraint from correct object colour. A monochrome value does not uniquely determine hue. Period guidance and a tested period-colour adapter changed the palette without resolving that ambiguity. More accurate historical colour requires independent colour evidence; disclose surviving colour, stock-informed constraints and interpretation separately. Earlier skin, foliage and low-detail limitations retain their scope. The route is not published yet.

See [black-and-white colourization]({{ '/black-and-white-colourization/' | relative_url }}).

## 6. Diffusion Upscaling

**Research idea.** Reference-based video upscaling and basic resolution/detail enhancement, separate from whole-shot regeneration and selective healing. No workflow, benchmark or result is qualified for the new project. A first audit of candidate tape-derived sources on 28 October found neither clean enough to go on with; no upscaling has been run. Historical Tinterillo upscaling records remain Full Reconstruction evidence. See [Diffusion Upscaling]({{ '/diffusion-upscaling/' | relative_url }}).

## 7. Diffusion Inpainting

Selective scratch repair is a separate experimental line: declare a repair mask, use surviving spatial and temporal evidence, retain the raw diffusion result, and protect all channels outside the mask. A first round was approved with notes on 14 October; later rounds had changes requested, and the current candidate, a recovery-first preparation followed by a light diffusion pass, awaits review. The masks are working decisions, not approved results, and none of this establishes full-resolution, full-length acceptance. Temporal boundaries, fine scratches and authentic photographed lines require inspection.

## App integration

The independent Restoration Research Lab is an experimental application under development. Since late October 2026, colour-recovery and healing tests run inside it. Research knowledge, connected inference procedures, verified result custody and user acceptance are separate states. These pages are research upstream; they do not distribute app releases or its signed knowledge feed.

## What can be reproduced

Every example on the site has a [record]({{ '/records/' | relative_url }}) of its source, route, models and settings, and the [download kits]({{ '/downloads/' | relative_url }}) reproduce four of them from the published files and say how closely (ΔE against the published result). Every graph is published laid out with notes that say what the step does and what should and should not happen on the footage, and as the API-format prompt the server runs. The graphs use built-in ComfyUI nodes only. The model file names, prompt, seed, steps, cfg and sampler are in the graph itself, and ComfyUI writes the whole graph into every PNG it saves, so a run is repeatable on another machine to within the models' own run-to-run variation, which is small at a fixed seed but not zero.

## Comfy Cloud

Not everyone has a GPU, so the two still-frame graphs (the single-frame kit and the balanced kit's palette still) are built to open and run in Comfy Cloud as they are, with the bf16 Qwen Image Edit model from Cloud's own library. A recorded test run of the current graphs on Comfy Cloud is planned; until then this is what the graphs are built for, not a tested result. The published recipe uses the fp8mixed model, which has to be imported from Hugging Face (Creator plan or higher), and the bf16 model gives a visibly different colour on some surfaces (ΔE 2.67 on the palette still). The video steps (MiniMax H3, Wan VACE) and the Python steps run locally.

## Next

The original-resolution pass for the healed shots. The owner's rating of the balanced-source test. Lips on the *El Tinterillo* shots. A hard-Canny run of the video routes, or a decision on whether merged-Canny qualifies. One app that runs the current colour route on new shots, which is possible now but still needs too many decisions to be left alone. And the healing and reconstruction routes as self-contained graphs, beyond the second-pass and window kits that are published.

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

Everything on this site was reviewed at full size before it was published; a result's approval and its publication are separate decisions. Colour that survived in the scan is evidence. Colour the model filled in is an interpretation the film can't confirm. Generated picture is an inference, and the records say where it is.

The examples on these pages are research tests: faded trailers from a 35mm trailer reel scan posted publicly on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps), public-domain films, copies of other films used in the research, and material shown by courtesy of the George Eastman Museum. The films belong to their rights holders.
