---
layout: default
title: Preparation & Alignment
parent: CopyCat Workflow
nav_order: 1
grand_parent: "Temporal CbCr"
---

# Preparation and Alignment: Stages 0–2

This page covers the first stages of the [CopyCat workflow]({{ '/copycat-workflow/' | relative_url }}): Resolve export, Nuke project setup, dataset curation, alignment and the shared crop. Then continue with [building the colour target]({{ '/chroma-recovery/' | relative_url }}).

If the reference is hard to match (a telecine, a broadcast master, a DVD with different edits), see [Preparing Reliable Training Pairs]({{ '/automated-dataset-preparation/' | relative_url }}): lining things up reel by reel, shot by shot and frame by frame, and throwing out the pairs you can't trust.

<figure class="figure">
  <img src="{{ '/images_kebab/general/full-overview-comparison.png' | relative_url }}" alt="Workflow overview">
  <figcaption>The whole workflow, start to finish.</figcaption>
</figure>

---

## Stage 0: Resolve Export + Nuke Project Setup

Before anything else, make sure the scan keeps as much of the picture as it can: no clipping, no automatic white balance, no creative grade baked in, no compressed low-bit-depth intermediates. The scan is what you have to work with, and whatever it lost the model can't get back. For the background, see [Digitization: First Scan, Last Chance]({{ '/additional-resources/' | relative_url }}#digitization-first-scan-last-chance).

### Source and Reference Preparation

What matters is whether the reference has the colour, not whether it is newer, sharper or higher resolution. A soft DVD with the right colour is a better reference than a sharp copy with the wrong one.

**Source preparation:**

- Balance the source technically, not creatively: neutral blacks and whites, nothing that looks like a grade.
- Take out severe flicker, dirt, splice flashes and instability first. The model will learn them otherwise.
- If the grain gets in the way of learning the colour, degrain the source for training only. Write down the settings and keep the original plate; the grain comes back with the original luma at the end, because only the colour is taken from the model.
- If the whole scan has a strong cast, from dye fade or from the scanner, give it a neutral, technical pre-balance first. For the background on magenta dye fade and channel imbalance, see [Why Faded Scans Turn Magenta]({{ '/additional-resources/' | relative_url }}#why-faded-scans-turn-magenta).

<div class="media-grid media-grid-2">
  <figure class="figure">
    <img src="{{ '/images_kebab/candy-candy/candy-candy-faded-balancer-raw.png' | relative_url }}" alt="Raw faded scan">
    <figcaption>Before (raw faded scan)</figcaption>
  </figure>
  <figure class="figure">
    <img src="{{ '/images_kebab/candy-candy/candy-candy-faded-balancer-finished.png' | relative_url }}" alt="Balanced scan">
    <figcaption>After a neutral pre-balance</figcaption>
  </figure>
</div>

<p class="experiment-credit"><em>Candy Candy</em>: the magenta cast neutralised in Resolve before going into Nuke.</p>

**Reference preparation:**

- Clean enough that transfer artefacts don't mislead the model.
- A light denoise, deband or median takes care of dust, compression noise and banding. Don't change the geometry and don't warp in time.

**Geometry and stabilisation:** prefer cleanup that leaves the geometry alone. If you have to stabilise or reframe, do exactly the same thing to both exports.

### Resolve Export

1. Put both sources in one timeline. Turn off retimes, effects and per-clip grades.
2. Line the reference up with the source in Edit/Inspector (Translate/Scale/Rotate). Letterbox or pillarbox is fine; what matters is that the framing doesn't move.
3. Use one colour-management path for both elements and write it down. If you train in display-referred Rec.709, give both exports the same display transform and check their range before they go anywhere near CopyCat.
4. Check that resolution, pixel aspect, frame range and rate, and channel set (RGB only, no alpha) match.
5. Note any global offsets (scale, translate, rotate); you will want them later.

**Rules:**

- Same frame range, framing, and resolution.
- No creative grading.
- Fix interlacing, cadence problems, and decode issues before export.

**QC checklist:**

- [ ] Dimensions, frame ranges, and pixel aspect match
- [ ] Channel sets match (RGB), values in 0–1 when read into Nuke
- [ ] No retimes or extra colour transforms that crept in

### Nuke Project Setup

**Project settings:**

- Colour management: the OCIO/ACES configuration the project uses.
- Working space: one working space for the whole project, written down.
- Viewer process: the display transform that matches the display you review on.

**Read node settings (both Source and Reference):**

- Set the input transform to match what Resolve actually exported.
- An archival ACES master and a display-referred training file are two different things; don't label one as the other.

**Verify:**

- Flip the viewer between Source and Reference; they should look consistent under the chosen ODT.
- Both branches should have the same ingest transform.

### ACES and Color Management Reference

**The domain this workflow trains in:** display-referred Rec.709. The same transform on source and reference, check the range, and build the YCbCr target from those matched files.

**Log, as an alternative:** it works in theory, but it is a lot slower and, in testing, the colour came out worse. Only if the footage demands it.

**Don't clamp linear ACES:** reading ACES 2065-1 and clamping it to [0–1] crushes the highlights and spoils the colour mapping. If you start from ACES masters, go to display-referred first.

**Input and Target have to be in exactly the same domain with the same transforms.** Don't mix linear on one branch with display-referred on the other.

**Write nodes (delivery):**

- Archival: `Write.colorspace = ACES - ACES2065-1` (AP0), EXR 16-bit half (ZIP/DWAA).
- Review/proxy: Rec.709 ODT → ProRes/H.264. Note the viewing intent and the ODT.

**Resolve interop:**

- Write down the exact ACES/OCIO configuration and transforms the project uses.
- Keep archival masters separate from display-referred training exports.
- Keep frame size, pixel aspect ratio, channel set, and frame range identical between paired training files.

---

## Stage 1: Dataset Curation

Train on a small set of frames that represent the shot, not the whole sequence. A handful of good pairs beats hundreds of doubtful ones.

<figure class="figure">
  <img src="{{ '/images_kebab/cropped/dataset-curation-cropped.png' | relative_url }}" alt="Dataset curation">
  <figcaption>Building paired training examples in Nuke.</figcaption>
</figure>

### Selection Criteria

- **Source frames:** intact luma and texture, typical grain, as little gate weave as possible. Avoid frames that are mostly motion blur unless the reference has the same blur.
- **Reference frames:** the same shot and timecode when you have it, or a well-made stand-in. Avoid heavy compression, burned-in subtitles or logos, and grades that wander.
- **Leave out:** pairs where one side has something the other doesn't (a flash, a splice mark). The model can't reconcile those.

### Pair Counts

| Scope | Pairs | Notes |
| --- | --- | --- |
| Shot | 4–9 | Add more if convergence stalls |
| Scene | 12–24 | |
| Sequence | 24–64+ | Scale with variability |

For a short range (say frames 20–60), take a frame at the beginning, two in the middle and one at the end.

### Coverage

Cover the range of what is in the shot:

- **Lighting:** warm/cool, day/night, interior/exterior
- **Subjects:** skin tones, foliage/sky, fabrics, neutrals
- **Extremes:** deep shadows, specular highlights, saturated primaries

### Pairing Rules

- **In time:** the same frame index or timecode. If it is one frame out, take the frame where the static structure overlaps most.
- **In space:** the same resolution and orientation. Overscan and crop have to be shared; what is left over is dealt with in Stage 2.
- **Colour space:** both sides under the same transform (a Rec.709 export, say) so the values stay in 0–1.

### Nuke Build

1. Create a `FrameHold` per selected index on both Source and Reference branches.
2. Assemble ordered stacks with `AppendClip`: one for Source (Input), one for Reference (Target).
3. Keep a staging `AppendClip` upstream of the one the `PostageStamp` nodes point at, so you can reorder pairs without breaking anything.
4. Check each pair with a viewer wipe or `Merge (difference)`. You are judging geometry and alignment here, not colour.
5. Label the pairs consistently and keep a table of indices and timecodes, so you can find your way back later.

### Documentation

- Write down the shot, the pair indices and why you chose them.
- Note whether the reference is direct (a telecine, a DVD, a print) or constructed, and where it came from.
- Flag the compromises (compression, leftover parallax) so you remember to look for them during training.

---

## Stage 2: Alignment

The point of this stage is that Source and Reference end up differing only in colour: pixel-accurate alignment, and the same crop on both.

<figure class="figure">
  <img src="{{ '/images_kebab/cropped/alignment-cropped.png' | relative_url }}" alt="Alignment workflow">
  <figcaption>Auto and manual alignment paths inside the template.</figcaption>
</figure>

### Strategy

1. One global solve with `F_Align` on a conservative central ROI. Don't iterate on it.
2. Check it straight away with `Merge (difference)`. If edges or geometry are still showing, switch to a manual `Transform` with keyframes.
3. Keep a `Dissolve` so you can flip between the auto and manual paths quickly.

<figure class="figure">
  <img src="{{ '/images_kebab/general/merge-difference-alignment-check.gif' | relative_url }}" alt="Merge (difference) alignment check">
  <figcaption>Merge (difference) in the viewer: geometry and edges should be close to black. Colour differences are expected, that is the whole point; only a structural misalignment is a problem.</figcaption>
</figure>

### Crop and Subtitle Handling

- Take the black borders and overscan off both branches. Don't train on anything that isn't picture.
- Keep burned-in subtitles and logos out. Where you can't, animate a shared crop.
- Give Source and Reference the **exact same crop** (clone or link the node) so the pixels correspond.

<figure class="figure">
  <img src="{{ '/images_kebab/cropped/crop-node-settings-cropped.png' | relative_url }}" alt="Crop node settings">
  <figcaption>Shared crop keeping both branches in the same live picture area.</figcaption>
</figure>

### Nuke Build

- Compare Reference to Source with Viewer wipe and `Merge (difference)`.
- A `Dissolve` switches between the auto and manual paths. Keyframe it per frame (0 = auto, 1 = manual) once you have looked.
- **Auto path:** `F_Align` with a conservative central ROI, one global solve (Translate/Scale/Rotate/Perspective). Don't chase parameters.
- **Manual path:** `Transform` (translate/scale/rotate) keyed as needed. Judge it with `Merge (difference)`.
- **Reference crop, last:** add a `Crop` on the aligned Reference to take off overscan and anything that comes and goes. Keep it bypassed while solving and turn it on at the end. Keep this node; it gets cloned or linked in Stage 3. Don't crop the Source here.

### Verification Checklist

- [ ] `Merge (difference)` shows only colour differences; geometry and edges close to black. No Grade or colour correction at this point.
- [ ] No shimmer at the borders or corners when flipping between Source and Reference.
- [ ] The reference crop takes off overscan and mattes without hiding what you align by.

**Troubleshooting:** gate weave and parallax on a warped reference several generations down can mean a lot of manual `Transform` keyframing. It takes time; there is no shortcut.

---

## Next: Stage 3, the colour target

The ground-truth target takes its brightness (`Y`) from the Source and its colour (`Cb/Cr`) from the Reference.

<figure class="figure">
  <img src="{{ '/images_kebab/cropped/colorspace-node-linear-to-ycbcr-settings-cropped.png' | relative_url }}" alt="Colorspace node settings">
  <figcaption>Convert both branches to YCbCr before channel recombination.</figcaption>
</figure>

<figure class="figure">
  <img src="{{ '/images_kebab/cropped/shuffle-node-settings-cropped.png' | relative_url }}" alt="Shuffle node settings">
  <figcaption>Shuffle node used to build the ground-truth target.</figcaption>
</figure>

<figure class="figure">
  <img src="{{ '/images_kebab/general/copybbox-node-settings.png' | relative_url }}" alt="CopyBBox node">
  <figcaption>CopyBBox gives Source and Ground Truth the same bounding box before they go into CopyCat.</figcaption>
</figure>

Continue with [building the colour target]({{ '/chroma-recovery/' | relative_url }}), then [training, inference and review]({{ '/training-inference-review/' | relative_url }}).

### Common Failure Modes

- Training on an unstable source (flicker, dirt, severe imbalance).
- Trusting a bad reference just because it is higher resolution.
- Keeping misaligned frames in the dataset.
- Leaving borders, subtitles, or overlays inside the training area.
- Expecting one model to solve every shot in a difficult sequence.

## Downloads

The images on this page, full size:

- [Workflow overview]({{ '/images_kebab/general/full-overview-comparison.png' | relative_url }}) (PNG, 3.5 MB)
- [Raw faded scan]({{ '/images_kebab/candy-candy/candy-candy-faded-balancer-raw.png' | relative_url }}) (PNG, 4.3 MB)
- [Balanced scan]({{ '/images_kebab/candy-candy/candy-candy-faded-balancer-finished.png' | relative_url }}) (PNG, 4.3 MB)
- [Dataset curation]({{ '/images_kebab/cropped/dataset-curation-cropped.png' | relative_url }}) (PNG, 1.0 MB)
- [Alignment workflow]({{ '/images_kebab/cropped/alignment-cropped.png' | relative_url }}) (PNG, 0.8 MB)
- [Merge (difference) alignment check]({{ '/images_kebab/general/merge-difference-alignment-check.gif' | relative_url }}) (GIF, 12.5 MB)
- [Crop node settings]({{ '/images_kebab/cropped/crop-node-settings-cropped.png' | relative_url }}) (PNG, 0.1 MB)
- [Colorspace node settings]({{ '/images_kebab/cropped/colorspace-node-linear-to-ycbcr-settings-cropped.png' | relative_url }}) (PNG, 0.3 MB)
- [Shuffle node settings]({{ '/images_kebab/cropped/shuffle-node-settings-cropped.png' | relative_url }}) (PNG, 0.2 MB)
- [CopyBBox node]({{ '/images_kebab/general/copybbox-node-settings.png' | relative_url }}) (PNG, 3.5 MB)
