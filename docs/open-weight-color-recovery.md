---
layout: default
title: "Unbalanced Sources: Open-Weight Routes"
nav_order: 2
has_children: true
permalink: /open-weight-color-recovery/
parent: "Faded Colour Recovery"
---


# Open-Weight Colour Recovery

Open-weight image models create a new possibility for faded-film restoration: they can propose plausible colour even when no perfectly matching reference survives. This research studies how to use that ability without allowing the model to replace the photographic identity of the source.

Qwen Image Edit is the current focus because it can respond to the source frame, visual references, and written direction in one workflow. The model is not treated as an oracle. It is treated as one instrument in a larger restoration process.

<div class="hero-buttons">
  <a href="{{ '/open-weight-color-recovery/research-routes/' | relative_url }}" class="btn btn-outline">See what works and what remains open</a>
</div>

> **Current status:** this is active research, not a finished archival system or a fixed recipe. The dated [research route map]({{ '/open-weight-color-recovery/research-routes/' | relative_url }}) records what has been demonstrated, what remains bounded, and what is still unresolved.

## The central idea

The source frame should remain authoritative for:

- composition and framing;
- faces, bodies, objects, and silhouettes;
- luminance, texture, grain, softness, and damage;
- edge placement and local detail.

The model is asked to contribute colour information. Its proposal can be guided by a matched reference frame, a broader visual atlas, period evidence, a colour chart, or a carefully written description. The proposal is then recombined with the source so that original luminance and fine structure are retained.

<div class="method-flow" role="list" aria-label="Open-weight colour recovery method">
  <div role="listitem"><span>01</span><strong>Prepare</strong><p>Balance the faded scan without inventing a creative look.</p></div>
  <div role="listitem"><span>02</span><strong>Guide</strong><p>Choose the strongest available colour evidence and state its limits.</p></div>
  <div role="listitem"><span>03</span><strong>Generate</strong><p>Ask Qwen Image Edit for a source-faithful colour proposal.</p></div>
  <div role="listitem"><span>04</span><strong>Recombine</strong><p>Return to the original luminance, geometry, and texture.</p></div>
  <div role="listitem"><span>05</span><strong>Review</strong><p>Compare alternatives across frames and record uncertainty.</p></div>
</div>

<div class="link-grid">
  <a href="{{ '/open-weight-color-recovery/research-routes/' | relative_url }}"><strong>Research routes and evidence</strong><span>A plain-language account of demonstrated, promising, and unresolved approaches.</span></a>
  <a href="{{ '/seapavaa-2026-companion/' | relative_url }}"><strong>SEAPAVAA 2026 companion</strong><span>The examples from my June 2026 talk, kept as a dated archive.</span></a>
</div>

Every published experiment separates the surviving source, the evidence supplied to the model, the raw proposal, and the final composite. When historical colour is unknown, the result is described as proposed or interpreted, not as verified original colour.
