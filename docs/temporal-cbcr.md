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

Colour learned from a reference for the shot and carried through every frame. The scan keeps its brightness, detail, grain and motion; only the colour (the Cb and Cr channels) comes from the reference. A small model is trained for the shot alone, in minutes, and it is what finishes most of the whole-shot results on this site.

<figure class="reveal">
  <video autoplay muted loop playsinline preload="auto" poster="{{ '/images_kebab/examples/unman-wittering-zigo-choir-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/unman-wittering-zigo-choir-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/unman-wittering-zigo-choir-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
  <figcaption><span class="reveal-tag">Reveal</span> <em>Unman, Wittering and Zigo</em> (1971), the choir. A trailer faded to magenta, 164 frames with a pan; 101 frames that passed review taught the adapter, which coloured the rest in a minute and a half. <a href="{{ '/records/unman-wittering-zigo-choir/' | relative_url }}">Record</a></figcaption>
</figure>

## Two kinds of reference

- **Historical.** A better copy of the same frames survives: a DVD, a telecine, another print. If it lines up with the scan, it teaches the colour, and the result is a recovery.
- **Synthetic.** No better copy survives, so open models (MiniMax H3, Qwen Image Edit, TeleStyle) make candidate colour frames, and only the frames that pass a person's review are used. The result is an interpretation.

## How it works

1. **Align the reference** to the scan in time and position, and check the alignment by eye.
2. **Pick the frames to learn from.** Matching frame pairs from the historical reference, or the synthetic frames that passed review.
3. **Train a small model for the shot.** The Temporal CbCr adapter learns only the colour, so it trains in about 90 seconds. With a historical reference, CopyCat in Nuke does the same job; the [CopyCat workflow]({{ '/copycat-workflow/' | relative_url }}) walks through it.
4. **Run it over the whole shot.** The colour holds from frame to frame, with no flicker, at the scan's full resolution.

## Examples

<figure class="pair">
  <span class="pair-labels"><span>Faded source</span><span>Adapter</span></span>
  <div class="pair-media pair-video" data-inspect="unman-wittering-zigo-choir" data-frames="a,b,c">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/unman-wittering-zigo-choir-a-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/unman-wittering-zigo-choir-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/unman-wittering-zigo-choir-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption><em>Unman, Wittering and Zigo</em> (1971), choir, 164 frames: a synthetic reference. TeleStyle made the candidate frames; 101 passed review and taught the adapter, which coloured the rest. The stained glass stays put through the pan. <a href="{{ '/records/unman-wittering-zigo-choir/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>16mm scan</span><span>CopyCat result</span></span>
  <div class="pair-media pair-video" data-inspect="candy-candy" data-frames="a,b,c">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/candy-candy-a-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/candy-candy-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/candy-candy-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption><em>Candy Candy</em> (1976), the opening titles: a historical reference. A 16mm print faded to magenta, scanned at 4400 × 3300, with the colour learned from a French PAL DVD in CopyCat. Detail and grain from the print, colour from the DVD. <a href="{{ '/records/candy-candy/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels pair-labels-3"><span>16mm scan</span><span>PAL DVD reference</span><span>CopyCat result</span></span>
  <div class="pair-media pair-3">
    <img src="{{ '/images_kebab/examples/candy-candy-f1200-source.jpg' | relative_url }}" alt="Candy Candy, frame 1200 of the comparison: the 16mm scan, faded to pink, Candy leaning against a wall" loading="lazy">
    <img src="{{ '/images_kebab/examples/candy-candy-f1200-reference.jpg' | relative_url }}" alt="The PAL DVD frame used as the colour reference: soft, cropped, with the original colour" loading="lazy">
    <img src="{{ '/images_kebab/examples/candy-candy-f1200-result.jpg' | relative_url }}" alt="The CopyCat result: the DVD's colour on the 16mm scan's detail" loading="lazy">
  </div>
  <figcaption><em>Candy Candy</em>, frame 1200 of the <a href="https://drive.google.com/file/d/11UucDpEAC5QRlfF3BN12f3mggg-S58Ds/view">comparison video</a>. A standard-definition DVD is enough, because only its colour is used. Both copies were cropped to the picture they share, so the model never learned the DVD's borders or subtitles. <a href="{{ '/records/candy-candy/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels pair-labels-3"><span>Faded scan</span><span>Adapter result</span><span>Telecine reference</span></span>
  <div class="pair-media pair-3">
    <img src="{{ '/images_kebab/examples/frontier-experience-f020-source.jpg' | relative_url }}" alt="Frontier Experience, frame 20: the faded print, an ox cart on the prairie, almost no colour left" loading="lazy">
    <img src="{{ '/images_kebab/examples/frontier-experience-f020-result.jpg' | relative_url }}" alt="The same frame coloured by the adapter: the sky, the grass, the oxen" loading="lazy">
    <img src="{{ '/images_kebab/examples/frontier-experience-f020-reference.jpg' | relative_url }}" alt="The telecine reference frame, soft and cropped, with its colour intact" loading="lazy">
  </div>
  <figcaption><em>Frontier Experience</em> (1975), frame 20: a historical reference, the adapter. A faded print, with the colour learned from a telecine of the same film supplied by Ross Lipman. Trained on 926 frame pairs at 1464 × 1080; on 16 test shots it beat CopyCat on nine. <a href="{{ '/records/frontier-experience/' | relative_url }}">Record</a></figcaption>
</figure>

## Where it stands

- **The finishing step for whole shots.** The adapter is what turns a set of reviewed frames into a consistent shot: the crowd, the ballroom and the balanced-source results on the [colour recovery]({{ '/colour-recovery/' | relative_url }}) page all end with it.
- **Any reference will do.** A DVD, a telecine, another print, or a hundred reviewed synthetic frames; standard definition is enough, because only the colour is learned.
- **Open.** Lining up the reference is still partly done by hand, and cuts and changing speeds are checked by eye. A synthetic reference is only as good as the frames a person lets through. A DVD brings its own grading and softness of colour, and the result inherits it.

## Downloads

<ul class="downloads">
  <li><a href="https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest">The Nuke template for CopyCat</a><span class="size">.nkind / .nk</span><span class="what">For Nuke Non-Commercial or Indie, with the <a href="{{ '/copycat-workflow/' | relative_url }}">CopyCat workflow</a> guide.</span></li>
  <li><a href="{{ '/downloads/faded-colour-recovery-t185/' | relative_url }}">Temporal CbCr adapter code</a><span class="size">Python · in the balanced-source kit</span><span class="what">The adapter, its training step and the registration check. Each adapter is trained for one shot, so no weights are shared. Also on GitHub: <a href="https://github.com/fabiocolor/temporal-cbcr-adapter">temporal-cbcr-adapter</a>.</span></li>
  <li><a href="https://drive.usercontent.google.com/download?id=11UucDpEAC5QRlfF3BN12f3mggg-S58Ds&export=download&confirm=t">Candy Candy: comparison video</a><span class="size">MP4 · 1 min 10 s · 102 MB</span><span class="what">Original scan, balanced scan, DVD reference and result, side by side. On Google Drive.</span></li>
  <li><a href="https://drive.usercontent.google.com/download?id=1EgkquRW2zm2lQzR_uWOQCSvpl0agE7G1&export=download&confirm=t">Candy Candy: the recovered scan at 4400 × 3300</a><span class="size">MP4 · 1 min 10 s · 298 MB</span><span class="what">The full-resolution result. On Google Drive.</span></li>
  <li><a href="https://drive.usercontent.google.com/download?id=1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD&export=download&confirm=t">Unman, Wittering and Zigo: adapter comparison</a><span class="size">MP4 · 7 s · 20 MB</span><span class="what">Faded source and adapter result, side by side. On Google Drive.</span></li>
</ul>

## Sources and references

<ul class="refs">
  <li><em>Unman, Wittering and Zigo</em> (1971, dir. John Mackenzie): trailer from a 35mm trailer reel scan posted publicly on <a href="https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps">archive.org</a>.</li>
  <li><em>Candy Candy</em> (キャンディ・キャンディ, 1976, Toei Animation): a 16mm print of the opening titles and a French PAL DVD, used for research. The series belongs to its rights holders.</li>
  <li><em>Frontier Experience</em> (1975, dir. Barbara Loden): a faded print and a telecine of the same film, the telecine supplied by Ross Lipman.</li>
  <li>CopyCat, in Foundry <a href="https://www.foundry.com/products/nuke-family/nuke">Nuke</a>.</li>
  <li>TeleStyle V2, TeleAI (<a href="https://huggingface.co/Tele-AI/TeleStyleV2">model card</a>); MiniMax H3, MiniMax (<a href="https://huggingface.co/MiniMaxAI/MiniMax-H3">model card</a>); Qwen Image Edit 2511, Qwen team, Alibaba (<a href="https://huggingface.co/Qwen/Qwen-Image-Edit-2511">model card</a>).</li>
  <li>Fabio P. Bedoya Huerta, <a href="https://library.imaging.org/archiving/articles/22/1/35">Exploring Experimental Machine Learning in Film Restoration</a>, <em>Archiving Conference</em> 22(1), 2025: the CopyCat workflow.</li>
</ul>
