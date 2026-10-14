---
layout: default
title: Preparing Training Pairs
parent: CopyCat Workflow
nav_order: 5
permalink: /automated-dataset-preparation/
grand_parent: "Temporal CbCr"
---

# Preparing Reliable Training Pairs

A reference-trained model can only be as trustworthy as the examples used to teach it. Each training pair should show the same instant and the same image content in both the degraded source and the better reference.

This is simple when two scans come from the same film element. It becomes much harder when the reference is a telecine, broadcast master, home-video release, or another generation with different edits, cadence, framing, distortion, or missing frames.

## What counts as a good pair

A training pair is useful when:

- both images represent the same moment;
- important edges and moving subjects occupy the same positions;
- neither image comes from a fade, dissolve, splice, or unrelated shot;
- the reference contains genuinely better information for the chosen task;
- the alignment has not stretched faces, bodies, or objects into false shapes;
- the pair still agrees after the aligned files are rendered and inspected.

If a pair is uncertain, it should not be used. A smaller honest teaching set is safer than a larger one padded with weak matches.

## A careful preparation sequence

1. **Understand both elements.** Record frame rate, dimensions, pixel shape, field order, reel boundaries, and known editorial differences.
2. **Find broad correspondence.** Establish the overall timing relationship before solving individual shots.
3. **Work shot by shot.** A single offset rarely describes a complete historical transfer.
4. **Try the simplest alignment first.** Translation, scale, rotation, and a modest affine correction are easier to interpret than a complex warp.
5. **Use stronger methods only when they make a clear improvement.** Perspective correction or learned feature matching can help difficult material, but should not be accepted simply because a solver returned an answer.
6. **Render the candidates.** Judge the files the model will actually see, not only the alignment controls.
7. **Check motion and shot boundaries.** Background agreement can hide a moving face, hand, or object that is one frame out of time.
8. **Keep only defensible pairs.** Record rejections instead of filling gaps with generated or interpolated “ground truth.”
9. **Review the whole selection.** Contact sheets and difference views reveal repeated frames, coverage gaps, and outliers that are easy to miss one at a time.

## Why motion needs special attention

Two frames can look almost identical in a static background while a person or foreground object is displaced. That mismatch teaches the network that motion errors are part of the desired restoration.

The Frontier Experience research therefore added checks that pay special attention to moving regions, compare each candidate with neighbouring frames, and reject examples close to uncertain shot boundaries. Difficult shots can use more advanced alignment methods, but they must pass the same final review as easy shots.

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

## The Frontier Experience example

The Frontier Experience project tested this method on a long reference with timing drift, shot changes, and difficult foreground motion. The preparation process began with conservative whole-sequence alignment, then expanded under-represented shots without lowering the acceptance standard.

The example demonstrates why accepted-pair counts alone are not enough: coverage, source identity, rendered-file integrity, and review of moving subjects all have to agree before a dataset is treated as ready. Another film may need fewer pairs, more pairs, or a different balance between sequence-wide and shot-specific models.

## When to train by shot

Begin with a sequence-wide model when the material is reasonably coherent. It offers more examples and is simpler to manage.

Move to shot-level training only after reviewing the sequence result and identifying shots that the shared model cannot represent well. Reuse the already approved pairs for those shots, keep the complete source range for inference, and compare the shot result against the sequence baseline before replacing it.

## A practical rule

Automation may suggest correspondences, align images, and organise files. It should not quietly redefine what counts as truth. Final acceptance remains a restoration decision, supported by visual evidence and recorded so it can be revisited.
