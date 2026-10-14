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

For films beyond repair, where every frame is too damaged for conventional restoration.

Restoration tools take picture information from the same frame or neighbouring frames. When every frame is damaged, no clean information is available. In this approach a video model rebuilds the picture from the surviving elements, following their structure and movement.

The model generates fine detail that the film no longer contains. This is not restoration in the conventional sense, but for some footage no other method is available.

## Example: *El Tinterillo*

*El Tinterillo* is a medium-length black-and-white film that survives as a heavily damaged 16mm print and a telecine that is cleaner but soft, cropped and with the irregular cadence of telecines from that period.

The stairs shot, 624 frames, also shown in the [FIAT/IFTA 2026 talk]({{ '/fiat-ifta-2026-companion/' | relative_url }}):

<figure class="pair">
  <div class="pair-media" data-compare="Hybrid|Reconstruction">
    <img src="{{ '/images_kebab/examples/el-tinterillo-stairs-w1-f120-source.jpg' | relative_url }}" alt="El Tinterillo, stairs, frame 121: the hybrid of the damaged 16mm print and the telecine, a man on the stairs behind a balustrade" loading="lazy">
    <img src="{{ '/images_kebab/examples/el-tinterillo-stairs-w1-f120-result.jpg' | relative_url }}" alt="The reconstructed frame: the balustrade, the man and the wall rebuilt by the video model" loading="lazy">
  </div>
  <figcaption><em>El Tinterillo</em>, stairs, frame 121 (window w1). The hybrid (left) is the median-cleaned 16mm frame with the registered telecine inside it; the reconstruction (right) is the MiniMax H3 window at 768 × 432, before the seam blend.</figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Hybrid|Reconstruction">
    <img src="{{ '/images_kebab/examples/el-tinterillo-stairs-w2b-f150-source.jpg' | relative_url }}" alt="Frame 278: the hybrid, heavily damaged over the figure and the wall" loading="lazy">
    <img src="{{ '/images_kebab/examples/el-tinterillo-stairs-w2b-f150-result.jpg' | relative_url }}" alt="The reconstruction of the same frame" loading="lazy">
  </div>
  <figcaption>Frame 278 (window w2b). The four windows overlap and are joined with a short tone blend at the cuts; the kit has the blend.</figcaption>
</figure>

<figure class="figure">
  <video controls playsinline preload="metadata" poster="{{ '/images_kebab/upscaling/tinterillo-stairs-approved-f300.jpg' | relative_url }}" src="{{ '/media/upscaling/tinterillo-stairs-approved.mp4' | relative_url }}"></video>
  <figcaption>The whole stairs shot, 624 frames (26 seconds, 768 × 432), as approved on 26 September 2026 and shown in the <a href="{{ '/fiat-ifta-2026-companion/' | relative_url }}">FIAT/IFTA 2026 talk</a>.</figcaption>
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

<ul class="downloads">
  <li><a href="{{ '/downloads/upscaling-stairs/' | relative_url }}">Stairs kit</a><span class="size">ComfyUI + Python</span><span class="what">The H3 reference-mode graphs for each window, the hybrid step, the seam blend and the example windows. Checked against the result above: hybrid identical, seam blend average ΔE 1.07.</span></li>
  <li><a href="{{ '/media/upscaling/tinterillo-stairs-approved.mp4' | relative_url }}">The stairs shot</a><span class="size">MP4 · 26 s · 23 MB</span><span class="what">The approved reconstruction at 768 × 432.</span></li>
</ul>
