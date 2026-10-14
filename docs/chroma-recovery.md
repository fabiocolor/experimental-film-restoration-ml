---
layout: default
title: Building the Colour Target
parent: CopyCat Workflow
nav_order: 2
grand_parent: "Temporal CbCr"
---

# Building the Colour Target

Picture detail survives in the scan, but its colour has faded, shifted or collapsed; a better copy of the same frames keeps the colour. Complete the [preparation and alignment stages]({{ '/start-here/' | relative_url }}) first. Training, inference and delivery are on [Training, Inference and Review]({{ '/training-inference-review/' | relative_url }}).

## Record the reference

Note the reference's edition, owner or provider, transforms, compression, crop and alignment limits. A DVD, a telecine, another print or a video master can all work, as long as it shows the same frames with better colour.

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

## Checks

- Difference the input and target in YCbCr. Their luminance should be nearly identical.
- Confirm that the paired crops and bounding boxes match.
- Reject a frame if alignment errors could be learned as colour edges.
- During review, watch for hue drift, colour bleeding, unstable skin tones, and flicker.
- In Resolve, use the recovered render above the original with Composite Mode set to `Color` when the delivery needs explicit source-luminance protection.

<figure class="figure">
  <img src="{{ '/images_kebab/candy-candy/candy-candy-training-steps.jpeg' | relative_url }}" alt="Training steps progression">
  <figcaption>Candy Candy training checkpoints. The PAL DVD provided the colour reference.</figcaption>
</figure>

## Troubleshooting

| Problem | Check |
| --- | --- |
| Detail becomes softer | Verify that Source Y, not Reference Y, enters the target |
| Wrong hue or colour bleeding | Recheck the YCbCr mapping, alignment, crop, and reference transforms |
| Flicker between frames | Add representative pairs around the transition and inspect reference consistency |
| Model misses a colour family | Add well-aligned examples containing that family rather than simply extending training |

Continue with [Training, Inference, and Review]({{ '/training-inference-review/' | relative_url }}).

## Downloads

The images on this page, full size:

- [CopyCat training setup]({{ '/images_kebab/cropped/copycat-training-cropped.png' | relative_url }}) (PNG, 0.6 MB)
- [Shuffle node settings]({{ '/images_kebab/cropped/shuffle-node-settings-cropped.png' | relative_url }}) (PNG, 0.2 MB)
- [Training steps progression]({{ '/images_kebab/candy-candy/candy-candy-training-steps.jpeg' | relative_url }}) (JPG, 0.2 MB)
