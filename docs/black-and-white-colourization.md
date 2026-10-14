---
layout: default
title: "Black-and-White Colourization"
nav_order: 5
permalink: /black-and-white-colourization/
---

<span class="kicker">Research area 5</span>

# Black-and-white colourization

Adding colour to film shot in black and white. Film does not record brightness the way the eye sees it; it records according to the spectral sensitivity of its stock. The greyscale is therefore a measurement, and the colour has to agree with it.

## Orthochromatic and panchromatic film

- **Orthochromatic** stock is sensitive to blue and green but almost insensitive to red. It was the normal negative until the mid-1920s. Red lips and ruddy skin record dark, blue skies and blue eyes record pale.
- **Panchromatic** stock is sensitive to the whole visible range, but more to blue and less to red than the eye. It became standard for features around 1926–1928, often shot with filters outdoors.

If either is treated as ordinary video brightness, the colour is wrong in predictable places.

## Method

1. **Source.** Public-domain or rights-cleared scans only.
2. **Colour frames for the shot.** Qwen Image Edit 2511 makes a few colour frames from the shot itself, placed on the exact source picture and checked at full size.
3. **Carry them through the shot.** MiniMax H3 with the Fun ControlNet follows the shot's motion and gives a colour donor.
4. **Fit the colour to the film.** For each film, stock weights are chosen (how much red, green and blue the stock recorded), once per film, never per shot. The colour is rebuilt so that the stock would record exactly the greyscale on the film. The whole frame is processed the same way: no masks, no local fixes.
5. **Review.** Full-size crops, frame-to-frame strips, and checks on skin and foliage.

A red dress on orthochromatic film can therefore come out lighter than it appears in the scan. This is correct, because the film did not record its red.

## Examples

One shot per film, from public-domain fiction and non-fiction of the 1920s. The palettes are an interpretation, not historical fact.

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/general-1926-garden-f062-source.jpg' | relative_url }}" alt="The General, garden: the black-and-white original on the left and the colourized result on the right" loading="lazy">
    <img src="{{ '/images_kebab/examples/general-1926-garden-f062-result.jpg' | relative_url }}" alt="The General, garden: the colourized result" loading="lazy">
  </div>
  <figcaption><em>The General</em> (1926, Buster Keaton and Clyde Bruckman): frame 62. <a href="{{ '/records/general-1926-garden/' | relative_url }}">Record</a>.</figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/her-boy-friend-cafe-f062-source.jpg' | relative_url }}" alt="Her Boy Friend, café: the black-and-white original on the left and the colourized result on the right" loading="lazy">
    <img src="{{ '/images_kebab/examples/her-boy-friend-cafe-f062-result.jpg' | relative_url }}" alt="Her Boy Friend, café: the colourized result" loading="lazy">
  </div>
  <figcaption><em>Her Boy Friend</em> (1924, Larry Semon): frame 62. <a href="{{ '/records/her-boy-friend-cafe/' | relative_url }}">Record</a>.</figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/below-the-deadline-parlour-f062-source.jpg' | relative_url }}" alt="Below the Deadline, parlour: the black-and-white original on the left and the colourized result on the right" loading="lazy">
    <img src="{{ '/images_kebab/examples/below-the-deadline-parlour-f062-result.jpg' | relative_url }}" alt="Below the Deadline, parlour: the colourized result" loading="lazy">
  </div>
  <figcaption><em>Below the Deadline</em> (1929): frame 62. <a href="{{ '/records/below-the-deadline-parlour/' | relative_url }}">Record</a>.</figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/racing-fool-couple-f062-source.jpg' | relative_url }}" alt="The Racing Fool, couple: the black-and-white original on the left and the colourized result on the right" loading="lazy">
    <img src="{{ '/images_kebab/examples/racing-fool-couple-f062-result.jpg' | relative_url }}" alt="The Racing Fool, couple: the colourized result" loading="lazy">
  </div>
  <figcaption><em>The Racing Fool</em> (1927), reel 2: frame 62. <a href="{{ '/records/racing-fool-couple/' | relative_url }}">Record</a>.</figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/wildcat-yard-f062-source.jpg' | relative_url }}" alt="The Wildcat, ranch yard: the black-and-white original on the left and the colourized result on the right" loading="lazy">
    <img src="{{ '/images_kebab/examples/wildcat-yard-f062-result.jpg' | relative_url }}" alt="The Wildcat, ranch yard: the colourized result" loading="lazy">
  </div>
  <figcaption><em>The Wildcat</em> (1925), reel 3: frame 62. <a href="{{ '/records/wildcat-yard/' | relative_url }}">Record</a>.</figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/books-manuscript-classroom-f062-source.jpg' | relative_url }}" alt="Books: From Manuscript to Classroom: the black-and-white original on the left and the colourized result on the right" loading="lazy">
    <img src="{{ '/images_kebab/examples/books-manuscript-classroom-f062-result.jpg' | relative_url }}" alt="Books: From Manuscript to Classroom: the colourized result" loading="lazy">
  </div>
  <figcaption><em>Books: From Manuscript to Classroom</em> (late 1920s), non-fiction: frame 62. <a href="{{ '/records/books-manuscript-classroom/' | relative_url }}">Record</a>.</figcaption>
</figure>

<figure class="pair">
  <div class="pair-media" data-compare="Original|Colourized">
    <img src="{{ '/images_kebab/examples/rambles-round-rio-oxcart-f062-source.jpg' | relative_url }}" alt="Rambles 'Round Rio, ox cart: the black-and-white original on the left and the colourized result on the right" loading="lazy">
    <img src="{{ '/images_kebab/examples/rambles-round-rio-oxcart-f062-result.jpg' | relative_url }}" alt="Rambles 'Round Rio, ox cart: the colourized result" loading="lazy">
  </div>
  <figcaption><em>Rambles 'Round Rio</em> (1921), non-fiction: frame 62. <a href="{{ '/records/rambles-round-rio-oxcart/' | relative_url }}">Record</a>.</figcaption>
</figure>

## Status

Two things are still open: skin can come out too red on the earliest shots, and foliage in some exteriors still looks artificial.
