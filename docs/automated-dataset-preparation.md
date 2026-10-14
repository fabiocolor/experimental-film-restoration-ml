---
layout: default
title: Preparing Training Pairs
parent: CopyCat Workflow
nav_order: 5
permalink: /automated-dataset-preparation/
grand_parent: "Temporal CbCr"
---

# Preparing Reliable Training Pairs

A model is only as good as the pairs it learns from. Each pair has to show the same moment in the faded scan and the better reference.

That's easy when both scans come from the same element. It's much harder with a telecine, a broadcast master or a home-video release, which can differ in edits, cadence, framing, distortion and missing frames.

## What counts as a good pair

A good pair:

- shows the same moment in both images;
- has edges and moving subjects in the same places;
- isn't from a fade, dissolve, splice or a different shot;
- has a reference that's actually better for the job;
- hasn't had faces, bodies or objects stretched by the alignment;
- still matches once the aligned files are rendered.

If you're not sure about a pair, drop it. A few good pairs beat many weak ones.

## A careful preparation sequence

1. **Understand both elements.** Record frame rate, dimensions, pixel shape, field order, reel boundaries, and known editorial differences.
2. **Find broad correspondence.** Establish the overall timing relationship before solving individual shots.
3. **Work shot by shot.** A single offset rarely describes a complete historical transfer.
4. **Try the simplest alignment first.** Translation, scale, rotation, and a modest affine correction are easier to interpret than a complex warp.
5. **Use stronger methods only when they clearly help.** Perspective correction or feature matching can rescue hard material, but a solver returning an answer doesn't make it right.
6. **Render the candidates.** Judge the files the model will actually see, not only the alignment controls.
7. **Check motion and shot boundaries.** Background agreement can hide a moving face, hand, or object that is one frame out of time.
8. **Keep only defensible pairs.** Record rejections instead of filling gaps with generated or interpolated “ground truth.”
9. **Review the whole selection.** Contact sheets and difference views reveal repeated frames, coverage gaps, and outliers that are easy to miss one at a time.

## Why motion needs special attention

Two frames can match perfectly in the background while a person in front is a frame off. Train on that and the model learns the error.

So check the moving areas, compare each candidate with its neighbours, and drop pairs near uncertain cuts. Hard shots can use stronger alignment, but they get the same final review as easy ones.

## What should be saved

A reusable training set should be accompanied by:

- the identity of every source and reference frame;
- the accepted and rejected pairs, with reasons;
- the alignment method used for each accepted pair;
- a visual review sheet;
- file counts and checksums;
- the crop, colour transforms, and frame ranges used in Nuke;
- enough information to return from an output frame to its original source.

These records are not administrative decoration. They are what allows another person to understand where the model learned its result and to remove a bad example later.

## Long references that drift

On a long reference with timing drift, shot changes and difficult foreground motion, start with conservative whole-sequence alignment, then add pairs for under-represented shots without lowering the acceptance standard.

Accepted-pair counts alone are not enough: coverage, source identity, rendered-file integrity and review of moving subjects all have to agree before a dataset is treated as ready. Another film may need fewer pairs, more pairs, or a different balance between sequence-wide and shot-specific models.

## When to train by shot

Begin with a sequence-wide model when the material is reasonably coherent. It offers more examples and is simpler to manage.

Move to shot-level training only after reviewing the sequence result and identifying shots that the shared model cannot represent well. Reuse the already approved pairs for those shots, keep the complete source range for inference, and compare the shot result against the sequence baseline before replacing it.

## A practical rule

Automation may suggest correspondences, align images, and organise files. It should not quietly redefine what counts as truth. Final acceptance remains a restoration decision, supported by visual evidence and recorded so it can be revisited.
