---
layout: default
title: CopyCat Workflow
nav_order: 1
has_children: true
permalink: /copycat-workflow/
parent: "Temporal CbCr"
redirect_from:
  - /HOW_TO_USE_RESEARCH_DOCS/
  - /research-evidence/
  - /research-evidence/README/
  - /research-evidence/COPYCAT_CHROMA_METHOD_TRAIL/
  - /research-evidence/DOCUMENTATION_BACKLOG_CHECKPOINT/
---

# The CopyCat workflow

Temporal CbCr with a historical reference, in Nuke. CopyCat trains a small model for one shot or sequence from matching frame pairs: the faded scan, and a better copy of the same moment. The scan keeps its brightness and detail; the model learns only the colour. This is how the [Candy Candy]({{ '/temporal-cbcr/' | relative_url }}) example was made.

The Nuke template runs locally in Nuke Non-Commercial or Nuke Indie, with your own footage.

<div class="hero-buttons">
  <a href="{{ '/start-here/' | relative_url }}" class="btn btn-primary">Start the workflow</a>
  <a href="https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest" class="btn btn-outline">Get the Nuke template</a>
</div>

## The steps

1. Prepare the scan and the reference without creative grading.
2. Align them in time and position.
3. Pick a small set of trustworthy frame pairs.
4. Build a target from the scan's brightness and the reference's colour.
5. Train, and compare checkpoints on frames the model hasn't seen.
6. Run the model over the whole shot and review it.
7. Keep the original scan, the reference, the settings and your review notes with the result.

## In this section

- [Preparation and alignment]({{ '/start-here/' | relative_url }}): getting the scan and the reference ready, picking frame pairs and lining them up.
- [Building the colour target]({{ '/chroma-recovery/' | relative_url }}): the scan's brightness with the reference's colour.
- [Training, inference and review]({{ '/training-inference-review/' | relative_url }}): training, rendering the shot and deciding whether it's acceptable.
- [Preparing training pairs]({{ '/automated-dataset-preparation/' | relative_url }}): what makes a pair trustworthy when the reference is hard to match.
- [Video walkthrough](https://youtu.be/kXerjFGX9Kg) of the workflow, and the [peer-reviewed paper](https://library.imaging.org/archiving/articles/22/1/35) behind it.
