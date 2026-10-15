# Experimental Film Restoration with Machine Learning

Research on machine learning for film restoration. What survives in the film is treated as evidence and kept. The models fill only what was lost: faded colour, missing frames and lost picture. The process is not automatic. A restorer decides what is acceptable and records what was generated.

**Website:** [fabiocolor.github.io/experimental-film-restoration-ml/](https://fabiocolor.github.io/experimental-film-restoration-ml/)

## Five research areas

1. **[Faded Colour Recovery](https://fabiocolor.github.io/experimental-film-restoration-ml/colour-recovery/)**: the original colour of faded film, from balanced and unbalanced scans. Examples: *Obsession*, *Counter Attack* (three shots), Folgers, *Juggernaut*. Two kits: a [single-frame graph](https://fabiocolor.github.io/experimental-film-restoration-ml/downloads/colour-recovery-single-frame/) that runs in ComfyUI locally or in Comfy Cloud, and the [balanced-source route](https://fabiocolor.github.io/experimental-film-restoration-ml/downloads/faded-colour-recovery-t185/) end to end.
2. **[Temporal CbCr](https://fabiocolor.github.io/experimental-film-restoration-ml/temporal-cbcr/)**: colour recovery or colourization from a direct historical or synthetic reference, carried through the shot. Examples: *Frontier Experience* and *Candy Candy* (historical reference), *Unman, Wittering and Zigo* (synthetic reference). Includes the [CopyCat workflow](https://fabiocolor.github.io/experimental-film-restoration-ml/copycat-workflow/) for Nuke.
3. **[Diffusion Healing](https://fabiocolor.github.io/experimental-film-restoration-ml/diffusion-healing/)**: nitrate decay, missing frames or emulsion damage, healed while keeping everything that survives. Examples: *Knights of the Trail* (courtesy of the George Eastman Museum) and the Wong flute players.
4. **[Diffusion Reconstruction](https://fabiocolor.github.io/experimental-film-restoration-ml/diffusion-reconstruction/)**: for films beyond repair. Example: a reel of *El Tinterillo*, shot by shot.
5. **[Black-and-White Colourization](https://fabiocolor.github.io/experimental-film-restoration-ml/black-and-white-colourization/)**: colour for panchromatic and orthochromatic film, inferred from the recorded greyscale and the stock's spectral response. Examples: *The General* (1926), *A Trip Down Market Street* (1906) and six other public-domain films of the 1920s.

[What is possible now](https://fabiocolor.github.io/experimental-film-restoration-ml/research-status/) summarises the state of the research as of October 2026: what is done, what is still open, what can be reproduced, and what hardware it takes. Every example has a [record](https://fabiocolor.github.io/experimental-film-restoration-ml/records/) of its source, models, settings and approval; the [download kits](https://fabiocolor.github.io/experimental-film-restoration-ml/downloads/) reproduce four of them from the published files. The [tools](https://fabiocolor.github.io/experimental-film-restoration-ml/tools/) used alongside the research have their own repositories.

## Faded colour recovery example

| Faded source | Model output | Final composite |
| --- | --- | --- |
| ![Faded frame from the Reptilicus trailer](docs/images_kebab/seapavaa2026/originals/reptilicus_beach/01_source_reptilicus_tlr_000025-40689881.jpg) | ![Qwen Image Edit output](docs/images_kebab/seapavaa2026/originals/reptilicus_beach/04_inference_frame_000000_seed_0_cfg_1.000_Belak-0c1f0329.png) | ![Final composite on the source brightness](docs/images_kebab/seapavaa2026/originals/reptilicus_beach/05_final_composite_reptilicus_tlr_05_beach_woman_source-38de94d1.png) |

*Reptilicus* (1961) trailer, from a 35mm trailer reel scan posted publicly on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps). The trailer belongs to its rights holders.

The examples are workflow demonstrations, not finished restorations.

## Talks and writing

- Fabio P. Bedoya Huerta, [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35), *Archiving Conference* 22(1), 2025.
- FIAT/IFTA 2026, *The Current Limits of AI in Film Restoration and How They May Be Surpassed*, Cinemateca Brasileira, São Paulo, October 2026: [companion page](https://fabiocolor.github.io/experimental-film-restoration-ml/fiat-ifta-2026-companion/).
- [SEAPAVAA 2026 companion: Advancing Open-Weight AI Models for Color Recovery in Faded Film](https://fabiocolor.github.io/experimental-film-restoration-ml/seapavaa-2026-companion/).
- [Video walkthrough of the CopyCat workflow](https://youtu.be/kXerjFGX9Kg).

## Repository guide

- `docs/`: the website (Jekyll, Just the Docs), including the download kits in `docs/downloads/` and one record per example in `docs/records/`
- `templates/`: the Nuke Indie template for the CopyCat workflow (the Non-Commercial version is on the [releases page](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest))
- `tools/site-check/`: the link and asset audit that runs in CI; `tools/examples/`: how the example figures were cut from the published videos
- Files over 1 MiB are not added to the repository; they go on the [examples release](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/tag/examples-2026-10) and are linked.

## Building the site locally

```
cd docs
bundle install
bundle exec jekyll serve
```

The site builds with the `github-pages` gem (Jekyll 3.10), the same as GitHub Pages. `python3 tools/site-check/audit_links.py . --strict` checks every internal link and asset without a build.

## Responsible use

Generated colour or picture is an interpretation unless a known reference backs it up. Keep the original scan, name your references, show the in-between results and note the choices you made. The source takes priority over the model.

## Support

If this research is useful to your work, you can [sponsor it on GitHub](https://github.com/sponsors/fabiocolor) or [support it through PayPal](https://paypal.me/fabiocolor).

## Rights, licences, and attribution

No single licence covers everything here. Original material, third-party footage, references, models and software each have their own owners and terms.

See [Credits & Attribution](docs/credits.md) for the public source record and [Third-Party Notices](THIRD_PARTY_NOTICES.md) for the principal model and software projects. Credit is not permission to reuse third-party material, and this repository does not relicense it.
