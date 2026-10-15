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

The colour of a faded film, brought back from the film itself. No surviving print, no DVD, no telecine: the scan's own brightness, grain and damage stay exactly as they are, and the colour that faded is rebuilt around them, frame after frame, through the whole shot.

<figure class="reveal">
  <video autoplay muted loop playsinline preload="auto" src="{{ '/media/examples/counter-attack-crowd-reveal.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/counter-attack-crowd-b-source.jpg' | relative_url }}"></video>
  <figcaption><span class="reveal-tag">Reveal</span> <em>Counter Attack</em> (1976), crowd shot. A film copy faded to red, 385 frames with a fast pan; the recovered colour on the scan's own brightness. <a href="{{ '/records/counter-attack-crowd/' | relative_url }}">Record</a></figcaption>
</figure>

## How it works

1. **One colour frame for the shot.** Qwen Image Edit makes a colour proposal for one frame, guided by an edge map of the frame and a soft colour chart, so it has nothing to copy but colour. A person approves it. Nothing goes forward on a frame that would not be approved.
2. **Carried through the shot.** MiniMax H3 with Alibaba's Fun ControlNet follows the edges of every frame and carries that colour through the movement: crowds, pans, hands, a change of light.
3. **Finished by a small model trained for that shot.** The frames that pass review teach the [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}) adapter, which colours every frame consistently, in minutes.
4. **Composited on the scan.** Only the colour is taken. Brightness, detail, grain, scratches and dirt are the film's, at the scan's full resolution.

Scans that were balanced before recovery (black is black, white is white, the colour collapsed) go through the same route with one rule added: the red-green colour that survived in the dyes is kept and may only be strengthened, never flipped. Yellow is the dye that fades first, so the yellow-blue axis is what the recovery supplies.

## Examples

<figure class="pair">
  <span class="pair-labels"><span>Faded source</span><span>Recovered</span></span>
  <div class="pair-media pair-video">
    <video controls muted playsinline preload="metadata" src="{{ '/media/examples/obsession-ballroom-sbs.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/obsession-ballroom-a-source.jpg' | relative_url }}"></video>
  </div>
  <figcaption><em>Obsession</em> (1976), the ballroom, 254 frames at 2048 × 1556. Four approved colour anchors, H3 in four overlapping sections, the colour registered onto the scan's own brightness. The faded source is a Cineon log scan, shown through a Rec.709 view. <a href="{{ '/records/obsession-ballroom/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>Faded source</span><span>Recovered</span></span>
  <div class="pair-media pair-video">
    <video controls muted playsinline preload="metadata" src="{{ '/media/examples/counter-attack-crowd-sbs.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/counter-attack-crowd-f040-source.jpg' | relative_url }}"></video>
  </div>
  <figcaption><em>Counter Attack</em> (1976), crowd shot, 9 of 13 seconds. H3 with the Fun ControlNet on overlapping sections, 278 frames admitted as teachers, the adapter over all 385 frames. Approved 30 September 2026. <a href="{{ '/records/counter-attack-crowd/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>Faded source</span><span>Recovered</span></span>
  <div class="pair-media pair-video">
    <video controls muted playsinline preload="metadata" src="{{ '/media/examples/counter-attack-quarry-sbs.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/counter-attack-quarry-a-source.jpg' | relative_url }}"></video>
  </div>
  <figcaption><em>Counter Attack</em> (1976), the quarry, 681 frames at 1920 × 1440. Six H3 sections stitched in their overlaps, with the palette changing between the second and third as the scene changes. The H3 pass; a final detector pass is still to come. <a href="{{ '/records/counter-attack-quarry/' | relative_url }}">Record</a></figcaption>
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
  <div class="pair-media pair-video">
    <video controls muted playsinline preload="metadata" src="{{ '/media/examples/counter-attack-waterfront-sbs.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/counter-attack-waterfront-b-source.jpg' | relative_url }}"></video>
  </div>
  <figcaption><em>Counter Attack</em> (1976), the waterfront, 338 frames. The comparison published in July 2026 from the TeleStyle route; the approved shot of August refined it with H3 and kept TeleStyle on 30 frames of fast hand movement. <a href="{{ '/records/counter-attack-waterfront/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>Balanced scan</span><span>Recovered</span></span>
  <div class="pair-media pair-video">
    <video controls muted playsinline preload="metadata" src="{{ '/media/examples/folgers-sbs.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/folgers-f020-source.jpg' | relative_url }}"></video>
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

The first colour frame of any shot is made this way. The stills below are from the June 2026 study shown at SEAPAVAA; the trailer scans are Cineon log, shown here through a Cineon-to-Rec.709 view so that before and after sit in the same display space.

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

## Where it stands

- **Whole shots, with movement.** In June a single still was the result and a moving shot flickered. By September whole shots with pans, crowds and dancing were approved: the ballroom, the crowd, the waterfront, the quarry. Hard motion is a matter of sections, teachers and review, not a wall. Given enough passes, every faded shot tried so far has come back.
- **Full resolution.** The video models see a reduced picture, but only their colour is used, so every result is at the scan's full resolution with the scan's own grain.
- **Time.** The first whole shot took four hours of TeleStyle. H3 with the ControlNet does a 124-frame section in 20 to 45 minutes, and the adapter trains in about 90 seconds.
- **Open.** The target is three out of four new shots right on the first pass; some shots still take a second pass. Deep shadows keep a tint on the hardest cadences. The colour is an interpretation unless a surviving reference confirms it, and every page says so.

## Downloads

<ul class="downloads">
  <li><a href="{{ '/downloads/colour-recovery-single-frame/' | relative_url }}">Single-frame kit</a><span class="size">ComfyUI · local or Comfy Cloud</span><span class="what">One faded frame to one colour frame, with the composite on the scan's brightness made inside the graph. Built-in nodes only, no Python. Test frame, chart, edge map and the approved still included.</span></li>
  <li><a href="{{ '/downloads/faded-colour-recovery-t185/' | relative_url }}">Balanced-source kit</a><span class="size">ComfyUI + Python · NVIDIA GPU</span><span class="what">The whole route for a balanced shot, with the <em>Folgers</em> test shot reproduced within ΔE 1.5 at every stage. The palette still also runs in Comfy Cloud.</span></li>
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
