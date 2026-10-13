---
layout: default
title: Colour Recovery
nav_order: 1
has_children: true
permalink: /colour-recovery/
---


# Colour recovery

This is about rescuing the original colour of faded film. It isn't black-and-white colorization. Whatever colour still survives in the picture is evidence, so I respect it first and build on top of it. References and generated colour only fill what was lost; they never override what survived. The film also keeps its own picture: every final frame is the scan's own brightness (luma) with recovered colour on top, so the grain, the detail and even the dirt stay.

## Balance first, then recover

In a proper restoration the scan usually arrives balanced: black is black, white is white, and the colour is collapsed, often towards cyan. So the normal first step is to balance the scan, for example with the [Faded Balancer DCTL](https://github.com/fabiocolor/Faded-Balancer-DCTL) in DaVinci Resolve, and then recover.

Balancing only sets levels, so a balanced and an unbalanced scan hold the same dye information. Working from the unbalanced scan is just a convenience for footage loaded as found.

<div class="media-grid media-grid-2">
  <figure class="figure">
    <img src="{{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-after.png' | relative_url }}" alt="Faded scan with a strong red cast">
    <figcaption>Before (faded scan)</figcaption>
  </figure>
  <figure class="figure">
    <img src="{{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-before.png' | relative_url }}" alt="The same frame after balancing">
    <figcaption>After (Faded Balancer DCTL)</figcaption>
  </figure>
</div>

<p class="experiment-credit">A faded trailer from a 35mm trailer reel scan posted on <a href="https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps">archive.org</a>, before and after balancing in Resolve.</p>

## With a reference: CopyCat in Nuke

When a better copy survives (a telecine, a DVD, another print, the negative where the two overlap), I train a small model for that film on matching frames of the two copies. It learns how to get from the faded scan to the colour of the better copy. The [Nuke template]({{ '/copycat-workflow/' | relative_url }}) runs locally in Nuke Non-Commercial or Nuke Indie, with your own footage, to build a small dataset for each shot.

## Without a reference: open-weight models

When there's no better copy, I make what I call a synthetic reference: an approved colour frame for each shot, made with Qwen Image Edit in ComfyUI.

- **Pre-balanced scans.** This is the route I use now for balanced footage. One palette still comes from the scan's luma, with the faded frame as a hint of which hue each object had. MiniMax H3 with Alibaba's Fun ControlNet for H3 and my Temporal CbCr adapter carry it through the shot. Then the red-green colour that survived in the scan is respected: the recovery may strengthen it, but never flip or weaken it. The yellow-blue choices are still an interpretation, because yellow is mostly the dye that's lost. I've tested it on four shots from one source so far, at reduced resolution. The [kit for this route]({{ '/qwen-color-recovery-app/' | relative_url }}) is available to download.
- **Single frames.** Qwen Image Edit 2511, guided by an edge map of the frame and a softly blurred colour chart, gives useful colour on all kinds of faded material, with someone reviewing every frame. The earlier single-frame workflow is no longer offered for download.
- **Whole shots.** The frames only agree with each other when the whole shot is guided by an approved reference. The Temporal CbCr adapter is a small model I built for that: you keep the frames from H3 or TeleStyle (a LoRA for Qwen Image Edit) that pass review, I call them teachers, and the adapter learns the colour of that one shot from them and fills in the rest. On the choir scene from *Unman, Wittering and Zigo*, about a hundred frames became teachers and training took about a minute and a half.

## Examples

**Candy Candy: colour from a DVD reference (CopyCat).** A faded 16mm print of the opening, with colour learned from a matched French PAL DVD. The detail comes from the 16mm scan and the colour from the DVD. The limit is the reference itself: a standard-definition DVD with its own grading.

<figure class="figure">
  <a href="https://drive.google.com/file/d/11UucDpEAC5QRlfF3BN12f3mggg-S58Ds/view"><img src="{{ '/images_kebab/candy-candy/candy-candy-comparison-still.jpg' | relative_url }}" alt="Candy Candy: the original scan, the balanced scan, the DVD reference and the colour-recovered result, side by side" loading="lazy"></a>
  <figcaption>Candy Candy: the original scan, the balanced scan, the DVD reference and the recovered result. A still from the video on Google Drive.</figcaption>
</figure>

**Counter Attack (1976): the whole shot.** No reference survives for this Chinese film. With MiniMax H3 and the Fun ControlNet giving teacher frames, the Temporal CbCr adapter carried the colour through a 385-frame crowd shot with a fast pan, and I approved it on 30 September. Some tint remains in the shadows, because my copy had a broken cadence. The clip I showed at FIAT/IFTA is in the [talk archive]({{ '/fiat-ifta-2026-companion/' | relative_url }}).

**Unman, Wittering and Zigo (1971): the Temporal CbCr adapter.** A choir scene from a faded trailer. About a hundred frames passed review and became teachers, training took about a minute and a half, and the stained glass stays consistent through the pan.

<figure class="figure">
  <a href="https://drive.google.com/file/d/1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD/view"><img src="https://drive.google.com/thumbnail?id=1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD&amp;sz=w960" alt="Unman, Wittering and Zigo: the faded choir shot and the adapter result, side by side" loading="lazy" referrerpolicy="no-referrer"></a>
  <figcaption><em>Unman, Wittering and Zigo</em>: the faded choir shot and the adapter result, side by side (video on Google Drive).</figcaption>
</figure>

**La Muralla Verde: CopyCat with a DVD and DCP reference.** One of the longer CopyCat projects; it's in the [case studies]({{ '/case-studies/' | relative_url }}).

**A 1970s commercials compilation: pre-balanced footage.** The four shots I tested the neutral-source route on, where the surviving red-green colour is kept and the lost colour is filled in. I don't have shareable files of these yet.

## What still doesn't work

- **Frame by frame.** Each frame on its own is a fair interpretation, but together they flicker.
- **Semantic contamination.** If you use a leader lady as the reference, she ends up in the shot. A plain colour chart, softly blurred, avoids that.
- **Resolution and length.** The video models see a reduced picture, around 768 × 432, about ten seconds at a time.
- **New shots.** I'd like at least three out of four new shots to work on the first pass. I'm not there yet.

## Downloads

- [Candy Candy: comparison video, 1 min 10 s (102 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=11UucDpEAC5QRlfF3BN12f3mggg-S58Ds&export=download&confirm=t)
- [Candy Candy: the recovered scan at 4400 × 3300, 1 min 10 s (298 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=1EgkquRW2zm2lQzR_uWOQCSvpl0agE7G1&export=download&confirm=t)
- [Unman, Wittering and Zigo: Temporal CbCr adapter, 7 s (20.4 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD&export=download&confirm=t)
- [Faded colour recovery kit for pre-balanced scans: ComfyUI graphs, Python steps and a README](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/tree/main/docs/downloads/faded-colour-recovery-t185)
- [Faded Balancer before (PNG)]({{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-after.png' | relative_url }}) · [after (PNG)]({{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-before.png' | relative_url }})
- Earlier examples from my talks are kept as a dated archive on the [SEAPAVAA 2026]({{ '/seapavaa-2026-companion/' | relative_url }}) and [FIAT/IFTA 2026]({{ '/fiat-ifta-2026-companion/' | relative_url }}) pages.

## In this section

- [Open-weight colour recovery]({{ '/open-weight-color-recovery/' | relative_url }}) and the [research routes and evidence]({{ '/open-weight-color-recovery/research-routes/' | relative_url }}).
- [Reference-trained recovery with CopyCat]({{ '/copycat-workflow/' | relative_url }}), step by step.
- [Case studies]({{ '/case-studies/' | relative_url }}) from the CopyCat work.
- [Where the research stands]({{ '/research-status/' | relative_url }}), for the full picture as of October 2026.
