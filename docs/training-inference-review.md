---
layout: default
title: Training, Inference & Review
parent: CopyCat Workflow
nav_order: 4
grand_parent: "Temporal CbCr"
---

# Training, Inference, and Review

The last stages of the [CopyCat workflow]({{ '/copycat-workflow/' | relative_url }}). Build the [colour target]({{ '/chroma-recovery/' | relative_url }}) first: Source Y with Reference Cb and Cr.

## Stage 4: Train and monitor

Start with a modest model, and keep back a frame the model never trains on. That held-out frame is how you know whether it has learned the colour or just memorised the pairs.

| Setting | Starting point | Review note |
| --- | --- | --- |
| Model | Medium | Try Large only after pair quality and alignment are sound |
| Patch | 512 | Use 256 when the crop is limited, then expect more steps |
| Batch | 3 | Reduce only when memory requires it |
| Steps | 40,000 to 80,000 | Stop or carry on according to the held-out frame, not the loss alone |
| Checkpoints | Every 10,000 steps | Compare the same held-out material at each checkpoint |
| Contact sheets | About every 100 steps | Use them to spot divergence and memorisation |

A little geometric augmentation is fine when the composition allows it, and mild exposure variation can help. Don't use anything that changes the colour relationships; colour is the thing the model is learning.

<figure class="figure">
  <img src="{{ '/images_kebab/cropped/copycat-settings-contact-sheet-cropped.png' | relative_url }}" alt="CopyCat Progress contact sheet">
  <figcaption>The Progress tab shows loss and training crops over time.</figcaption>
</figure>

<figure class="figure">
  <img src="{{ '/images_kebab/cropped/copycat-settings-preview-cropped.png' | relative_url }}" alt="CopyCat held-out preview">
  <figcaption>A held-out preview tells you more than the loss, because it is a frame the model hasn't seen.</figcaption>
</figure>

Check that input and target have the same range and bounding box. Their luminance should still be nearly identical.

## Stage 5: Infer the source sequence

You train on a few pairs; you run the model on the whole source.

1. Read the original source in the same colour-management domain you trained in.
2. Apply the same live-area crop, but not the alignment transforms, which were only for training.
3. Repeat any preprocessing you did to the source for training.
4. Load the chosen `.cat` checkpoint in an `Inference` node.
5. Render 50 to 100 frames from around the shot before you commit to the full range.
6. Review motion, transitions, first and last frames, and shot joins.
7. Add new pairs only to fix something you actually saw go wrong, then test again.

<figure class="figure">
  <img src="{{ '/images_kebab/cropped/inference-render-cropped.png' | relative_url }}" alt="Inference workflow">
  <figcaption>The trained model run over the whole source sequence.</figcaption>
</figure>

For archival renders, follow whatever the project delivers in. A common choice is 16-bit half-float EXR with ZIP or DWAA compression in ACES2065-1. Put the shot, the version and the model or checkpoint in the file name.

## Final review

Compare the original and the recovered render in the same colour-managed Resolve project, with grades and effects off. Wipe, split screen or toggle the tracks, then watch the sequence at normal speed as well as frame by frame. Some things only show up at speed.

| Protect in the source | Optional Resolve composite | Reject when |
| --- | --- | --- |
| Luminance and detail | `Color` | Colour bleeds, flickers, changes identity, or contradicts evidence |

Scopes show you range, luminance and chroma changes, but they don't tell you whether the result is good. That is decided by a person looking at it.

## Record the delivery

Keep:

- the original scan and exact reference edition;
- source and reference credits and permissions;
- selected pair indices and alignment notes;
- model, checkpoint, Nuke version, and colour-management settings;
- short validation renders and rejected examples;
- a note on the assumptions, what still isn't right, and who made the final call.

The [provenance guide]({{ '/provenance-metadata/' | relative_url }}) has a fuller record to follow.

## Shared troubleshooting

| Problem | First action |
| --- | --- |
| Residual geometry in a difference view | Return to [alignment]({{ '/start-here/' | relative_url }}#stage-2-alignment) and use keyed transforms where necessary |
| Training stalls | Better pairs and better alignment before a bigger model |
| Results fail only on certain shots | Add pairs for those shots, or give them a model of their own |
| Full-range output differs from the held-out test | Check that ingest, crop, preprocessing and inference settings match what you trained with |

## Downloads

The images on this page, full size:

- [CopyCat Progress contact sheet]({{ '/images_kebab/cropped/copycat-settings-contact-sheet-cropped.png' | relative_url }}) (PNG, 1.1 MB)
- [CopyCat held-out preview]({{ '/images_kebab/cropped/copycat-settings-preview-cropped.png' | relative_url }}) (PNG, 1.1 MB)
- [Inference workflow]({{ '/images_kebab/cropped/inference-render-cropped.png' | relative_url }}) (PNG, 0.6 MB)
