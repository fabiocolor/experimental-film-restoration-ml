---
layout: default
title: Gap Filling & Reconstruction
nav_order: 2
permalink: /gap-filling/
---

<p class="eyebrow">Section 2</p>

# Gap filling and reconstruction

Sometimes the picture isn't damaged, it's gone. This happens a lot with nitrate: a decaying section was cut out so it wouldn't damage the rest of the reel. Or a camera negative has a short gap while the sound keeps running, so the shot can't just be shortened.

With tools like Phoenix, DIAMANT or DaVinci Resolve you can bridge two or three missing frames with optical flow, and that kind of works. Across a longer gap the movement starts to feel wrong, because you're only interpolating what survives.

## How I approach it

1. **Use everything that survives first.** If there are several elements of the same film, I line them up (colour, warping, framing) and pick, frame by frame, whichever one survives undamaged. A timeline of the shot then works as a map of what's actually missing.
2. **Generate only inside the gap.** Where nothing survives, a video model (Wan VACE 14B, or MiniMax H3) fills only the missing or damaged area, guided by the movement around it: skeletons tracked from the frames before and after the gap. Everything that survives stays original.
3. **Say what was generated.** The generated frames are an inference, not a recovery. I can't know what was really there, so I always mark which pixels were generated.

## Where it stands

I don't have a finished example I can show publicly yet. The footage I've tested on belongs to archives and rights holders, and I'm looking for public-domain nitrate material so I can share a complete one.

What I can say from the tests:

- Keeping the surviving picture untouched and generating only inside masked areas works much better than regenerating whole frames.
- Resolution and length are still the main limits. These models see a reduced picture, around 768 × 432, and about ten seconds at a time.
- Small or fast movement, like hands, mouths or a drumstick, is often smoothed or lost.
- Every shot takes several attempts and a lot of review.

The workflows aren't public yet. A cleaner ComfyUI version is planned.
