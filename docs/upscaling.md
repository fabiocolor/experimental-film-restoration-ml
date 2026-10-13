---
layout: default
title: Upscaling
nav_order: 4
permalink: /upscaling/
---


# Upscaling

Sometimes the picture survives, but it's too damaged for a traditional restoration. Our tools borrow from the same frame or the frames around it, and when every frame is damaged there's nothing clean left to borrow. That's where I use what I call diffusion upscaling: a video model rebuilds the picture from what survives, following its structure and movement.

The result is partly synthetic. The model invents fine detail the film no longer carries. Some people will call this heresy, and to a degree it is. I wouldn't call it proper film restoration myself, but for some footage I don't see another way.

## Example: *El Tinterillo*

*El Tinterillo* is a medium-length black-and-white film that survives as a 16mm print with almost everything wrong with it, and a telecine that's cleaner, but soft, cropped and with the odd cadence of telecines from that time.

The approved stairs shot, 624 frames, was shown in my [FIAT/IFTA 2026 talk]({{ '/fiat-ifta-2026-companion/' | relative_url }}). I'll put files here once they're exported straight from the approved master.

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

Nothing to download yet. The workflow and the example files will go up once they reproduce the approved result.
