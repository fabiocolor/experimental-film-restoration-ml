---
layout: default
title: "Counter Attack, crowd"
parent: "Example Records"
nav_order: 2
permalink: /records/counter-attack-crowd/
---

# Counter Attack (1976), crowd shot: record

The whole-shot example on the [faded colour recovery]({{ '/colour-recovery/' | relative_url }}) page and the home page, and the shot shown on slide 11 of the [FIAT/IFTA 2026 talk]({{ '/fiat-ifta-2026-companion/' | relative_url }}#h3-controlnet). It is the first shot finished with the current default route for unbalanced sources: MiniMax H3 with the Fun ControlNet, finished with the Temporal CbCr adapter. The same film's waterfront shot has its own [record]({{ '/records/counter-attack-waterfront/' | relative_url }}).

<dl class="facts">
  <dt>Source</dt><dd>A faded film copy of <em>Counter Attack</em> (1976), a Chinese feature; the crowd shot with a fast pan in the middle. 385 frames at 1920 × 1440 and 30 frames per second, unbalanced (magenta-red cast). 77 frames were near-duplicates from a broken cadence, so the 308 distinct frames were mapped to 24 frames per second.</dd>
  <dt>Reference</dt><dd>None survives. Two synthetic palettes: the main outdoor palette and one for an indoor close-up, each a Qwen Image Edit 2511 still laid on the source brightness and checked at full size before the run.</dd>
  <dt>Route</dt><dd>Edge map (Canny) of every frame after a small median filter and a local-contrast step → MiniMax H3 with the Fun ControlNet on 124-frame sections at 768 × 576, 24 fps → each H3 frame registered to the source and admitted as a teacher only if its brightness lined up within 1.5 pixels overall (278 passed) → Temporal CbCr adapter trained on the teachers, best epoch on held-out frames, then fitted on all → colour run at 640 × 480, upscaled with guidance, put on the original brightness at 1920 × 1440 for all 385 frames.</dd>
  <dt>Models</dt><dd>Qwen Image Edit 2511 (palettes); MiniMax H3 with Fun ControlNet Union (original release); the Temporal CbCr adapter (931,274 parameters, trained for this shot).</dd>
  <dt>Finished</dt><dd>30 September 2026. Remaining tint in the shadowed folds of a yellow jacket in the first frames.</dd>
  <dt>On this site</dt><dd>Frames 40 and 230 of the 308-frame comparison video (faded source and result side by side), cut from the video shown at FIAT/IFTA. The comparison video (1920 × 840, 13 s) is on <a href="https://drive.google.com/file/d/1OQcp7SrwmFZoUiFJ6NC8EfHgI68TGmxi/view">Google Drive</a>.</dd>
  <dt>Reproduced from the published files</dt><dd>Not yet. The H3 and adapter steps are the same as in the <a href="{{ '/downloads/faded-colour-recovery-t185/' | relative_url }}">balanced-source kit</a>, but this shot's palettes, edge maps and teacher list are not published.</dd>
</dl>
