---
layout: default
title: Dirt Removal
nav_order: 3
permalink: /dirt-removal/
---

<p class="eyebrow">Section 3</p>

# Dirt removal

Advanced Dirt Removal is a free Fusion macro for DaVinci Resolve. I made it so that Resolve can be a low-cost option for archival and educational restoration. It builds on Resolve's own Automatic Dirt Removal and adds what I kept missing: a way to protect moving areas, and a way to bring back real picture that the cleaning took away.

## What it does

- **Motion Mask.** Limits repairs to areas with little or no motion, where automatic cleaning is safest.
- **Recovery Brush.** You paint over anything the cleaning shouldn't have removed, and the original comes back.
- **Spanish Dirt Removal.** The opposite: you paint the specific repairs you want.
- **Difference View.** Shows exactly what is being changed, so you can judge it.
- **Two versions.** One for standard video footage (Rec.709 and similar) and one for Cineon log film scans, which converts to linear for the cleaning and back again.

It needs DaVinci Resolve 18 or later. The free version works; Resolve Studio gives better optical flow.

## Get it

- **Windows:** `winget install FabioColor.AdvancedDirtRemoval` (and `winget upgrade FabioColor.AdvancedDirtRemoval` to update).
- **Windows and macOS installers**, and the two `.setting` files for a manual install, are on the [latest release](https://github.com/fabiocolor/Advanced-Dirt-Removal/releases/latest) (v1.1.3).
- **Instructions and source:** [Advanced Dirt Removal on GitHub](https://github.com/fabiocolor/Advanced-Dirt-Removal).
- **Video tutorial:** [watch it on YouTube](https://youtu.be/Gepw0XG0FGw).

