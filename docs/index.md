---
layout: home
title: Home
nav_order: 0
---

<div class="research-hero">
  <h1>Experimental Film Restoration with Machine Learning</h1>
  <p class="hero-lede">What survives in the film is evidence and is kept. The models fill only what was lost: faded colour, missing frames, lost picture.</p>
  <div class="hero-buttons">
    <a href="{{ '/research-status/' | relative_url }}" class="btn btn-primary">Where the research stands</a>
    <a href="{{ '/downloads/' | relative_url }}" class="btn btn-outline">Download kits</a>
  </div>
</div>

<div class="stage-strip" aria-label="How a frame is recovered: source, model output, composite">
  <figure>
    <img src="{{ '/images_kebab/examples/reptilicus-beach-f025-source.jpg' | relative_url }}" alt="Faded frame from the Reptilicus trailer: the beach, a woman at the left, everything shifted to magenta">
    <figcaption><strong>1 · Source</strong>The faded frame, as scanned. It stays the record.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/examples/reptilicus-beach-f025-model.jpg' | relative_url }}" alt="What Qwen Image Edit returns for the same frame: a colour proposal at the model's lower resolution">
    <figcaption><strong>2 · Model output</strong>A colour proposal, at the model's own, lower resolution.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/examples/reptilicus-beach-f025-result.jpg' | relative_url }}" alt="The final composite: the proposed colour on the scan's own brightness, grain and detail">
    <figcaption><strong>3 · Composite</strong>The proposed colour on the scan's own brightness, grain and detail.</figcaption>
  </figure>
</div>

<p class="experiment-credit"><em>Reptilicus</em> (1961) trailer, frame 25, single-frame route of June 2026 (<a href="{{ '/records/reptilicus-beach/' | relative_url }}">record</a>). From a 35mm trailer reel scan posted publicly on <a href="https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps">archive.org</a>; the trailer belongs to its rights holders.</p>

<div class="research-intro">
  <p>Independent research on machine learning for film restoration. Each area addresses a different kind of loss with the same rule: start from the scan, keep its picture, and use a model only for what is missing. Nothing here is automatic. A restorer decides what is acceptable, and every published example has a <a href="{{ '/records/' | relative_url }}">record</a> of its source, models, settings and approval.</p>
</div>

## Five research areas

<ol class="areas">
  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/colour-recovery/' | relative_url }}">Faded colour recovery</a></h3>
      <p>The original colour of faded film, from balanced or unbalanced scans. Colour that survives is kept; only the lost dye is filled in, and every frame keeps the scan's brightness.</p>
      <a class="area-link" href="{{ '/colour-recovery/' | relative_url }}">Method, examples and two kits</a>
    </div>
    <figure class="pair">
      <div class="pair-media" data-compare="Faded source|Recovered">
        <img src="{{ '/images_kebab/examples/counter-attack-crowd-f040-source.jpg' | relative_url }}" alt="Counter Attack, crowd shot, faded to red: the surviving film copy" loading="lazy">
        <img src="{{ '/images_kebab/examples/counter-attack-crowd-f040-result.jpg' | relative_url }}" alt="The same frame with the recovered colour: blue jackets, white shirts, a grey sky" loading="lazy">
      </div>
      <figcaption><em>Counter Attack</em> (1976), crowd shot, frame 40 of the 308-frame proxy. MiniMax H3 with the Fun ControlNet, finished with the Temporal CbCr adapter. <a href="{{ '/records/counter-attack-crowd/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/temporal-cbcr/' | relative_url }}">Temporal CbCr</a></h3>
      <p>Colour learned from a reference for the shot, historical or synthetic, and carried through every frame by a small model trained for that shot alone. Includes the CopyCat workflow for Nuke.</p>
      <a class="area-link" href="{{ '/temporal-cbcr/' | relative_url }}">Method, examples and the Nuke template</a>
    </div>
    <figure class="pair">
      <div class="pair-media" data-compare="Faded source|Adapter">
        <img src="{{ '/images_kebab/examples/unman-wittering-zigo-choir-f120-source.jpg' | relative_url }}" alt="Unman, Wittering and Zigo, choir: the faded trailer frame, red throughout" loading="lazy">
        <img src="{{ '/images_kebab/examples/unman-wittering-zigo-choir-f120-result.jpg' | relative_url }}" alt="The same frame coloured by the Temporal CbCr adapter: blue cassocks, white ruffs, stained glass" loading="lazy">
      </div>
      <figcaption><em>Unman, Wittering and Zigo</em> (1971), choir, frame 120 of 164. A synthetic reference: 101 approved frames taught the adapter, which coloured the rest. <a href="{{ '/records/unman-wittering-zigo-choir/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/diffusion-healing/' | relative_url }}">Diffusion healing</a></h3>
      <p>Damage across the frame, or missing frames, where most of the original survives. Every surviving element is used first; a video model fills only what is gone, and the generated picture is labelled.</p>
      <a class="area-link" href="{{ '/diffusion-healing/' | relative_url }}">Method, example and kit</a>
    </div>
    <figure class="pair">
      <div class="pair-media" data-compare="Scan|Healed">
        <img src="{{ '/images_kebab/examples/wong-flute-players-f095-source.jpg' | relative_url }}" alt="Wong flute players, frame 95: the 16mm scan, faded to magenta, the emulsion broken up across the picture" loading="lazy">
        <img src="{{ '/images_kebab/examples/wong-flute-players-f095-result.jpg' | relative_url }}" alt="The healed frame: the players and the drummer intact, in colour" loading="lazy">
      </div>
      <figcaption>Wong flute players, 16mm colour reversal, frame 95 of 183. MiniMax H3 from one storyboard sheet, the film's own drumming, one Wan VACE pass. <a href="{{ '/records/wong-flute-players/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/diffusion-reconstruction/' | relative_url }}">Diffusion reconstruction</a></h3>
      <p>For films beyond repair, where every frame is too damaged for restoration. A video model rebuilds the picture from the surviving elements. Some of the detail is synthetic and is said to be.</p>
      <a class="area-link" href="{{ '/diffusion-reconstruction/' | relative_url }}">Method, example and kit</a>
    </div>
    <figure class="pair">
      <div class="pair-media" data-compare="Hybrid|Reconstruction">
        <img src="{{ '/images_kebab/examples/el-tinterillo-stairs-w3-f060-source.jpg' | relative_url }}" alt="El Tinterillo, stairs, frame 442: the hybrid of the damaged 16mm print and the telecine" loading="lazy">
        <img src="{{ '/images_kebab/examples/el-tinterillo-stairs-w3-f060-result.jpg' | relative_url }}" alt="The reconstructed frame: the banister, the figure and the wall rebuilt by the video model" loading="lazy">
      </div>
      <figcaption><em>El Tinterillo</em>, stairs, frame 442 (window w3). The median-cleaned hybrid of the 16mm print and the telecine, rebuilt by MiniMax H3 from a synthetic reference. <a href="{{ '/records/el-tinterillo-stairs/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/black-and-white-colourization/' | relative_url }}">Black-and-white colourization</a></h3>
      <p>Colour for orthochromatic and panchromatic film, inferred from the recorded greyscale and the stock's spectral response, so that the stock would have recorded exactly the greys on the film.</p>
      <a class="area-link" href="{{ '/black-and-white-colourization/' | relative_url }}">Method and seven public-domain examples</a>
    </div>
    <figure class="pair">
      <div class="pair-media" data-compare="Original|Colourized">
        <img src="{{ '/images_kebab/examples/rambles-round-rio-oxcart-f062-source.jpg' | relative_url }}" alt="Rambles 'Round Rio, ox cart: the black-and-white original" loading="lazy">
        <img src="{{ '/images_kebab/examples/rambles-round-rio-oxcart-f062-result.jpg' | relative_url }}" alt="The same frame colourized through the stock model: red earth, green hillside, white oxen" loading="lazy">
      </div>
      <figcaption><em>Rambles 'Round Rio</em> (1921), ox cart, frame 62. Panchromatic stock read through its spectral response. <a href="{{ '/records/rambles-round-rio-oxcart/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>
</ol>

<div class="quiet-panel">
  <div>
    <h3>Try it</h3>
    <p>Two colour-recovery kits run in ComfyUI, on your own GPU or in Comfy Cloud: one for a single faded frame, one for a balanced shot. The healing and reconstruction kits reproduce their published examples. Each is checked against the approved result.</p>
  </div>
  <a href="{{ '/downloads/' | relative_url }}" class="btn btn-primary">Download kits</a>
</div>

## Talks and writing

- [Where the research stands]({{ '/research-status/' | relative_url }}): what works, what does not yet, what can be reproduced, and what hardware it takes. October 2026.
- [Talks]({{ '/talks/' | relative_url }}): companion pages for FIAT/IFTA 2026 (São Paulo) and SEAPAVAA 2026.
- [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35), *Archiving Conference* 22(1), 2025: the peer-reviewed paper behind the CopyCat workflow.
- [Tools]({{ '/tools/' | relative_url }}) used alongside this research, each in its own repository.
