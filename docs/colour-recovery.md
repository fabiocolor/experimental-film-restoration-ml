---
layout: default
title: Colour Recovery
nav_order: 1
has_children: true
permalink: /colour-recovery/
---

<p class="eyebrow">Section 1</p>

# Colour recovery

This is about rescuing the original colour of faded film. It isn't black-and-white colorization. Whatever colour still survives in the picture is evidence, so I respect it first and build on top of it. References and generated colour only fill what was lost; they never override what survived. The film also keeps its own picture: every final frame is the scan's own brightness (luma) with recovered colour on top, so the grain, the detail and even the dirt stay.

## Balance first, then recover

In a proper restoration the scan usually arrives balanced: black is black, white is white, and the colour is collapsed, often towards cyan. So the normal first step is to balance the scan, for example with the [Faded Balancer DCTL](https://github.com/fabiocolor/Faded-Balancer-DCTL) in DaVinci Resolve, and then recover.

Balancing only sets levels, so a balanced and an unbalanced scan hold the same dye information. Working from the unbalanced scan is just a convenience for footage loaded as found.

| Before (faded scan) | After (Faded Balancer DCTL) |
| --- | --- |
| ![Faded scan with a strong red cast]({{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-before.png' | relative_url }}) | ![The same frame after balancing]({{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-after.png' | relative_url }}) |

*A faded trailer from a 35mm trailer reel scan posted on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps), before and after balancing in Resolve.*

## With a reference: CopyCat in Nuke

When a better copy survives (a telecine, a DVD, another print, the negative where the two overlap), I train a small model for that film on matching frames of the two copies. It learns how to get from the faded scan to the colour of the better copy. The [Nuke template]({{ '/copycat-workflow/' | relative_url }}) runs locally in Nuke Non-Commercial or Nuke Indie, with your own footage, to build a small dataset for each shot.

## Without a reference: open-weight models

When there's no better copy, I make what I call a synthetic reference: an approved colour frame for each shot, made with Qwen Image Edit in ComfyUI.

- **Pre-balanced scans.** This is the route I use now for balanced footage. One palette still comes from the scan's luma, with the faded frame as a hint of which hue each object had. MiniMax H3 with Alibaba's Fun ControlNet for H3 and my Temporal CbCr adapter carry it through the shot. Then the red-green colour that survived in the scan is respected: the recovery may strengthen it, but never flip or weaken it. The yellow-blue choices are still an interpretation, because yellow is mostly the dye that's lost. I've tested it on four shots from one source so far, at reduced resolution.
- **Single frames.** Qwen Image Edit 2511, guided by an edge map of the frame and a softly blurred colour chart, gives useful colour on all kinds of faded material, with someone reviewing every frame. You can [download the workflow]({{ '/qwen-color-recovery-app/' | relative_url }}) and try it on your own frames.
- **Whole shots.** The frames only agree with each other when the whole shot is guided by an approved reference. The Temporal CbCr adapter is a small model I built for that: you keep the frames from H3 or TeleStyle (a LoRA for Qwen Image Edit) that pass review, I call them teachers, and the adapter learns the colour of that one shot from them and fills in the rest. On the choir scene from *Unman, Wittering and Zigo*, about a hundred frames became teachers and training took about a minute and a half.

## What still doesn't work

- **Frame by frame.** Each frame on its own is a fair interpretation, but together they flicker.
- **Semantic contamination.** If you use a leader lady as the reference, she ends up in the shot. A plain colour chart, softly blurred, avoids that.
- **Resolution and length.** The video models see a reduced picture, around 768 × 432, about ten seconds at a time.
- **New shots.** I'd like at least three out of four new shots to work on the first pass. I'm not there yet.

## In this section

- [Open-weight colour recovery]({{ '/open-weight-color-recovery/' | relative_url }}), with the [single-frame workflow and downloads]({{ '/qwen-color-recovery-app/' | relative_url }}) and the [research routes and evidence]({{ '/open-weight-color-recovery/research-routes/' | relative_url }}).
- [Reference-trained recovery with CopyCat]({{ '/copycat-workflow/' | relative_url }}), step by step.
- [Case studies]({{ '/case-studies/' | relative_url }}) from the CopyCat work.
- [Where the research stands]({{ '/research-status/' | relative_url }}), for the full picture as of October 2026.
