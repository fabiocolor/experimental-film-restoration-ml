---
layout: default
title: Preparing Training Pairs
parent: CopyCat Workflow
nav_order: 5
permalink: /automated-dataset-preparation/
grand_parent: "Temporal CbCr"
---

# Preparing Reliable Training Pairs

The model learns whatever is in the training pairs, so a bad pair gives you a bad result. Each pair has to show the same moment in the faded scan and the better reference.

This is simple when both scans come from the same element. It is harder with a telecine, a broadcast master or a home-video release, which can differ in edits, cadence, framing, distortion and missing frames.

## What counts as a good pair

A good pair:

- shows the same moment in both images;
- has edges and moving subjects in the same places;
- is not from a fade, dissolve, splice or a different shot;
- has a reference that is better for the task;
- has not had faces, bodies or objects stretched by the alignment;
- still matches once the aligned files are rendered.

If you are not sure about a pair, drop it. A few pairs you trust beat a big set with mistakes in it.

## Preparation sequence

1. **Get to know both elements.** Write down frame rate, dimensions, pixel shape, field order, where the reels change and any editorial differences you already know about.
2. **Find the rough match first.** Work out how the two line up overall before you solve individual shots.
3. **Then go shot by shot.** One offset almost never describes a whole historical transfer.
4. **Try the simplest alignment first.** Translation, scale, rotation and a modest affine correction are easier to understand than a complex warp, and easier to spot when they go wrong.
5. **Bring in the heavier methods only when they clearly help.** Perspective correction or feature matching can save a difficult shot, but a solver's result still has to be looked at.
6. **Render the candidates.** Judge the files the model will actually see, not the alignment controls.
7. **Check motion and shot boundaries.** A matching background can hide a moving face, hand or object that is one frame out of time.
8. **Keep only the pairs you have checked.** Write down what you threw out and why, rather than filling the gaps with generated or interpolated “ground truth.”
9. **Review the whole selection.** Contact sheets and difference views show repeated frames, coverage gaps and outliers.

## Why motion needs special attention

Two frames can match in the background while a person in the foreground is one frame off. A model trained on that pair learns the error.

Check the moving areas, compare each candidate with its neighbouring frames, and remove pairs near uncertain cuts. Difficult shots can use stronger alignment, but they get the same final review.

## What should be saved

A training set someone can reuse needs, alongside it:

- the identity of every source and reference frame;
- the pairs kept and the pairs dropped, with the reasons;
- the alignment method used for each pair kept;
- a visual review sheet;
- file counts and checksums;
- the crop, colour transforms, and frame ranges used in Nuke;
- enough information to return from an output frame to its original source.

These records let another person trace what the model learned from and remove a bad example later.

## Long references that drift

On a long reference with timing drift, shot changes and difficult foreground motion, start with a conservative alignment of the whole sequence, then add pairs for the shots that are under-represented, without lowering the bar for what counts as a good pair.

The number of pairs on its own tells you nothing: coverage, where each frame came from, whether the rendered files are intact and a look at the moving subjects all have to check out before a dataset is ready. Another film may need fewer pairs, more pairs, or a different balance between one model for the sequence and models per shot.

## When to train by shot

Start with one model for the whole sequence when the material hangs together. It has more examples to learn from and there is less to manage.

Go to a model per shot only after you have looked at the sequence result and found shots the shared model can't do well. Reuse the pairs you already checked for those shots, keep the complete source range for inference, and compare the shot model's result against the sequence model before you replace it.

## Automation and review

Automation can suggest matches, align images and organise files. Whether a pair goes in is a restoration decision: someone looks at it, and the decision is written down so it can be revisited.
