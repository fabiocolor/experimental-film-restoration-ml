# Experimental Film Restoration with Machine Learning

Research on machine learning for film restoration. What survives in the film is treated as evidence and kept. The models fill only what was lost: faded colour, missing frames and lost picture. The process is not automatic. A restorer decides what is acceptable and records what was generated.

**Website:** [fabiocolor.github.io/experimental-film-restoration-ml/](https://fabiocolor.github.io/experimental-film-restoration-ml/)

## Five research areas

1. **[Faded Colour Recovery](https://fabiocolor.github.io/experimental-film-restoration-ml/colour-recovery/)**: the original colour of faded film, from balanced and unbalanced scans. Examples: *Counter Attack*, Folgers. Download kit for balanced scans included.
2. **[Temporal CbCr](https://fabiocolor.github.io/experimental-film-restoration-ml/temporal-cbcr/)**: colour recovery or colourization from a direct historical or synthetic reference, carried through the shot. Examples: *Frontier Experience* and *Candy Candy* (historical reference), *Unman, Wittering and Zigo* (synthetic reference). Includes the [CopyCat workflow](https://fabiocolor.github.io/experimental-film-restoration-ml/copycat-workflow/) for Nuke.
3. **[Diffusion Healing](https://fabiocolor.github.io/experimental-film-restoration-ml/diffusion-healing/)**: full-frame damage or missing frames, healed while keeping most of the original. Example: the Wong flute players.
4. **[Diffusion Reconstruction](https://fabiocolor.github.io/experimental-film-restoration-ml/diffusion-reconstruction/)**: for films beyond repair. Example: the *El Tinterillo* stairs.
5. **[Black-and-White Colourization](https://fabiocolor.github.io/experimental-film-restoration-ml/black-and-white-colourization/)**: colour for panchromatic and orthochromatic film, inferred from the recorded greyscale and the stock's spectral response. Examples: seven public-domain films from 1921–1929, including *Her Boy Friend*, *The Wildcat* and *Rambles 'Round Rio*.

[Where the research stands](https://fabiocolor.github.io/experimental-film-restoration-ml/research-status/) summarises the state of the research as of October 2026: what works, what does not yet, and what can be reproduced. The [tools](https://fabiocolor.github.io/experimental-film-restoration-ml/tools/) used alongside the research have their own repositories.

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

- `docs/`: the website, including the download kits in `docs/downloads/`
- `templates/`: the Nuke Indie template for the CopyCat workflow (the Non-Commercial version is on the [releases page](https://github.com/fabiocolor/experimental-film-restoration-ml/releases/latest))

## Responsible use

Generated colour or picture is an interpretation unless a known reference backs it up. Keep the original scan, name your references, show the in-between results and note the choices you made. The source takes priority over the model.

## Support

If this research is useful to your work, you can [sponsor it on GitHub](https://github.com/sponsors/fabiocolor) or [support it through PayPal](https://paypal.me/fabiocolor).

## Rights, licences, and attribution

No single licence covers everything here. Original material, third-party footage, references, models and software each have their own owners and terms.

See [Credits & Attribution](docs/credits.md) for the public source record and [Third-Party Notices](THIRD_PARTY_NOTICES.md) for the principal model and software projects. Credit is not permission to reuse third-party material, and this repository does not relicense it.
