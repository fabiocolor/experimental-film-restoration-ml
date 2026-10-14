---
layout: default
title: "Diffusion Reconstruction"
nav_order: 4
permalink: /diffusion-reconstruction/
redirect_from: 
  - /upscaling/
  - /spatial-recovery/
---


# Diffusion reconstruction

For films beyond repair, where every frame is too damaged for conventional restoration.

Conventional restoration tools borrow from the same frame or the frames around it. When every frame is damaged, there's nothing clean left to borrow. That's where I use diffusion reconstruction: a video model rebuilds the picture from what survives, following its structure and movement.

The result is partly synthetic. The model invents fine detail the film no longer carries. Some people will call this heresy, and to a degree it is. I wouldn't call it proper film restoration myself, but for some footage I don't see another way.

## Example: *El Tinterillo*

*El Tinterillo* is a medium-length black-and-white film that survives as a 16mm print with almost everything wrong with it, and a telecine that's cleaner, but soft, cropped and with the odd cadence of telecines from that time.

The stairs shot, 624 frames, also shown in my [FIAT/IFTA 2026 talk]({{ '/fiat-ifta-2026-companion/' | relative_url }}):

<figure class="figure">
  <video controls playsinline preload="metadata" poster="{{ '/images_kebab/upscaling/tinterillo-stairs-approved-f300.jpg' | relative_url }}" src="{{ '/media/upscaling/tinterillo-stairs-approved.mp4' | relative_url }}"></video>
  <figcaption>The stairs shot (26 seconds, 768 × 432).</figcaption>
</figure>

**What I did**

1. **Combine the sources.** The telecine goes inside and the 16mm around it, which gives the full frame. I call this the hybrid.
2. **Clean the hybrid with a strong median filter.** That removes the damage and leaves a rough outline to guide the geometry, but it also removes the fine detail.
3. **Make a synthetic reference** for how the picture should look, with an image generator. One "look" reference for the whole shot keeps every part reading as the same film.
4. **Generate with MiniMax H3** in reference mode, in overlapping sections of about ten seconds. Each section starts in a calm passage, because a section that starts mid-move lags behind.
5. **Join the sections** with cuts or a short blend inside the overlaps.

**What worked, and what didn't**

- On the 624-frame stairs shot the sections join into one consistent look. It's now the method for the other shots in the film.
- The model works at about 768 × 432, so faces and fine detail are limited.
- Small mouths don't follow the dialogue well; the lips get damped.
- Video upscalers (SeedVR2, FlashVSR) and VACE were the wrong direction for this material. So was my earlier attempt with CopyCat, a small model learning detail from the telecine.
- I keep the original scan and the raw sections as the record, and I say what was generated.

## Downloads

- [The stairs shot (26 s, MP4, 23 MB)]({{ '/media/upscaling/tinterillo-stairs-approved.mp4' | relative_url }})
- [Stairs kit]({{ '/downloads/upscaling-stairs/' | relative_url }}): ComfyUI graphs, seam blend and the example windows. Checked against the result above (average colour difference ΔE 1.07).
