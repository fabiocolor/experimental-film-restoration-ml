---
layout: default
title: "Diffusion Healing"
nav_order: 3
permalink: /diffusion-healing/
redirect_from: 
  - /gap-filling/
---

<span class="kicker">Research area 3</span>

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

<figure class="pair">
  <div class="pair-media" data-compare="Scan|Healed">
    <img src="{{ '/images_kebab/examples/wong-flute-players-f030-source.jpg' | relative_url }}" alt="Frame 30 of the 16mm scan: three flute players, the image faded to magenta and the emulsion broken up" loading="lazy">
    <img src="{{ '/images_kebab/examples/wong-flute-players-f030-result.jpg' | relative_url }}" alt="The healed frame: the players intact, in colour, with the film's grain" loading="lazy">
  </div>
  <figcaption>Frame 30 of 183: the scan and the approved reconstruction at 768 × 560.</figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Scan|Healed">
    <img src="{{ '/images_kebab/examples/wong-flute-players-f160-source.jpg' | relative_url }}" alt="Frame 160 of the scan: a flute player and the drummer, the drum half destroyed by decay" loading="lazy">
    <img src="{{ '/images_kebab/examples/wong-flute-players-f160-result.jpg' | relative_url }}" alt="The healed frame: the drum and the hands intact" loading="lazy">
  </div>
  <figcaption>Frame 160: the drummer. In the feathered area around the hands and beater, the film's own brightness is kept with the restored colour.</figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>Scan</span><span>Healed</span></span>
  <div class="pair-media" data-sync>
    <video controls playsinline preload="metadata" muted src="{{ '/media/gap-filling/16mm-flute-players-scan-web.mp4' | relative_url }}"></video>
    <video controls playsinline preload="metadata" muted src="{{ '/media/gap-filling/16mm-flute-players-reconstruction-web.mp4' | relative_url }}"></video>
  </div>
  <figcaption>The whole shot, 8 seconds. The two players run together; play either one. Smaller previews of the <a href="#downloads">approved files</a>.</figcaption>
</figure>

**Workflow** ([record]({{ '/records/wong-flute-players/' | relative_url }}))

1. **One storyboard sheet for the whole shot.** All keyframes were restored together on one sheet so that people, props and look are consistent. The sheet then guided MiniMax H3 across the shot.
2. **The film's own drumming.** H3 redrew the fast, hooked drumstick regardless of the control used. In a feathered area that follows the drummer's hands and beater (about 8% of the frame), the film's own brightness was used with the restored colour.
3. **One low-denoise pass to make it a single picture.** A light video-to-video pass with Wan VACE, starting from that assembly, made the drumming area and the rest of the frame match without moving the geometry or the motion.

**Results**

- Approved, with notes, at the working resolution of 768 × 560. The drumming area now matches its surroundings much better, specks drop from about 10% to 7.5% of the frame, and the picture is steadier from frame to frame.
- The picture is softer and less detailed than the earlier version. More detail should come from a sharper first pass or an upscale, not from more denoising.
- Some unnatural movement remains around the drum during the fastest strikes. In many of those frames the emulsion around the beater is destroyed, so no original beater remains to keep. Work on the shot is paused here, to be combined later with conventional restoration.

## Downloads

<ul class="downloads">
  <li><a href="{{ '/downloads/gap-filling-second-pass/' | relative_url }}">Second-pass kit</a><span class="size">ComfyUI + Python</span><span class="what">The Wan VACE graph, the seam blend and the example windows. Checked against the approved result: average ΔE 0.9.</span></li>
  <li><a href="https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/16mm-flute-players-scan.mp4">The scan</a><span class="size">MP4 · 8 s · 34 MB</span><span class="what">The approved file at 768 × 560.</span></li>
  <li><a href="https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/16mm-flute-players-reconstruction.mp4">The approved reconstruction</a><span class="size">MP4 · 8 s · 22 MB</span><span class="what">The approved file at 768 × 560.</span></li>
</ul>

## Limits

- The models work at around 768 × 432 to 768 × 576, about ten seconds at a time.
- Small or fast movement is often smoothed or lost.
- Every shot takes several attempts and a lot of review.
- Only the second pass is public so far; the first pass isn't yet.
