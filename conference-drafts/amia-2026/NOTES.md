# AMIA 2026 — working draft

**15 Nov 2026.** For Fabio’s revision and the requested unmerged draft PR. No printing, email, AMIA upload, site deployment, Review Hub upload or merge. No GitHub Actions. This directory is outside the published site’s `docs/` root.

**Repo choice:** `fabiocolor/experimental-film-restoration-ml` holds the public São Paulo companion, example records and workflow kits. Base: `eb3157c16263b185e6a7c2bea36965e182887210`.

## Files

- `poster.html` → `poster.pdf`: one page, **36 × 36 in / 2592 × 2592 pt**. `poster-preview.png`: 1200 × 1200, rasterised from the PDF.
- `handout.html` → `handout.pdf`: one page, **US Letter / 612 × 792 pt**.
- Edit HTML/CSS directly. Install `requirements.txt`, use Noto Sans, then run `python build.py --chromium /usr/bin/chromium`. `urls.json` supplies QR destinations. The build checks layout and renders locally; it does not publish or run inference.
- `assets.json`: exact source/result locators, frame numbers, hashes, dimensions and approval scope for all eight JPEGs. These are resized draft derivatives, without cropping, grading, retouching or new inference. Exact-luma preservation describes the research master, not resampled JPEGs. No video or masters are committed.

## Abstract and talk sources

[`abstract-v3.md`](abstract-v3.md) preserves the **verbatim submitted abstract**, supplied by the Research Assistant/T3 Bot relay in this conversation. It identifies Fabio’s `abstract_v3_20261017.md`, headed submitted **19 Oct 2026, 01:28 BST**, via SurveyMonkey. Text was supplied, not original file bytes. **No title mismatch:** v3 already carries the accepted title. The 16 Oct “Source-First…” version was not submitted and is unused.

Talk: **The Current Limits of AI in Film Restoration and How They May Be Surpassed**, São Paulo, 8 Oct 2026. Sources: [public companion](https://fabiocolor.github.io/experimental-film-restoration-ml/fiat-ifta-2026-companion/) at the base commit; vault `60_TALKS/Conferences/2026/FIAT 2026 Research Talk Handoff 2026-09-30/deck-v2/`, specifically `FIAT2026_Final_Rehearsal_v15.pptx`, `slides_content.py`, `rehearsal/SCRIPT_v5.md`. The 23-slide v15 package was inspected; references below are presentation order.

| Draft material | Talk reference |
| --- | --- |
| Evidence rule; masking versus recovery | Slide 3; closing “Where the Limits Are Now”; submitted abstract |
| Model limits and costs | Slide 4 and closing section; no new benchmark claims |
| Faded colour / temporal CbCr / Counter Attack | Slides 7–13, especially **11**; companion `#h3-controlnet`, `#temporal-cbcr` |
| El Tinterillo stairs Q47 | Slides **14–15**; called Full Reconstruction under current project names, with generated detail and seam blending declared |
| Selective healing and provenance | Slides 16–19, **principle only**; no restricted footage |
| Local, open workflow direction | Slide 2 and closing section; an integration aim, no finished-app claim |

## Still selection and approvals

| Set | Approved result and source record | Generated content |
| --- | --- | --- |
| **Counter Attack (1976)**, crowd, zero-based frames **74, 112** | **T182**, approved by Fabio 30 Sep 2026; Faded repo `benchmarks/unbalanced/t182_counterattack_contamination_audit_20260929/owner_final_approval_20260930.json`. Registry retains T182 over T179–T181. Master SHA `30263b8566683403d8c3a42e1c29d332b3b8345ed94b7aedad63b9d2c92d17f0`. | Chroma throughout the frame; master keeps original luma. Remaining shadow tint declared. |
| **El Tinterillo**, stairs, one-based frames **80, 480** | **Q47**, approved 26 Sep 2026, submitted revision 1, review `9182b66b`; Full Reconstruction repo `configs/tinterillo_stairs_seam_blend_q47_20260926/REVIEW_DECISION_rev1.json`. Tracker retains Q47 over Q46/older cuts. Lossless SHA `d97854362aea6e8218c559b94f528fb2fe15b262adfc3b200a85d7f381d886f6`. | Whole picture, 768 × 432; tone bridge/dissolves declared. ChatGPT Images reference stills are a cloud step, explicitly stated on both drafts. |

Both master hashes were verified before extraction. Files exist on **JIMINU** and were read there; **no JIMINX access**. Fabio’s 15 Nov request clears both titles for this online artifact. Approvals cover exact outputs only; still inspection supplies no new motion verdict.

**Omitted:** Poison Pen, all other StudioCanal/client material, Mission Kill, Prelinger B&W colourisations. Knights is omitted because its recorded permission is **view-only**, with George Eastman Museum courtesy, while PR/PDF assets are downloadable. Folgers and Wong were allowed but unnecessary. Film images remain their rights holders’ property.

## Checks

`validation.json`: single-page PDFs at exact sizes, zero overflow, all images loaded, **24 pt minimum poster text** (27 pt principal body). Handout body is 10 pt, table 9.5 pt. Both PDF rasters were visually inspected; all four printed QR occurrences decoded correctly. All new files are under 1 MiB. The low-resolution PNG/JPEGs are draft assets, not a production print proof.

All three QR destinations returned **HTTP 200 without authentication**: public workflow repo, public kits, public companion. The four pillar repos were verified **private**; the handout marks their public code URLs unresolved. No private URL is encoded and no sharing setting changed.

## Open questions for Fabio

1. Keep two visual examples, or add a separately cleared selective-healing example? Knights’ view-only permission does not settle downloadable poster use.
2. Which public code URLs should replace the four-private-repos placeholder? Public kits are linked now.
3. Keep Q47’s declared cloud-reference exception, or later use a **newly approved** end-to-end local example?
4. Hard Canny is the current default. Whether historical H3 merged-Canny qualifies remains open in the records; this draft keeps them distinct.
5. Confirm author/affiliation and any additional courtesy wording. No institutional affiliation or logo was assumed.
6. Prelinger colourisations stay excluded unless Fabio explicitly changes the scope.
7. Final copy, higher-resolution cleared derivatives, print/colour proof and AMIA PNG export still need Fabio’s revision. No printer booked or paid.

**Logistics from Fabio’s task:** Poster Session II, **Fri 4 Dec 2026, 12:00–2:00pm**, Pittsburgh. Set up outside the Pavilion; remove by end of day. **36 × 36 in**, self-printed; boards provided, two posters per board, shared 6 ft table, no electricity. AMIA also posts the image publicly online. These facts supersede older call-page dimensions.
