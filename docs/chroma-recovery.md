---
layout: default
title: Chroma Recovery
parent: CopyCat Workflow
nav_order: 2
grand_parent: Colour Recovery
---

# Chroma Recovery: Building the Colour Target

Use this branch when picture detail survives but colour has faded, shifted, or collapsed. Complete the [shared preparation and alignment stages]({{ '/start-here/' | relative_url }}) first. This page covers only the branch-specific target. Training, inference, and delivery are documented once in [Training, Inference, and Review]({{ '/training-inference-review/' | relative_url }}).

## Choose the evidence

| Reference approach | When to use it | What must be recorded |
| --- | --- | --- |
| **Matched reference** | A DVD, telecine, alternate print, or other colour record shows the same frame | Edition, owner or provider, transforms, compression, crop, and alignment limits |
| **Constructed reference** | No direct colour record survives | Historical sources, creative decisions, assumptions, and the people who approved them |

A constructed reference can support a plausible interpretation, but it is not historical proof. The [case studies]({{ '/case-studies/' | relative_url }}) show both approaches.

<figure class="figure">
  <img src="{{ '/images_kebab/general/chroma-recovery-non-reference.png' | relative_url }}" alt="Non-reference chroma recovery example">
  <figcaption>Faded scan at left and an output trained from a constructed colour reference at right.</figcaption>
</figure>

<figure class="figure">
  <img src="{{ '/images_kebab/ben/ben-photoshop-chroma-reference-creation-3.jpeg' | relative_url }}" alt="Photoshop Colorize reference creation">
  <figcaption>A constructed reference for Ben. Focal points guide the colour proposal; the result remains interpretive.</figcaption>
</figure>

## Build the target

The training target combines **source luminance** with **reference chroma**. This teaches colour recovery without asking the model to replace surviving source detail.

1. If necessary, apply a restrained median or debanding pass to a compressed video reference. Record it.
2. Clone the aligned reference crop onto the source so both branches use the same picture area.
3. Convert source and reference from the working space to YCbCr.
4. In a `Shuffle`, map:
   - red from Source red (`Y`);
   - green from Reference green (`Cb`);
   - blue from Reference blue (`Cr`);
   - alpha to black.
5. Convert the target from YCbCr back to the working space.
6. Clamp input and target to the expected range, remove alpha, and copy the same bounding box to both.
7. Connect the prepared source as CopyCat input and the combined image as target.

<figure class="figure">
  <img src="{{ '/images_kebab/cropped/copycat-training-cropped.png' | relative_url }}" alt="CopyCat training setup">
  <figcaption>CopyCat training layout with YCbCr channel separation.</figcaption>
</figure>

<figure class="figure">
  <img src="{{ '/images_kebab/cropped/shuffle-node-settings-cropped.png' | relative_url }}" alt="Shuffle node settings">
  <figcaption>The chroma target uses Source Y with Reference Cb and Cr.</figcaption>
</figure>

## Branch-specific checks

- Difference the input and target in YCbCr. Their luminance should be nearly identical.
- Confirm that the paired crops and bounding boxes match.
- Reject a frame if alignment errors could be learned as colour edges.
- During review, watch for hue drift, colour bleeding, unstable skin tones, and flicker.
- In Resolve, use the recovered render above the original with Composite Mode set to `Color` when the delivery needs explicit source-luminance protection.

<figure class="figure">
  <img src="{{ '/images_kebab/candy-candy/candy-candy-training-steps.jpeg' | relative_url }}" alt="Training steps progression">
  <figcaption>Candy Candy training checkpoints. The PAL DVD provided the colour reference.</figcaption>
</figure>

## Chroma troubleshooting

| Problem | Check |
| --- | --- |
| Detail becomes softer | Verify that Source Y, not Reference Y, enters the target |
| Wrong hue or colour bleeding | Recheck the YCbCr mapping, alignment, crop, and reference transforms |
| Flicker between frames | Add representative pairs around the transition and inspect reference consistency |
| Model misses a colour family | Add well-aligned examples containing that family rather than simply extending training |

Continue with [Training, Inference, and Review]({{ '/training-inference-review/' | relative_url }}).

## Downloads

The images on this page, full size:

- [Non-reference chroma recovery example]({{ '/images_kebab/general/chroma-recovery-non-reference.png' | relative_url }}) (PNG, 1.4 MB)
- [Photoshop Colorize reference creation]({{ '/images_kebab/ben/ben-photoshop-chroma-reference-creation-3.jpeg' | relative_url }}) (JPG, under 0.1 MB)
- [CopyCat training setup]({{ '/images_kebab/cropped/copycat-training-cropped.png' | relative_url }}) (PNG, 0.6 MB)
- [Shuffle node settings]({{ '/images_kebab/cropped/shuffle-node-settings-cropped.png' | relative_url }}) (PNG, 0.2 MB)
- [Training steps progression]({{ '/images_kebab/candy-candy/candy-candy-training-steps.jpeg' | relative_url }}) (JPG, 0.2 MB)
