---
layout: default
title: Upscaling
nav_order: 4
permalink: /upscaling/
---

<p class="eyebrow">Section 4</p>

# Upscaling

Sometimes the picture survives, but it's too damaged for a traditional restoration. Our tools borrow from the same frame or the frames around it, and when every frame is damaged there's nothing clean left to borrow. That's where I use what I call diffusion upscaling: a video model rebuilds the picture from what survives, following its structure and movement.

The result is partly synthetic. The model invents fine detail the film no longer carries. Some people will call this heresy, and to a degree it is. I wouldn't call it proper film restoration myself, but for some footage I don't see another way.

## Example: *El Tinterillo*

*El Tinterillo* is a medium-length black-and-white film that survives as a 16mm print with almost everything wrong with it, and a telecine that's cleaner, but soft, cropped and with the odd cadence of telecines from that time.

<figure class="figure">
  <img src="{{ '/images_kebab/upscaling/el-tinterillo-stairs-scan-vs-result-f300.jpg' | relative_url }}" alt="Left: the damaged 16mm scan of a man on a balcony. Right: the approved result, clean and stable.">
  <figcaption>The stairs shot: the 16mm scan on the left, the approved result on the right.</figcaption>
</figure>

<figure class="figure">
  <img src="{{ '/images_kebab/upscaling/el-tinterillo-stairs-scan-vs-result-f060.jpg' | relative_url }}" alt="Left: the washed-out 16mm scan of a street with two men walking. Right: the result, with the wall, the door and the men restored.">
  <figcaption>Earlier in the same shot.</figcaption>
</figure>

<figure class="figure">
  <video controls playsinline preload="metadata" src="{{ '/media/upscaling/el-tinterillo-stairs-scan-vs-result.mp4' | relative_url }}"></video>
  <figcaption>The 16mm scan and the approved result, side by side (4 seconds).</figcaption>
</figure>

**What I did**

1. **Combine the sources.** The telecine goes inside and the 16mm around it, which gives the full frame. I call this the hybrid.
2. **Clean the hybrid with a strong median filter.** That removes the damage and leaves a rough outline to guide the geometry, but it also removes the fine detail.
3. **Make a synthetic reference** for how the picture should look, with an image generator. One "look" reference for the whole shot keeps every part reading as the same film.
4. **Generate with MiniMax H3** in reference mode, in overlapping sections of about ten seconds. Each section starts in a calm passage, because a section that starts mid-move lags behind.
5. **Join the sections** with cuts or a short blend inside the overlaps.

**What worked, and what didn't**

- On the 624-frame stairs shot the sections join into one consistent look, and I approved it. It's now the method for the other shots in the film, and several reels have been approved, some with notes.
- The model works at about 768 × 432, so faces and fine detail are limited.
- Small mouths don't follow the dialogue well; the lips get damped.
- Video upscalers (SeedVR2, FlashVSR) and VACE were the wrong direction for this material.
- I keep the original scan and the raw sections as the record, and I say what was generated.

Before diffusion, I tried spatial recovery with CopyCat on the same film: a small model learning detail from the telecine. It's in the [case studies]({{ '/case-studies/' | relative_url }}).

## Downloads

- [Scan and result, side by side (4 s, MP4, 0.4 MB)]({{ '/media/upscaling/el-tinterillo-stairs-scan-vs-result.mp4' | relative_url }})
- [The full stairs comparison from my FIAT/IFTA talk (26 s, MP4, 62 MB, on Google Drive)](https://drive.usercontent.google.com/download?id=1IMC4AAJydIX2pnxw4hvxSTr4l9RWtrAw&export=download&confirm=t)
- [Frame 300, side by side (JPEG)]({{ '/images_kebab/upscaling/el-tinterillo-stairs-scan-vs-result-f300.jpg' | relative_url }})
- [Frame 60, side by side (JPEG)]({{ '/images_kebab/upscaling/el-tinterillo-stairs-scan-vs-result-f060.jpg' | relative_url }})

The workflow isn't public yet.
