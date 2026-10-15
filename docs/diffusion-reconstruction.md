---
layout: default
title: "Diffusion Reconstruction"
nav_order: 4
permalink: /diffusion-reconstruction/
redirect_from: 
  - /upscaling/
  - /spatial-recovery/
---

<span class="kicker">Research area 4</span>

# Diffusion reconstruction

This started as an upscaling project, and upscaling is still not quite the right word for it. *El Tinterillo* survives as a 16mm print with everything wrong with it: frames stuck together, dirt, the emulsion damaged, and a telecine with no resolution and a crop, made close enough to the original that at least the picture is clean. If you try normal restoration tools on the print you can't even start, because there is not enough spatial or temporal information left to borrow from.

So this calls for a different approach. A video model rebuilds the picture from what survives, following the structure and the movement of the two elements. That is not film restoration in the proper sense: the result is based on an interpretation, a restorer's and the model's, of how an image of this era should look, and the fine detail is filled from the model's training, not from the film. It is a reconstruction, and it is labelled as one. But for this kind of footage there is no other way, and it is better than nothing.

<figure class="reveal">
  <video autoplay muted loop playsinline preload="auto" poster="{{ '/images_kebab/examples/el-tinterillo-fg02-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/el-tinterillo-fg02-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/el-tinterillo-fg02-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
  <figcaption><span class="reveal-tag">Reveal</span> <em>El Tinterillo</em>, shot FG02, 410 frames. The damaged 16mm print, and the shot rebuilt by MiniMax H3 from the print, the telecine and one look reference. <a href="{{ '/records/el-tinterillo-stairs/' | relative_url }}">Record</a></figcaption>
</figure>

## How it works

First the two elements are combined into a hybrid: the telecine goes inside, the 16mm print around it, so you get the full frame with the best of both. Then a strong median, which is like a blur but really an average of the pixels around each point, takes out the damage. It also takes out all the fine detail, so what is left is the geometry of the shot, a baseline the model can follow.

From that comes a synthetic reference: one still that sets how the picture should look, and the same still for every shot of the reel, so the whole film comes out with one look. MiniMax H3 in reference mode then generates the shot in windows of about ten seconds, each starting in a calm passage. The windows don't always agree with each other, so the frames where they do are joined with a short blend. Unlike colour recovery, where the film's luma is kept and only the chroma is taken, here the luma is beyond saving and the model's picture is what there is. It has a more plastic quality than film. It is double synthetic, if you like.

## The *El Tinterillo* reel

In September 2026 the whole reel was brought to the same look, shot by shot. The stairs shot came first and set the look; the others followed it.

<figure class="pair">
  <span class="pair-labels"><span>16mm print</span><span>Reconstruction</span></span>
  <div class="pair-media pair-video" data-inspect="el-tinterillo-fg02" data-frames="a,b,c">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/el-tinterillo-fg02-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/el-tinterillo-fg02-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/el-tinterillo-fg02-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption>Shot FG02, 410 frames.</figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>16mm print</span><span>Reconstruction</span></span>
  <div class="pair-media pair-video" data-inspect="el-tinterillo-fg04" data-frames="a,b">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/el-tinterillo-fg04-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/el-tinterillo-fg04-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/el-tinterillo-fg04-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption>Shot FG04, 422 frames.</figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>16mm print</span><span>Reconstruction</span></span>
  <div class="pair-media pair-video" data-inspect="el-tinterillo-fg03" data-frames="b">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/el-tinterillo-fg03-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/el-tinterillo-fg03-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/el-tinterillo-fg03-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption>Shot FG03, 176 frames. The look is there; the lip movement is the next target.</figcaption>
</figure>

<figure class="figure">
  <video controls playsinline preload="metadata" poster="{{ '/images_kebab/upscaling/tinterillo-stairs-f300.jpg' | relative_url }}" src="{{ '/media/upscaling/tinterillo-stairs.mp4' | relative_url }}"></video>
  <figcaption>The stairs shot, 624 frames (26 seconds), the first shot finished and the look reference for the reel. Shown at <a href="{{ '/fiat-ifta-2026-companion/' | relative_url }}">FIAT/IFTA 2026</a>. <a href="{{ '/records/el-tinterillo-stairs/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Hybrid|Reconstruction">
    <img src="{{ '/images_kebab/examples/el-tinterillo-stairs-w1-f120-source.jpg' | relative_url }}" alt="El Tinterillo, stairs, frame 121: the hybrid of the damaged 16mm print and the telecine, a man on the stairs behind a balustrade" loading="lazy">
    <img src="{{ '/images_kebab/examples/el-tinterillo-stairs-w1-f120-result.jpg' | relative_url }}" alt="The reconstructed frame: the balustrade, the man and the wall rebuilt by the video model" loading="lazy">
  </div>
  <figcaption>Stairs, frame 121. The hybrid (left) is the 16mm frame cleaned with a median filter, with the telecine aligned inside it.</figcaption>
</figure>

## What works and what doesn't

Five shots of *El Tinterillo* are finished with the same method and the same look. Small faces and lip movement are the weak point, because the model works at 768 × 432; a test showed the detail is there in the source, so the limit is in how the model is guided, not in the film, and the lips are the next pass.

The obvious things were tried first and dropped: video upscalers (SeedVR2, FlashVSR), Wan VACE driven by the source, a CopyCat detail model. None of them suited this material. What works is windows, and making the windows agree with each other, which wastes inference and takes iterations. Maybe somebody has a more straightforward way; at the moment this is the only one that works here. The original scan and every raw window are kept, and the result is labelled as a reconstruction.

## Downloads

<ul class="downloads">
  <li><a href="{{ '/downloads/upscaling-stairs/' | relative_url }}">Stairs kit</a><span class="size">ComfyUI + Python</span><span class="what">The H3 reference-mode graphs for the four windows of the stairs shot, the hybrid step, the seam blend and the example windows. Checked against the published result: hybrid identical, seam blend ΔE 1.07.</span></li>
  <li><a href="{{ '/media/upscaling/tinterillo-stairs.mp4' | relative_url }}">The stairs shot</a><span class="size">MP4 · 26 s · 23 MB</span><span class="what">The reconstruction at 768 × 432.</span></li>
</ul>

## Sources and references

<ul class="refs">
  <li><em>El Tinterillo</em>: a 16mm print and a telecine of a medium-length black-and-white film, used for research; the film belongs to its rights holders.</li>
  <li>MiniMax H3, MiniMax (<a href="https://huggingface.co/MiniMaxAI/MiniMax-H3">model card</a>), reference-to-video mode.</li>
  <li>Fabio Bedoya, <em>The Current Limits of AI in Film Restoration and How They May Be Surpassed</em>, FIAT/IFTA World Conference, São Paulo, October 2026 (<a href="{{ '/fiat-ifta-2026-companion/' | relative_url }}">companion page</a>).</li>
</ul>
