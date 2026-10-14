# Changelog

All notable changes to this repository are documented here.

## [Unreleased]

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
