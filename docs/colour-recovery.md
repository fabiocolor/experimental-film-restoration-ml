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

Bringing back the colour of faded film, from balanced or unbalanced scans. The colour that survives is evidence, so I keep it and fill in only what faded. Every final frame keeps the scan's own brightness (luma), so the grain, the detail and even the dirt stay.

If a better copy of the same frames survives, use [Temporal CbCr]({{ '/temporal-cbcr/' | relative_url }}) instead.

## Balanced and unbalanced sources

In a proper restoration the scan usually arrives balanced: black is black, white is white, and the colour has collapsed, often towards cyan. Footage loaded as found is usually unbalanced, with a strong magenta or red cast. Balancing only sets levels, so both carry the same dye information.

With no better copy, I make a colour frame for the shot with Qwen Image Edit in ComfyUI and review it before going further.

## Balanced sources

1. **One palette still.** Qwen Image Edit 2511 colours one frame from the scan's luma, with the faded frame as a hint of which hue each object had.
2. **Carry it through the shot.** MiniMax H3 with Alibaba's Fun ControlNet follows the edges of every frame, and the Temporal CbCr adapter learns the colour of the shot from the frames that pass review.
3. **Respect the surviving colour.** The red-green colour left in the scan can be strengthened, never flipped or weakened.

Yellow is mostly the dye that's lost, so the yellow-blue choices are still an interpretation. So far I've tested this on four shots from one source, at reduced resolution. The [download kit]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}) has the graphs, the Python steps and an example shot.

## Unbalanced sources

- **Single frames.** Qwen Image Edit 2511, guided by an edge map of the frame and a softly blurred colour chart, gives useful colour on most faded material, with every frame reviewed. Use a plain chart as the guide, not a picture: a person in the guide tends to turn up in the shot.
- **Whole shots.** Frames coloured one at a time flicker, so one approved reference has to guide the whole shot. MiniMax H3 with the Fun ControlNet, or TeleStyle (a LoRA for Qwen Image Edit), makes candidate frames. The good ones teach the Temporal CbCr adapter, which colours the rest.

## Examples

**Counter Attack (1976): an unbalanced source, the whole shot.** No colour reference survives for this Chinese film. MiniMax H3 and the Fun ControlNet gave the teacher frames, and the Temporal CbCr adapter carried the colour through a 385-frame crowd shot with a fast pan. Some tint remains in the shadows, because my copy had a broken cadence.

<figure class="figure">
  <a href="https://drive.google.com/file/d/1OQcp7SrwmFZoUiFJ6NC8EfHgI68TGmxi/view"><img src="https://drive.google.com/thumbnail?id=1OQcp7SrwmFZoUiFJ6NC8EfHgI68TGmxi&amp;sz=w960" alt="Counter Attack: the faded crowd shot and the recovered colour, side by side" loading="lazy" referrerpolicy="no-referrer"></a>
  <figcaption><em>Counter Attack</em>: the faded source and the result, side by side (video on Google Drive).</figcaption>
</figure>

**Folgers (1970s commercial): a balanced source.** One of four shots from a compilation of commercials, recovered with the balanced-source route.

<figure class="figure">
  <img src="{{ '/images_kebab/colour-recovery/commercials-folgers-before-after-f067.jpg' | relative_url }}" alt="A Folgers coffee commercial: the balanced, faded scan on the left and the recovered colour on the right" loading="lazy">
  <figcaption>The balanced scan on the left, the result on the right. The shot and the result are in the <a href="{{ '/downloads/faded-colour-recovery-t185/' | relative_url }}">download kit</a>.</figcaption>
</figure>

## What still doesn't work

- **Frame by frame.** Each frame on its own is a fair interpretation, but together they flicker.
- **Plausible isn't the same as right.** On a hard-to-read frame the model can invent objects or faces, so every result gets checked against the scan.
- **Resolution and length.** The video models work at around 768 × 432, about ten seconds at a time. Tiling keeps more detail, but the colour drifts between tiles and leaves seams.
- **New shots.** I'd like at least three out of four new shots to work on the first pass. I'm not there yet.

## Downloads

- [Faded colour recovery kit for balanced scans]({{ '/downloads/faded-colour-recovery-t185/' | relative_url }}): ComfyUI graphs, Python steps and the Folgers example.
- [Counter Attack: the whole shot, 13 s (11.6 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=1OQcp7SrwmFZoUiFJ6NC8EfHgI68TGmxi&export=download&confirm=t)
