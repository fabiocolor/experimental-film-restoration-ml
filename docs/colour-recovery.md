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

# Faded colour recovery

Recovery of the colour of faded film from balanced or unbalanced scans. The surviving colour is treated as evidence and kept; only faded colour is filled in. Every final frame keeps the scan's own brightness (luma), so grain, detail and dirt are preserved.

If a better copy of the same frames survives, use [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}) instead.

## Balanced and unbalanced sources

In a proper restoration the scan usually arrives balanced: black is black, white is white, and the colour has collapsed, often towards cyan. Footage loaded as found is usually unbalanced, with a strong magenta or red cast. Balancing only sets levels, so both carry the same dye information.

When no better copy exists, a colour frame for the shot is made with Qwen Image Edit in ComfyUI and reviewed before the next step.

## Balanced sources

1. **One palette still.** Qwen Image Edit 2511 colours one frame from the scan's luma, with the faded frame as a hint of which hue each object had.
2. **Carry it through the shot.** MiniMax H3 with Alibaba's Fun ControlNet follows the edges of every frame, and the Temporal CbCr adapter learns the colour of the shot from the frames that pass review.
3. **Respect the surviving colour.** The red-green colour left in the scan can be strengthened, never flipped or weakened.

Yellow is usually the lost dye, so the yellow-blue choices remain an interpretation. The route has been tested on four shots from one source, at reduced resolution. The [download kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}) has the graphs, the Python steps and a test shot.

## Unbalanced sources

- **Single frames.** Qwen Image Edit 2511, guided by an edge map of the frame and a softly blurred colour chart, gives useful colour on most faded material, with every frame reviewed. Use a plain chart as the guide, not a picture; a person in the guide image tends to appear in the shot.
- **Whole shots.** Frames coloured one at a time flicker, so one approved reference has to guide the whole shot. MiniMax H3 with the Fun ControlNet, or TeleStyle (a LoRA for Qwen Image Edit), makes candidate frames. The good ones teach the Temporal CbCr adapter, which colours the rest.

## Examples

**Counter Attack (1976): an unbalanced source, the whole shot.** A waterfront crowd from a film copy faded to magenta-red. No colour reference survives. MiniMax H3 with three reference stills carried the colour through the 338-frame shot. On 30 frames of fast hand movement, where H3 lost registration, an independent TeleStyle pass on the same shot replaced the colour. The scan's luma is kept on every frame.

<figure class="figure">
  <img src="{{ '/images_kebab/colour-recovery/counter-attack-waterfront-t148-f160.jpg' | relative_url }}" alt="Counter Attack: the faded waterfront crowd on the left and the recovered colour on the right" loading="lazy">
  <figcaption><em>Counter Attack</em>: the faded source and the result, frame 160. <a href="{{ '/records/counter-attack-waterfront/' | relative_url }}">Record</a>.</figcaption>
</figure>

## What still doesn't work

- **Frame by frame.** Each frame on its own is a fair interpretation, but together they flicker.
- **Plausible results can be wrong.** On an unclear frame the model can invent objects or faces, so every result is checked against the scan.
- **Resolution and length.** The video models work at around 768 × 432, about ten seconds at a time. Tiling keeps more detail, but the colour drifts between tiles and leaves seams.
- **New shots.** The target is for at least three out of four new shots to work on the first pass. This has not been reached yet.

**Folgers (1970s commercial): a balanced source.** The test shot for the balanced-source kit, reproduced at every stage within ΔE 1.5. The yellow-blue result is limited, as is usual when yellow is the lost dye.

<figure class="figure">
  <img src="{{ '/images_kebab/colour-recovery/commercials-folgers-before-after-f067.jpg' | relative_url }}" alt="A Folgers coffee commercial: the balanced, faded scan on the left and the recovered colour on the right" loading="lazy">
  <figcaption><em>Folgers</em>: the balanced scan and the result, frame 67. The shot and the result are in the <a href="{{ '/downloads/faded-colour-recovery-t185/' | relative_url }}">download kit</a>. <a href="{{ '/records/folgers/' | relative_url }}">Record</a>.</figcaption>
</figure>

## Downloads

- [Faded colour recovery kit for balanced scans]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}): ComfyUI graphs, Python steps and a test shot from a 1970s commercial, reproduced at every stage within ΔE 1.5 ([record]({{ '/records/folgers/' | relative_url }})).
