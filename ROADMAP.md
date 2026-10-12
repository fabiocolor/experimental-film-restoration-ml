# Research Roadmap

This roadmap sets out the research questions and practical materials planned for the project.

## Primary track: open-weight colour recovery

- Expand the Qwen Image Edit workflow from still-frame tests to controlled shot-level experiments.
- Repeat the approved same-shot anchor route across films with different motion, faces, materials, and reference quality.
- Compare true paired-data chroma learning with Qwen-guided pseudo-target training while keeping the two evidence classes clearly separated.
- Compare matched references, visual atlases, palette boards, period references, and reference-free prompts.
- Develop clearer safeguards against altered identity, geometry, texture, and lighting.
- Measure colour stability across neighbouring frames and complete shots.
- Publish failures and uncertain results alongside successful examples.
- Add repeatable comparisons with other open-weight image models as they become suitable for preservation work.
- Improve provenance records for prompts, references, model versions, settings, and human decisions.
- Build a cleaner, self-contained ComfyUI version of the shot-level route that runs without my own job system.
- Make a few workflows from the best examples usable on ComfyUI Cloud, so people can try them without their own GPU. This is a goal; it isn't ready yet.

## Continuing track: reference-trained recovery

- Turn the Frontier training-pair research into a production-neutral guide.
- Add a clear example project showing source, reference, accepted pairs, training, inference, and review material.
- Add visual troubleshooting for alignment, unstable references, weak crops, clipping, and checkpoint selection.
- Continue evaluating when a sequence-wide CopyCat model should give way to shot-level models.
- Extend spatial recovery beyond its current experimental status.

## Communication and access

- Keep the website readable for a broad preservation audience while retaining the technical detail needed to understand the methods.
- Add translated editions only after they have been reviewed for technical and cultural accuracy.
- Publish compact downloadable examples that can be studied without access to restricted preservation material.
- Use only footage whose source is clear for public examples (for now, faded trailers from a 35mm trailer reel scan posted on archive.org), and add more as their provenance is confirmed.
