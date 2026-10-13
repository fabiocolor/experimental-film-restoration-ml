---
layout: home
title: Home
nav_order: 0
---

<div class="research-hero">
  <p class="eyebrow">Independent research in film preservation</p>
  <h1>Experimental Film Restoration with Machine Learning</h1>
  <p class="hero-lede">What survives in the film is evidence. I respect it first, and let the models fill only what was lost: the colour that faded, the frames that are missing, the detail that's gone.</p>
  <div class="hero-buttons">
    <a href="{{ '/colour-recovery/' | relative_url }}" class="btn btn-primary">Start with colour recovery</a>
    <a href="{{ '/research-status/' | relative_url }}" class="btn btn-outline">Where the research stands</a>
  </div>
</div>

<div class="research-intro">
  <p>This is where I keep all my research on machine learning for film restoration. Each section below is one kind of problem, worked the same way: start from the scan, keep its original picture, and let a model add only what's missing. I write down what worked, what didn't and what you can try yourself. None of it is one click, and it's always a restorer who decides what's acceptable and who says what was generated.</p>
</div>

## The research

<div class="track-grid">
  <article class="research-card research-card-featured">
    <p class="card-kicker">1 · Leads the research</p>
    <h3>Colour recovery</h3>
    <p>Rescuing the original colour of faded film, not colorizing it. Balance the scan first, keep the colour that survived, and fill only what faded, with a reference when one exists and with open-weight models when it doesn't.</p>
    <a class="card-link" href="{{ '/colour-recovery/' | relative_url }}">Colour recovery <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">2</p>
    <h3>Gap filling and reconstruction</h3>
    <p>Rebuilding frames that are completely gone, using every surviving element first and generating only inside the gap.</p>
    <a class="card-link" href="{{ '/gap-filling/' | relative_url }}">Gap filling <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">3</p>
    <h3>Dirt removal</h3>
    <p>Advanced Dirt Removal, a free macro for DaVinci Resolve that cleans dirt and lets you bring back what the cleaning took.</p>
    <a class="card-link" href="{{ '/dirt-removal/' | relative_url }}">Dirt removal <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">4</p>
    <h3>Upscaling</h3>
    <p>When every frame is too damaged to restore conventionally, a video model rebuilds the picture. The detail is partly synthetic, and I say so.</p>
    <a class="card-link" href="{{ '/upscaling/' | relative_url }}">Upscaling <span aria-hidden="true">→</span></a>
  </article>

</div>

## Colour recovery: source, proposal, composite

These examples are research demos that show the workflow and what it can do. They aren't production-quality exports, so you may spot some issues.

<div class="app-hero-strip" aria-label="Colour recovery example">
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

<div class="quiet-panel">
  <div>
    <p class="card-kicker">Try it</p>
    <h3>Single-frame colour recovery in ComfyUI</h3>
    <p>Download the workflow and try it on a frame from your own material.</p>
  </div>
  <a href="{{ '/qwen-color-recovery-app/' | relative_url }}" class="btn btn-primary">Open the workflow guide</a>
</div>

## Talks and writing

- [Talks]({{ '/talks/' | relative_url }}): the companion pages for FIAT/IFTA 2026 and SEAPAVAA 2026.
- [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35): the peer-reviewed paper behind the CopyCat research.
- [Video walkthrough](https://youtu.be/kXerjFGX9Kg) of the Nuke colour-recovery workflow.
