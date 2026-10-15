---
layout: default
title: "Black-and-White Colourization"
nav_order: 5
permalink: /black-and-white-colourization/
---

<span class="kicker">Research area 5</span>

# Black-and-white colourization

Colourization is a different thing from the rest of this site: there was never any colour on the film, so everything here is an interpretation, and every page says so. What can be done is to make the interpretation agree with the film. A black-and-white stock doesn't see brightness the way the eye does; it records according to its own spectral sensitivity, so the greys on the film are a measurement, and any colour put on them has to be a colour that stock would have recorded as exactly those greys. Every result here is rebuilt that way, whole shots at a time, with the picture untouched.

<figure class="reveal">
  <video autoplay muted loop playsinline preload="auto" poster="{{ '/images_kebab/examples/the-general-garden-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/the-general-garden-reveal.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/the-general-garden-reveal.mp4' | relative_url }}" type="video/mp4">
    </video>
  <figcaption><span class="reveal-tag">Reveal</span> <em>The General</em> (1926), Annabelle in the garden, 124 frames at full resolution. The picture is untouched; only the colour was added. <a href="{{ '/records/general-1926-garden/' | relative_url }}">Record</a></figcaption>
</figure>

## Orthochromatic and panchromatic film

- **Orthochromatic** stock is sensitive to blue and green but almost blind to red. It was the normal negative until the mid-1920s: red lips and ruddy skin record dark, blue skies and blue eyes record pale.
- **Panchromatic** stock sees the whole visible range, but more blue and less red than the eye. It became standard for features around 1926–1928, often shot with filters outdoors.

Treat either as ordinary video brightness and the colour comes out wrong in predictable places. A red dress on orthochromatic film can rightly come out lighter than it looks in the scan, because the film never recorded its red.

## How it works

Only public-domain or rights-cleared scans are used for this. Qwen Image Edit 2511 makes a few colour frames from the shot itself, on the exact source picture, checked at full size. MiniMax H3, with the Fun ControlNet where the movement needs it, carries them through the shot; on a pan it gets several anchors so it stays on course. Then, once per film, a choice is made of how much red, green and blue the stock recorded, and the colour is rebuilt so that the stock would have recorded exactly the greyscale on the film. The whole frame is processed the same way, no masks, no local fixes. Then review: full-size crops, frame-to-frame strips, skin and foliage at normal speed.

## Examples

<figure class="pair">
  <span class="pair-labels"><span>Original</span><span>Colourized</span></span>
  <div class="pair-media pair-video" data-inspect="the-general-train" data-frames="b">
    <video controls muted playsinline preload="metadata" poster="{{ '/images_kebab/examples/the-general-train-b-source.jpg' | relative_url }}">
      <source src="{{ '/media/examples/the-general-train-sbs.av1.mp4' | relative_url }}" type='video/mp4; codecs="av01.0.08M.08"'>
      <source src="{{ '/media/examples/the-general-train-sbs.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption><em>The General</em> (1926), the locomotive below the pines, 124 frames with a pan. Three anchors from the same shot, start, middle and end, through H3. <a href="{{ '/records/general-1926-garden/' | relative_url }}">Record</a></figcaption>
</figure>

One shot per film from public-domain fiction and non-fiction of the 1920s. The palettes are an interpretation, not historical fact.

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/her-boy-friend-cafe-f062-source.jpg' | relative_url }}" alt="Her Boy Friend, café: the black-and-white original" loading="lazy">
    <img src="{{ '/images_kebab/examples/her-boy-friend-cafe-f062-result.jpg' | relative_url }}" alt="Her Boy Friend, café: the colourized result" loading="lazy">
  </div>
  <figcaption><em>Her Boy Friend</em> (1924, Larry Semon), frame 62. <a href="{{ '/records/her-boy-friend-cafe/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/below-the-deadline-parlour-f062-source.jpg' | relative_url }}" alt="Below the Deadline, parlour: the black-and-white original" loading="lazy">
    <img src="{{ '/images_kebab/examples/below-the-deadline-parlour-f062-result.jpg' | relative_url }}" alt="Below the Deadline, parlour: the colourized result" loading="lazy">
  </div>
  <figcaption><em>Below the Deadline</em> (1929), frame 62. <a href="{{ '/records/below-the-deadline-parlour/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/racing-fool-couple-f062-source.jpg' | relative_url }}" alt="The Racing Fool, couple: the black-and-white original" loading="lazy">
    <img src="{{ '/images_kebab/examples/racing-fool-couple-f062-result.jpg' | relative_url }}" alt="The Racing Fool, couple: the colourized result" loading="lazy">
  </div>
  <figcaption><em>The Racing Fool</em> (1927), reel 2, frame 62. <a href="{{ '/records/racing-fool-couple/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/wildcat-yard-f062-source.jpg' | relative_url }}" alt="The Wildcat, ranch yard: the black-and-white original" loading="lazy">
    <img src="{{ '/images_kebab/examples/wildcat-yard-f062-result.jpg' | relative_url }}" alt="The Wildcat, ranch yard: the colourized result" loading="lazy">
  </div>
  <figcaption><em>The Wildcat</em> (1925), reel 3, frame 62. <a href="{{ '/records/wildcat-yard/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/books-manuscript-classroom-f062-source.jpg' | relative_url }}" alt="Books: From Manuscript to Classroom: the black-and-white original" loading="lazy">
    <img src="{{ '/images_kebab/examples/books-manuscript-classroom-f062-result.jpg' | relative_url }}" alt="Books: From Manuscript to Classroom: the colourized result" loading="lazy">
  </div>
  <figcaption><em>Books: From Manuscript to Classroom</em> (late 1920s), non-fiction, frame 62. <a href="{{ '/records/books-manuscript-classroom/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/rambles-round-rio-oxcart-f062-source.jpg' | relative_url }}" alt="Rambles 'Round Rio, ox cart: the black-and-white original" loading="lazy">
    <img src="{{ '/images_kebab/examples/rambles-round-rio-oxcart-f062-result.jpg' | relative_url }}" alt="Rambles 'Round Rio, ox cart: the colourized result" loading="lazy">
  </div>
  <figcaption><em>Rambles 'Round Rio</em> (1921), non-fiction, frame 62. <a href="{{ '/records/rambles-round-rio-oxcart/' | relative_url }}">Record</a></figcaption>
</figure>

## What works and what doesn't

Fifteen shots are finished, whole shots at the scan's resolution with its grain and its damage, because the picture is never touched. A pan with several anchors holds its colour. The next tests are more complex movement and more complex subjects.

Skin can come out too red on the earliest shots, foliage in some exteriors still looks artificial, and a soft, low-detail source gives the model too little to hold on to. The route is not published yet; the examples are here, and the graphs follow once the stock models are settled.

## Sources and references

<ul class="refs">
  <li><em>The General</em> (1926, Buster Keaton and Clyde Bruckman): US public domain; the 1926 picture from a copy on <a href="https://archive.org/details/the-general-1926-remux-1080p-dts-hd-ma-51-x264">archive.org</a>.</li>
  <li><em>Her Boy Friend</em> (1924), <em>The Wildcat</em> (1925), <em>The Racing Fool</em> (1927), <em>Below the Deadline</em> (1929), <em>Books: From Manuscript to Classroom</em> (late 1920s), <em>Rambles 'Round Rio</em> (1921): US public domain; each record names its copy.</li>
  <li>Qwen Image Edit 2511, Qwen team, Alibaba (<a href="https://huggingface.co/Qwen/Qwen-Image-Edit-2511">model card</a>); MiniMax H3, MiniMax (<a href="https://huggingface.co/MiniMaxAI/MiniMax-H3">model card</a>); Fun ControlNet for H3, Alibaba PAI (<a href="https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union">model card</a>).</li>
  <li>On the spectral sensitivity of early stocks: Barbara Flueckiger, <a href="https://filmcolors.org/">Timeline of Historical Film Colors</a>, University of Zurich.</li>
</ul>
