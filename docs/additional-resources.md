---
layout: default
title: Additional Resources
parent: Resources
nav_order: 1
---

# Additional Resources

These notes aren't steps of the workflow; they are the background to it. Read them when planning a scan, working out what happened to a faded print, or writing down restoration choices.

## Video Walkthrough: Nuke Chroma Recovery {#video-walkthrough-nuke-chroma-recovery}

The quickest way to see the CopyCat colour-recovery workflow working before reading the [step-by-step guide]({{ '/copycat-workflow/' | relative_url }}).

<figure class="figure">
  <a href="https://youtu.be/kXerjFGX9Kg" target="_blank" rel="noopener">
    <img src="{{ '/images_kebab/video_previews/color-recovery-video-preview.gif' | relative_url }}" alt="Animated preview of the Nuke chroma recovery YouTube walkthrough">
  </a>
  <figcaption>Source video: <a href="https://youtu.be/kXerjFGX9Kg" target="_blank" rel="noopener">Nuke Chroma Recovery: Rebuilding Faded Film Color with CopyCat</a>.</figcaption>
</figure>

## Digitization: First Scan, Last Chance {#digitization-first-scan-last-chance}

Digitisation is the moment the picture leaves its fragile physical container. The scan is the foundation of every restoration step that follows, so it should not be a quick transfer or a creative grade baked in. For damaged or rare material the first scan may also be the only one: the film may not survive being handled again, the budget may not stretch to a second pass, or the decay may get there first. Everything on this site works with the scan as it is, because most of the time the scan is all that is left.

<figure class="figure">
  <a href="https://fabiocolor.substack.com/p/first-scan-last-chance" target="_blank" rel="noopener">
    <img src="{{ '/images_kebab/digitization/first-scan-last-chance-hero.png' | relative_url }}" alt="First Scan, Last Chance article hero image">
  </a>
  <figcaption>Article image from <a href="https://fabiocolor.substack.com/p/first-scan-last-chance" target="_blank" rel="noopener">"First Scan, Last Chance"</a>: digitisation as the moment the picture is separated from its fragile film container.</figcaption>
</figure>

The aim is to capture as much of the picture as the film still holds, in RGB and in brightness. A good scan keeps the film's dynamic range, the separation between the colour channels, the variation in density, the grain and the texture, so that whatever comes later has something to work with. A poor scan throws evidence away for good: clipped highlights, crushed shadows, a bad white balance, automatic exposure decisions or a clipped channel can't be reliably put back afterwards.

<div class="media-grid media-grid-2">
  <figure class="figure">
    <a href="https://fabiocolor.substack.com/p/first-scan-last-chance" target="_blank" rel="noopener">
      <img src="{{ '/images_kebab/digitization/first-scan-last-chance-scanner-color-controls.png' | relative_url }}" alt="Article excerpt about adjusting scanner color controls">
    </a>
    <figcaption>The scanner's exposure and RGB controls decide how much usable picture gets captured before restoration even begins.</figcaption>
  </figure>
  <figure class="figure">
    <a href="https://fabiocolor.substack.com/p/first-scan-last-chance" target="_blank" rel="noopener">
      <img src="{{ '/images_kebab/digitization/first-scan-last-chance-color-systems-review.png' | relative_url }}" alt="Color systems for motion picture film digitization article screenshot">
    </a>
    <figcaption>Digitisation choices should be tested against the film element and what you are preserving it for, not treated as one colour path that fits everything.</figcaption>
  </figure>
</div>

**Scanning principles:**

- Capture a preservation-grade scan before any restoration decision gets baked in.
- No clipped highlights, no crushed shadows, no automatic white balance, no heavy noise reduction, no sharpening, no creative LUTs at capture.
- Watch the RGB parade, the waveform, the histogram and channel clipping during setup and during the capture itself.
- Do a first pass to find the sequence's tonal extremes, density shifts, splice flashes, severe fading, and any scanner setting that is going to fail.
- Write down the scanner model, gate, optics, resolution, bit depth, colour encoding, transforms, exposure settings, and any wet-gate or cleanup choices.
- Keep the raw scan or archival master separate from restoration renders, review proxies and creative grades.

| Risk during digitization | Why it matters later |
| --- | --- |
| Clipped highlights or channels | Picture gone for good, and colour recovery, deflicker, dust removal and grading all have less to work with. |
| Incorrect white point | Adds a false colour relationship that restoration tools may learn or amplify. |
| Automatic scanner decisions | Can change from shot to shot, giving you flicker, unstable density or a channel balance that wanders. |
| Baked creative grade | Narrows the evidence left for a future restoration or a different interpretation. |
| Low bit depth / compressed delivery format | Loses the subtle density and colour information that restoration needs, especially in faded material. |

For historical or deteriorated material, go for a conservative, high-bit-depth scan that keeps everything the scanner captured, and make the restoration choices afterwards, in post, where they can be undone. ADX, Cineon, linear, ACES and display-referred workflows all have their place, but test them against the actual film element rather than assume one is right. For this colour-recovery method the one rule is continuity: whatever scan and transform path you choose, Source and Reference go into training with the same transforms, written down.

Digitisation, restoration and remastering are three different things. Digitisation turns the film into data. Restoration deals with the damage or loss that came from the physical container. Remastering adapts the work for a new display, release or audience. Keep those lines visible in the metadata, so whoever comes later knows which decisions came from the object, which from the restoration and which from the delivery master.

Source article and images: [First Scan, Last Chance: The Critical Role of Digitization in Preserving Film Heritage](https://fabiocolor.substack.com/p/first-scan-last-chance).

## Why Faded Scans Turn Magenta {#why-faded-scans-turn-magenta}

Colour film records the picture in subtractive dye layers. When those dyes no longer have the density they had, the scan no longer carries even RGB information. The common failure is the pink or magenta cast: the cyan and yellow dyes weaken against the magenta, so red and blue dominate and the green channel loses its useful separation.

For this workflow the point is practical, not aesthetic: the magenta picture usually still has usable brightness, texture and grain, but its colour channels are biased, compressed or partly clipped. A neutral pre-balance gives `CopyCat` a cleaner input to start from before the colour comes in from the reference.

<div class="media-grid media-grid-2">
  <figure class="figure">
    <img src="{{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-after.png' | relative_url }}" alt="Faded live-action scan with strong red/magenta bias">
    <figcaption>Faded scan with a strong red/magenta bias.</figcaption>
  </figure>
  <figure class="figure">
    <img src="{{ '/images_kebab/resolve-dctl/faded-film-resolve-dctl-strong-red-compress-before.png' | relative_url }}" alt="Live-action scan after technical rebalance">
    <figcaption>A technical red compression and rebalance, to give the model a cleaner input.</figcaption>
  </figure>
</div>

<figure class="figure">
  <img src="{{ '/images_kebab/candy-candy/candy-candy-resolve-dctl-parade-scope-faded-film.png' | relative_url }}" alt="Resolve parade scope showing channel imbalance in faded film">
  <figcaption>The Resolve parade scope showing channel imbalance in faded film. The goal is a technical pre-balance, not a final creative grade.</figcaption>
</figure>

<div class="media-grid media-grid-2">
  <figure class="figure">
    <img src="{{ '/images_kebab/candy-candy/candy-candy-faded-balancer-raw.png' | relative_url }}" alt="Faded Candy Candy scan before balancing">
    <figcaption>The faded scan in Resolve, before balancing.</figcaption>
  </figure>
  <figure class="figure">
    <img src="{{ '/images_kebab/candy-candy/candy-candy-faded-balancer-finished.png' | relative_url }}" alt="Balanced Candy Candy scan">
    <figcaption>The same scan after a neutral, technical balance.</figcaption>
  </figure>
</div>

### What is going on in the film

**What is failing:** in chromogenic film the picture is made of cyan, magenta and yellow dye clouds, one on top of the other, in gelatin layers. These organic dyes don't age at the same rate. When the cyan and the yellow fade faster than the magenta, the balance shifts towards pink, purple or magenta. NARA's inspection guidance says exactly this: magenta film has faded because the cyan and yellow dye layers have weakened and the magenta is left dominant. The NFPF describes the same pattern for modern colour motion picture film: spontaneous chemical changes in the image dyes, often with a purplish cast from the cyan and yellow going first.

**Why it happened:** not a bad scan or a bad grade, though either can make it look worse. It is chemical deterioration that has been going on for decades: broken bonds in the dyes, dyes of unequal stability, heat, humidity, light, time and the storage history. Graphics Atlas notes that chromogenic dyes fade in the dark as well as in the light; cyan fading in dark storage can leave the whole picture magenta. Older chromogenic stocks and prints, especially mid-century material from before the stability improvements, are more vulnerable than modern stocks.

**Why ordinary grading isn't enough:** an RGB grade can rebalance the channels globally, but it can't bring back colour that isn't there any more, or that has been compressed into contaminated channel relationships. Recent digital unfading research treats this as a reconstruction problem, limited by what dye is left, the quality of the scan and the references you have. Severe cases need informed inference: a direct reference, a constructed one, spectral or density analysis, documented memory colour, or a model trained on pairs.

**Data worth capturing before restoration:**

| Data | Why it helps |
| --- | --- |
| Stock, generation, and approximate date | Tells you how much the dyes were at risk and which chromogenic process it is likely to be. |
| Storage history | Heat, humidity and light explain how fast it faded and in what pattern. |
| Physical inspection | Separates dye fading from vinegar syndrome, dirt, shrinkage, mould, mechanical damage or emulsion problems. |
| RGB parade scopes / histograms | Shows channel compression, clipping and separation before and after the pre-balance. |
| Dmin/Dmax or neutral patches when available | Measures the density loss and the contamination in highlights and shadows. |
| Reference comparison | A DVD, a telecine, another print, artwork or a constructed reference: what separates evidence from somebody's opinion. |
| Transform log | The scanner settings, ODT, colour space, pre-balance, cleanup and clamp choices before CopyCat. |

**How this workflow deals with it:** first deal with the film itself: cool, dry storage, inspection, cleaning, and a scan before the decay goes any further. Then a technical, non-creative pre-balance to take the worst of the cast off and give Nuke a more useful source. In colour recovery `CopyCat` doesn't replace the picture: it keeps the source's brightness and detail and learns to rebuild the Cb and Cr from an aligned or constructed reference. If a channel is biased but still carries information, the pre-balance may get a lot back. If the colour is genuinely gone, the recovery depends on outside evidence and has to be written down as an interpretation.

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
- [Faded Candy Candy scan before balancing]({{ '/images_kebab/candy-candy/candy-candy-faded-balancer-raw.png' | relative_url }}) (PNG, 4.3 MB)
- [Balanced Candy Candy scan]({{ '/images_kebab/candy-candy/candy-candy-faded-balancer-finished.png' | relative_url }}) (PNG, 4.3 MB)
