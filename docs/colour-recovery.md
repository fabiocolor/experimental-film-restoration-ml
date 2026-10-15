---
layout: default
title: "Faded Colour Recovery"
nav_order: 1
has_children: true
permalink: /colour-recovery/
redirect_from:
  - /open-weight-color-recovery/
  - /open-weight-color-recovery/research-routes/
  - /qwen-color-recovery-app/
---

<span class="kicker">Research area 1</span>

# Faded colour recovery

Colour recovery is the main thread of this research. The case that matters most is the one that keeps coming up in Latin America and Southeast Asia: the magenta scan, or the red scan, is the only thing left of the film. There is no negative to go back to, no better print, no DVD. Whatever a spectral scanner might get out of the element, you don't have the element. So everything here works with the scan as it is right now.

The idea is simple to say. Don't add anything, don't clean the film, don't make it HD. Just get the colour back. The scan keeps its own brightness, grain and damage, and only the colour is rebuilt, frame after frame, through the whole shot.

<figure class="reveal">
  <video autoplay muted loop playsinline preload="auto" poster="{{ '/images_kebab/examples/counter-attack-crowd-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/counter-attack-crowd-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/counter-attack-crowd-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
  <figcaption><span class="reveal-tag">Reveal</span> <em>Counter Attack</em> (1976), crowd shot. A film copy faded to red, 385 frames with a fast pan; the recovered colour on the scan's own brightness. <a href="{{ '/records/counter-attack-crowd/' | relative_url }}">Record</a></figcaption>
</figure>

## How it works

The first problem is getting one good colour frame. A lot of prompts and workflows were tested for this before one recipe came out that most consistently gives an acceptable colour. Qwen Image Edit gets the faded frame, an edge map of that frame, and a softly blurred colour chart, so it has nothing to copy except colour. The result is checked at full size. If it doesn't pass, nothing else happens on that shot.

The second problem is the real one: temporal consistency. You could just run that image model 24 times a second, but these models make a different decision every time they run, so you end up with 24 different decisions every second. Fine for a thumbnail, useless for a film. What carries the colour through the shot is MiniMax H3, a video model, with Alibaba's Fun ControlNet. The ControlNet is what makes the model behave: it follows the edges of every frame, so the people stay where they are and only the colour changes. That works on crowds, pans, hands and changing light, up to a point, and when the model gets lost the shot is done in sections, which means running more inference than you would like.

The frames that pass review then teach a small model built for this, the [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}) adapter. It learns the colour of that one shot in about 90 seconds and colours every frame consistently. Finally the colour goes back onto the scan. Only the chroma is taken; the luma, which is where the resolution and the grain live, is the film's, at the scan's full size. We are not very sensitive to the resolution of colour, so even if the model saw a reduced picture, the result doesn't look reduced.

Some scans arrive already balanced (black is black, white is white, and the colour has collapsed to almost nothing). Those go through the same route with one rule added: the red-green colour that survived in the dyes is kept and may only be strengthened, never flipped. Yellow is the dye that fades first, so the yellow-blue axis is what the recovery has to supply.

## Examples

<figure class="pair">
  <span class="pair-labels"><span>Faded source</span><span>Recovered</span></span>
  <div class="pair-media pair-video" data-inspect="obsession-ballroom" data-frames="a,b,c">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/obsession-ballroom-a-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/obsession-ballroom-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/obsession-ballroom-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption><em>Obsession</em> (1976), the ballroom, 254 frames at 2048 × 1556. Four chosen colour anchors, H3 in four overlapping sections, the colour registered onto the scan's own brightness. <a href="{{ '/records/obsession-ballroom/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>Faded source</span><span>Recovered</span></span>
  <div class="pair-media pair-video" data-inspect="counter-attack-crowd" data-frames="a,b,c">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/counter-attack-crowd-f040-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/counter-attack-crowd-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/counter-attack-crowd-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption><em>Counter Attack</em> (1976), crowd shot, 9 of 13 seconds. MiniMax H3 with the Fun ControlNet on overlapping sections; 278 of its frames passed review and taught the adapter, which coloured all 385. <a href="{{ '/records/counter-attack-crowd/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>Faded source</span><span>Recovered</span></span>
  <div class="pair-media pair-video" data-inspect="counter-attack-quarry" data-frames="a,b,c">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/counter-attack-quarry-a-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/counter-attack-quarry-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/counter-attack-quarry-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption><em>Counter Attack</em> (1976), the quarry, 681 frames at 1920 × 1440. Six H3 sections stitched in their overlaps, with the palette changing between the second and third as the scene changes. <a href="{{ '/records/counter-attack-quarry/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Faded source|Recovered">
    <img src="{{ '/images_kebab/examples/counter-attack-quarry-c-source.jpg' | relative_url }}" alt="Counter Attack, quarry: a faded frame, red throughout" loading="lazy">
    <img src="{{ '/images_kebab/examples/counter-attack-quarry-c-result.jpg' | relative_url }}" alt="The same frame recovered: the rock face, the workers' clothes, the sky" loading="lazy">
  </div>
  <figcaption><em>Counter Attack</em>, the quarry, near the end of the shot. Drag to compare. <a href="{{ '/records/counter-attack-quarry/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>Faded source</span><span>Recovered</span></span>
  <div class="pair-media pair-video" data-inspect="counter-attack-waterfront" data-frames="a,b,c">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/counter-attack-waterfront-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/counter-attack-waterfront-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/counter-attack-waterfront-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption><em>Counter Attack</em> (1976), the waterfront, 338 frames at 1920 × 1440. H3 from three reference stills; on 30 frames of fast hand movement an independent TeleStyle pass took over. <a href="{{ '/records/counter-attack-waterfront/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>Balanced scan</span><span>Recovered</span></span>
  <div class="pair-media pair-video" data-inspect="folgers" data-frames="a,b,c">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/folgers-f020-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/folgers-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/folgers-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption><em>Folgers</em>, 1970s commercial, 135 frames. A balanced scan: the surviving red-green record kept, the lost yellow-blue axis recovered. The whole route is the <a href="{{ '/downloads/faded-colour-recovery-t185/' | relative_url }}">balanced-source kit</a>, reproduced within ΔE 1.5 at every stage. <a href="{{ '/records/folgers/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Faded source|Recovered">
    <img src="{{ '/images_kebab/examples/folgers-f110-source.jpg' | relative_url }}" alt="Folgers commercial, frame 110: the balanced scan, almost grey" loading="lazy">
    <img src="{{ '/images_kebab/examples/folgers-f110-result.jpg' | relative_url }}" alt="The same frame recovered: the red tin, warm skin, the blue blouse" loading="lazy">
  </div>
  <figcaption><em>Folgers</em>, frame 110 of 135. Drag to compare. <a href="{{ '/records/folgers/' | relative_url }}">Record</a></figcaption>
</figure>

## One frame, step by step

This is what the first colour frame of any shot looks like at each step. The stills are from the June 2026 study shown at SEAPAVAA, as delivered.

<div class="stage-strip" aria-label="Juggernaut auditorium: source, model output, composite">
  <figure>
    <img src="{{ '/images_kebab/examples/juggernaut-auditorium-f066-source.jpg' | relative_url }}" alt="Juggernaut trailer, frame 66: the auditorium, faded to magenta" loading="lazy">
    <figcaption><strong>Source</strong>The faded frame, 2048 × 1556.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/examples/juggernaut-auditorium-f066-model.jpg' | relative_url }}" alt="Qwen Image Edit's colour proposal for the frame, at 1184 × 880" loading="lazy">
    <figcaption><strong>Model output</strong>Qwen Image Edit, guided by the edge map and a soft colour chart.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/examples/juggernaut-auditorium-f066-result.jpg' | relative_url }}" alt="The composite: the proposed colour on the scan's own brightness and detail" loading="lazy">
    <figcaption><strong>Composite</strong>Only the colour is taken; brightness, grain and damage are the scan's.</figcaption>
  </figure>
</div>

<p class="experiment-credit"><em>Juggernaut</em> (1974) trailer, from a 35mm trailer reel scan posted publicly on <a href="https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps">archive.org</a>. The full study, with the prompts and the failures, is on the <a href="{{ '/seapavaa-2026-companion/' | relative_url }}">SEAPAVAA 2026 companion</a>.</p>

## What works and what doesn't

In June the result was a single still, and anything that moved flickered. By September there were whole shots with pans, crowds and dancing: the ballroom, the crowd, the waterfront, the quarry. Every faded shot tried so far has come back, given enough passes. Hard motion is not a wall any more; it is sections, review and the adapter, and time.

Time is the honest cost. The first whole shot took four hours of TeleStyle. H3 with the ControlNet does a 124-frame section in 20 to 45 minutes on an RTX 5090, and you waste inference, because out of a 200-frame run you may only keep 50 and go again. The adapter trains in about 90 seconds, which is why it finishes everything.

Is it production ready? Not yet. The target is three out of four new shots right on the first pass, and some still need a second. Deep shadows keep a tint on the hardest shots. And the colour is an interpretation unless a surviving reference confirms it; every page here says so. The goal at the beginning was an app where you upload a shot and get it back in colour. That is technically possible now, but these films need care, and the decisions are still too many to leave unattended.

## Downloads

<ul class="downloads">
  <li><a href="{{ '/downloads/colour-recovery-single-frame/' | relative_url }}">Single-frame kit</a><span class="size">ComfyUI · local or Comfy Cloud</span><span class="what">One faded frame in, one colour frame out, with the composite on the scan's brightness done inside the graph. Built-in nodes only, no Python. The test frame, the chart, the edge map and the published still are included so you can check your setup gives the same thing.</span></li>
  <li><a href="{{ '/downloads/faded-colour-recovery-t185/' | relative_url }}">Balanced-source kit</a><span class="size">ComfyUI + Python · NVIDIA GPU</span><span class="what">The whole route for a balanced shot, end to end, on the <em>Folgers</em> test shot. Every stage reproduces the published result within ΔE 1.5. The palette still also runs in Comfy Cloud.</span></li>
</ul>

## Sources and references

<ul class="refs">
  <li><em>Counter Attack</em> (反击, 1976): a faded film copy used for research. The film belongs to its rights holders.</li>
  <li><em>Juggernaut</em> (1974, dir. Richard Lester), <em>Reptilicus</em> (1961), <em>Obsession</em> (1976): trailers from a 35mm trailer reel scan posted publicly on <a href="https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps">archive.org</a>.</li>
  <li><em>Folgers</em>: one shot from a compilation of 1970s television commercials.</li>
  <li>Qwen Image Edit 2511, Qwen team, Alibaba (<a href="https://huggingface.co/Qwen/Qwen-Image-Edit-2511">model card</a>, Apache-2.0); Lightning LoRA, LightX2V (<a href="https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning">model card</a>).</li>
  <li>MiniMax H3, MiniMax (<a href="https://huggingface.co/MiniMaxAI/MiniMax-H3">model card</a>); Fun ControlNet for H3, Alibaba PAI (<a href="https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union">model card</a>).</li>
  <li>TeleStyle V2, TeleAI (<a href="https://huggingface.co/Tele-AI/TeleStyleV2">model card</a>).</li>
  <li>Fabio P. Bedoya Huerta, <a href="https://library.imaging.org/archiving/articles/22/1/35">Exploring Experimental Machine Learning in Film Restoration</a>, <em>Archiving Conference</em> 22(1), 2025.</li>
</ul>
