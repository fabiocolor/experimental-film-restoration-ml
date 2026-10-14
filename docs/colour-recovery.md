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

Recovery of the colour of faded film from balanced or unbalanced scans. The surviving colour is treated as evidence and kept; only the lost colour is filled in. Every final frame keeps the scan's own brightness (luma), so grain, detail and dirt are preserved.

If a better copy of the same frames survives (a DVD, a telecine, another print), that copy is the reference: use [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}) instead. This page is for film with no surviving colour reference.

## Balanced and unbalanced sources

In a proper restoration the scan usually arrives balanced: black is black, white is white, and the colour has collapsed, often towards cyan. Footage loaded as found is usually unbalanced, with a strong magenta or red cast. Balancing only sets levels, so both carry the same dye information; the routes differ in how the first colour frame is made.

In both cases a colour frame for the shot is made with Qwen Image Edit in ComfyUI and reviewed before anything else happens. One good frame sets the colour of the whole shot, so nothing goes forward unless that frame would be approved.

## Unbalanced sources

1. **One frame.** Qwen Image Edit 2511, guided by an edge map of the frame and a softly blurred colour chart, gives useful colour on most faded material. Use a plain chart as the guide, not a picture: a person in the guide image tends to appear in the shot. Every frame is reviewed.
2. **The whole shot.** Frames coloured one at a time flicker, so one approved frame guides the shot. MiniMax H3 with Alibaba's Fun ControlNet follows the edges of every frame and carries the colour through it; TeleStyle (a LoRA for Qwen Image Edit) is the slower alternative, or the repair where H3 loses registration.
3. **Finish with the adapter.** The H3 or TeleStyle frames that pass review teach the [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}) adapter, which colours every frame of the shot consistently.

The [single-frame kit]({{ '/downloads/colour-recovery-single-frame/' | relative_url }}) is step 1 as a ComfyUI graph, with a test frame from *Counter Attack*. It runs locally or in Comfy Cloud.

<figure class="pair">
  <div class="pair-media" data-compare="Faded source|Recovered">
    <img src="{{ '/images_kebab/examples/counter-attack-crowd-f230-source.jpg' | relative_url }}" alt="Counter Attack, crowd shot, frame 230: the surviving film copy, faded to red, a man raising his fist above the crowd" loading="lazy">
    <img src="{{ '/images_kebab/examples/counter-attack-crowd-f230-result.jpg' | relative_url }}" alt="The same frame with the recovered colour: blue and white clothes, flags, a pale sky" loading="lazy">
  </div>
  <figcaption><em>Counter Attack</em> (1976), crowd shot, frame 230 of the 308-frame proxy. An unbalanced source, no colour reference. H3 with the Fun ControlNet on 124-frame sections; 278 frames admitted as teachers; the adapter coloured all 385 frames on the scan's brightness. Approved 30 September 2026. <a href="{{ '/records/counter-attack-crowd/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Faded source|Recovered">
    <img src="{{ '/images_kebab/examples/counter-attack-waterfront-f160-source.jpg' | relative_url }}" alt="Counter Attack, waterfront, frame 160: the faded crowd on the quay, red throughout" loading="lazy">
    <img src="{{ '/images_kebab/examples/counter-attack-waterfront-f160-result.jpg' | relative_url }}" alt="The same frame recovered: a red shirt, a white towel, blue work clothes, the sky" loading="lazy">
  </div>
  <figcaption><em>Counter Attack</em> (1976), waterfront, frame 160 of 338. The earlier route: MiniMax H3 from three reference stills, and on 30 frames of fast hand movement, where H3 lost registration, an independent TeleStyle pass replaced the colour. <a href="{{ '/records/counter-attack-waterfront/' | relative_url }}">Record</a></figcaption>
</figure>

## Balanced sources

1. **One palette still.** Qwen Image Edit 2511 colours one frame from the scan's luma, with the faded frame as a hint of which hue each object had.
2. **Carry it through the shot.** MiniMax H3 with the Fun ControlNet follows the edges of every frame; the Temporal CbCr adapter learns the colour of the shot from the frames that pass review.
3. **Respect the surviving colour.** The red-green colour left in the scan can be strengthened, never flipped or weakened. Yellow is usually the lost dye, so the yellow-blue choices remain an interpretation.

The route has been tested on four shots from one source, at reduced resolution. The [balanced-source kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}) has every step: the ComfyUI graphs, the Python steps and a test shot reproduced within ΔE 1.5 at every stage.

<figure class="pair">
  <div class="pair-media" data-compare="Balanced scan|Recovered">
    <img src="{{ '/images_kebab/examples/folgers-f067-source.jpg' | relative_url }}" alt="Folgers commercial, frame 67: the balanced scan, almost grey, a woman holding up a coffee tin" loading="lazy">
    <img src="{{ '/images_kebab/examples/folgers-f067-result.jpg' | relative_url }}" alt="The same frame recovered: the red tin, warm skin, the blue blouse" loading="lazy">
  </div>
  <figcaption><em>Folgers</em>, 1970s commercial, frame 67 of 135. The balanced-source route end to end; the shot and the approved result are in the kit. <a href="{{ '/records/folgers/' | relative_url }}">Record</a></figcaption>
</figure>

## The single-frame route, step by step

The first, still-frame route from June 2026, shown at SEAPAVAA. It is still the way the first colour frame of any shot is made.

<div class="stage-strip" aria-label="Juggernaut auditorium: source, model output, composite">
  <figure>
    <img src="{{ '/images_kebab/examples/juggernaut-auditorium-f066-source.jpg' | relative_url }}" alt="Juggernaut trailer, frame 66: the auditorium, faded to magenta" loading="lazy">
    <figcaption><strong>Source</strong>The faded frame, 2048 × 1556.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/examples/juggernaut-auditorium-f066-model.jpg' | relative_url }}" alt="Qwen Image Edit's colour proposal for the frame, at 1184 × 880" loading="lazy">
    <figcaption><strong>Model output</strong>Qwen Image Edit 2511, guided by the edge map and a soft colour chart, 1184 × 880.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/examples/juggernaut-auditorium-f066-result.jpg' | relative_url }}" alt="The composite: the proposed colour on the scan's own brightness and detail" loading="lazy">
    <figcaption><strong>Composite</strong>Only the colour is taken; the brightness, grain and damage are the scan's.</figcaption>
  </figure>
</div>

<p class="experiment-credit"><em>Juggernaut</em> (1974) trailer, from the same 35mm trailer reel scan as <em>Reptilicus</em>. The full comparison set, prompts and failures are on the <a href="{{ '/seapavaa-2026-companion/' | relative_url }}">SEAPAVAA 2026 companion</a>.</p>

## What still doesn't work

- **Frame by frame.** Each frame on its own is a fair interpretation, but together they flicker. That is why one approved frame has to guide the shot.
- **Plausible results can be wrong.** On an unclear frame the model can invent objects or faces, so every result is checked against the scan.
- **Resolution and length.** The video models work at around 768 × 432 to 768 × 576, about ten seconds at a time. Tiling keeps more detail, but the colour drifts between tiles and leaves seams.
- **Hard motion and broken cadence** still leave some tint, as in the shadows of the crowd shot above.
- **New shots.** The target is for at least three out of four new shots to work on the first pass. This has not been reached yet.

## Downloads

<ul class="downloads">
  <li><a href="{{ '/downloads/colour-recovery-single-frame/' | relative_url }}">Single-frame kit</a><span class="size">ComfyUI · local or Comfy Cloud</span><span class="what">One faded frame to one colour frame: the Qwen Image Edit graph with the edge map and the colour chart, a test frame from <em>Counter Attack</em>, and the composite on the scan's brightness inside the graph. Two variants: the exact published model, and the model in Comfy Cloud's free library.</span></li>
  <li><a href="{{ '/downloads/faded-colour-recovery-t185/' | relative_url }}">Balanced-source kit</a><span class="size">ComfyUI + Python · NVIDIA GPU</span><span class="what">The whole route for a balanced shot: palette still, H3 with the Fun ControlNet, the Temporal CbCr adapter and the surviving-colour step, with the <em>Folgers</em> test shot reproduced within ΔE 1.5 at every stage. The palette still also runs in Comfy Cloud.</span></li>
</ul>
