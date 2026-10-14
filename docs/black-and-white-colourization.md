---
layout: default
title: "Black-and-White Colourization"
nav_order: 5
permalink: /black-and-white-colourization/
---

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

## Status

Fifteen shots from public-domain fiction and non-fiction films, from the 1920s to 1970, are approved or approved with notes. Two things are still open: skin can come out too red on the earliest shots, and foliage in some exteriors still looks artificial. Examples will be added once they are cleared.
