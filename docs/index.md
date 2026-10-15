---
layout: home
title: Home
nav_order: 0
---

<div class="research-hero">
  <h1>Experimental Film Restoration with Machine Learning</h1>
  <p class="hero-lede">Faded colour brought back. Decayed nitrate healed. Films beyond repair rebuilt. The film's own picture stays the record; the models supply only what was lost.</p>
  <div class="hero-buttons">
    <a href="{{ '/research-status/' | relative_url }}" class="btn btn-primary">What is possible now</a>
    <a href="{{ '/downloads/' | relative_url }}" class="btn btn-outline">Run it yourself</a>
  </div>
</div>

<figure class="reveal">
  <video autoplay muted loop playsinline preload="auto" src="{{ '/media/examples/obsession-ballroom-reveal.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/obsession-ballroom-b-source.jpg' | relative_url }}"></video>
  <figcaption><span class="reveal-tag">Reveal</span> <em>Obsession</em> (1976), the ballroom. A trailer faded to solid red, 254 frames of dancing and a moving camera; the colour recovered on the scan's own brightness at 2048 × 1556. <a href="{{ '/records/obsession-ballroom/' | relative_url }}">Record</a></figcaption>
</figure>

<div class="research-intro">
  <p>Independent research into what open machine-learning models can do for film restoration, and how far they can be trusted. The rule is the same in every area: start from the scan, keep its picture, use a model only for what is missing, and write down what the model did. Nothing here is automatic. A restorer approves every result, and every example has a <a href="{{ '/records/' | relative_url }}">record</a> of its source, models, settings and approval.</p>
</div>

## Five research areas

<ol class="areas">
  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/colour-recovery/' | relative_url }}">Faded colour recovery</a></h3>
      <p>The original colour of a faded film, rebuilt from the film itself and carried through whole shots: pans, crowds, dancing, changing light. Every frame keeps the scan's brightness, grain and resolution.</p>
      <a class="area-link" href="{{ '/colour-recovery/' | relative_url }}">Method, five shots and two kits</a>
    </div>
    <figure class="reveal">
      <video autoplay muted loop playsinline preload="metadata" src="{{ '/media/examples/counter-attack-quarry-reveal.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/counter-attack-quarry-b-source.jpg' | relative_url }}"></video>
      <figcaption><span class="reveal-tag">Reveal</span> <em>Counter Attack</em> (1976), the quarry: 681 frames, six sections, one colour. <a href="{{ '/records/counter-attack-quarry/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/temporal-cbcr/' | relative_url }}">Temporal CbCr</a></h3>
      <p>Colour learned from a reference for the shot, a surviving DVD or telecine or a set of approved synthetic frames, and carried through every frame by a small model trained for that shot alone, in minutes.</p>
      <a class="area-link" href="{{ '/temporal-cbcr/' | relative_url }}">Method, examples and the Nuke template</a>
    </div>
    <figure class="reveal">
      <video autoplay muted loop playsinline preload="metadata" src="{{ '/media/examples/candy-candy-reveal.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/candy-candy-b-source.jpg' | relative_url }}"></video>
      <figcaption><span class="reveal-tag">Reveal</span> <em>Candy Candy</em> (1976), a 16mm print faded to pink; the colour learned from a PAL DVD, the detail the print's. <a href="{{ '/records/candy-candy/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/diffusion-healing/' | relative_url }}">Diffusion healing</a></h3>
      <p>Nitrate decay, missing frames, emulsion breaking up. Everything that survives is used first; a video model generates only the missing picture, guided by the movement around it, and every generated pixel is on record.</p>
      <a class="area-link" href="{{ '/diffusion-healing/' | relative_url }}">Method, examples and kit</a>
    </div>
    <figure class="pair">
      <div class="pair-media" data-compare="Nitrate scan|Healed">
        <img src="{{ '/images_kebab/examples/knights-of-the-trail-gap826-source.jpg' | relative_url }}" alt="Knights of the Trail, frame 826 of the nitrate scan: the decay has eaten the middle of the picture, the cowboy at the table half gone" loading="lazy">
        <img src="{{ '/images_kebab/examples/knights-of-the-trail-gap826-result.jpg' | relative_url }}" alt="The healed frame: the cowboy, the table and the cabin wall complete" loading="lazy">
      </div>
      <figcaption><em>Knights of the Trail</em>, nitrate, frame 826: the worst frame of the shot. Drag to compare. Courtesy of the George Eastman Museum. <a href="{{ '/records/knights-of-the-trail/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/diffusion-reconstruction/' | relative_url }}">Diffusion reconstruction</a></h3>
      <p>For films beyond repair, where every frame is damaged. A video model rebuilds the picture from the surviving elements, shot after shot, to one look for the whole reel. The result is labelled for what it is: a reconstruction.</p>
      <a class="area-link" href="{{ '/diffusion-reconstruction/' | relative_url }}">Method, a whole reel and kit</a>
    </div>
    <figure class="reveal">
      <video autoplay muted loop playsinline preload="metadata" src="{{ '/media/examples/el-tinterillo-fg04-reveal.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/el-tinterillo-fg04-b-source.jpg' | relative_url }}"></video>
      <figcaption><span class="reveal-tag">Reveal</span> <em>El Tinterillo</em>, shot FG04: the damaged 16mm print, and the shot rebuilt. <a href="{{ '/records/el-tinterillo-stairs/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/black-and-white-colourization/' | relative_url }}">Black-and-white colourization</a></h3>
      <p>Colour for films shot in black and white, fitted to the stock that recorded them, so that the greys on the film are exactly what that stock would have recorded of the colour. Whole shots, at full resolution, with the picture untouched.</p>
      <a class="area-link" href="{{ '/black-and-white-colourization/' | relative_url }}">Method and public-domain examples</a>
    </div>
    <figure class="reveal">
      <video autoplay muted loop playsinline preload="metadata" src="{{ '/media/examples/the-general-train-reveal.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/the-general-train-b-source.jpg' | relative_url }}"></video>
      <figcaption><span class="reveal-tag">Reveal</span> <em>The General</em> (1926), the locomotive below the pines. <a href="{{ '/records/general-1926-garden/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>
</ol>

<div class="quiet-panel">
  <div>
    <h3>Run it yourself</h3>
    <p>Two single-frame colour-recovery graphs, for an unbalanced and a balanced scan, run in Comfy Cloud with no GPU and no installation. The whole-shot, healing and reconstruction kits run on a local NVIDIA card and reproduce their published examples. Every graph is published laid out with notes, so it can be read node by node, and every kit is checked against the approved result and says how close it gets.</p>
  </div>
  <a href="{{ '/downloads/' | relative_url }}" class="btn btn-primary">Download kits</a>
</div>

## Talks and writing

- [What is possible now]({{ '/research-status/' | relative_url }}): what works, what is still open, what can be reproduced, and what hardware it takes. October 2026.
- [Talks]({{ '/talks/' | relative_url }}): companion pages for FIAT/IFTA 2026 (São Paulo) and SEAPAVAA 2026.
- [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35), *Archiving Conference* 22(1), 2025: the peer-reviewed paper behind the CopyCat workflow.
- [Tools]({{ '/tools/' | relative_url }}) used alongside this research, each in its own repository.
