---
layout: default
title: Training, Inference & Review
parent: CopyCat Workflow
nav_order: 4
grand_parent: Colour Recovery
---

# Training, Inference, and Review

This page covers the stages shared by chroma and spatial recovery. Build the correct branch target first:

- [Chroma recovery]({{ '/chroma-recovery/' | relative_url }}): Source Y with Reference Cb and Cr.
- [Spatial recovery]({{ '/spatial-recovery/' | relative_url }}): Reference Y with Source Cb and Cr.

## Stage 4: Train and monitor

Start with a modest model and a held-out frame that is not part of the training set.

| Setting | Starting point | Review note |
| --- | --- | --- |
| Model | Medium | Try Large only after pair quality and alignment are sound |
| Patch | 512 | Use 256 when the crop is limited, then expect more steps |
| Batch | 3 | Reduce only when memory requires it |
| Steps | 40,000 to 80,000 | Stop or extend according to held-out evidence, not loss alone |
| Checkpoints | Every 10,000 steps | Compare the same held-out material at each checkpoint |
| Contact sheets | About every 100 steps | Use them to spot divergence and memorisation |

Use small geometric augmentation only when the composition allows it. Mild exposure variation can help, but do not introduce transformations that change the property being learned. Chroma training should not distort colour relationships. Spatial training should not add sharpening, blur, or synthetic grain.

![CopyCat Progress contact sheet]({{ '/images_kebab/cropped/copycat-settings-contact-sheet-cropped.png' | relative_url }})
*The Progress tab shows loss and training crops over time.*

![CopyCat held-out preview]({{ '/images_kebab/cropped/copycat-settings-preview-cropped.png' | relative_url }})
*A held-out preview is more useful than loss alone because it tests an unseen frame.*

Check range and bounding-box parity in both branches. For chroma recovery, source and target luminance should remain nearly identical. For spatial recovery, source and target chroma should remain nearly identical.

## Stage 5: Infer the source sequence

Train on selected pairs and infer on the complete source.

1. Read the original source in the same colour-management domain used for training.
2. Apply the same live-area crop, while excluding training-only alignment transforms.
3. Repeat any source preprocessing that was intentionally used during training.
4. Load the chosen `.cat` checkpoint in an `Inference` node.
5. Render 50 to 100 representative frames before committing to the full range.
6. Review motion, transitions, first and last frames, and shot joins.
7. Add new pairs only when they address a specific observed failure, then test again.

![Inference workflow]({{ '/images_kebab/cropped/inference-render-cropped.png' | relative_url }})
*The trained model is applied to the complete source sequence.*

For archival renders, follow the project’s delivery standard. A common working choice is 16-bit half-float EXR with ZIP or DWAA compression in ACES2065-1. Include the shot, version, and model or checkpoint identifier in the file naming.

## Final review

Compare original and recovered renders in the same colour-managed Resolve project with grades and effects disabled. Use a wipe, split screen, or track toggle, then watch the sequence at normal speed as well as frame by frame.

| Recovery branch | Protect in the source | Optional Resolve composite | Reject when |
| --- | --- | --- | --- |
| Chroma | Luminance and detail | `Color` | Colour bleeds, flickers, changes identity, or contradicts evidence |
| Spatial | Chroma | `Luminosity` | Detail is invented, halos appear, or grain and sharpness vary through time |

Scopes can reveal range, luminance, or chroma changes, but they do not decide whether a restoration is historically or aesthetically acceptable. Human review remains the acceptance gate.

## Record the delivery

Keep:

- the original scan and exact reference edition;
- source and reference credits and permissions;
- selected pair indices and alignment notes;
- model, checkpoint, Nuke version, and colour-management settings;
- short validation renders and rejected examples;
- a note explaining assumptions, remaining limits, and who approved the result.

The [provenance guide]({{ '/provenance-metadata/' | relative_url }}) provides a fuller record structure.

## Shared troubleshooting

| Problem | First action |
| --- | --- |
| Residual geometry in a difference view | Return to [alignment]({{ '/start-here/' | relative_url }}#stage-2-alignment) and use keyed transforms where necessary |
| Training stalls | Improve pair coverage and alignment before increasing model size |
| Results fail only on certain shots | Add targeted pairs or split those shots into a separate model |
| Full-range output differs from the held-out test | Confirm ingest, crop, preprocessing, and inference settings match training |

## Downloads

The images on this page, full size:

- [CopyCat Progress contact sheet]({{ '/images_kebab/cropped/copycat-settings-contact-sheet-cropped.png' | relative_url }}) (PNG, 1.1 MB)
- [CopyCat held-out preview]({{ '/images_kebab/cropped/copycat-settings-preview-cropped.png' | relative_url }}) (PNG, 1.1 MB)
- [Inference workflow]({{ '/images_kebab/cropped/inference-render-cropped.png' | relative_url }}) (PNG, 0.6 MB)
