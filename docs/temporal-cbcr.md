---
layout: default
title: "Temporal CbCr"
nav_order: 2
has_children: true
permalink: /temporal-cbcr/
redirect_from:
  - /case-studies/
  - /research-evidence/CANDY_CANDY_CHROMA_COPYCAT/
---

# Temporal CbCr

Colour learned from a historical or synthetic reference for the shot. The scan keeps its brightness, detail and motion. Only the colour (the Cb and Cr channels) comes from the reference.

## Two kinds of reference

- **Historical.** A better copy of the same frames survives: a DVD, a telecine, another print. If it lines up with the scan, it teaches the colour, and the result is a recovery.
- **Synthetic.** No better copy survives, so open models (MiniMax H3, Qwen Image Edit, TeleStyle) make candidate colour frames, and only approved frames are used. The result is an interpretation.

## How it works

1. **Align the reference** to the scan in time and position, and check the alignment by eye.
2. **Pick teachers.** Matching frame pairs from the historical reference, or the approved synthetic frames.
3. **Train a small model for the shot.** The Temporal CbCr adapter learns only the colour, so it trains in minutes. With a historical reference, CopyCat in Nuke does the same job; the [CopyCat workflow]({{ '/copycat-workflow/' | relative_url }}) walks through it.
4. **Run it over the whole shot.** The colour holds from frame to frame.

## Examples

**Frontier Experience (1975): a historical reference, Temporal CbCr adapter.** A faded film print, with the colour learned from a telecine of the same film supplied by Ross Lipman. The telecine had cadence problems but stayed aligned closely enough to serve as a colour reference. The adapter was trained on 926 frame pairs at 1464 × 1080. On 16 held-out shots it had lower colour error than CopyCat on 9; its overall colour error was 1.79% higher. Some skies and shadows do not fully resolve ([record]({{ '/records/frontier-experience/' | relative_url }})).

<figure class="figure">
  <img src="{{ '/images_kebab/temporal-cbcr/frontier-experience-scan-reference-result-f020.jpg' | relative_url }}" alt="Frontier Experience: the faded scan, the adapter result and the telecine reference" loading="lazy">
  <figcaption><em>Frontier Experience</em>: the original scan (left), the adapter result (right) and the telecine reference (bottom).</figcaption>
</figure>

**Candy Candy (1976): a historical reference, CopyCat.** The same approach in Nuke, before the adapter existed. A 16mm print of the opening, faded to magenta, with the colour learned from a French PAL DVD in CopyCat. The detail and grain come from the 16mm scan, the colour from the DVD ([record]({{ '/records/candy-candy/' | relative_url }})).

- The standard-definition DVD was usable as a colour reference, because only its colour is used, not its detail.
- Both copies were cropped to the picture area they share, so the model never learned the DVD's borders or burned-in subtitles.
- One model for the whole sequence failed on fast pans and changing light. Separate models for the difficult shots, with four to nine frame pairs each, solved this.
- A DVD brings its own grading and softness, and the result inherits it.

<figure class="figure">
  <a href="https://drive.google.com/file/d/11UucDpEAC5QRlfF3BN12f3mggg-S58Ds/view"><img src="{{ '/images_kebab/candy-candy/candy-candy-comparison-still.jpg' | relative_url }}" alt="Candy Candy: the original scan, the balanced scan, the DVD reference and the colour-recovered result, side by side" loading="lazy"></a>
  <figcaption><em>Candy Candy</em>: the original scan, the balanced scan, the DVD reference and the result. A still from the video on Google Drive.</figcaption>
</figure>

**Unman, Wittering and Zigo (1971): a synthetic reference.** A choir scene from a trailer faded to magenta, 164 frames. TeleStyle made the candidate frames; 101 passed review and became teachers, and the adapter coloured the rest. Training took about a minute and a half. The stained glass stays consistent through the pan ([record]({{ '/records/unman-wittering-zigo-choir/' | relative_url }})).

<figure class="figure">
  <a href="https://drive.google.com/file/d/1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD/view"><img src="{{ '/images_kebab/temporal-cbcr/unman-wittering-zigo-choir-adapter.jpg' | relative_url }}" alt="Unman, Wittering and Zigo: the faded choir shot on the left and the adapter result on the right" loading="lazy"></a>
  <figcaption><em>Unman, Wittering and Zigo</em>: the faded source and the adapter result. A still from the video on Google Drive.</figcaption>
</figure>

## What still doesn't work

- Alignment is still semi-manual; cuts and changing speeds need checking by hand.
- A synthetic reference is only as good as the frames a person approves.
- The adapter code is published in the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}). Each adapter is trained for one shot, so no weights are shared.

## Downloads

- [Candy Candy: comparison video, 1 min 10 s (102 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=11UucDpEAC5QRlfF3BN12f3mggg-S58Ds&export=download&confirm=t)
- [Candy Candy: the recovered scan at 4400 × 3300, 1 min 10 s (298 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=1EgkquRW2zm2lQzR_uWOQCSvpl0agE7G1&export=download&confirm=t)
- [Unman, Wittering and Zigo: Temporal CbCr adapter, 7 s (20.4 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD&export=download&confirm=t)
- [The Nuke template for CopyCat](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest), for Nuke Non-Commercial or Indie.
