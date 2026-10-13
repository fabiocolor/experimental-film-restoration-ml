---
layout: default
title: Case Studies
nav_order: 3
parent: Colour Recovery
---

# Case Studies

Real-world applications of the CopyCat workflow across different film stocks, gauges, degradation types, and reference sources. Each case demonstrates a different challenge and strategy within the same core method.

> For a peer-reviewed discussion of these experiments, see: Bedoya Huerta, F.P. (2025). [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35). *Archiving Conference*, 22(1), 35.

Rights, source context, software, and contributor information is collected on the [Credits & Attribution]({{ '/credits/' | relative_url }}) page.

I've taken the frames off this page for now, until I've checked that each film can be shown publicly. The notes on each project are still here.

---

## Candy Candy (1976)

**Branch:** Chroma Recovery | **Gauge:** 16mm positive print | **Reference:** PAL DVD (French release)


| Field | Details |
|---|---|
| **Director** | Hiroshi Shidara |
| **Problem** | Severe magenta dominance from dye fading. Green and blue channels retain most information; red/cyan layers heavily degraded. Significant flicker concentrated on the red channel. |
| **Reference** | 33 frames extracted from a French PAL DVD set (MPEG-2/MKV → AV1/MP4 via Handbrake for deinterlacing, then imported into Resolve). Standard definition with compression artifacts, but intact color. DVD frame has less image area than the 16mm scan, different warping, and occasional subtitle burn-ins. |
| **Approach** | Reference-based chroma recovery. 33 degraded + 33 DVD reference pairs. Phoenix & Loki (Filmworkz) for cleaning; NukeX CopyCat for color transfer. Pre-balancing with Faded Balancer DCTL to reduce channel imbalance before training. Highlights clamped before training to prevent artifacts and improve convergence. |
| **Key decisions** | The DVD reference is SD, which is acceptable because CopyCat learns colour mapping (Cb/Cr), not spatial detail. The 16mm source was cropped to the valid reference area so CopyCat did not learn black borders. Shot-specific models outperformed a single sequence-level model when motion became too complex. |
| **Result** | Successfully replicated DVD colors onto 16mm while preserving original film resolution and grain structure. Established a reusable working method for reference alignment, frame selection, and highlight management. |

### What worked
- **SD DVD as colour reference:** Resolution mismatch did not matter because CopyCat learns colour (CbCr), not spatial detail
- **Pre-balancing with Faded Balancer DCTL:** Neutralized magenta cast and improved training convergence
- **Cropping to valid reference area:** Prevented model from learning borders and subtitles
- **Highlight clamping:** Reduced artifacts in bright areas by preventing the model from learning incorrect colour relationships in blown highlights
- **Shot-specific pivot:** When sequence model failed on complex motion, switching to shot-level models (4–9 pairs per shot) rescued the result

### What failed or had limits
- **Sequence-level model on complex motion:** Could not generalize across fast pans and varied character movement
- **Manual alignment:** DVD framing differences required time-consuming manual Transform keyframing
- **Subtitle handling:** Frames with burned-in subtitles required animated crops or exclusion from training

### Reuse and skip guidance
**Reuse this pattern when:**
- Source has intact detail but faded colour
- Reference is SD video (DVD, VHS, Betacam) with good colour integrity
- You can invest time in alignment and shot-specific training if needed

**Skip or adapt when:**
- Source has lost spatial detail (wrong branch — use spatial recovery)
- Reference colour is worse than source
- You cannot align due to parallax or geometric distortion

**For full decision trail:** See [Candy Candy Chroma Recovery Trail]({% link research-evidence/CANDY_CANDY_CHROMA_COPYCAT.md %})


---

## Beta

**Branch:** Chroma Recovery | **Gauge:** Film print | **Reference:** Beta tape / earlier video reference


| Field | Details |
|---|---|
| **Problem** | Faded print with yellow skew, flicker, blue dust, ghosting, and blue-channel loss. |
| **Reference** | An earlier video state of the film (beta tape) created closer to the original period. Lower quality and compressed, but preserves most color information. |
| **Approach** | Standard reference-based chroma recovery in Resolve + Nuke/CopyCat. Source balanced and lightly cleaned before training. Reference placed into a `2048x858` container from its native `720x576` to reduce alignment problems. Training target keeps source luminance and replaces chroma with beta reference in YCbCr space. |
| **Key decisions** | Work began sequence by sequence, then moved shot by shot where the broader model was insufficient. The Beta tape was accepted as a colour reference despite compression, following the same reasoning as the Candy Candy DVD. |
| **Result** | Color recovered from the beta reference while preserving the film scan's spatial detail. Both sequence-level and shot-level methods validated. |

### What worked
- **Betacam as colour reference:** Despite compression and low resolution, the tape preserved usable colour information
- **Container approach:** Placing 720×576 reference into 2048×858 container reduced alignment problems
- **Sequence-to-shot progression:** Starting broad, then training shot-specific models for problem areas

### Reuse and skip guidance
**Reuse this pattern when:** Your reference is archived video (Betacam, VHS, U-matic) with better colour than the film scan.

**Skip when:** Video reference has severe banding, posterization, or baked-in creative grades that don't match source intent.


---

## PSM

**Branch:** Chroma Recovery | **Gauge:** Film (720x576 source, 2048x858 container) | **Reference:** Betacam


| Field | Details |
|---|---|
| **Problem** | Faded Indian film with color degradation. Source at 720x576, placed into a 2048x858 container for alignment. |
| **Reference** | Betacam tape from an earlier video state that preserves colour information. |
| **Approach** | Mixed chroma and luma experimentation. Multiple dedicated training runs explored color recovery, chroma plus luma, luma extension, and reference luma. Training checkpoints ranged from 40,000 to 160,000 steps. This was the earliest experimental case in the series and established the iterative training method later used for Beta. |
| **Key decisions** | Tested both chroma-only and combined chroma+luma output stages. Multiple branch structures (`COLOR_RECOVERY`, `CHROMA_LUMA`, `LUMA_EXTEND`, `REF_LUMA`) confirm this was not a single-pass experiment but an iterative exploration of different recovery strategies. |
| **Result** | Produced about 70 seconds of test material in both chroma-only and combined modes. This showed that the same CopyCat workflow could explore several recovery strategies on one source. |


---

## Friends (2001)

**Branch:** Chroma Recovery | **Gauge:** Film/video | **Reference:** Direct color reference


| Field | Details |
|---|---|
| **Problem** | Color damage with significant cast shifts across scenes. |
| **Approach** | Standard reference-based chroma recovery workflow. Direct reference with intact color data used for supervised training pairs. Grouped with Frontier Experience as a straightforward direct-reference case. |
| **Result** | Successful color recovery with natural skin tones and consistent scene-to-scene color. |


---

## La Muralla Verde

**Branch:** Chroma Recovery | **Reference:** DVD and DCP material


| Field | Details |
|---|---|
| **Problem** | Faded source with magenta shift requiring both traditional balancing and ML-assisted recovery. |
| **Reference** | DVD and recent DCP material used as color references. |
| **Approach** | Full workflow: raw scan → Faded Balancer DCTL for initial rebalancing → reference preparation and alignment in Resolve → CopyCat training → inference rendering. Custom balancing tools were tested before and alongside the machine-learning stage. |
| **Result** | Mature project with exported script overviews, contact sheets, comparisons, and output frames. Demonstrates the complete Resolve → Nuke → Resolve validation loop. |


---

## Frontier Experience (1975)

**Branch:** Chroma Recovery | **Gauge:** Film print | **Reference:** Telecine (archival secondary source)


| Field | Details |
|---|---|
| **Director** | Barbara Loden |
| **Problem** | Faded surviving print with lost chroma information. |
| **Reference** | Telecine supplied by Ross Lipman. Had cadence issues but stayed aligned enough to remain usable as a chroma guide. |
| **Approach** | Standard reference-based chroma recovery. Telecine used only as a source of demonstrable color evidence, not as a spatial reference. Important because it uses a standard archival secondary source rather than artwork or a consumer DVD. |
| **Key challenge** | Difficult sky and shadow areas may need either more training frames or segmentation by scene groups (interiors vs. exteriors). |
| **Result** | Structurally convincing result. Some skies and shadows do not fully resolve, pointing to the limits of sequence-level models on varied lighting conditions. |

### What worked
- **Telecine as archival colour reference:** Standard archival secondary source provided demonstrable colour evidence
- **Basic alignment:** Despite cadence issues, reference stayed aligned enough to train

### What failed or had limits
- **Sequence model on varied lighting:** Model struggled with skies, shadows, and interior/exterior transitions
- **Single model for mixed conditions:** Day vs. night and interior vs. exterior exceeded what one model could generalize

### Reuse and skip guidance
**Reuse this pattern when:** You have archival telecine with acceptable colour and limited cadence problems.

**Expect limits when:** Lighting varies significantly (day/night, interior/exterior). Plan for scene-group segmentation or shot-specific models.

**Learning:** This case teaches the stopping rule for sequence models. When held-out frames show persistent failures in specific conditions (skies, shadows, lighting transitions), segment by scene type rather than forcing one model to learn everything.


---

## Ben

**Branch:** Chroma Recovery (Constructed Reference) | **Reference:** Photoshop-created references


| Field | Details |
|---|---|
| **Problem** | Source material lacks a direct color reference (no DVD, telecine, or alternate print). |
| **Reference** | Color references manually constructed in Photoshop using Neural Filters (Colorize). Shot-specific reference frames built rather than a single global reference. |
| **Approach** | Non-reference / operator-assisted recovery. Each shot gets its own Photoshop-created reference frame. Contact sheets and comparison passes validate the result across multiple shots. Grouped with Rebelion de las Tapadas as a constructed-reference workflow. |
| **Result** | Reached comparison-ready output stage with 4-way comparisons and a finished output. Demonstrates that when no historical reference survives, operator-constructed references can still drive CopyCat training. |



---

## Rebelion de las Tapadas (1943)

**Branch:** Chroma Recovery (Non-Reference) | **Gauge:** 35mm positive | **Reference:** Colonial-era watercolor paintings


| Field | Details |
|---|---|
| **Director** | Nelson Garcia Miranda |
| **Problem** | Advanced vinegar syndrome, strong magenta shift, heavy blue-channel loss, and significant physical damage. No direct reference survives: no DVD, telecine, or alternate print. |
| **Reference** | Colonial-era artwork associated with the visual culture of the film, including work by Johann Moritz Rugendas and Pancho Fierro. |
| **Approach** | Non-reference recovery. One-light balancing pass to reduce magenta cast. DVO Steady for stabilization. RGB flicker removal (material behaves as duotone). Manual clone/paint for heavy defects. CopyCat trained on curated historical paintings to learn plausible period color relationships and texture behavior. |
| **Key decisions** | Some source images in the film are intentionally black and white, so the model had to learn what *not* to colourise. The output is presented as a plausible reconstruction rather than a faithful recovery. All assumptions are documented. |
| **Result** | Recovered color while keeping visible film texture. Demonstrates that artwork can function as a constrained visual reference when direct color reference does not survive. |


---

## El Gran Tinterillo (1975)

**Branch:** Spatial Recovery (Analog Video Reference) | **Gauge:** 16mm | **Reference:** Analog telecine



| Field | Details |
|---|---|
| **Problem** | 16mm film with severe damage, warping, cropping issues, and limited recoverable spatial data. The telecine preserves spatial data lost in the film print, but introduces its own artifacts: cropping, limited detail, mask movement, interlacing defects. |
| **Reference** | Analog video telecine made closer to the film's original life. |
| **Approach** | Two-step analogue video reference recovery. The first model trained on the least-damaged sections where both sources overlap and learned the spatial relationship. The second model uses those results to restore the full film frame. The telecine is a guide rather than a direct replacement because it is too cropped and soft for direct telecine-to-film recovery. |
| **Key decision** | Tested in both directions: telecine-to-16mm and 16mm-to-telecine. Both produced results, demonstrating the bidirectional nature of the concept. |
| **Status** | Proof of concept. Two-step approach produced more convincing full-frame results than direct transfer. Damage and haze reduced while keeping the full 16mm frame instead of collapsing to telecine bounds. Typical spatial recovery artifacts remain. |


---

The examples above use different kinds of evidence, from matched video references to constructed and multi-element targets. The [CopyCat workflow overview]({{ '/copycat-workflow/' | relative_url }}) explains how those reference types fit the two recovery branches.

*See also: [Shared Workflow]({{ '/start-here/' | relative_url }}) | [Chroma Recovery]({{ '/chroma-recovery/' | relative_url }}) | [Spatial Recovery]({{ '/spatial-recovery/' | relative_url }})*
