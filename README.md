# Experimental Film Restoration with Machine Learning

This is where I keep my research on machine learning for film restoration. What survives in the film is evidence: I respect it first and let the models fill only what was lost, whether that's the colour that faded, frames that are missing or picture that's gone. None of it is one click, and it's always a restorer who decides what's acceptable and who says what was generated.

**Website:** [fabiocolor.github.io/custom-machine-learning-for-film-restoration/](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/)

## Five research areas

1. **[Faded Colour Recovery](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/colour-recovery/)**: the original colour of faded film, from balanced and unbalanced scans. Examples: *Counter Attack*, Folgers. Download kit for balanced scans included.
2. **[Temporal CbCr](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/temporal-cbcr/)**: colour recovery or colourization from a direct historical or synthetic reference, carried through the shot. Examples: *Candy Candy* (historical reference), *Unman, Wittering and Zigo* (synthetic reference). Includes the [CopyCat workflow](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/copycat-workflow/) for Nuke.
3. **[Diffusion Healing](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/diffusion-healing/)**: full-frame damage or missing frames, healed while keeping most of the original. Example: the Wong flute players.
4. **[Diffusion Reconstruction](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/diffusion-reconstruction/)**: for films beyond repair. Example: the *El Tinterillo* stairs.
5. **[Black-and-White Colourization](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/black-and-white-colourization/)**: colour for panchromatic and orthochromatic film, inferred from the recorded greyscale and the stock's spectral response.

[Where the research stands](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/research-status/) has the full picture as of October 2026: what works, what doesn't yet, and what you can try yourself. The [tools](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/tools/) I use alongside the research have their own repositories.

## Faded colour recovery example

| Faded source | Model output | Final composite |
| --- | --- | --- |
| ![Faded frame from the Reptilicus trailer](docs/images_kebab/seapavaa2026/originals/reptilicus_beach/01_source_reptilicus_tlr_000025-40689881.jpg) | ![Qwen Image Edit output](docs/images_kebab/seapavaa2026/originals/reptilicus_beach/04_inference_frame_000000_seed_0_cfg_1.000_Belak-0c1f0329.png) | ![Final composite on the source brightness](docs/images_kebab/seapavaa2026/originals/reptilicus_beach/05_final_composite_reptilicus_tlr_05_beach_woman_source-38de94d1.png) |

*Reptilicus* (1961) trailer, from a 35mm trailer reel scan posted publicly on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps). The trailer belongs to its rights holders.

The examples are workflow demonstrations, not finished restorations.

## Talks and writing

- Fabio P. Bedoya Huerta, [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35), *Archiving Conference* 22(1), 2025.
- FIAT/IFTA 2026, *The Current Limits of AI in Film Restoration and How They May Be Surpassed*, Cinemateca Brasileira, São Paulo, October 2026: [companion page](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/fiat-ifta-2026-companion/).
- [SEAPAVAA 2026 companion: Advancing Open-Weight AI Models for Color Recovery in Faded Film](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/seapavaa-2026-companion/).
- [Video walkthrough of the CopyCat workflow](https://youtu.be/kXerjFGX9Kg).

## Repository guide

- `docs/`: the website, including the download kits in `docs/downloads/`
- `templates/`: the Nuke Indie template for the CopyCat workflow (the Non-Commercial version is on the [releases page](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/latest))

## Responsible use

Generated colour or picture is an interpretation unless supported by a known reference. Keep the original scan, identify all references, show intermediate results, and record the choices that shaped the output. The source and its historical context should remain more authoritative than the model.

## Support

If this research is useful to your work, you can [sponsor it on GitHub](https://github.com/sponsors/fabiocolor) or [support it through PayPal](https://paypal.me/fabiocolor).

## Rights, licences, and attribution

No single licence covers everything referenced in this repository. Original research material, third-party film footage, visual references, model files, and software may each have different owners and terms.

See [Credits & Attribution](docs/credits.md) for the public source record and [Third-Party Notices](THIRD_PARTY_NOTICES.md) for the principal model and software projects. Credit is not permission to reuse third-party material, and this repository does not relicense it.
