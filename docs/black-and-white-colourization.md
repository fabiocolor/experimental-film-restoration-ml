---
layout: default
title: "Black-and-White Colourization"
nav_order: 5
permalink: /black-and-white-colourization/
---

<span class="kicker">Research area 5</span>

# Black-and-white colourization

Colour for films shot in black and white, whole shots at a time, with the picture untouched. Film does not record brightness the way the eye sees it; it records according to the spectral sensitivity of its stock, so the greyscale is a measurement, and the colour has to agree with it. Here it does: every result is rebuilt so that the stock would have recorded exactly the greys on the film.

<figure class="reveal">
  <video autoplay muted loop playsinline preload="auto" src="{{ '/media/examples/the-general-garden-reveal.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/the-general-garden-b-source.jpg' | relative_url }}"></video>
  <figcaption><span class="reveal-tag">Reveal</span> <em>The General</em> (1926), Annabelle in the garden, 124 frames at full resolution. The source luminance is byte-exact; only the colour was added. <a href="{{ '/records/general-1926-garden/' | relative_url }}">Record</a></figcaption>
</figure>

## Orthochromatic and panchromatic film

- **Orthochromatic** stock is sensitive to blue and green but almost blind to red. It was the normal negative until the mid-1920s: red lips and ruddy skin record dark, blue skies and blue eyes record pale.
- **Panchromatic** stock sees the whole visible range, but more blue and less red than the eye. It became standard for features around 1926–1928, often shot with filters outdoors.

Treat either as ordinary video brightness and the colour comes out wrong in predictable places. A red dress on orthochromatic film can rightly come out lighter than it appears in the scan, because the film did not record its red.

## How it works

1. **Source.** Public-domain or rights-cleared scans only.
2. **Colour frames for the shot.** Qwen Image Edit 2511 makes a few colour frames from the shot itself, placed on the exact source picture and checked at full size.
3. **Carry them through the shot.** MiniMax H3, with the Fun ControlNet where the motion needs it, follows the shot and gives a colour donor for every frame; several anchors across a pan keep it on course.
4. **Fit the colour to the film.** For each film, once, stock weights are chosen (how much red, green and blue the stock recorded), and the colour is rebuilt so that the stock would record exactly the greyscale on the film. The whole frame is processed the same way: no masks, no local fixes.
5. **Review.** Full-size crops, frame-to-frame strips, and checks on skin and foliage, at normal speed.

## Examples

<figure class="pair">
  <span class="pair-labels"><span>Original</span><span>Colourized</span></span>
  <div class="pair-media pair-video">
    <video controls muted playsinline preload="metadata" src="{{ '/media/examples/the-general-train-sbs.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/the-general-train-b-source.jpg' | relative_url }}"></video>
  </div>
  <figcaption><em>The General</em> (1926), the locomotive below the pines, 124 frames with a pan. Three anchors from the same shot, start, middle and end, through H3. Approved 25 September 2026. <a href="{{ '/records/general-1926-garden/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <span class="pair-labels"><span>Original</span><span>Colourized</span></span>
  <div class="pair-media pair-video">
    <video controls muted playsinline preload="metadata" src="{{ '/media/examples/market-street-1906-sbs.mp4' | relative_url }}" poster="{{ '/images_kebab/examples/market-street-1906-b-source.jpg' | relative_url }}"></video>
  </div>
  <figcaption><em>A Trip Down Market Street</em> (1906), 155 frames, the camera on the front of a cable car. The fourth pass, with the colour integrated into the luminance. Approved with notes: the soft source leaves the model less to hold on to, and the colour is not yet of professional grade. <a href="{{ '/records/market-street-1906/' | relative_url }}">Record</a></figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/market-street-1906-a-source.jpg' | relative_url }}" alt="A Trip Down Market Street, 1906: the street from the front of the cable car, in black and white" loading="lazy">
    <img src="{{ '/images_kebab/examples/market-street-1906-a-result.jpg' | relative_url }}" alt="The same frame colourized: brick and ochre buildings, a blue sky, the Ferry Building at the end of the street" loading="lazy">
  </div>
  <figcaption><em>A Trip Down Market Street</em>, near the start of the shot. Drag to compare.</figcaption>
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

## Where it stands

- **Whole shots, full resolution.** Fifteen shots are approved; the picture is never touched, so every result is at the scan's resolution with its grain and its damage.
- **Motion.** A pan with several anchors holds its colour; the next tests are more complex movement and more complex subjects.
- **Open.** Skin can come out too red on the earliest shots, foliage in some exteriors still looks artificial, and a soft source (the 1906 cable-car ride) gives the model less to hold on to. The palettes are interpretations, and every page says so.

## Sources and references

<ul class="refs">
  <li><em>The General</em> (1926, Buster Keaton and Clyde Bruckman): US public domain; the 1926 picture from a copy on <a href="https://archive.org/details/the-general-1926-remux-1080p-dts-hd-ma-51-x264">archive.org</a>.</li>
  <li><em>A Trip Down Market Street</em> (1906, Miles Brothers): US public domain; the film is held by the <a href="https://www.loc.gov/item/00694408">Library of Congress</a>. The record names the copy used.</li>
  <li><em>Her Boy Friend</em> (1924), <em>The Wildcat</em> (1925), <em>The Racing Fool</em> (1927), <em>Below the Deadline</em> (1929), <em>Books: From Manuscript to Classroom</em> (late 1920s), <em>Rambles 'Round Rio</em> (1921): US public domain; each record names its copy.</li>
  <li>Qwen Image Edit 2511, Qwen team, Alibaba (<a href="https://huggingface.co/Qwen/Qwen-Image-Edit-2511">model card</a>); MiniMax H3, MiniMax (<a href="https://huggingface.co/MiniMaxAI/MiniMax-H3">model card</a>); Fun ControlNet for H3, Alibaba PAI (<a href="https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union">model card</a>).</li>
  <li>On the spectral sensitivity of early stocks: Barbara Flueckiger, <a href="https://filmcolors.org/">Timeline of Historical Film Colors</a>, University of Zurich.</li>
</ul>
