---
layout: default
title: "Faded Colour Recovery"
nav_order: 1
has_children: true
permalink: /colour-recovery/
---


# Faded colour recovery

This is about rescuing the original colour of faded film. It isn't black-and-white colorization. Whatever colour still survives in the picture is evidence, so I respect it first and build on top of it. References and generated colour only fill what was lost; they never override what survived. The film also keeps its own picture: every final frame is the scan's own brightness (luma) with recovered colour on top, so the grain, the detail and even the dirt stay.

## Balance first, then recover

In a proper restoration the scan usually arrives balanced: black is black, white is white, and the colour is collapsed, often towards cyan. So the normal first step is to balance the scan, for example with the [Faded Balancer]({{ '/tools/faded-balancer/' | relative_url }}) in DaVinci Resolve, and then recover.

Balancing only sets levels, so a balanced and an unbalanced scan hold the same dye information. Working from the unbalanced scan is just a convenience for footage loaded as found.



## With a reference

When a better copy survives (a telecine, a DVD, another print), the colour can be learned from it directly. That is its own research area: [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}).

## Balanced and unbalanced sources

When there's no better copy, I make what I call a synthetic reference: an approved colour frame for each shot, made with Qwen Image Edit in ComfyUI.

- **Balanced sources.** This is the route I use now for balanced footage. One palette still comes from the scan's luma, with the faded frame as a hint of which hue each object had. MiniMax H3 with Alibaba's Fun ControlNet for H3 and my Temporal CbCr adapter carry it through the shot. Then the red-green colour that survived in the scan is respected: the recovery may strengthen it, but never flip or weaken it. The yellow-blue choices are still an interpretation, because yellow is mostly the dye that's lost. I've tested it on four shots from one source so far, at reduced resolution. The [kit for this route]({{ '/qwen-color-recovery-app/' | relative_url }}) is available to download.
- **Unbalanced sources, single frames.** Qwen Image Edit 2511, guided by an edge map of the frame and a softly blurred colour chart, gives useful colour on all kinds of faded material, with someone reviewing every frame. The earlier single-frame workflow is no longer offered for download.
- **Unbalanced sources, whole shots.** The frames only agree with each other when the whole shot is guided by an approved reference. The Temporal CbCr adapter is a small model I built for that: you keep the frames from H3 or TeleStyle (a LoRA for Qwen Image Edit) that pass review, I call them teachers, and the adapter learns the colour of that one shot from them and fills in the rest. On the choir scene from *Unman, Wittering and Zigo*, about a hundred frames became teachers and training took about a minute and a half.

## Examples

**Counter Attack (1976): the whole shot.** No reference survives for this Chinese film. With MiniMax H3 and the Fun ControlNet giving teacher frames, the Temporal CbCr adapter carried the colour through a 385-frame crowd shot with a fast pan, and I approved it on 30 September. Some tint remains in the shadows, because my copy had a broken cadence. The clip I showed at FIAT/IFTA is in the [talk archive]({{ '/fiat-ifta-2026-companion/' | relative_url }}).

**A 1970s commercials compilation: pre-balanced footage.** The route for balanced scans, where the red-green colour that survived is kept and the lost colour is filled in. I approved four shots from this compilation; here's one, a Folgers coffee commercial.

<figure class="figure">
  <img src="{{ '/images_kebab/colour-recovery/commercials-folgers-before-after-f067.jpg' | relative_url }}" alt="A Folgers coffee commercial: the balanced, faded scan on the left and the recovered colour on the right" loading="lazy">
  <figcaption>The balanced scan on the left, the approved result on the right. The shot and the result are in the <a href="https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/tree/main/docs/downloads/faded-colour-recovery-t185">kit</a>.</figcaption>
</figure>

## What still doesn't work

- **Frame by frame.** Each frame on its own is a fair interpretation, but together they flicker.
- **Semantic contamination.** If you use a leader lady as the reference, she ends up in the shot. A plain colour chart, softly blurred, avoids that.
- **Resolution and length.** The video models see a reduced picture, around 768 × 432, about ten seconds at a time.
- **New shots.** I'd like at least three out of four new shots to work on the first pass. I'm not there yet.

## Downloads

- [Faded colour recovery kit for pre-balanced scans: ComfyUI graphs, Python steps and a README](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/tree/main/docs/downloads/faded-colour-recovery-t185)
- Earlier examples from my talks are kept as a dated archive on the [SEAPAVAA 2026]({{ '/seapavaa-2026-companion/' | relative_url }}) and [FIAT/IFTA 2026]({{ '/fiat-ifta-2026-companion/' | relative_url }}) pages.

## In this section

- [Balanced sources: download kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}), checked against the approved result.
- [Unbalanced sources: open-weight routes]({{ '/open-weight-color-recovery/' | relative_url }}) and the [research routes and evidence]({{ '/open-weight-color-recovery/research-routes/' | relative_url }}).
- [Where the research stands]({{ '/research-status/' | relative_url }}).
