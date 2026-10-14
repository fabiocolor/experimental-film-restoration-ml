---
layout: default
title: "Black-and-White Colourization"
nav_order: 5
permalink: /black-and-white-colourization/
---

# Black-and-white colourization

Adding colour to film that was shot in black and white. Black-and-white film doesn't record brightness the way the eye sees it. It records the scene through the spectral sensitivity of its stock, so the greyscale is a measurement, and the colour can be inferred so that it agrees with that measurement.

## Orthochromatic and panchromatic film

- **Orthochromatic** stock sees blue and green but is nearly blind to red. It was the normal negative until the mid-1920s. Red lips and ruddy skin record dark, blue skies and blue eyes record pale.
- **Panchromatic** stock sees the whole visible range, but is still blue-heavy and red-weak compared with the eye. It became standard for features around 1926–1928, often shot with filters outdoors.

Treating either one as ordinary video brightness gets the colour wrong in predictable places.

## The approved route

1. **Source.** Public-domain or rights-cleared scans only.
2. **Colour frames for the shot.** Qwen Image Edit 2511 makes a few colour frames from the shot itself, placed on the exact source picture and checked at full size.
3. **Carry them through the shot.** MiniMax H3 with the Fun ControlNet follows the shot's motion and gives a colour donor.
4. **Fit the colour to the film.** For each film I choose stock weights (how much red, green and blue the stock recorded), once per film, never per shot. The colour is rebuilt so the stock would record exactly the greyscale that's on the film. The whole frame is processed the same way: no masks, no local fixes.
5. **Review.** Full-size crops, frame-to-frame strips, and checks on skin and foliage.

Because the film's record is what's preserved, not video brightness, a red dress on orthochromatic film can come out lighter than it looks in the black-and-white scan. That is the point: the film never recorded its red.

## Where it stands

Fifteen shots from public-domain fiction and non-fiction films, from the 1920s to 1970, are approved or approved with notes. Two things are still open: skin can come out too red on the earliest shots, and foliage in some exteriors still reads as artificial. Examples will be added here once they're cleared for publication.
