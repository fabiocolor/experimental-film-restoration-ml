---
layout: default
title: CopyCat Workflow
nav_order: 2
has_children: true
permalink: /copycat-workflow/
---

<p class="eyebrow">Established research track</p>

# Reference-Trained Recovery with CopyCat

This workflow trains a small neural network for one film project. It learns from carefully chosen pairs: a degraded source frame and a better reference to the same moment. The method can recover colour, or it can recover spatial detail, while keeping the surviving source material at the centre of the process.

It is intended for film archives, restoration practitioners, colourists, and researchers who have access to Nuke with CopyCat and Inference.

The Nuke template runs locally in Nuke Non-Commercial or Nuke Indie, with your own footage. You use it to build a small dataset for each shot and train CopyCat on it.

<div class="hero-buttons">
  <a href="{{ '/start-here/' | relative_url }}" class="btn btn-primary">Start the workflow</a>
  <a href="https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/latest" class="btn btn-outline">Get the Nuke template (Non-Commercial / Indie)</a>
</div>

## Choose the recovery task

<div class="track-grid">
  <article class="research-card">
    <p class="card-kicker">When colour has faded</p>
    <h3>Chroma recovery</h3>
    <p>Use the source frame’s luminance and detail, then learn colour from a stronger reference such as another print, a telecine, a home-video release, or a carefully constructed guide.</p>
    <a class="card-link" href="{{ '/chroma-recovery/' | relative_url }}">Read the chroma guide <span aria-hidden="true">→</span></a>
  </article>
  <article class="research-card">
    <p class="card-kicker">When detail has been lost</p>
    <h3>Spatial recovery</h3>
    <p>Use a sharper or more complete reference to reconstruct detail while preserving the colour information that remains in the source.</p>
    <a class="card-link" href="{{ '/spatial-recovery/' | relative_url }}">Read the spatial guide <span aria-hidden="true">→</span></a>
  </article>
</div>

## The working method

1. Prepare the source and reference without creative grading.
2. Align them in time and space.
3. Select a small, representative set of trustworthy frame pairs.
4. Build a target that isolates the information being recovered.
5. Train and compare checkpoints on material the model has not seen.
6. Apply the model to the complete source and review the result shot by shot.
7. Keep the original scan, references, settings, and review notes alongside the output.

## Continue

- [Shared workflow]({{ '/start-here/' | relative_url }}): preparation, alignment, dataset selection, and project setup.
- [Chroma recovery]({{ '/chroma-recovery/' | relative_url }}) or [spatial recovery]({{ '/spatial-recovery/' | relative_url }}): build the branch-specific target.
- [Training, inference, and review]({{ '/training-inference-review/' | relative_url }}): the stages shared by both branches.
- [Preparing training pairs]({{ '/automated-dataset-preparation/' | relative_url }}): what makes a pair trustworthy and how difficult references are handled.
- [Case studies]({{ '/case-studies/' | relative_url }}): practical examples across different formats and reference types.
- [Provenance and metadata]({{ '/provenance-metadata/' | relative_url }}): recording how a result was made.
