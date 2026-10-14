---
layout: default
title: "Faded Balancer"
parent: "Tools Used in This Research"
nav_order: 1
permalink: /tools/faded-balancer/
---

# Faded Balancer

A free tool for DaVinci Resolve that balances a faded scan: black becomes black, white becomes white, and the remaining colour is spread back out. It only sets levels, so it doesn't add or remove dye information. It's the usual first step before [faded colour recovery]({{ '/colour-recovery/' | relative_url }}).

<div class="media-grid media-grid-2">
  <figure class="figure">
    <img src="{{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-after.png' | relative_url }}" alt="Faded scan with a strong red cast">
    <figcaption>Before (faded scan)</figcaption>
  </figure>
  <figure class="figure">
    <img src="{{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-before.png' | relative_url }}" alt="The same frame after balancing">
    <figcaption>After (Faded Balancer DCTL)</figcaption>
  </figure>
</div>

## Get it

- [Faded Balancer DCTL](https://github.com/fabiocolor/Faded-Balancer-DCTL) for DaVinci Resolve.
