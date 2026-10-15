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

For films that are beyond repair. When every frame is damaged, no clean information is left for a restoration tool to borrow. Here a video model rebuilds the picture from the surviving elements, following their structure and their movement, and the result is said to be what it is: a reconstruction, with detail the film no longer holds.

<figure class="reveal">
  <video autoplay muted loop playsinline preload="auto" poster="{{ '/images_kebab/examples/el-tinterillo-fg02-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/el-tinterillo-fg02-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/el-tinterillo-fg02-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
  <figcaption><span class="reveal-tag">Reveal</span> <em>El Tinterillo</em>, shot FG02, 410 frames. The damaged 16mm print, and the shot rebuilt by MiniMax H3 from the print, the telecine and one look reference. <a href="{{ '/records/el-tinterillo-stairs/' | relative_url }}">Record</a></figcaption>
</figure>

## How it works

1. **Combine the sources.** The telecine goes inside, the 16mm print around it: the full frame, with the best of both. This is the hybrid.
2. **Reduce it to structure.** A strong median filter removes the damage and the fine detail and leaves the geometry to follow.
3. **One look for the whole film.** A single reference still sets how the picture should look, so every shot of the reel matches.
4. **Generate in overlapping windows.** MiniMax H3 in reference mode, about ten seconds at a time, each window starting in a calm passage; the windows are joined with a short tone blend.

## The *El Tinterillo* reel

*El Tinterillo* survives as a heavily damaged 16mm print and a soft, cropped telecine with the uneven frame rate of its period. In September 2026 the whole reel was brought to the same look, shot by shot.

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

## Where it stands

- **A whole reel, one look.** Five shots of *El Tinterillo* are finished with the same method; the stairs set the look and the others followed.
- **Faces and lips.** The models work at 768 × 432, so small faces are limited and lip movement is reduced. The next pass targets the lips; a test showed the detail is there in the source, so the limit is in how the model is guided, not in the film.
- **What was tried and dropped.** Video upscalers (SeedVR2, FlashVSR), Wan VACE driven by the source, and a CopyCat detail model did not suit this material.
- **The record.** The original scan and every raw window are kept, and the reconstruction is labelled as one.

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
