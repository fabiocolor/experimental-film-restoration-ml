---
layout: default
title: Matte Recovery
nav_order: 5
permalink: /matte-recovery/
---

<p class="eyebrow">Section 5</p>

# Matte recovery

Automatic dirt-cleaning filters, like Dry Clean in Phoenix, remove dirt and scratches, but they also remove real picture: a highlight in an eye, a thin wire, a bit of texture. A restorer then paints protection mattes over everything the filter shouldn't have touched, so the original comes back. On a feature film that's thousands of small decisions on every reel.

This research teaches a small model to make most of those decisions, so the restorer reviews and corrects instead of painting everything by hand.

## How it works

1. **Find what the filter changed.** Each frame is compared with its cleaned version, and every connected area that changed becomes one candidate: something the filter removed.
2. **Decide: bring it back, or leave it cleaned.** A small image classifier (a ResNet-18) looks at small full-resolution crops around each candidate: the scan, the cleaned frame, and the frames before and after, so it can tell dirt, which is there for one frame, from picture, which carries on.
3. **Learn from finished work.** The labels come from shots a restorer has already finished. A candidate under their protection stroke means "bring it back"; on a finished shot, a candidate they left alone means "leave it cleaned".
4. **Write it back as mattes.** The candidates the model brings back are turned into ordinary protection strokes inside the restoration project, where the restorer can see, delete or add to them like their own.

## Results so far

These are from finished reels of a 35mm feature, reviewed by the restorers who finished them:

- On one reel, after reviewing about a hundred shots, the restorer estimated that about 95% of the lost picture was recovered by the model.
- On two reels that were reviewed completely, the restorer removed about 5% of the model's picks on one and about 19% on the other, and added the misses by hand.
- Clean beats more recovery. On reels cleaned at full strength, the model brought back too much, including dirt inside moving faces. Raising its threshold to keep the number of picks per frame close to what restorers accepted fixed that, at the cost of more misses for the restorer to add.

## Limits

- Fast movement and faces are where it's most likely to bring back dirt.
- It learns from one restorer's finished decisions, so it inherits their judgment, and it needs their finished shots to start.
- It works inside one restoration system's projects; it isn't a standalone tool.

I showed an early version of this idea at FIAT/IFTA 2026 on a public trailer, in the [AI inside the tools we already use]({{ '/fiat-ifta-2026-companion/' | relative_url }}#inside-existing-tools) section.
