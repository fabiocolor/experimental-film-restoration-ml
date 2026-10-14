---
layout: default
title: Research Routes & Evidence
parent: "Unbalanced Sources: Open-Weight Routes"
nav_order: 2
permalink: /open-weight-color-recovery/research-routes/
grand_parent: "Faded Colour Recovery"
---


# Open-Weight Colour Recovery: Research Routes

This work is not yet a general-purpose colour-recovery system. It is a set of connected research routes, each tested under different conditions and each carrying different levels of confidence.

The most useful public account is therefore not a list of features. It is a map of what has been demonstrated, what looks promising, and what remains unresolved.

This map is a dated research snapshot rather than a permanent ranking. Routes may be revised, combined, downgraded, or replaced as new experiments are completed and reviewed.

<div class="status-legend" aria-label="Research status key">
  <span class="status status-demonstrated">Demonstrated</span><span>Repeated or completed on a defined test.</span>
  <span class="status status-promising">Promising</span><span>Strong evidence, but still narrow or awaiting broader review.</span>
  <span class="status status-open">Open question</span><span>A necessary route whose general solution has not been shown.</span>
</div>

## Selected experiments, with context

The images below are not a gallery of finished restorations. Each one answers a narrower question. The notes explain what went into the test, what the comparison can support, and what it cannot prove. Film, model, software, and source information is collected on the [Credits & Attribution]({{ '/credits/' | relative_url }}) page.

<article class="experiment-evidence">
  <div class="experiment-evidence-copy">
    <p class="card-kicker">Source preservation</p>
    <h3>Can a model contribute colour without replacing the surviving image?</h3>
    <dl class="experiment-facts">
      <dt>Test</dt>
      <dd>A faded source frame, a soft colour-chart reference, and source-derived edge control were passed to Qwen Image Edit. The model’s direct RGB proposal was then separated from the final source-preserving composite.</dd>
      <dt>What to look for</dt>
      <dd>Read the board from left to right. The source, reference, control, raw proposal, and final composite remain visibly separate, so the generated image cannot be mistaken for the source or for historical evidence.</dd>
      <dt>What it supports</dt>
      <dd>The workflow can return proposed chroma to the source image while retaining the source as the record of luminance, framing, texture, and damage.</dd>
      <dt>Limit</dt>
      <dd>This structure limits the model’s authority; it does not prove that every proposed colour is correct.</dd>
    </dl>
  </div>
  <figure class="experiment-figure">
    <a href="{{ '/images_kebab/seapavaa2026/jug_auditorium_full_lineage_5stage.png' | relative_url }}" target="_blank">
      <img src="{{ '/images_kebab/seapavaa2026/jug_auditorium_full_lineage_5stage.png' | relative_url }}" alt="Five-stage Qwen experiment showing the faded source, soft colour reference, source edge control, raw generated proposal, and final source-preserving composite">
    </a>
    <figcaption><em>Juggernaut</em> (1974), directed by Richard Lester. Five-stage lineage from surviving frame to final composite.</figcaption>
  </figure>
</article>

<article class="experiment-evidence experiment-evidence-reverse">
  <div class="experiment-evidence-copy">
    <p class="card-kicker">No matched reference</p>
    <h3>Can Qwen produce a useful colour candidate when no matching colour frame survives?</h3>
    <dl class="experiment-facts">
      <dt>Test</dt>
      <dd>The <em>Counter Attack</em> garden frame used the faded source, a source-derived edge guide, a soft colour chart, and a restrained restoration prompt. It did not use a matched colour frame from the scene.</dd>
      <dt>What to look for</dt>
      <dd>The split moves from the faded source on the left to the source-luminance composite on the right. Building, trees, crowd, and framing remain tied to the source while the colour interpretation changes.</dd>
      <dt>What it supports</dt>
      <dd>A reference-free still can become a plausible candidate for human review.</dd>
      <dt>Limit</dt>
      <dd>Plausible is not the same as historically verified. The blue sky, green foliage, clothing, and architecture are interpretations unless other evidence confirms them.</dd>
    </dl>
  </div>
  <figure class="experiment-figure">
    <a href="{{ '/images_kebab/seapavaa2026/fanji_c4_row3_garden_split_comparison_fullframe_clean.png' | relative_url }}" target="_blank">
      <img src="{{ '/images_kebab/seapavaa2026/fanji_c4_row3_garden_split_comparison_fullframe_clean.png' | relative_url }}" alt="Split comparison with the faded Counter Attack garden source on the left and the source-preserving colour composite on the right">
    </a>
    <figcaption><em>Counter Attack</em> (1976). Faded source at left; reviewed colour proposal recombined with source luminance at right.</figcaption>
  </figure>
</article>

<article class="experiment-evidence experiment-evidence-wide">
  <div class="experiment-evidence-copy">
    <p class="card-kicker">Temporal colour</p>
    <h3>When does a colour interpretation hold together through time?</h3>
    <p>The same basic idea was tested on two very different shots: use the source sequence and source-derived structure to guide a video-aware colour proposal, then return the proposed chroma to source luminance.</p>
    <p>The comparison matters because a favourable result and a failure can look equally convincing in a single still. Motion exposes whether colour remains attached to the same face, garment, wall, or object.</p>
  </div>
  <div class="experiment-video-grid">
    <figure class="experiment-figure">
      <img src="{{ '/media/seapavaa2026/shot0006-source-proposal-composite.gif' | relative_url }}" alt="Animated source, raw inference, and source-preserving composite comparison for a favourable low-motion shot">
      <figcaption><strong>Favourable shot.</strong> Low-to-moderate motion remains coherent enough to demonstrate that video-aware chroma can work under bounded conditions. Source context is listed in the <a href="{{ '/credits/' | relative_url }}">credits</a>.</figcaption>
    </figure>
    <figure class="experiment-figure">
      <img src="{{ '/media/seapavaa2026/shot0011-source-proposal-composite.gif' | relative_url }}" alt="Animated source, raw inference, and source-preserving composite comparison showing a hard-motion failure">
      <figcaption><strong>Hard-motion failure.</strong> Faster movement and chunked processing expose inconsistent interpretation and temporal breakdown. This is why the method is not presented as a general video solution. Source context is listed in the <a href="{{ '/credits/' | relative_url }}">credits</a>.</figcaption>
    </figure>
  </div>
</article>

<div class="experiment-pair">
  <article class="experiment-note">
    <p class="card-kicker">Semantic failure</p>
    <h3>A plausible image can still be the wrong image</h3>
    <a href="{{ '/images_kebab/seapavaa2026/ben_row2_source_vs_bad_semantic_inference.png' | relative_url }}" target="_blank">
      <img src="{{ '/images_kebab/seapavaa2026/ben_row2_source_vs_bad_semantic_inference.png' | relative_url }}" alt="Faded source compared with a visually polished but semantically incorrect generated image">
    </a>
    <p class="experiment-credit"><em>Ben</em> (1972), directed by Phil Karlson.</p>
    <p>The source is difficult to read, and the model invents a polished wooden structure and a face. The output is visually coherent but no longer describes the photographed scene. This is direct evidence for keeping the source visible and requiring human acceptance.</p>
  </article>
  <article class="experiment-note">
    <p class="card-kicker">High-resolution tiling</p>
    <h3>More local resolution can create a less coherent frame</h3>
    <a href="{{ '/images_kebab/seapavaa2026/reptilicus_beach_tiled_vs_fullframe_raw_inference.png' | relative_url }}" target="_blank">
      <img src="{{ '/images_kebab/seapavaa2026/reptilicus_beach_tiled_vs_fullframe_raw_inference.png' | relative_url }}" alt="Tiled raw Qwen inference with visible colour discontinuities compared with a coherent full-frame inference">
    </a>
    <p class="experiment-credit"><em>Reptilicus</em> (US release 1962), directed by Sidney Pink and Poul Bang.</p>
    <p>The four-tile result at left contains visible boundaries and conflicting local colour decisions. The full-frame result at right is more coherent, although it still remains a generated interpretation. This experiment is evidence against treating tiling as a solved route.</p>
  </article>
</div>

These are selected public examples. The [SEAPAVAA 2026 companion]({{ '/seapavaa-2026-companion/' | relative_url }}) contains the larger comparison set, individual source files, prompts, and presentation media.

## Route 1 · Source-owned luminance, generated chroma

<span class="status status-demonstrated">Demonstrated foundation</span>

The current public workflow and successful temporal tests keep the source responsible for luminance, geometry, texture, and damage. The model contributes chroma. This limits the model’s authority and makes colour errors easier to review, but it does not prevent colour from crossing an edge or attaching to the wrong region.

## Route 2 · Still-frame recovery without a matched reference

<span class="status status-demonstrated">Demonstrated, bounded</span>

Tests using a faded source, source-derived edge control, a softened colour chart, and a restrained prompt have produced useful first-pass candidates without a matched colour frame. These candidates are worth human review, but they are not historically authoritative or consistently correct across subjects.

## Route 3 · One approved same-shot colour anchor

<span class="status status-promising">Promising, strongest reference-driven route</span>

When one frame in a shot has an approved colour interpretation, that frame can act as a restrained palette and material guide for neighbouring source frames. Each new frame still enters as the primary image; the anchor is not allowed to dictate pose, framing, or object layout.

The public [context-board experiment]({{ '/seapavaa-2026-companion/' | relative_url }}#slide-14) demonstrates the anchor idea on a defined sequence. It supports further controlled testing, but it does not establish general success across films, motion types, or restoration aesthetics.

## Route 4 · True paired data and reference-trained chroma recovery

<span class="status status-demonstrated">Demonstrated on paired material</span>

Where real source/reference pairs exist, a compact project-specific model can learn chroma directly rather than asking a general image model to reinterpret every frame.

The published CopyCat case studies demonstrate this route on aligned film elements, while the [Frontier preparation guide]({{ '/automated-dataset-preparation/' | relative_url }}) documents how drifting references were matched and reviewed before training. The evidence supports paired learning as a practical project-specific method; it does not establish one model or setting as a general solution for every film.

## Route 5 · Video-aware chroma generation

<span class="status status-demonstrated">Demonstrated on favourable shots</span>

Wan/VACE-style video models can see a short sequence as a temporal object rather than as unrelated stills. The most successful setup used the source video, hard source-derived edge control, and one recovered middle-frame reference, then returned generated chroma to source luminance.

Two experiments show coherent shot-level chroma on favourable low- or moderate-motion material. Other tests altered faces, clothing, objects, or geometry. On harder motion, temporal coherence sometimes stabilised the wrong interpretation.

## Route 6 · Full-resolution and tiled inference

<span class="status status-open">Open question</span>

High-resolution film scans can exceed the model’s comfortable image-editing range. Tiling can recover local detail, but it introduces seams, inconsistent colour ownership, and different interpretations of the same subject across tiles.

Some tiled tests were useful; others produced reference-content takeover or a scene assembled from incompatible local decisions. Tiling is therefore a research direction, not a recommended default.

The important next step is not simply “more pixels.” It is shared evidence across overlaps, source-bound registration, and a review method that catches tile-to-tile semantic drift.

The central open problem is temporal colour ownership: keeping an evidence-aware interpretation attached to the same face, garment, wall, tree, or object through motion and occlusion without allowing the model to redesign the film. Generated colour remains an interpretation unless historical evidence supports it, and human viewing remains the final acceptance gate.

For the underlying examples, prompts, intermediate files, and presentation media, continue to the [SEAPAVAA 2026 companion]({{ '/seapavaa-2026-companion/' | relative_url }}).

## Downloads

The images on this page, full size:

- [Five-stage Qwen experiment showing the faded source, soft colour reference, source edge control, raw generated proposal, and final source-preserving composite]({{ '/images_kebab/seapavaa2026/jug_auditorium_full_lineage_5stage.png' | relative_url }}) (PNG, 0.4 MB)
- [Animated source, raw inference, and source-preserving composite comparison for a favourable low-motion shot]({{ '/media/seapavaa2026/shot0006-source-proposal-composite.gif' | relative_url }}) (GIF, 1.4 MB)
- [Animated source, raw inference, and source-preserving composite comparison showing a hard-motion failure]({{ '/media/seapavaa2026/shot0011-source-proposal-composite.gif' | relative_url }}) (GIF, 7.1 MB)
- [Faded source compared with a visually polished but semantically incorrect generated image]({{ '/images_kebab/seapavaa2026/ben_row2_source_vs_bad_semantic_inference.png' | relative_url }}) (PNG, 1.1 MB)
- [Tiled raw Qwen inference with visible colour discontinuities compared with a coherent full-frame inference]({{ '/images_kebab/seapavaa2026/reptilicus_beach_tiled_vs_fullframe_raw_inference.png' | relative_url }}) (PNG, 1.3 MB)
- [Counter Attack garden frame: faded source and recovered composite]({{ '/images_kebab/seapavaa2026/fanji_c4_row3_garden_split_comparison_fullframe_clean.png' | relative_url }}) (PNG, 0.9 MB)
