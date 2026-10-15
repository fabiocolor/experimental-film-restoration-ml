---
layout: default
title: Provenance & Metadata
parent: Resources
nav_order: 3
---

# Provenance and Metadata for ML Restoration

## Motivation

If a model touched the picture, whoever comes after should be able to see what was trained, on what, with what settings, and run it again. That is the whole point of the record: a future restorer or an archive can understand the work and check it. A result you can't check is just a nice picture.

## Core Principles

Four things to do every time. Say that a model was involved: tag the output with the tool, the method and the date. Say where the picture came from: the source and reference elements, the scan details, and who gave permission. Say what the model learned from: the shots and frames, the steps, the model size, the checkpoint. And say what kind of recovery it was: colour (with a reference or without one), spatial, or both.

## Minimum public record

For every published result, record:

- the source element and scan used;
- every visual reference and the right to use it;
- the model, workflow, prompt, seed, and relevant settings;
- whether the output is reference-based, reference-free, spatial, chroma-only, or combined;
- the training frames and checkpoint when a project-specific model was trained;
- the processing date and the person or institution that made the final call;
- a plain statement of what is generated interpretation and what is historical evidence.

Keep this record with the output even when the same fields are also written into the image file. Files get converted; sidecars get lost; one of them should survive.

### IPTC Digital Source Type

Tag the output with `trainedAlgorithmicMedia` or `compositeWithTrainedAlgorithmicMedia`, so that anyone reading the file knows a model was involved.

### EXR Metadata (Nuke)

A `ModifyMetaData` node before the `Write` puts the record into the EXR itself, where Resolve and archival systems can read it:

```python
metadata = nuke.nodes.ModifyMetaData()
metadata['metadata'].fromScript("""
  set exr/MLProcessing "CopyCat Color Recovery"
  set exr/RecoveryType "Reference-Based Color"
  set exr/SourceElement "16mm positive print"
  set exr/ReferenceSource "PAL DVD 2003"
  set exr/ModelCheckpoint "checkpoint_60000"
  set exr/IPTCDigitalSourceType "trainedAlgorithmicMedia"
""")
```

### Sidecar files

Keep a small machine-readable record and a plain-language note beside the renders. At minimum, name the source and reference elements, the model and checkpoint, the frames used for training, the processing date, and the person or institution responsible for the restoration decisions.

### Resolve integration

Resolve reads the EXR metadata in its Metadata panel. Map the keys to Description, Scene/Shot/Take, Keywords, Creator, Rights and Dates, and use Batch Change for the fields that are the same across clips.

## Standards context

- The IPTC fields say that AI was involved. What that means for the archive is for its own policy to say.
- C2PA Content Credentials can add signed provenance to the record, where the production system supports them.
