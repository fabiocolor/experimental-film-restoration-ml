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

When part of a film is simply gone: a stretch of nitrate that decayed to nothing, a gap in a negative while the sound runs on, emulsion breaking up across the frame. Everything that survives, in every element of the film, is used first. A video model generates only what is missing, guided by the movement around it, and every generated pixel is on record.

<figure class="reveal">
  <video autoplay muted loop playsinline preload="auto" poster="{{ '/images_kebab/examples/knights-of-the-trail-gap826-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/knights-of-the-trail-gap-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/knights-of-the-trail-gap-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
  <figcaption><span class="reveal-tag">Reveal</span> <em>Knights of the Trail</em>, nitrate, frames 734–959. The scan plays to its worst frame, holds, and heals: the cowboy, his hands and the bag are the film's in every frame, and only the ruined background is generated. Courtesy of the George Eastman Museum. <a href="{{ '/records/knights-of-the-trail/' | relative_url }}">Record</a></figcaption>
</figure>

## How it works

1. **Map what survives.** When several elements of the same film exist, they are aligned, and frame by frame the undamaged one is chosen. The shot's timeline becomes a map: which element each frame comes from, and where nothing survives.
2. **Heal only the gaps.** Inside the gaps a video model (Wan VACE, or MiniMax H3) generates the missing picture, steered by the frames before and after and by the movement tracked across them. Everything outside the gap stays original.
3. **Keep the film's own motion.** Fast, thin action that a model would redraw, a hand, a drumstick, stays the film's where the film still carries it.
4. **Say what was generated.** Generated frames and regions are an inference, not a recovery, and are labelled as such in the record.

## Examples

<figure class="pair">
  <span class="pair-labels"><span>Nitrate scan</span><span>Healed</span></span>
  <div class="pair-media pair-video" data-inspect="knights-of-the-trail-gap" data-frames="748,826,871,937">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/knights-of-the-trail-gap-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/knights-of-the-trail-gap-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/knights-of-the-trail-gap-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption><em>Knights of the Trail</em>, 226 frames. Two frames come from a diacetate copy, 18 are healed with Wan VACE 14B, and the other 206 are the nitrate scan untouched, byte for byte. In the healed frames, 65 per cent of the pixels are still the film's. Courtesy of the George Eastman Museum. <a href="{{ '/records/knights-of-the-trail/' | relative_url }}">Record</a></figcaption>
</figure>

<div class="stage-strip" aria-label="Knights of the Trail, frame 826: scan, healed, and where the pixels were generated">
  <figure>
    <img src="{{ '/images_kebab/examples/knights-of-the-trail-gap826-source.jpg' | relative_url }}" alt="Frame 826 of the nitrate scan: the decay has consumed the middle of the picture" loading="lazy">
    <figcaption><strong>Scan</strong>Frame 826, the worst of the shot.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/examples/knights-of-the-trail-gap826-result.jpg' | relative_url }}" alt="Frame 826 healed: the cowboy at the table, the cabin wall and door complete" loading="lazy">
    <figcaption><strong>Healed</strong>The cowboy is the film's; the wall, door and table are generated.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/examples/knights-of-the-trail-gap826-generated.jpg' | relative_url }}" alt="Frame 826 with the generated pixels tinted red: the background, not the actor" loading="lazy">
    <figcaption><strong>On record</strong>Generated pixels in red. Everything else is original.</figcaption>
  </figure>
</div>

<figure class="pair">
  <div class="pair-media" data-compare="Nitrate scan|Healed">
    <img src="{{ '/images_kebab/examples/knights-of-the-trail-gap748-source.jpg' | relative_url }}" alt="Frame 748 of the nitrate scan: decay down the right-hand side of the cabin" loading="lazy">
    <img src="{{ '/images_kebab/examples/knights-of-the-trail-gap748-result.jpg' | relative_url }}" alt="Frame 748 healed" loading="lazy">
  </div>
  <figcaption><em>Knights of the Trail</em>, frame 748. Drag to compare. Courtesy of the George Eastman Museum.</figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>16mm scan</span><span>Healed</span></span>
  <div class="pair-media pair-video" data-inspect="wong-flute-players" data-frames="a,b,c">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/wong-flute-players-f030-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/wong-flute-players-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/wong-flute-players-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption>Wong flute players, 16mm colour reversal from the Wong Rengifo collection, 183 frames: the emulsion breaking up across the whole frame and the colour gone to magenta. Healed from one storyboard sheet with MiniMax H3, the film's own drumming kept, one Wan VACE pass to make it one picture. Approved at working size; work continues on a version that heals the original scan. <a href="{{ '/records/wong-flute-players/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Scan|Healed">
    <img src="{{ '/images_kebab/examples/wong-flute-players-f160-source.jpg' | relative_url }}" alt="Frame 160 of the scan: a flute player and the drummer, the drum half destroyed by decay" loading="lazy">
    <img src="{{ '/images_kebab/examples/wong-flute-players-f160-result.jpg' | relative_url }}" alt="The healed frame: the drum and the hands intact" loading="lazy">
  </div>
  <figcaption>Wong flute players, frame 160: the drummer. Around the hands and the beater the film's own brightness is kept with the restored colour. Drag to compare.</figcaption>
</figure>

## Where it stands

- **Nitrate decay is healed.** The Knights of the Trail shot above went through six versions, each closer to the rule that what moves stays the film's; the version shown carries out the notes on the approved fifth. A 15-frame hole in the camera negative of <em>Poison Pen</em> (1939), with the sound running on, is being filled the same way, with the actors' movement tracked across the gap.
- **Whole-frame decay is the frontier.** The Wong shot proved the storyboard method and stops at a good result at working size, to be finished together with conventional restoration.
- **Resolution.** The models work at around 768 × 560 and ten seconds at a time; shots are done in overlapping windows, and the Knights of the Trail shot was reviewed at its 640 × 512 working size. The original-resolution pass is a separate, final step.
- **Public footage.** A search through 847 films in public archives found no other public-domain title with loss on this scale, which is why these examples come from collections rather than from a trailer reel.

## Downloads

<ul class="downloads">
  <li><a href="{{ '/downloads/gap-filling-second-pass/' | relative_url }}">Healing second-pass kit</a><span class="size">ComfyUI + Python · NVIDIA GPU</span><span class="what">The Wan VACE refinement pass and the seam blend on the Wong flute players shot, with the example windows. Checked against the approved result: ΔE 0.9.</span></li>
  <li><a href="https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/16mm-flute-players-scan.mp4">Wong flute players: the scan</a><span class="size">MP4 · 8 s · 34 MB</span><span class="what">The approved file at 768 × 560.</span></li>
  <li><a href="https://github.com/fabiocolor/experimental-film-restoration-ml/releases/download/examples-2026-10/16mm-flute-players-reconstruction.mp4">Wong flute players: the healed shot</a><span class="size">MP4 · 8 s · 22 MB</span><span class="what">The approved file at 768 × 560.</span></li>
</ul>

The Knights of the Trail material is shown by courtesy of the George Eastman Museum and is not offered for download.

## Sources and references

<ul class="refs">
  <li><em>Knights of the Trail</em>: nitrate elements and a safety copy, George Eastman Museum. Shown by courtesy of the Museum.</li>
  <li>Wong flute players: 16mm colour reversal footage from the Wong Rengifo collection.</li>
  <li>Wan 2.1 VACE 14B, Wan team, Alibaba (<a href="https://github.com/ali-vilab/VACE">VACE</a>, <a href="https://github.com/Wan-Video/Wan2.1">Wan 2.1</a>).</li>
  <li>MiniMax H3, MiniMax (<a href="https://huggingface.co/MiniMaxAI/MiniMax-H3">model card</a>); Fun ControlNet for H3, Alibaba PAI (<a href="https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union">model card</a>).</li>
  <li>Fabio Bedoya, <em>The Current Limits of AI in Film Restoration and How They May Be Surpassed</em>, FIAT/IFTA World Conference, São Paulo, October 2026 (<a href="{{ '/fiat-ifta-2026-companion/' | relative_url }}">companion page</a>).</li>
</ul>
