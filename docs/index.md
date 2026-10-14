---
layout: home
title: Home
nav_order: 0
---

<div class="research-hero">
  <h1>Experimental Film Restoration with Machine Learning</h1>
  <p class="hero-lede">What survives in the film is treated as evidence and kept. The models fill only what was lost: faded colour, missing frames and lost picture.</p>
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

<p class="experiment-credit">Made with an earlier single-frame route (<a href="{{ '/records/reptilicus-beach/' | relative_url }}">record</a>). <em>Reptilicus</em> (1961) trailer, from a 35mm trailer reel scan posted publicly on <a href="https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps">archive.org</a>. The trailer belongs to its rights holders.</p>

<div class="research-intro">
  <p>Research on machine learning for film restoration. Each area addresses a different problem with the same approach: start from the scan, keep its picture, and use a model only for what is missing. The process is not automatic. A restorer decides what is acceptable and records what was generated.</p>
</div>

## Five research areas

<div class="track-grid">
  <article class="research-card research-card-featured">
    <p class="card-kicker">1</p>
    <h3>Faded colour recovery</h3>
    <p>Recovery of the colour of faded film from balanced or unbalanced scans. Surviving colour is kept; only faded colour is filled in.</p>
    <p class="card-link-secondary">Example: Counter Attack</p>
    <a class="card-link" href="{{ '/colour-recovery/' | relative_url }}">Faded colour recovery <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">2</p>
    <h3>Temporal CbCr</h3>
    <p>Colour learned from a historical or synthetic reference and kept consistent through the shot.</p>
    <p class="card-link-secondary">Examples: Candy Candy, Reptilicus</p>
    <a class="card-link" href="{{ '/temporal-cbcr/' | relative_url }}">Temporal CbCr <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">3</p>
    <h3>Diffusion healing</h3>
    <p>Repair of full-frame damage or missing frames while keeping most of the original.</p>
    <p class="card-link-secondary">Example: Wong flute players</p>
    <a class="card-link" href="{{ '/diffusion-healing/' | relative_url }}">Diffusion healing <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">4</p>
    <h3>Diffusion reconstruction</h3>
    <p>For films beyond repair. A video model rebuilds the picture from the surviving elements. Some of the detail is synthetic and is labelled as such.</p>
    <p class="card-link-secondary">Example: El Tinterillo</p>
    <a class="card-link" href="{{ '/diffusion-reconstruction/' | relative_url }}">Diffusion reconstruction <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">5</p>
    <h3>Black-and-white colourization</h3>
    <p>Colour for panchromatic and orthochromatic film, inferred from the recorded greyscale and the stock's spectral response.</p>
    <a class="card-link" href="{{ '/black-and-white-colourization/' | relative_url }}">Black-and-white colourization <span aria-hidden="true">→</span></a>
  </article>
</div>

## Examples\*

<div class="example-grid">
  <figure>
    <a href="{{ '/colour-recovery/' | relative_url }}"><img src="{{ '/images_kebab/colour-recovery/counter-attack-waterfront-t148-f160.jpg' | relative_url }}" alt="Counter Attack: the faded waterfront crowd and the recovered colour, side by side" loading="lazy"></a>
    <figcaption><strong>Counter Attack</strong>: faded colour recovery, the whole shot.</figcaption>
  </figure>
  <figure>
    <a href="{{ '/temporal-cbcr/' | relative_url }}"><img src="{{ '/images_kebab/candy-candy/candy-candy-comparison-still.jpg' | relative_url }}" alt="Candy Candy: the scan, the DVD reference and the result, side by side" loading="lazy"></a>
    <figcaption><strong>Candy Candy</strong>: Temporal CbCr from a historical reference.</figcaption>
  </figure>
  <figure>
    <a href="{{ '/temporal-cbcr/' | relative_url }}"><img src="{{ '/images_kebab/temporal-cbcr/reptilicus-office-t178-f66.jpg' | relative_url }}" alt="Reptilicus: the faded office scene and the result, side by side" loading="lazy"></a>
    <figcaption><strong>Reptilicus</strong>: Temporal CbCr from a synthetic reference.</figcaption>
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
    <p>What works, what does not yet, and what can be reproduced. Each example has a <a href="{{ '/records/' | relative_url }}">record</a> of its source, models and approval.</p>
  </div>
  <a href="{{ '/research-status/' | relative_url }}" class="btn btn-primary">Read the status</a>
</div>

## Talks and writing

- [Talks]({{ '/talks/' | relative_url }}): the companion pages for FIAT/IFTA 2026 and SEAPAVAA 2026.
- [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35): the peer-reviewed paper behind the CopyCat workflow.
- [Video walkthrough](https://youtu.be/kXerjFGX9Kg) of the CopyCat colour-recovery workflow in Nuke.
- [Tools]({{ '/tools/' | relative_url }}) used alongside this research.
