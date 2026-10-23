---
layout: home
title: Home
nav_order: 0
---

<div class="research-hero">
  <h1>Experimental Film Restoration with Machine Learning</h1>
  <p class="hero-lede">Faded colour brought back, decayed nitrate healed, films beyond repair rebuilt, with open-weight models running on local hardware. The film's own picture stays the record; the model only supplies what is lost.</p>
  <div class="hero-buttons">
    <a href="{{ '/research-status/' | relative_url }}" class="btn btn-primary">Where things stand</a>
    <a href="{{ '/downloads/' | relative_url }}" class="btn btn-outline">Run it yourself</a>
  </div>
</div>

<figure class="reveal">
  <video autoplay muted loop playsinline preload="auto" poster="{{ '/images_kebab/examples/obsession-ballroom-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/obsession-ballroom-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/obsession-ballroom-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
  <figcaption><span class="reveal-tag">Reveal</span> <em>Obsession</em> (1976), the ballroom. A trailer faded to solid red, 254 frames of dancing and a moving camera; the colour recovered on the scan's own brightness at 2048 × 1556. <a href="{{ '/records/obsession-ballroom/' | relative_url }}">Record</a></figcaption>
</figure>

<div class="research-intro">
  <p>Independent research by <a href="{{ '/credits/' | relative_url }}">Fabio Bedoya</a>, done alongside commercial restoration work in London, into what open-weight AI models can do for the archives that can't afford the commercial route, and how far those models can be trusted. If you think about it, digital restoration was never really about recovery. The usual tools copy information from the frames around the damage and mask it. These models can put back what was actually lost, and that is new. It is also where the risk is, so the rule is the same in every area here: start from the scan, keep its picture, use a model only for what is missing, and write down what the model did. Nothing is automatic. Every result is reviewed at full size before it goes up, and every example has a <a href="{{ '/records/' | relative_url }}">record</a> of its source, models and settings.</p>
</div>

## Six research areas

<ol class="areas">
  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/colour-recovery/' | relative_url }}">Faded colour recovery</a></h3>
      <p>When the faded scan is all that survives. The colour is rebuilt from the film itself and carried through whole shots, pans, crowds, dancing and all, while every frame keeps the scan's own brightness, grain and resolution.</p>
      <a class="area-link" href="{{ '/colour-recovery/' | relative_url }}">How it works, five shots and two kits</a>
    </div>
    <figure class="reveal">
      <video data-autoplay muted loop playsinline preload="none" poster="{{ '/images_kebab/examples/counter-attack-quarry-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/counter-attack-quarry-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/counter-attack-quarry-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
      <figcaption><span class="reveal-tag">Reveal</span> <em>Counter Attack</em> (1976), the quarry: 681 frames, six sections, one colour. <a href="{{ '/records/counter-attack-quarry/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/temporal-cbcr/' | relative_url }}">Temporal CbCr</a></h3>
      <p>When something with the colour still survives: a DVD, a telecine, an overlapping negative, or a set of reviewed frames. A small model learns the colour of that one shot in about 90 seconds and carries it through every frame.</p>
      <a class="area-link" href="{{ '/temporal-cbcr/' | relative_url }}">How it works, examples and the Nuke template</a>
    </div>
    <figure class="reveal">
      <video data-autoplay muted loop playsinline preload="none" poster="{{ '/images_kebab/examples/candy-candy-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/candy-candy-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/candy-candy-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
      <figcaption><span class="reveal-tag">Reveal</span> <em>Candy Candy</em> (1976), a 16mm print faded to pink; the colour learned from a PAL DVD, the detail the print's. <a href="{{ '/records/candy-candy/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/diffusion-healing/' | relative_url }}">Diffusion healing</a></h3>
      <p>Nitrate decay, a gap of fifteen frames, emulsion breaking up. Far beyond what Phoenix or DIAMANT can interpolate. Everything that survives is used first, a video model generates only the missing picture, and every generated pixel is on record.</p>
      <a class="area-link" href="{{ '/diffusion-healing/' | relative_url }}">How it works, examples and kit</a>
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
      <h3><a href="{{ '/diffusion-full-reconstruction/' | relative_url }}">Diffusion reconstruction</a></h3>
      <p>For films where every frame is damaged and normal tools have nothing clean to borrow from. A video model rebuilds the picture from what survives, shot after shot, to one look for the whole reel. The result is called what it is: a reconstruction, with a synthetic quality the film never had.</p>
      <a class="area-link" href="{{ '/diffusion-full-reconstruction/' | relative_url }}">How it works, a whole reel and kit</a>
    </div>
    <figure class="reveal">
      <video data-autoplay muted loop playsinline preload="none" poster="{{ '/images_kebab/examples/el-tinterillo-fg04-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/el-tinterillo-fg04-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/el-tinterillo-fg04-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
      <figcaption><span class="reveal-tag">Reveal</span> <em>El Tinterillo</em>, shot FG04: the damaged 16mm print, and the shot rebuilt. <a href="{{ '/records/el-tinterillo-stairs/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>

  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/black-and-white-colourization/' | relative_url }}">Black-and-white colourization</a></h3>
      <p>Colour for films shot in black and white, fitted to the stock that recorded them, so that the greys on the film are exactly what that stock would have seen of the colour. Whole shots, full resolution, the picture untouched. The palettes are an interpretation, and every page says so.</p>
      <a class="area-link" href="{{ '/black-and-white-colourization/' | relative_url }}">How it works, and public-domain examples</a>
    </div>
    <figure class="reveal">
      <video data-autoplay muted loop playsinline preload="none" poster="{{ '/images_kebab/examples/the-general-train-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/the-general-train-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/the-general-train-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
      <figcaption><span class="reveal-tag">Reveal</span> <em>The General</em> (1926), the locomotive below the pines. <a href="{{ '/records/general-1926-garden/' | relative_url }}">Record</a></figcaption>
    </figure>
  </li>
  <li class="area">
    <div class="area-copy">
      <h3><a href="{{ '/diffusion-upscaling/' | relative_url }}">Diffusion Upscaling</a></h3>
      <p>A separate research idea for reference-based video resolution/detail enhancement. No workflow or result has been qualified for this new project.</p>
      <a class="area-link" href="{{ '/diffusion-upscaling/' | relative_url }}">Scope and evidence state</a>
    </div>
  </li>
</ol>

<div class="quiet-panel">
  <div>
    <h3>Run it yourself</h3>
    <p>Not everyone has a room full of GPUs, so the two single-frame colour graphs run in Comfy Cloud with no card and no installation. The whole-shot, healing and reconstruction kits need a local NVIDIA card. Every graph is published laid out with notes, so you can read it node by node and see what each step is supposed to do, and every kit is checked against the published result and says how close it gets.</p>
  </div>
  <a href="{{ '/downloads/' | relative_url }}" class="btn btn-primary">Download kits</a>
</div>

## Talks and writing

- [Where things stand]({{ '/research-status/' | relative_url }}): what works, what doesn't yet, what can be reproduced, and what it costs in hardware and time. October 2026.
- [Talks]({{ '/talks/' | relative_url }}): companion pages for FIAT/IFTA 2026 (São Paulo) and SEAPAVAA 2026.
- [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35), *Archiving Conference* 22(1), 2025: the peer-reviewed paper behind the CopyCat workflow.
- [Tools]({{ '/tools/' | relative_url }}) used alongside this research, each in its own repository.
