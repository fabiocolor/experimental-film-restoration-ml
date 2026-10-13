# Experimental Film Restoration with Machine Learning

This is where I keep all my research on machine learning for film restoration. It follows one source-first approach: what survives in the film is evidence. I respect it first and let the models fill only what was lost, whether that's the colour that faded, frames that are missing or detail that's gone. None of it is one click, and it's always a restorer who decides what's acceptable and who says what was generated.

**Website:** [fabiocolor.github.io/custom-machine-learning-for-film-restoration/](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/)

## The research, in order

1. **[Colour recovery](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/colour-recovery/)** leads the research. It rescues the original colour of faded film; it isn't colorization. The surviving colour is evidence. Pre-balanced scans are the common case, so I balance first with the [Faded Balancer DCTL](https://github.com/fabiocolor/Faded-Balancer-DCTL) and then recover; balanced and unbalanced scans hold the same dye information. It covers:
   - the neutral-source route, which respects the surviving colour;
   - the [single-frame Qwen Image Edit workflow](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/qwen-color-recovery-app/), with downloads;
   - the Temporal CbCr adapter for whole shots;
   - the reference-trained [CopyCat workflow](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/copycat-workflow/) in Nuke. Its template runs locally in Nuke Non-Commercial or Indie, with your own footage, and is available from the [latest release](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/latest).
2. **[Gap filling and reconstruction](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/gap-filling/)**: rebuilding missing frames, using every surviving element first and generating only inside the gap.
3. **[Dirt removal](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/dirt-removal/)**: [Advanced Dirt Removal](https://github.com/fabiocolor/Advanced-Dirt-Removal), a free macro for DaVinci Resolve (`winget install FabioColor.AdvancedDirtRemoval`).
4. **[Upscaling](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/upscaling/)**: rebuilding picture that is too damaged to restore conventionally. The detail is partly synthetic.

[Where the research stands](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/research-status/) has the full picture as of October 2026: what works, what doesn't yet, and what you can reproduce. On hardware, the Qwen Image Edit workflows need a modern NVIDIA GPU, with 8 GB of VRAM or more for still frames and 16 GB or more for video.

## Colour recovery example

| Faded source | Model output | Final composite |
| --- | --- | --- |
| ![Faded frame from the Reptilicus trailer](docs/images_kebab/seapavaa2026/originals/reptilicus_beach/01_source_reptilicus_tlr_000025-40689881.jpg) | ![Qwen Image Edit output](docs/images_kebab/seapavaa2026/originals/reptilicus_beach/04_inference_frame_000000_seed_0_cfg_1.000_Belak-0c1f0329.png) | ![Final composite on the source brightness](docs/images_kebab/seapavaa2026/originals/reptilicus_beach/05_final_composite_reptilicus_tlr_05_beach_woman_source-38de94d1.png) |

*Reptilicus* (1961) trailer, from a 35mm trailer reel scan posted publicly on [archive.org](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps). The trailer belongs to its rights holders.

## Talks and writing

- Fabio P. Bedoya Huerta, [Exploring Experimental Machine Learning in Film Restoration](https://library.imaging.org/archiving/articles/22/1/35), *Archiving Conference* 22(1), 2025.
- FIAT/IFTA 2026, *The Current Limits of AI in Film Restoration and How They May Be Surpassed*, Cinemateca Brasileira, São Paulo, October 2026: [companion page](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/fiat-ifta-2026-companion/).
- [SEAPAVAA 2026 companion: Advancing Open-Weight AI Models for Color Recovery in Faded Film](https://fabiocolor.github.io/custom-machine-learning-for-film-restoration/seapavaa-2026-companion/).
- [Video walkthrough of the CopyCat chroma-recovery workflow](https://youtu.be/kXerjFGX9Kg).

## Repository guide

- `docs/`: the website, including the downloadable colour-recovery workflow
- `templates/`: the Nuke Indie workflow template (the Non-Commercial version is on the releases page)
- `scripts/`: checks for the downloadable Qwen material

## Responsible use

Generated colour is an interpretation unless supported by a known reference. Keep the original scan, identify all references, show intermediate results, and record the choices that shaped the output. The source and its historical context should remain more authoritative than the model.

## Support

If this research is useful to your work, you can [sponsor it on GitHub](https://github.com/sponsors/fabiocolor) or [support it through PayPal](https://paypal.me/fabiocolor).

## Rights, licences, and attribution

No single licence covers everything referenced in this repository. Original research material, third-party film footage, visual references, model files, and software may each have different owners and terms.

See [Credits & Attribution](docs/credits.md) for the public source record and [Third-Party Notices](THIRD_PARTY_NOTICES.md) for the principal model and software projects. Credit is not permission to reuse third-party material, and this repository does not relicense it.
