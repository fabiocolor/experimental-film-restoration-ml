---
layout: home
title: Home
nav_order: 0
---

<div class="research-hero">
  <p class="eyebrow">Independent research in film preservation</p>
  <h1>Machine learning for recovering colour and detail in moving images</h1>
  <p class="hero-lede">Rescuing the original colour of faded film, not colorizing it. The colour that survives in the picture is evidence: I respect it first and only fill what was lost.</p>
  <div class="hero-buttons">
    <a href="{{ '/open-weight-color-recovery/' | relative_url }}" class="btn btn-primary">Explore open-weight colour recovery</a>
    <a href="{{ '/copycat-workflow/' | relative_url }}" class="btn btn-outline">Explore the CopyCat workflow</a>
  </div>
</div>

<div class="research-intro">
  <p>The project combines an established, reference-trained Nuke workflow with active research into Qwen Image Edit and other open-weight models. In a proper restoration the scan usually arrives balanced, so the normal order is to balance first, with a tool like the <a href="https://github.com/fabiocolor/Faded-Balancer-DCTL">Faded Balancer DCTL</a> in Resolve, and then recover. Balancing only sets levels; the dye information is the same. I document the source material, the intermediate results and the failures along the way.</p>
  <p><strong>New, October 2026:</strong> <a href="{{ '/research-status/' | relative_url }}">where the research stands</a> after SEAPAVAA and FIAT/IFTA: what works, what doesn't yet, and what you can reproduce. Talk pages: <a href="{{ '/fiat-ifta-2026-companion/' | relative_url }}">FIAT/IFTA 2026</a> · <a href="{{ '/seapavaa-2026-companion/' | relative_url }}">SEAPAVAA 2026</a>.</p>
</div>

## Current research

<div class="track-grid">
  <article class="research-card research-card-featured">
    <p class="card-kicker">Primary research track</p>
    <h3>Open-weight colour recovery</h3>
    <p>Using Qwen Image Edit and related open models to fill only the colour that was lost, while the original frame keeps its composition, texture, damage, light and detail, and the colour that survived.</p>
    <ul class="plain-list">
      <li>Source-preserving colour reconstruction</li>
      <li>Reference images and palette guidance</li>
      <li>Temporal consistency across shots</li>
      <li>Transparent comparisons and downloadable workflows</li>
    </ul>
    <a class="card-link" href="{{ '/open-weight-color-recovery/' | relative_url }}">Read the research overview <span aria-hidden="true">→</span></a><br>
    <a class="card-link card-link-secondary" href="{{ '/open-weight-color-recovery/research-routes/' | relative_url }}">See the evidence and open questions <span aria-hidden="true">→</span></a>
  </article>

  <article class="research-card">
    <p class="card-kicker">Established research track</p>
    <h3>Reference-trained recovery in Nuke</h3>
    <p>Training compact CopyCat models on carefully aligned source and reference frames to recover chroma or spatial detail, shot by shot, on your own footage in Nuke.</p>
    <ul class="plain-list">
      <li>Chroma and spatial recovery</li>
      <li>Training-pair preparation</li>
      <li>Shot and sequence workflows</li>
      <li>Nine documented case studies</li>
    </ul>
    <a class="card-link" href="{{ '/copycat-workflow/' | relative_url }}">Read the CopyCat overview <span aria-hidden="true">→</span></a>
  </article>
</div>

## Qwen Image Edit: source, proposal, composite

<div class="app-hero-strip" aria-label="Qwen Image Edit colour recovery example">
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/01_source_reptilicus_tlr_000025-40689881.jpg' | relative_url }}" alt="Faded frame from the Reptilicus trailer">
    <figcaption><strong>Source</strong><br>The faded frame given to the model.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/04_inference_frame_000000_seed_0_cfg_1.000_Belak-0c1f0329.png' | relative_url }}" alt="Qwen Image Edit colour proposal for the Reptilicus frame">
    <figcaption><strong>Colour proposal</strong><br>What Qwen Image Edit returns.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/05_final_composite_reptilicus_tlr_05_beach_woman_source-38de94d1.png' | relative_url }}" alt="Final composite: the proposed colour on the original brightness of the Reptilicus frame">
    <figcaption><strong>Final composite</strong><br>The proposed colour on the scan's own brightness and detail.</figcaption>
  </figure>
</div>

<div class="quiet-panel">
  <div>
    <p class="card-kicker">Try the current workflow</p>
    <h3>Qwen Image Edit colour recovery</h3>
    <p>Download the public ComfyUI workflow and try it on a frame from your own material.</p>
  </div>
  <a href="{{ '/qwen-color-recovery-app/' | relative_url }}" class="btn btn-primary">Open the workflow guide</a>
</div>

## Publications and presentations

The research is accompanied by working files, comparisons, and talks rather than presented as a finished “one-click” restoration product.

- [SEAPAVAA 2026 presentation companion]({{ '/seapavaa-2026-companion/' | relative_url }}): open-weight colour recovery examples, prompts, workflows, and source media.
- [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35): the peer-reviewed paper behind the CopyCat research.
- [Case studies]({{ '/case-studies/' | relative_url }}): practical results across animation, live action, nitrate, video references, and constructed references.
- [Video walkthrough](https://youtu.be/kXerjFGX9Kg): an introduction to the earlier Nuke-based chroma-recovery workflow.

> These methods are experimental. A generated result is a restoration proposal, not historical proof. Decisions should be reviewed by people who understand the film, its production context, and the archive’s ethical responsibilities.
