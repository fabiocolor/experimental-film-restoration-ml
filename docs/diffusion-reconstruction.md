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

Restoration tools take picture information from the same frame or neighbouring frames. When every frame is damaged, no clean information is available. In this approach a video model rebuilds the picture from the surviving elements, following their structure and movement.

The model generates fine detail that the film no longer contains. This is not restoration in the conventional sense, but for some footage no other method is available.

## Example: *El Tinterillo*

*El Tinterillo* is a medium-length black-and-white film that survives as a heavily damaged 16mm print and a telecine that is cleaner but soft, cropped and with the irregular cadence of telecines from that period.

The stairs shot, 624 frames, also shown in the [FIAT/IFTA 2026 talk]({{ '/fiat-ifta-2026-companion/' | relative_url }}):

<figure class="figure">
  <video controls playsinline preload="metadata" poster="{{ '/images_kebab/upscaling/tinterillo-stairs-approved-f300.jpg' | relative_url }}" src="{{ '/media/upscaling/tinterillo-stairs-approved.mp4' | relative_url }}"></video>
  <figcaption>The stairs shot (26 seconds, 768 × 432).</figcaption>
</figure>

**Workflow** ([record]({{ '/records/el-tinterillo-stairs/' | relative_url }}))

1. **Combine the sources.** The telecine goes inside and the 16mm around it, which gives the full frame. This is called the hybrid.
2. **Clean the hybrid with a strong median filter.** It removes the damage and the fine detail, leaving a rough outline to guide the geometry.
3. **Make a synthetic reference** for how the picture should look, with an image generator. One "look" reference for the whole shot keeps all sections visually consistent.
4. **Generate with MiniMax H3** in reference mode, in overlapping sections of about ten seconds. Each section starts in a calm passage, because a section that starts mid-move lags behind.
5. **Join the sections** with cuts or a short blend inside the overlaps.

**Results**

- On the 624-frame stairs shot the sections join into one consistent look. This is now the method for the other shots in the film.
- The model works at about 768 × 432, so faces and fine detail are limited.
- Small mouths do not follow the dialogue well; lip movement is reduced.
- Video upscalers (SeedVR2, FlashVSR) and VACE did not suit this material. Neither did an earlier attempt with CopyCat, a small model learning detail from the telecine.
- The original scan and the raw sections are kept as the record.

## Downloads

- [The stairs shot (26 s, MP4, 23 MB)]({{ '/media/upscaling/tinterillo-stairs-approved.mp4' | relative_url }})
- [Stairs kit]({{ '/downloads/upscaling-stairs/' | relative_url }}): ComfyUI graphs, seam blend and the example windows. Checked against the result above (average colour difference ΔE 1.07).
