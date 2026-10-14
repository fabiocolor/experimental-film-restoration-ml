---
layout: default
title: "Diffusion Healing"
nav_order: 3
permalink: /diffusion-healing/
redirect_from: 
  - /gap-filling/
---


# Diffusion healing

For films with damage across the whole frame, or missing frames, where most of the original still survives. Every surviving element is used first; the model only heals what is gone.

Sometimes the picture isn't just damaged, it's gone, or so decayed that there's nothing clean left to borrow. A nitrate section was cut out, a negative has a gap while the sound keeps running, or the emulsion has broken up across the whole shot.

With tools like Phoenix, DIAMANT or DaVinci Resolve you can bridge two or three missing frames with optical flow, and that kind of works. Across a longer gap, or a shot where every frame is damaged, it starts to feel wrong, because you're only interpolating what survives.

## How I approach it

1. **Use everything that survives first.** If there are several elements of the same film, I line them up and pick, frame by frame, whichever one survives undamaged.
2. **Generate only what's missing.** A video model (MiniMax H3 or Wan VACE) fills the missing or destroyed picture, guided by the movement around it and by references that keep people, props and look consistent through the shot.
3. **Keep the film's own motion where generation can't follow it.** Fast, thin action, like a hand or a drumstick, gets redrawn by the models. Where the film still carries it, I keep the film's own picture there.
4. **Say what was generated.** The generated picture is an inference, not a recovery, and I always mark it.

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

**What I did**

1. **One storyboard sheet for the whole shot.** I restored all the keyframes together on one sheet, so that people, props and look agree, then guided MiniMax H3 with it across the shot.
2. **The film's own drumming.** H3 redrew the fast, hooked drumstick no matter what control I gave it. So in a feathered area that follows the drummer's hands and beater (about 8% of the frame) I used the film's own brightness with the restored colour.
3. **One low-denoise pass to make it a single picture.** A light video-to-video pass with Wan VACE, starting from that assembly, made the drumming area and the rest of the frame match without moving the geometry or the motion.

**What worked, and what didn't**

- I approved it, with notes, at the working resolution of 768 × 560. The drumming area now matches its surroundings much better, specks drop from about 10% to 7.5% of the frame, and the picture is steadier from frame to frame.
- The cost is softness: the picture is less detailed than the earlier version. More detail should come from a sharper first pass or an upscale, not from more denoising.
- There's still some odd movement around the drum during the fastest strikes. In many of those frames the film's emulsion around the beater is destroyed, so there's no real beater left to keep. I've paused the shot here, to combine it later with conventional restoration.

## Downloads

- [The scan (8 s, MP4, 34 MB)](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/16mm-flute-players-scan.mp4)
- [The approved reconstruction (8 s, MP4, 22 MB)](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/16mm-flute-players-reconstruction.mp4)
- [Frame 30, side by side (JPEG)]({{ '/images_kebab/gap-filling/16mm-flute-players-scan-vs-reconstruction-f030.jpg' | relative_url }})
- [Frame 160, side by side (JPEG)]({{ '/images_kebab/gap-filling/16mm-flute-players-scan-vs-reconstruction-f160.jpg' | relative_url }})

These are the files I approved, at the working resolution of 768 × 560. The videos on this page are smaller web previews of them.

- [The second pass kit]({{ '/downloads/gap-filling-second-pass/' | relative_url }}): ComfyUI graph, seam blend and the example windows. Checked against the approved result (average colour difference ΔE 0.9).

## Limits

- These models see a reduced picture, around 768 × 432 to 768 × 576, and about ten seconds at a time.
- Small or fast movement is often smoothed or lost.
- Every shot takes several attempts and a lot of review.
- Only the second pass is public so far; the first pass isn't yet.
