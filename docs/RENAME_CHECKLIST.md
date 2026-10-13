# Rename checklist: custom-machine-learning-for-film-restoration → experimental-film-restoration-ml

Internal note for the planned repository rename. It isn't published (excluded in `_config.yml`). Counts are from a grep of the tracked tree on 13 October 2026 (updated after revision 5), as `file | matches | line numbers`.

**Most important:** GitHub redirects the repository (git URLs, github.com links, issues, releases), but it does **not** redirect GitHub Pages. Every `fabiocolor.github.io/custom-machine-learning-for-film-restoration/...` URL breaks after the rename unless a redirect page is published at the old path. That includes printed QR codes.

## 1. Site configuration
- `docs/_config.yml:9`: `baseurl: "/custom-machine-learning-for-film-restoration"`. Change it to the new name. `url` (line 8) is empty and stays.
- `docs/_config.yml:15`: `aux_links` GitHub URL (GitHub redirects it, but update it anyway).
- `docs/_config.yml:26`: `footer_content` has a hard-coded `/custom-machine-learning-for-film-restoration/` link. It doesn't go through `relative_url`, so it breaks.
- Pages and includes that use `{{ '...' | relative_url }}` follow `baseurl` automatically and need no change.

## 2. Hard-coded references in this repository (38 lines)
| File | Matches | Lines |
|---|---|---|
| `README.md` | 10 | 5, 9, 11, 13, 14, 15, 16, 18, 31, 32 |
| `STATUS.md` | 2 | 41, 42 |
| `THIRD_PARTY_NOTICES.md` | 1 | 7 |
| `docs/HOW_TO_USE_RESEARCH_DOCS.md` | 4 | 16, 17, 44, 138 |
| `docs/_config.yml` | 3 | 9, 15, 26 |
| `docs/copycat-workflow.md` | 1 | 22 |
| `docs/credits.md` | 1 | 49 |
| `docs/fiat-ifta-2026-companion-es.md` | 2 | 23, 384 |
| `docs/fiat-ifta-2026-companion-pt-br.md` | 2 | 23, 384 |
| `docs/fiat-ifta-2026-companion.md` | 2 | 24, 385 |
| `docs/research-evidence/DOCUMENTATION_BACKLOG_CHECKPOINT.md` | 1 | 16 |
| `docs/research-status.md` | 1 | 20 |
| `tools/site-i18n/test-site-i18n.mjs` | 6 | 28, 29, 68, 72, 76, 98 |
| `tools/site-i18n/translate-site.mjs` | 1 | 31 |

What these are:
- Absolute Pages URLs in `README.md`, `STATUS.md` and the two `THIRD_PARTY_NOTICES.md` files: they break after the rename, so update them.
- GitHub URLs in the docs and the FIAT pages: redirected, but update them.
- `tools/site-i18n/*.mjs` contains the old baseurl in tests and config. Update it with the baseurl.
- `docs/research-evidence/DOCUMENTATION_BACKLOG_CHECKPOINT.md:16` mentions the repository name in a historical note.

## 3. Things grep can't see
- **QR codes.** The FIAT/IFTA 2026 deck's slide-2 QR code points to `https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/fiat-ifta-2026-companion/` (recorded in the talk's review notes). `docs/images_kebab/seapavaa2026/custom_machine_learning_for_film_restoration_qr.png` (the SEAPAVAA QR) most likely encodes the old site URL; no QR decoder was available to confirm. Printed QR codes can't change, so keep a redirect page at the old Pages path. One way is to leave a small Pages site in a repository that keeps the old name, with redirect pages for the companion URLs.
- **Nuke Indie template** (`templates/COLOR_RECOVERY_TEMPLATE_INDIE.nkind`): encrypted, so it can't be searched. Check in Nuke whether any notes link to the site.
- **Release notes:** none of the releases of this repository, Advanced-Dirt-Removal or Faded-Balancer-DCTL mention the old name.
- **winget:** the `FabioColor.AdvancedDirtRemoval` package points to the Advanced-Dirt-Removal repository, not this one. No change.
- **Evidence viewer host** (Cloudflare Pages `fiat-ifta-2026-evidence`): CORS allows the origin `https://fabiocolor.github.io` (no path), so it keeps working.
- **Slides and talk notes** in the conference folders: 2 files mention the old URL.
- **Badges:** none reference this repository.
- **Google Drive videos** (FIAT/IFTA companion, Colour Recovery and Upscaling downloads) are linked by Drive file ID, so they keep working after the rename.

## 4. Other repositories (50 lines)

| Repository | Matching lines | Files |
|---|---|---|
| qwen-color-recovery-workflow (private) | 23 | 11 |
| diffusion-reconstruction (private) | 4 | 3 |
| diffusion-upscaling (private) | 3 | 2 |
| restoration-research-lab (private) | 1 | 1 |
| compute job-control repository (private) | 19 | 5 |

Each private README links to the public site, so update those links when the repositories go public. The rest are internal records and job-client configuration; update the configuration so it doesn't keep pointing at the old name. Run `git grep -n custom-machine-learning-for-film-restoration` in each repository for the exact lines.
