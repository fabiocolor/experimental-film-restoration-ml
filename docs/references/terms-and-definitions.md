---
layout: default
title: Glossary
parent: Resources
nav_order: 2
---

# Glossary

Terms used in the research on this site. Standard Nuke node names (`Read`, `Write`, `Merge`, `Transform`, `Crop`, etc.) are not redefined here; consult Foundry documentation for those.

### ACES 2065-1
Linear AP0 scene-referred colour space for archival/exchange masters. Recommended delivery space with EXR half.

### Alignment
Pixel-accurate registration of Reference to Source, including crop, so the two differ only in colour.

### Chroma (Cb, Cr)
Colour-difference channels in YCbCr. In chroma recovery, these come from the Reference branch.

### CopyCat
Nuke node that trains a compact CNN using supervised Input/Target pairs assembled in the node graph.

### F_Align
Furnace alignment operator used as an automated first pass before manual `Transform` refinement.

### Film gauge
Physical film width (16mm, 35mm). Different gauges have distinct spatial characteristics and damage patterns.

### Film generation
Duplication stage (original negative, internegative, print, duplicate). Generational differences affect spatial quality.

### Ground truth (Target)
The desired output used as Target during training. For colour recovery: Source Y + Reference Cb/Cr.

### Hold-out frames
Frame pairs excluded from training, used only for validation.

### Inference
Nuke node that applies a trained `.cat` model to new frames/sequences.

### Internegative
Intermediate negative created from a positive element. Often higher spatial quality than distribution prints.

### Luma (Y)
Brightness channel in YCbCr. In chroma recovery, luma comes from the Source branch.

### MatchGrade
Nuke node for look matching. Used in these workflows as an optional baseline to compare against learned reconstruction.

### Provenance
The written history of a result: the sources, the steps and the settings, so that someone else can check it and run it again.

### Synthetic reference
A colour frame for a shot, made with an open model when no better copy of the film survives and checked at full size. It guides the colour of the shot, and the result is an interpretation.

### Teacher frames
The frames of a shot that pass review and are used to train the Temporal CbCr adapter for that shot.

### Telecine
Video transfer of a film element from earlier preservation workflows. May preserve cleaner sections despite lower resolution.

### Temporal CbCr adapter
A small model, trained for one shot, that learns its colour (Cb and Cr) from teacher frames and carries it through every frame while the scan keeps its own brightness.

### Training pair
A single supervised example: Input (degraded) and Target (ground truth) sharing identical content and alignment.

### YCbCr
Color model separating luma (Y) from chroma (Cb, Cr). Used to construct ground truth by recombining channels from Source and Reference.
