---
layout: default
title: "Diffusion Healing"
nav_order: 3
permalink: /diffusion-healing/
redirect_from: 
  - /gap-filling/
---


# Diffusion healing

For damage across the whole frame, or missing frames, where most of the original survives. Every surviving element is used first, and the model fills only what is lost.

Typical cases: a nitrate section was cut out, a negative has a gap while the sound continues, or the emulsion has broken up across the shot.

Phoenix, DIAMANT or Resolve can bridge two or three missing frames with optical flow. Over a longer gap, or when every frame is damaged, interpolation no longer gives acceptable results.

## Method

1. **Use everything that survives first.** If several elements of the same film exist, they are aligned and, frame by frame, the undamaged one is used.
2. **Generate only what's missing.** A video model (MiniMax H3 or Wan VACE) fills the missing or destroyed picture, guided by the movement around it and by references that keep people, props and look consistent through the shot.
3. **Keep the film's own motion where generation cannot follow it.** The models redraw fast, thin action such as a hand or a drumstick. Where the film still carries it, the film's own picture is kept.
4. **Label what was generated.** Generated picture is an inference, not a recovery, and is marked as such.

## Example: Wong flute players

Flute players and a drummer, 183 frames of 16mm colour reversal footage from the Wong Rengifo collection. The colour has faded to magenta, and the emulsion is breaking up across the whole shot. No other print exists.

<figure class="figure">
  <img src="{{ '/images_kebab/gap-filling/16mm-flute-players-scan-vs-reconstruction-f030.jpg' | relative_url }}" alt="Left: the decayed, magenta-faded 16mm scan of three flute players. Right: the reconstructed frame with restored colour.">
  <figcaption>The scan on the left, the approved reconstruction on the right.</figcaption>
</figure>

<figure class="figure">
  <img src="{{ '/images_kebab/gap-filling/16mm-flute-players-scan-vs-reconstruction-f160.jpg' | relative_url }}" alt="Left: the decayed scan of a flute player and the drummer. Right: the reconstruction, with the drum and the hands intact.">
  <figcaption>Later in the shot: the drummer. The film's own drumming is kept.</figcaption>
</figure>

<figure class="figure">
  <video controls playsinline preload="metadata" src="{{ '/media/gap-filling/16mm-flute-players-scan-web.mp4' | relative_url }}"></video>
  <figcaption>The scan (8 seconds).</figcaption>
</figure>

<figure class="figure">
  <video controls playsinline preload="metadata" src="{{ '/media/gap-filling/16mm-flute-players-reconstruction-web.mp4' | relative_url }}"></video>
  <figcaption>The approved reconstruction (8 seconds).</figcaption>
</figure>

**Workflow**

1. **One storyboard sheet for the whole shot.** All keyframes were restored together on one sheet so that people, props and look are consistent. The sheet then guided MiniMax H3 across the shot.
2. **The film's own drumming.** H3 redrew the fast, hooked drumstick regardless of the control used. In a feathered area that follows the drummer's hands and beater (about 8% of the frame), the film's own brightness was used with the restored colour.
3. **One low-denoise pass to make it a single picture.** A light video-to-video pass with Wan VACE, starting from that assembly, made the drumming area and the rest of the frame match without moving the geometry or the motion.

**Results**

- Approved, with notes, at the working resolution of 768 × 560. The drumming area now matches its surroundings much better, specks drop from about 10% to 7.5% of the frame, and the picture is steadier from frame to frame.
- The picture is softer and less detailed than the earlier version. More detail should come from a sharper first pass or an upscale, not from more denoising.
- Some unnatural movement remains around the drum during the fastest strikes. In many of those frames the emulsion around the beater is destroyed, so no original beater remains to keep. Work on the shot is paused here, to be combined later with conventional restoration.

## Downloads

- [The scan (8 s, MP4, 34 MB)](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/16mm-flute-players-scan.mp4)
- [The approved reconstruction (8 s, MP4, 22 MB)](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/16mm-flute-players-reconstruction.mp4)
- [Frame 30, side by side (JPEG)]({{ '/images_kebab/gap-filling/16mm-flute-players-scan-vs-reconstruction-f030.jpg' | relative_url }})
- [Frame 160, side by side (JPEG)]({{ '/images_kebab/gap-filling/16mm-flute-players-scan-vs-reconstruction-f160.jpg' | relative_url }})

These are the approved files at 768 × 560. The videos above are smaller previews.

- [The second pass kit]({{ '/downloads/gap-filling-second-pass/' | relative_url }}): ComfyUI graph, seam blend and the example windows. Checked against the approved result (average colour difference ΔE 0.9).

## Limits

- The models work at around 768 × 432 to 768 × 576, about ten seconds at a time.
- Small or fast movement is often smoothed or lost.
- Every shot takes several attempts and a lot of review.
- Only the second pass is public so far; the first pass isn't yet.
