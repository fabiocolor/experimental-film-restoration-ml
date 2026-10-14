---
layout: default
title: "Temporal CbCr"
nav_order: 2
has_children: true
permalink: /temporal-cbcr/
---

# Temporal CbCr

Colour recovery or colourization when you have a direct reference for the shot. The scan keeps its brightness, detail and motion; only the colour (Cb and Cr) is learned from the reference and carried through the shot.

## Two kinds of reference

- **Historical.** A better copy of the same frames survives: a DVD, a telecine, another print. When it lines up with the scan, it teaches the colour, and the result can be called a recovery.
- **Synthetic.** No better copy survives, so an open model (MiniMax H3, Qwen Image Edit, TeleStyle) makes candidate colour frames for the shot, and a person approves the good ones. The result is an interpretation, and I say so.

## How it works

1. **Align the reference** to the scan in time and position, and check the alignment by eye.
2. **Pick teachers.** Matching frame pairs from the historical reference, or the approved synthetic frames.
3. **Train a small model for the shot.** The Temporal CbCr adapter learns only the colour difference, so it trains in minutes. In Nuke, CopyCat does the same job with a historical reference.
4. **Run it over the whole shot.** The colour stays consistent from frame to frame, and the scan's own brightness is kept.

## Examples

**Candy Candy: a historical reference (CopyCat).** A faded 16mm print of the opening, with colour learned from a matched French PAL DVD. The detail comes from the 16mm scan and the colour from the DVD. The limit is the reference itself: a standard-definition DVD with its own grading.

<figure class="figure">
  <a href="https://drive.google.com/file/d/11UucDpEAC5QRlfF3BN12f3mggg-S58Ds/view"><img src="{{ '/images_kebab/candy-candy/candy-candy-comparison-still.jpg' | relative_url }}" alt="Candy Candy: the original scan, the balanced scan, the DVD reference and the colour-recovered result, side by side" loading="lazy"></a>
  <figcaption>Candy Candy: the original scan, the balanced scan, the DVD reference and the recovered result. A still from the video on Google Drive.</figcaption>
</figure>

**Unman, Wittering and Zigo (1971): a synthetic reference.** A choir scene from a faded trailer. About a hundred frames passed review and became teachers, training took about a minute and a half, and the stained glass stays consistent through the pan.

<figure class="figure">
  <a href="https://drive.google.com/file/d/1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD/view"><img src="https://drive.google.com/thumbnail?id=1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD&amp;sz=w960" alt="Unman, Wittering and Zigo: the faded choir shot and the adapter result, side by side" loading="lazy" referrerpolicy="no-referrer"></a>
  <figcaption><em>Unman, Wittering and Zigo</em>: the faded choir shot and the adapter result, side by side (video on Google Drive).</figcaption>
</figure>

## What still doesn't work

- A reference brings its own limits: a standard-definition DVD brings its own grading and softness.
- Alignment is still semi-manual; cuts and changing speeds need checking by hand.
- A synthetic reference is only as good as the frames a person approves.

## Downloads

- [Candy Candy: comparison video, 1 min 10 s (102 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=11UucDpEAC5QRlfF3BN12f3mggg-S58Ds&export=download&confirm=t)
- [Candy Candy: the recovered scan at 4400 × 3300, 1 min 10 s (298 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=1EgkquRW2zm2lQzR_uWOQCSvpl0agE7G1&export=download&confirm=t)
- [Unman, Wittering and Zigo: Temporal CbCr adapter, 7 s (20.4 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD&export=download&confirm=t)

## In this section

- [CopyCat workflow]({{ '/copycat-workflow/' | relative_url }}): the Nuke template for a historical reference, step by step.
- [Case studies]({{ '/case-studies/' | relative_url }}) from the CopyCat work.
