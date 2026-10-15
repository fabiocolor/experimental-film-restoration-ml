# Changelog

All notable changes to this repository are documented here.

## [Unreleased]

### 15 October 2026: whole shots, videos and the current state of the research
- Every area page now opens with a reveal video (the result wiping across the source) and shows its examples as side-by-side videos cut from the approved results, with a different example on the home page: *Obsession* ballroom, *Counter Attack* quarry and waterfront, *Candy Candy*, *Knights of the Trail* (courtesy of the George Eastman Museum, not for download), the *El Tinterillo* reel (FG02, FG03, FG04), and *The General* garden and train. Videos are built by `_hub_work/build_videos.py` from the research store; the web copies are capped at 8 MiB (CI allows that for `docs/media/*.mp4`).
- The stills and videos are shown as delivered, with no log-to-display view: a Cineon-to-Rec.709 view (`tools/examples/viewlut.py`, kept for reference) was tried on the trailer-reel material and made the faded reds look hot.
- The *Counter Attack* waterfront and quarry videos are cut from the approved finals (T148, T157/T158) at 1920 × 1440.
- The research-status page is now "What is possible now": done, open and reproducible, area by area, as of October 2026. New records for *Knights of the Trail*, *Obsession* ballroom and *Counter Attack* quarry; the *General* and *El Tinterillo* records cover their second shots and the reel. Every area page ends with sources and references.
- Every kit graph is now also published laid out with notes (`_ui.json`): the H3 Fun ControlNet step, the Wan VACE second pass and the four stairs windows, built from their API recipes by `tools/examples/api_to_ui.py` and checked in the ComfyUI frontend to give back the identical prompt. The downloads page opens with the two single-frame graphs that run in Comfy Cloud.
- Video: every web comparison is published twice, as AV1 (offered first, about a third smaller) and H.264 (the fallback); only the hero reveal of a page loads on its own, the others start when they scroll into view; and every side-by-side video has a "Look at a frame" button that swaps it for a full-size still pair of the same shot in the compare wipe. `build_videos.py` makes the AV1 twins and tunes the H.264 for film grain.
- Compare wipe: the browser's native image drag no longer captures the pointer.

### 15 October 2026: design, kits, Comfy Cloud
- One stylesheet and one figure grammar for the whole site: every example is a labelled source | result pair with a compare wipe, cut from the published videos and stills (`tools/examples/make_examples.py`); the home page shows different frames from the area pages. Light and dark follow the system setting; the navigation is visible on desktop.
- New single-frame colour-recovery kit: the "Clara" Qwen Image Edit 2511 graph as a laid-out ComfyUI workflow with the composite (source brightness, shadow gate) made inside the graph, in a published-model (fp8mixed) and a Comfy Cloud library (bf16) variant, with the *Counter Attack* test frame, chart, edge map and approved still. The balanced kit's palette still has the same two Cloud-ready variants.
- A downloads index, a record for the *Counter Attack* crowd shot, a hardware table and a reproducibility note on the research-status page.
- CI: the new-file size check compares against the merge base with `main` instead of the first commit (it failed on every new branch); the internal link audit (`tools/site-check/audit_links.py`) runs in CI.

### October 2026: five research areas
- Reorganised the website, README and repository notes around five research areas: Faded Colour Recovery, Temporal CbCr, Diffusion Healing, Diffusion Reconstruction and Black-and-White Colourization.
- Folded the open-weight routes, research routes and Qwen workflow pages into Faded Colour Recovery; the case studies and research-evidence pages into Temporal CbCr and the CopyCat workflow; and the earlier spatial-recovery route into Diffusion Reconstruction. All old URLs redirect.
- Made the CopyCat workflow colour-only.
- Reduced the Tools page to links.
- Kept only the current examples: Reptilicus, Counter Attack, Folgers, Candy Candy, Unman Wittering and Zigo, the Wong flute players and El Tinterillo. The talk pages stay as dated archives.
- The seam-blend kits now read `INPUT_DIR` and `OUTPUT_DIR`.

### Earlier: website and research direction
- Reframed the project around two public research tracks: open-weight colour recovery and reference-trained CopyCat recovery.
- Made Qwen Image Edit the primary current research area, with a dedicated overview, workflow guide, downloads, and links to the SEAPAVAA 2026 evidence.
- Added a confidence-labelled route map separating demonstrated results, promising bounded routes, and unresolved temporal and high-resolution problems.
- Reorganised the website navigation so public research, practical workflows, case studies, and reference material have clear roles.
- Rewrote the automated training-pair page as a clear explanation of the method, evidence, and limits.
- Replaced the blue-purple visual treatment with a restrained warm research-publication design.
- Simplified the website navigation around current research, practical workflows, case studies, and resources.
- Rebuilt and revalidated the downloadable Qwen package with public-facing review guidance.
- Replaced embedded MP4 comparisons with browser-compatible GIFs on the research pages.
- Retired the incomplete translated pages so the public site contains only reviewed documentation.
- Clarified throughout the Qwen material that it is an ongoing research record whose workflows and conclusions will change as evidence develops.

### Added
- Public guide to preparing reliable training pairs from direct film matches and drifting video references, illustrated by the Frontier research.
- Case studies page (`docs/case-studies.md`) covering nine projects: Candy Candy, Beta, PSM, Friends, La Muralla Verde, Frontier Experience, Ben, Rebelion de las Tapadas, and El Gran Tinterillo.
- Comparison GIFs for: Candy Candy, Beta, PSM, Friends, Frontier Experience, Ben, Rebelion de las Tapadas, and El Tinterillo.
- GIF: merge difference alignment check (extracted from video walkthrough).

### Changed
- Restructured documentation: consolidated shared stages (0–2) into `start-here.md`, removed duplication from branch docs.
- Chroma and spatial recovery docs now cover only branch-specific content (Stages 3–5) and link back to shared workflow.
- Organized images into subject folders (per project + `cropped/`, `full/`, `nuke-ui/`, `workflow/`, `resolve-dctl/`, `general/`). Updated all doc references.
- Renamed 54 screenshot-timestamped files and 10 misnamed node-settings files to descriptive kebab-case names.
- Removed Annex A quick-reference sections (redundant with streamlined docs).
- Moved ACES/color management reference into `start-here.md` (single source of truth).
- Trimmed glossary to workflow-specific terms only.
- Reworked the provenance guide into a practical minimum record for published ML-restoration outputs.

## [0.1.0] - 2025-09-24

### Added
- Initial end-to-end workflow materials.
- Nuke Indie template.
- Supporting reference materials under `docs/`.

### Security
- Guidance to keep licensed scans and CopyCat weights out of public downloads and version control.
