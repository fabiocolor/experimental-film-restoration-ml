---
layout: default
title: Building the Colour Target
parent: CopyCat Workflow
nav_order: 2
grand_parent: "Temporal CbCr"
---

# Building the Colour Target

This is the stage for the common case: the scan still has its detail but the colour has faded or shifted, and a better copy of the same frames has the colour. Do the [preparation and alignment stages]({{ '/start-here/' | relative_url }}) first. Training, inference and delivery are on [Training, Inference and Review]({{ '/training-inference-review/' | relative_url }}).

## Record the reference

Write down which edition the reference is, who owns or supplied it, its transforms, its compression, the crop, and how far it could be aligned. A DVD, a telecine, another print or a video master all work, as long as it shows the same frames with better colour.

## Build the target

The training target is the **source's brightness** with the **reference's colour**. That is the whole trick: the model learns colour only, and never gets the chance to replace the scan's detail.

1. If the reference is compressed video, a restrained median or debanding pass helps. Write down what you did.
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

- Difference the input and the target in YCbCr. The luminance should be nearly identical; if it isn't, the reference's brightness has got in.
- Check that the paired crops and bounding boxes match.
- Drop a frame if an alignment error could be learned as a colour edge.
- During review, watch for hue drift, colour bleeding, unstable skin tones and flicker.
- In Resolve, put the recovered render above the original with Composite Mode set to `Color` when the delivery needs the source brightness protected explicitly.

<figure class="figure">
  <img src="{{ '/images_kebab/candy-candy/candy-candy-training-steps.jpeg' | relative_url }}" alt="Training steps progression">
  <figcaption>Candy Candy training checkpoints. The colour came from the PAL DVD.</figcaption>
</figure>

## Troubleshooting

| Problem | Check |
| --- | --- |
| Detail becomes softer | Check that Source Y, not Reference Y, is going into the target |
| Wrong hue or colour bleeding | Go back over the YCbCr mapping, the alignment, the crop and the reference transforms |
| Flicker between frames | Add pairs around the transition and check whether the reference itself is consistent there |
| Model misses a colour family | Add well-aligned pairs that contain that colour; training longer won't invent it |

Continue with [Training, Inference, and Review]({{ '/training-inference-review/' | relative_url }}).

## Downloads

The images on this page, full size:

- [CopyCat training setup]({{ '/images_kebab/cropped/copycat-training-cropped.png' | relative_url }}) (PNG, 0.6 MB)
- [Shuffle node settings]({{ '/images_kebab/cropped/shuffle-node-settings-cropped.png' | relative_url }}) (PNG, 0.2 MB)
- [Training steps progression]({{ '/images_kebab/candy-candy/candy-candy-training-steps.jpeg' | relative_url }}) (JPG, 0.2 MB)
