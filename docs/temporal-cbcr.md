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

<span class="kicker">Research area 2</span>

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

<figure class="pair">
  <span class="pair-labels pair-labels-3"><span>Faded scan</span><span>Adapter result</span><span>Telecine reference</span></span>
  <div class="pair-media pair-3">
    <img src="{{ '/images_kebab/examples/frontier-experience-f020-source.jpg' | relative_url }}" alt="Frontier Experience, frame 20: the faded print, an ox cart on the prairie, almost no colour left" loading="lazy">
    <img src="{{ '/images_kebab/examples/frontier-experience-f020-result.jpg' | relative_url }}" alt="The same frame coloured by the adapter: the sky, the grass, the oxen" loading="lazy">
    <img src="{{ '/images_kebab/examples/frontier-experience-f020-reference.jpg' | relative_url }}" alt="The telecine reference frame, soft and cropped, with its colour intact" loading="lazy">
  </div>
  <figcaption><em>Frontier Experience</em> (1975), frame 20. The adapter learned the colour from the telecine (right); the scan keeps its grain and frame edges. <a href="{{ '/records/frontier-experience/' | relative_url }}">Record</a></figcaption>
</figure>

**Candy Candy (1976): a historical reference, CopyCat.** The same approach in Nuke, before the adapter existed. A 16mm print of the opening, faded to magenta, with the colour learned from a French PAL DVD in CopyCat. The detail and grain come from the 16mm scan, the colour from the DVD ([record]({{ '/records/candy-candy/' | relative_url }})).

- The standard-definition DVD was usable as a colour reference, because only its colour is used, not its detail.
- Both copies were cropped to the picture area they share, so the model never learned the DVD's borders or burned-in subtitles.
- One model for the whole sequence failed on fast pans and changing light. Separate models for the difficult shots, with four to nine frame pairs each, solved this.
- A DVD brings its own grading and softness, and the result inherits it.

<figure class="pair">
  <span class="pair-labels pair-labels-3"><span>16mm scan</span><span>PAL DVD reference</span><span>CopyCat result</span></span>
  <div class="pair-media pair-3">
    <img src="{{ '/images_kebab/examples/candy-candy-f1200-source.jpg' | relative_url }}" alt="Candy Candy, frame 1200 of the comparison: the 16mm scan, faded to pink, Candy leaning against a wall" loading="lazy">
    <img src="{{ '/images_kebab/examples/candy-candy-f1200-reference.jpg' | relative_url }}" alt="The PAL DVD frame used as the colour reference: soft, cropped, with the original colour" loading="lazy">
    <img src="{{ '/images_kebab/examples/candy-candy-f1200-result.jpg' | relative_url }}" alt="The CopyCat result: the DVD's colour on the 16mm scan's detail" loading="lazy">
  </div>
  <figcaption><em>Candy Candy</em> (1976), opening, frame 1200 of the <a href="https://drive.google.com/file/d/11UucDpEAC5QRlfF3BN12f3mggg-S58Ds/view">comparison video</a>. CopyCat in Nuke, colour from the DVD, detail from the scan. <a href="{{ '/records/candy-candy/' | relative_url }}">Record</a></figcaption>
</figure>

**Unman, Wittering and Zigo (1971): a synthetic reference.** A choir scene from a trailer faded to magenta, 164 frames. TeleStyle made the candidate frames; 101 passed review and became teachers, and the adapter coloured the rest. Training took about a minute and a half. The stained glass stays consistent through the pan ([record]({{ '/records/unman-wittering-zigo-choir/' | relative_url }})).

<figure class="pair">
  <div class="pair-media" data-compare="Faded source|Adapter">
    <img src="{{ '/images_kebab/examples/unman-wittering-zigo-choir-f030-source.jpg' | relative_url }}" alt="Unman, Wittering and Zigo, choir, frame 30: the faded trailer frame, a boy singing in close-up, the choir behind" loading="lazy">
    <img src="{{ '/images_kebab/examples/unman-wittering-zigo-choir-f030-result.jpg' | relative_url }}" alt="The same frame coloured by the adapter: blue cassocks, white ruffs, warm skin, the stained glass" loading="lazy">
  </div>
  <figcaption><em>Unman, Wittering and Zigo</em> (1971), choir, frame 30 of 164. Teachers on 101 frames from TeleStyle; the adapter coloured the rest. The <a href="https://drive.google.com/file/d/1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD/view">7-second comparison</a> is on Google Drive. <a href="{{ '/records/unman-wittering-zigo-choir/' | relative_url }}">Record</a></figcaption>
</figure>

## What still doesn't work

- Alignment is still semi-manual; cuts and changing speeds need checking by hand.
- A synthetic reference is only as good as the frames a person approves.
- The adapter code is published in the [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}). Each adapter is trained for one shot, so no weights are shared.

## Downloads

<ul class="downloads">
  <li><a href="https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest">The Nuke template for CopyCat</a><span class="size">.nkind / .nk</span><span class="what">For Nuke Non-Commercial or Indie, with the <a href="{{ '/copycat-workflow/' | relative_url }}">CopyCat workflow</a> guide.</span></li>
  <li><a href="{{ '/downloads/faded-colour-recovery-t185/' | relative_url }}">Temporal CbCr adapter code</a><span class="size">Python · in the balanced-source kit</span><span class="what">The adapter, its training step and the registration check. Each adapter is trained for one shot, so no weights are shared.</span></li>
  <li><a href="https://drive.usercontent.google.com/download?id=11UucDpEAC5QRlfF3BN12f3mggg-S58Ds&export=download&confirm=t">Candy Candy: comparison video</a><span class="size">MP4 · 1 min 10 s · 102 MB</span><span class="what">Original scan, balanced scan, DVD reference and result, side by side. On Google Drive.</span></li>
  <li><a href="https://drive.usercontent.google.com/download?id=1EgkquRW2zm2lQzR_uWOQCSvpl0agE7G1&export=download&confirm=t">Candy Candy: the recovered scan at 4400 × 3300</a><span class="size">MP4 · 1 min 10 s · 298 MB</span><span class="what">The full-resolution result. On Google Drive.</span></li>
  <li><a href="https://drive.usercontent.google.com/download?id=1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD&export=download&confirm=t">Unman, Wittering and Zigo: adapter comparison</a><span class="size">MP4 · 7 s · 20 MB</span><span class="what">Faded source and adapter result, side by side. On Google Drive.</span></li>
</ul>
