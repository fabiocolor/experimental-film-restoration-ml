---
layout: default
title: How to Use These Docs
nav_order: 0
parent: Resources
---

# How to Use These Research Docs

This guide helps you navigate the documentation for the Experimental Film Restoration with Machine Learning project. It is written for film archives, restoration practitioners, colourists, researchers, and students who want to understand what has worked, what has not, and how to decide whether a method is right for their material.

## Recommended reading order

Start with the overview documents, then move into the specific workflow you need:

1. **[STATUS.md](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/blob/main/STATUS.md)** — Current project scope and research status
2. **[README.md](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/blob/main/README.md)** — Repository overview and quick links
3. **[Start Here]({% link start-here.md %})** — Shared workflow preparation and alignment stages
4. **[CopyCat Workflow]({% link copycat-workflow.md %})** — Overview of the reference-trained recovery method
5. **Branch-specific guides:**
   - **[Chroma Recovery]({% link chroma-recovery.md %})** — When colour has faded but detail remains
   - **[Spatial Recovery]({% link spatial-recovery.md %})** — When detail is lost but colour remains
6. **[Training, Inference, and Review]({% link training-inference-review.md %})** — The training and rendering stages
7. **[Case Studies]({% link case-studies.md %})** — Real-world examples with decisions and limitations
8. **[Provenance and Metadata]({% link provenance-metadata.md %})** — Recording how results were made

## Two research tracks

This repository documents two connected approaches:

### Reference-trained recovery (CopyCat workflow)

The **established research track**. This method trains a small neural network on aligned source/reference pairs to recover chroma or spatial detail in Nuke. The template runs locally in Nuke Non-Commercial or Nuke Indie, with your own footage.

**Start here if you:**
- Have a faded film and a colour reference (DVD, telecine, alternate print)
- Want to recover colour while preserving original film detail and grain
- Have access to Nuke with CopyCat (the template is for Nuke Non-Commercial or Nuke Indie)
- Want a documented, repeatable workflow to run on your own footage

**Key resources:**
- [CopyCat Workflow]({% link copycat-workflow.md %})
- [Case Studies]({% link case-studies.md %})
- [Nuke template for Non-Commercial and Indie (latest release)](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/latest)

### Open-weight colour recovery (Qwen Image Edit)

The **current research area**. This method uses open models like Qwen Image Edit to propose colour while preserving the source frame's luminance, texture, and photographic structure.

**Start here if you:**
- Want to experiment with generative AI for colour recovery
- Are comfortable with ComfyUI and Python workflows
- Understand that this is active research, not a finished product
- Want to follow transparent, reproducible experiments

**Key resources:**
- [Open-Weight Colour Recovery]({% link open-weight-color-recovery.md %})
- [Qwen Image Edit Workflow]({% link qwen-color-recovery-app.md %})
- [SEAPAVAA 2026 Companion]({% link seapavaa-2026-companion.md %})

**Important:** The Qwen material in this public repository is documentation and workflow guidance. For detailed experiment registries and decision trails on open-weight colour recovery research, see the related private repository: [fabiocolor/qwen-color-recovery-workflow](https://github.com/fabiocolor/qwen-color-recovery-workflow) (access restricted).

## Learning from decisions: what worked, what failed, and why

The case studies and workflow pages are written to teach judgment, not just procedures. When starting a CopyCat recovery project, look for:

### What worked
- **Candy Candy:** Shot-specific models outperformed sequence models when motion became complex
- **Candy Candy / Beta:** SD DVD and Betacam references worked well for chroma recovery because CopyCat learns colour mapping, not spatial detail
- **Reference alignment:** Cropping to the valid reference area (excluding borders and subtitles) improved training stability
- **Highlight management:** Clamping highlights before training prevented artifacts and improved convergence

### What failed or had limits
- **Frontier Experience:** Sequence-level models struggled with varied lighting (interiors vs. exteriors, day vs. night)
- **Reference quality:** Higher resolution does not always mean better reference — a compressed DVD can be better than a badly transferred HD source if colour is intact
- **Alignment:** Gate weave and parallax on warped references required manual keyframing, which is time-consuming
- **Spatial recovery from SD video:** Telecine references preserve some spatial information but introduce cropping, softness, and interlacing artifacts

### Key decision points

**When starting a chroma recovery:**
- Is your reference good enough? Check whether it preserves colour information, not just resolution
- Does your source need pre-balancing? Use tools like Faded Balancer DCTL to reduce severe magenta casts before training
- Should you train shot-specific or sequence-specific models? Start sequence-level; switch to shot-level when lighting or motion varies too much
- Are highlights causing problems? Clamp them before training to prevent the model from learning incorrect colour relationships in blown-out areas

**When reviewing results:**
- Compare held-out frames (not part of the training set) at each checkpoint
- Watch for memorisation: if the model reproduces training frames perfectly but fails on adjacent frames, add more diverse pairs
- Check transitions, first/last frames, and shot boundaries carefully
- If a sequence-level model fails on specific shots, train dedicated models for those sections

## Cross-references to related research

This project is part of a broader research portfolio. For context on related work:

### Private research repositories
- **Colour recovery experiments:** [fabiocolor/qwen-color-recovery-workflow](https://github.com/fabiocolor/qwen-color-recovery-workflow) — Detailed experiment registry, decision trails, and evidence evaluation for open-weight colour recovery (access restricted)
- **Temporal processing:** fabiocolor/temporal-cbcr-adapter — Temporally consistent chroma processing; CopyCat is a related historical baseline (access restricted)
- **Upscaling and reconstruction research** — Related diffusion-based methods (repositories not yet public)

### How CopyCat fits the research landscape
CopyCat is a reference-trained supervised learning method: it requires aligned pairs of degraded source and better reference. This makes it practical when references exist (DVDs, telecines, alternate prints), but unsuitable when no reference survives.

The open-weight Qwen research explores generative methods that can propose colour without direct frame-matched references. These are complementary approaches, not replacements.

## Using case studies as reusable trails

The [Case Studies]({% link case-studies.md %}) page documents real projects with their specific decisions, failures, and lessons. When planning your own work:

1. **Find a similar case:** Look for projects with similar source material, degradation type, or reference quality
2. **Read the "Key decisions" sections:** These explain why certain choices were made and what alternatives were rejected
3. **Note the limitations:** Every case has documented problems or unresolved issues — learn from them
4. **Check the reference type:** Matched references (DVD, telecine) vs. constructed references (Photoshop, historical paintings) require different expectations

For deeper technical trails on specific methods, see the [Research Evidence]({% link research-evidence/README.md %}) folder.

## Documentation scope and authority

**These docs teach you how to:**
- Prepare aligned source/reference pairs for CopyCat training
- Decide between chroma and spatial recovery
- Select training frames and build ground-truth targets
- Evaluate checkpoints and troubleshoot common problems
- Record provenance and metadata for archival delivery

**These docs do NOT:**
- Authorize new training runs or inference jobs without human review
- Replace archival policies or ethical oversight
- Provide finished "one-click" restoration products
- Act as experiment registries for private research (see related repositories above)

Generated colour is an interpretation unless supported by a known reference. Always keep the original scan, record all decisions, and involve archivists, colourists, or historians who understand the film's production context.

## Getting help

This is independent research, not a commercial product. Community support happens through:
- **GitHub Issues:** [Report bugs or documentation problems](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/issues)
- **GitHub Discussions:** Ask questions about the workflow or share your results
- **Publications:** Read the [peer-reviewed paper](https://library.imaging.org/archiving/articles/22/1/35) for research context

For Nuke/CopyCat technical support, consult Foundry's official documentation.

## Additional resources

- [Automated Dataset Preparation]({% link automated-dataset-preparation.md %}) — Reel-, shot-, and frame-level alignment with strict pair rejection
- [Additional Resources]({% link additional-resources.md %}) — Background on digitization, dye fade, and colour science
- [Terms and Definitions]({% link references/terms-and-definitions.md %}) — Glossary of technical terms
- [Credits and Attribution]({% link credits.md %}) — Source material, contributors, and third-party notices

---

*Last updated: 2026-09-14*
