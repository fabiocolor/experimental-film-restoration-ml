---
layout: default
title: Additional Resources
parent: Resources
nav_order: 1
---

# Additional Resources

These notes support the workflow without being workflow steps themselves. Use them as background when planning scans, diagnosing faded material, or documenting restoration choices.

## Video Walkthrough: Nuke Chroma Recovery {#video-walkthrough-nuke-chroma-recovery}

The public YouTube walkthrough is a visual companion to the repository. It belongs here as supporting material: a quick way to see the chroma-recovery idea in motion before reading the step-by-step workflow.

<figure class="figure">
  <a href="https://youtu.be/kXerjFGX9Kg" target="_blank" rel="noopener">
    <img src="{{ '/images_kebab/video_previews/color-recovery-video-preview.gif' | relative_url }}" alt="Animated preview of the Nuke chroma recovery YouTube walkthrough">
  </a>
  <figcaption>Source video: <a href="https://youtu.be/kXerjFGX9Kg" target="_blank" rel="noopener">Nuke Chroma Recovery: Rebuilding Faded Film Color with CopyCat</a>.</figcaption>
</figure>

## Digitization: First Scan, Last Chance {#digitization-first-scan-last-chance}

Digitization is the preservation handoff where the image content is separated from a fragile physical container. Treat the scan as the foundation for every later restoration step, not as a quick transfer or a baked creative grade. For damaged or rare materials, the first scan may also be the only practical scan: the film may not survive repeated handling, the budget may not allow a second pass, or decay may advance before another attempt is possible.

<figure class="figure">
  <a href="https://fabiocolor.substack.com/p/first-scan-last-chance" target="_blank" rel="noopener">
    <img src="{{ '/images_kebab/digitization/first-scan-last-chance-hero.png' | relative_url }}" alt="First Scan, Last Chance article hero image">
  </a>
  <figcaption>Article image from <a href="https://fabiocolor.substack.com/p/first-scan-last-chance" target="_blank" rel="noopener">"First Scan, Last Chance"</a>: digitization as the moment where content is separated from a fragile film container.</figcaption>
</figure>

The goal is to capture the maximum recoverable information in RGB and luminance. A good scan should preserve the film's dynamic range, color-channel separation, density variation, grain, and texture so later tools can make informed decisions. A poor scan can permanently remove evidence: clipped highlights, crushed shadows, bad white balance, automatic exposure decisions, or channel clipping cannot reliably be reconstructed downstream.

<div class="media-grid media-grid-2">
  <figure class="figure">
    <a href="https://fabiocolor.substack.com/p/first-scan-last-chance" target="_blank" rel="noopener">
      <img src="{{ '/images_kebab/digitization/first-scan-last-chance-scanner-color-controls.png' | relative_url }}" alt="Article excerpt about adjusting scanner color controls">
    </a>
    <figcaption>Scanner exposure and RGB controls affect how much useful image information is captured before restoration begins.</figcaption>
  </figure>
  <figure class="figure">
    <a href="https://fabiocolor.substack.com/p/first-scan-last-chance" target="_blank" rel="noopener">
      <img src="{{ '/images_kebab/digitization/first-scan-last-chance-color-systems-review.png' | relative_url }}" alt="Color systems for motion picture film digitization article screenshot">
    </a>
    <figcaption>Digitization choices should be tested against the film element and preservation goal, not treated as a fixed one-size-fits-all color path.</figcaption>
  </figure>
</div>

**Scanning principles:**

- Capture a preservation-grade digital surrogate before restoration decisions are baked in.
- Avoid highlight clipping, shadow crushing, automatic white balance, heavy noise reduction, sharpening, or creative LUTs during capture.
- Monitor RGB parade, waveform, histogram, and channel clipping during setup and final capture.
- Run a preliminary assessment pass to find the sequence's tonal extremes, density shifts, splice flashes, severe fading, and any scanner settings likely to fail.
- Record scanner model, gate, optics, resolution, bit depth, color encoding, transforms, exposure settings, and any wet-gate or cleanup choices.
- Preserve the raw scan or archival master separately from restoration renders, review proxies, and creative grades.

| Risk during digitization | Why it matters later |
| --- | --- |
| Clipped highlights or channels | Removes image information permanently and weakens color recovery, deflicker, dust removal, and grading. |
| Incorrect white point | Adds a false color relationship that restoration tools may learn or amplify. |
| Automatic scanner decisions | Can vary shot to shot, causing artificial flicker, unstable density, or inconsistent channel balance. |
| Baked creative grade | Narrows the evidence available for future restoration or alternate interpretation. |
| Low bit depth / compressed delivery format | Reduces subtle density and chroma information needed for restoration, especially in faded material. |

For historical or deteriorated material, prefer a conservative high-bit-depth scan that keeps the system's captured information intact, then make restoration choices in a controlled post-production workflow. ADX, Cineon, linear, ACES, and display-referred workflows can all be useful in the right context, but they should be tested against the specific film element rather than assumed correct. For this chroma-recovery method, the key rule is continuity: whatever scan and transform path is chosen, Source and Reference must be carried into training with matching, documented transforms.

Digitization, restoration, and remastering are related but distinct. Digitization captures the analog film as data. Restoration addresses damage or loss introduced by the physical container. Remastering may adapt the work for a new display, release, or audience. Keep those boundaries visible in metadata so future users know which decisions came from the object, the restoration process, or the delivery master.

Source article and images: [First Scan, Last Chance: The Critical Role of Digitization in Preserving Film Heritage](https://fabiocolor.substack.com/p/first-scan-last-chance).

## Why Faded Scans Turn Magenta {#why-faded-scans-turn-magenta}

Color film records the image through subtractive dye layers. When the surviving density is no longer balanced, the scan no longer carries even RGB information. A common failure is a pink/magenta cast: cyan and yellow densities weaken against the remaining dye, so red and blue dominate while the green channel loses useful chromatic separation.

For this workflow, the point is practical more than aesthetic: the magenta image often still preserves usable luma, texture, and grain, but its chroma channels are biased, compressed, or partly clipped. A neutral pre-balance gives `CopyCat` a cleaner input distribution before introducing chroma from the reference.

<div class="media-grid media-grid-2">
  <figure class="figure">
    <img src="{{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-after.png' | relative_url }}" alt="Faded live-action scan with strong red/magenta bias">
    <figcaption>Faded scan with a strong red/magenta bias.</figcaption>
  </figure>
  <figure class="figure">
    <img src="{{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-before.png' | relative_url }}" alt="Live-action scan after technical rebalance">
    <figcaption>Technical red compression/rebalance to prepare a cleaner input before ML training.</figcaption>
  </figure>
</div>

<figure class="figure">
  <img src="{{ '/images_kebab/candy-candy/candy-candy-resolve-dctl-parade-scope-faded-film.png' | relative_url }}" alt="Resolve parade scope showing channel imbalance in faded film">
  <figcaption>Resolve parade scope and Faded Balancer controls showing channel imbalance in faded film. The goal is a technical pre-balance, not a final creative grade.</figcaption>
</figure>

<div class="media-grid media-grid-2">
  <figure class="figure">
    <img src="{{ '/images_kebab/candy-candy/candy-candy-faded-balancer-raw.png' | relative_url }}" alt="Faded Candy Candy scan before DCTL correction">
    <figcaption>The faded scan in Resolve, before balancing.</figcaption>
  </figure>
  <figure class="figure">
    <img src="{{ '/images_kebab/candy-candy/candy-candy-faded-balancer-finished.png' | relative_url }}" alt="Balanced Candy Candy scan after DCTL correction">
    <figcaption>The same scan after balancing with the Faded Balancer DCTL.</figcaption>
  </figure>
</div>

### Technical Data For The Investigation

**What is failing:** In chromogenic materials, the final image is formed by superimposed cyan, magenta, and yellow dye clouds in gelatin layers. These organic dyes do not age at the same rate. When cyan and yellow density fade faster than magenta, the visual balance shifts toward pink, purple, or magenta. NARA's inspection guidance describes this diagnosis directly: magenta film has experienced color fading because the cyan and yellow dye layers have weakened, leaving magenta dominant. The NFPF describes the same pattern for modern color motion picture films: spontaneous chemical changes in image dyes, often with a purplish cast caused by rapid cyan and yellow dye fading.

**Why it happened:** The root cause is not a bad scan or a bad grade, though either can make the symptom more visible. It is accumulated chemical deterioration: broken molecular bonds in image dyes, unequal dye stability, heat, humidity, light exposure, time, and storage history. Graphics Atlas notes that chromogenic dye fading can happen in both light exposure and dark storage; cyan dye fade in dark storage can leave the image overall magenta. Older chromogenic stocks and prints, especially mid-century materials before later stability improvements, are more vulnerable than modern stocks.

**Why ordinary grading is limited:** An RGB grade can rebalance channels globally, but it cannot recreate chroma that is absent or compressed into contaminated channel relationships. Recent digital unfading research frames this as a reconstruction problem constrained by residual dye information, scan quality, and available references. Severe cases need informed inference: direct references, constructed references, spectral/density analysis, documented memory color, or supervised learning.

**Data worth capturing before restoration:**

| Data | Why it helps |
| --- | --- |
| Stock, generation, and approximate date | Establishes dye-stability risk and likely chromogenic process. |
| Storage history | Heat, humidity, and light help explain fading speed and pattern. |
| Physical inspection | Separates dye fading from vinegar syndrome, dirt, shrinkage, mold, mechanical damage, or emulsion problems. |
| RGB parade scopes / histograms | Shows channel compression, clipping, and separation before and after pre-balance. |
| Dmin/Dmax or neutral patches when available | Measures density loss and highlight/shadow contamination. |
| Reference comparison | DVD, telecine, alternate print, artwork, or constructed reference separates evidence from subjective decisions. |
| Transform log | Records scanner settings, ODT, color space, pre-balance, cleanup, and clamp choices before CopyCat. |

**How to deal with it in this workflow:** First stabilize preservation risk: cool/dry storage, inspection, cleaning, and digitization before decay advances. Then apply a technical, non-creative pre-balance to reduce extreme bias and give Nuke a more useful source plate. In chroma recovery, `CopyCat` does not replace the whole image: it preserves source luma/detail and learns to reconstruct Cb/Cr from an aligned or constructed reference. If a channel is biased but still carries information, pre-balance may recover a lot. If chroma is genuinely gone, restoration depends on external evidence and should be documented as interpretation.

**Technical references:**

- [National Archives - Motion Picture Film Condition Assessment](https://www.archives.gov/preservation/formats/motion-picture-film-condition-assessment.html)
- [National Film Preservation Foundation - Color Dye Fading](https://www.filmpreservation.org/preservation-basics/color-dye-fading)
- [Graphics Atlas - Chromogenic deterioration](https://new.graphicsatlas.org/chromogenic/object-view)
- [Heritage, 2023 - Digital Unfading of Chromogenic Film Informed by Its Spectral Densities](https://www.mdpi.com/2571-9408/6/4/181)
- [National Film Preservation Foundation - The Film Preservation Guide](https://www.filmpreservation.org/userfiles/image/PDFs/fpg.pdf)

## Downloads

The images on this page, full size:

- [Animated preview of the Nuke chroma recovery YouTube walkthrough]({{ '/images_kebab/video_previews/color-recovery-video-preview.gif' | relative_url }}) (GIF, 3.2 MB)
- [First Scan, Last Chance article hero image]({{ '/images_kebab/digitization/first-scan-last-chance-hero.png' | relative_url }}) (PNG, 0.8 MB)
- [Article excerpt about adjusting scanner color controls]({{ '/images_kebab/digitization/first-scan-last-chance-scanner-color-controls.png' | relative_url }}) (PNG, 0.9 MB)
- [Color systems for motion picture film digitization article screenshot]({{ '/images_kebab/digitization/first-scan-last-chance-color-systems-review.png' | relative_url }}) (PNG, 0.4 MB)
- [Faded live-action scan with strong red/magenta bias]({{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-after.png' | relative_url }}) (PNG, 4.2 MB)
- [Live-action scan after technical rebalance]({{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-before.png' | relative_url }}) (PNG, 3.6 MB)
- [Resolve parade scope showing channel imbalance in faded film]({{ '/images_kebab/candy-candy/candy-candy-resolve-dctl-parade-scope-faded-film.png' | relative_url }}) (PNG, 4.5 MB)
- [Faded Candy Candy scan before DCTL correction]({{ '/images_kebab/candy-candy/candy-candy-faded-balancer-raw.png' | relative_url }}) (PNG, 4.3 MB)
- [Balanced Candy Candy scan after DCTL correction]({{ '/images_kebab/candy-candy/candy-candy-faded-balancer-finished.png' | relative_url }}) (PNG, 4.3 MB)
