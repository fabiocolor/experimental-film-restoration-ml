---
layout: home
title: Home
nav_order: 0
---

<div class="research-hero">
  <h1>Experimental Film Restoration with Machine Learning</h1>
  <p class="hero-lede">What survives in the film is evidence. I respect it first, and let the models fill only what was lost: the colour that faded, the frames that are missing, the picture that's gone.</p>
  <div class="hero-buttons">
    <a href="{{ '/colour-recovery/' | relative_url }}" class="btn btn-primary">Start with faded colour recovery</a>
    <a href="{{ '/research-status/' | relative_url }}" class="btn btn-outline">Where the research stands</a>
  </div>
</div>

<div class="app-hero-strip" aria-label="Faded colour recovery on a frame from the Reptilicus trailer">
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/01_source_reptilicus_tlr_000025-40689881.jpg' | relative_url }}" alt="Faded frame from the Reptilicus trailer">
    <figcaption><strong>Source</strong><br>The faded frame.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/04_inference_frame_000000_seed_0_cfg_1.000_Belak-0c1f0329.png' | relative_url }}" alt="Qwen Image Edit colour proposal for the Reptilicus frame">
    <figcaption><strong>Model output</strong><br>What Qwen Image Edit returns.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/05_final_composite_reptilicus_tlr_05_beach_woman_source-38de94d1.png' | relative_url }}" alt="Final composite: the recovered colour on the original brightness of the Reptilicus frame">
    <figcaption><strong>Final composite</strong><br>The recovered colour on the scan's own brightness and detail.</figcaption>
  </figure>
</div>

<p class="experiment-credit"><em>Reptilicus</em> (1961) trailer, from a 35mm trailer reel scan posted publicly on <a href="https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps">archive.org</a>. The trailer belongs to its rights holders.</p>

<div class="research-intro">
  <p>My research on machine learning for film restoration. Each area is a different problem, but the approach is the same: start from the scan, keep its picture, and let a model add only what's missing. None of it is one click. A restorer decides what's acceptable and says what was generated.</p>
</div>

## Five research areas

<div class="track-grid">
  <article class="research-card research-card-featured">
    <p class="card-kicker">1</p>
    <h3>Faded colour recovery</h3>
    <p>Bringing back the colour of faded film, from balanced or unbalanced scans. What survived is kept; only what faded is filled in.</p>
    <p class="card-link-secondary">Examples: Counter Attack, Folgers</p>
    <a class="card-link" href="{{ '/colour-recovery/' | relative_url }}">Faded colour recovery <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">2</p>
    <h3>Temporal CbCr</h3>
    <p>Colour learned from a reference for the shot, historical or synthetic, and kept steady through it.</p>
    <p class="card-link-secondary">Examples: Candy Candy, Unman, Wittering and Zigo</p>
    <a class="card-link" href="{{ '/temporal-cbcr/' | relative_url }}">Temporal CbCr <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">3</p>
    <h3>Diffusion healing</h3>
    <p>Healing damage across the frame, or missing frames, while keeping most of the original.</p>
    <p class="card-link-secondary">Example: Wong flute players</p>
    <a class="card-link" href="{{ '/diffusion-healing/' | relative_url }}">Diffusion healing <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">4</p>
    <h3>Diffusion reconstruction</h3>
    <p>For films beyond repair. A video model rebuilds the picture from what's left. Some of the detail is synthetic, and I say so.</p>
    <p class="card-link-secondary">Example: El Tinterillo</p>
    <a class="card-link" href="{{ '/diffusion-reconstruction/' | relative_url }}">Diffusion reconstruction <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">5</p>
    <h3>Black-and-white colourization</h3>
    <p>Colour for panchromatic and orthochromatic film, worked out from the greyscale and what the stock could see.</p>
    <a class="card-link" href="{{ '/black-and-white-colourization/' | relative_url }}">Black-and-white colourization <span aria-hidden="true">→</span></a>
  </article>
</div>

## Examples\*

<div class="example-grid">
  <figure>
    <a href="{{ '/colour-recovery/' | relative_url }}"><img src="https://drive.google.com/thumbnail?id=1OQcp7SrwmFZoUiFJ6NC8EfHgI68TGmxi&amp;sz=w640" alt="Counter Attack: the faded crowd shot and the recovered colour, side by side" loading="lazy" referrerpolicy="no-referrer"></a>
    <figcaption><strong>Counter Attack</strong>: faded colour recovery, the whole shot.</figcaption>
  </figure>
  <figure>
    <a href="{{ '/colour-recovery/' | relative_url }}"><img src="{{ '/images_kebab/colour-recovery/commercials-folgers-before-after-f067.jpg' | relative_url }}" alt="A Folgers coffee commercial: the balanced scan and the recovered colour, side by side" loading="lazy"></a>
    <figcaption><strong>Folgers</strong>: faded colour recovery from a balanced scan.</figcaption>
  </figure>
  <figure>
    <a href="{{ '/temporal-cbcr/' | relative_url }}"><img src="{{ '/images_kebab/candy-candy/candy-candy-comparison-still.jpg' | relative_url }}" alt="Candy Candy: the scan, the DVD reference and the result, side by side" loading="lazy"></a>
    <figcaption><strong>Candy Candy</strong>: Temporal CbCr from a historical reference.</figcaption>
  </figure>
  <figure>
    <a href="{{ '/temporal-cbcr/' | relative_url }}"><img src="https://drive.google.com/thumbnail?id=1s7i8nd7tRFuwbACbc-MnJHQNtpNxyhDD&amp;sz=w640" alt="Unman, Wittering and Zigo: the faded choir shot and the result, side by side" loading="lazy" referrerpolicy="no-referrer"></a>
    <figcaption><strong>Unman, Wittering and Zigo</strong>: Temporal CbCr from a synthetic reference.</figcaption>
  </figure>
  <figure>
    <a href="{{ '/diffusion-healing/' | relative_url }}"><img src="{{ '/images_kebab/gap-filling/16mm-flute-players-scan-vs-reconstruction-f030.jpg' | relative_url }}" alt="Wong flute players: the decayed 16mm scan and the healed frame, side by side" loading="lazy"></a>
    <figcaption><strong>Wong flute players</strong>: diffusion healing.</figcaption>
  </figure>
  <figure>
    <a href="{{ '/diffusion-reconstruction/' | relative_url }}"><img src="{{ '/images_kebab/upscaling/tinterillo-stairs-approved-f300.jpg' | relative_url }}" alt="El Tinterillo: the stairs shot, rebuilt by diffusion reconstruction" loading="lazy"></a>
    <figcaption><strong>El Tinterillo</strong>: diffusion reconstruction.</figcaption>
  </figure>
</div>

<div class="quiet-panel">
  <div>
    <h3>Where the research stands</h3>
    <p>What works now, what doesn't yet, and what you can try yourself.</p>
  </div>
  <a href="{{ '/research-status/' | relative_url }}" class="btn btn-primary">Read the status</a>
</div>

## Talks and writing

- [Talks]({{ '/talks/' | relative_url }}): the companion pages for FIAT/IFTA 2026 and SEAPAVAA 2026.
- [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35): the peer-reviewed paper behind the CopyCat workflow.
- [Video walkthrough](https://youtu.be/kXerjFGX9Kg) of the CopyCat colour-recovery workflow in Nuke.
- [Tools]({{ '/tools/' | relative_url }}) I use alongside this research.
