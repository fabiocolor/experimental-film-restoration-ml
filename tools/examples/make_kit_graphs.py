"""Build the inspectable UI-format graphs of the download kits from their API-format recipes, with the
notes that say what each graph does and what should and should not happen on the footage.
Run from the repository root with a ComfyUI object_info.json (python3 tools/examples/make_kit_graphs.py object_info.json).
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from api_to_ui import convert

oi = json.load(open(sys.argv[1]))
D = Path(__file__).resolve().parents[2] / 'docs/downloads'

GPU = ('Hardware', 'This is a **video** step: MiniMax H3 at 768 × 576 for 124 frames wants an NVIDIA card with 24 GB of VRAM '
       'or more (RTX 3090/4090; 32 GB on an RTX 5090 is comfortable) and 64 GB of system RAM, and takes 20 to 45 minutes a section. '
       'It opens in Comfy Cloud for reading, but running it there is a paid, long job; the single-frame graphs are the ones meant for Cloud.')

# 1. Balanced-source kit, step 2: H3 with the Fun ControlNet ----------------------------------------
convert(D / 'faded-colour-recovery-t185/graphs/2_h3_fun_controlnet_local.json',
        D / 'faded-colour-recovery-t185/graphs/2_h3_fun_controlnet_ui.json', oi,
        titles={'1': '1 · Source section (context.mp4)', '20': '2 · Edge-map video (control.mp4)', '3': '3 · Palette still (picture 1)',
                '18': '3 · Palette still (picture 2)', '19': '3 · Palette still (picture 3)', '4': 'MiniMax H3 (ref2va, int8)',
                '5': 'Text encoder (Qwen3-VL 32B, NVFP4)', '6': 'Video VAE', '7': 'Audio VAE', '22': 'Fun ControlNet Union',
                '23': 'Apply ControlNet (edges, strength 1.0)', '8': 'Reference to video: prompt, 768 × 576 × 124', '13': 'Sample (20 steps)',
                '17': 'Colour donor video'},
        notes=[
            ('Step 2 of the balanced-source route: carry the colour through the shot',
             '## What this graph does\n\n'
             'One approved colour frame (the **palette still** from step 1) is carried through a 124-frame section of the shot by **MiniMax H3** '
             'in reference-to-video mode, with Alibaba\'s **Fun ControlNet** holding the model to the edge map of every frame.\n\n'
             '**Inputs.** `context.mp4`: the source section, 768 × 576, 24 fps, 124 frames. `control.mp4`: its Canny edge map, frame for frame. '
             '`palette.png`: the approved still, given three times (pictures 1 to 3) so the reference weighs more than the prompt.\n\n'
             '**Output.** `t185_h3_*.mp4`, a colour video at 768 × 576. It is a **colour donor only**: in the next step its brightness is thrown away '
             'and only its Cb/Cr is used, on the scan\'s own luma, at the scan\'s full resolution.'),
            ('What should and should not happen',
             '**Should.** Every person, garment and object takes the colour it has in the palette still, and keeps it through the movement. '
             'The picture follows the edge map exactly: same framing, same timing, same gestures.\n\n'
             '**Should not.** New objects, changed faces or hands, colour crossing an edge into the background, a palette that drifts between '
             'sections, flicker. A frame that shows any of these is not used to train the adapter (step 3): every frame is lined up '
             'against the source and used only if its brightness matches within 1.5 px.\n\n'
             '**Settings that matter.** Seed 0, 20 steps, `res_multistep` / `simple`, ControlNet strength 1.0 over the whole run. '
             'Sections overlap, and the seam is placed in a calm passage.'),
            GPU,
            ('Reproduced result', 'On the *Folgers* test shot this step comes within ΔE 1.34 of the approved result (pass mark 1.5). '
             'Run-to-run variation at a fixed seed is small but not zero, and an int8 model on a different card will not be bit-identical.'),
        ])

# 2. Healing second pass: Wan VACE refinement ------------------------------------------------------
convert(D / 'gap-filling-second-pass/graph/second_pass_vace_refine.json',
        D / 'gap-filling-second-pass/graph/second_pass_vace_refine_ui.json', oi,
        titles={'3': '1 · First-pass window (window.mp4)', '6': 'Wan 2.1 VACE 14B', '7': 'Shift 8', '8': 'Text encoder (UMT5 XXL)',
                '9': 'Prompt: what the shot is', '10': 'Negative: what must not appear', '11': 'Wan VAE', '30': 'Encode the window',
                '12': 'VACE: 768 × 560 × 81, strength 1.0', '13': 'Sample (30 steps, denoise 0.3)', '18': 'Refined frames'},
        notes=[
            ('Healing, second pass: make the window one picture',
             '## What this graph does\n\n'
             'The first pass (MiniMax H3 from a storyboard sheet, with the film\'s own drumming kept) gives a healed window whose frames do not yet '
             'share one grain and one surface. This pass runs the window through **Wan 2.1 VACE 14B** at a **low denoise (0.3)**: the model '
             're-draws each frame only lightly, enough to unify grain, texture and the last traces of damage, not enough to change what is in it.\n\n'
             '**Input.** `window.mp4`: one 81-frame window of the first-pass result at 768 × 560. **Output.** `second_pass_*.png`, the refined frames, '
             'which the seam blend (`tools/seam_blend.py`) joins with the neighbouring windows.'),
            ('What should and should not happen',
             '**Should.** The same people, hands, drum and beater in the same places, the same movement, a single even grain across the frame, '
             'natural colour without the magenta of the faded reversal.\n\n'
             '**Should not.** Changed faces, extra or deformed fingers, a shorter or straighter beater, a violet or magenta cast, waxy skin, '
             'over-sharpening, text, invented objects. The negative prompt lists exactly these; if one appears, the window is rejected and the '
             'denoise lowered, never raised.\n\n'
             '**Settings that matter.** Denoise 0.3 is the whole point of the pass; 0.5 starts to redraw the drumming. Seed 0, 30 steps, CFG 4.5, '
             'euler / simple, shift 8.'),
            ('Hardware', 'Wan VACE 14B in fp16 wants an NVIDIA card with 24 GB of VRAM or more and about 32 GB of model files; an 81-frame window '
             'takes some minutes. The graph opens in Comfy Cloud for reading; running it there is a paid job.'),
            ('Reproduced result', 'On the published window this pass comes within ΔE 0.9 of the approved result.'),
        ])

# 3. Reconstruction: the four stairs windows ---------------------------------------------------------
WIN = {'w1': ('frames 1–243', 'w1_source.mp4', '50, 118 and 200'), 'w2b': ('frames 128–370', 'w2b_source.mp4', 'the three window frames named in the prompt'),
       'w3b': ('frames 300–542', 'w3b_source.mp4', 'the three window frames named in the prompt'), 'w3': ('frames 382–624', 'w3_source.mp4', 'the three window frames named in the prompt')}
for w, (rng, src, refs) in WIN.items():
    convert(D / f'upscaling-stairs/graphs/stairs_{w}_h3_ref2va.json',
            D / f'upscaling-stairs/graphs/stairs_{w}_h3_ref2va_ui.json', oi,
            titles={'1': f'1 · Hybrid window ({src})', '3': '2 · Reference still 0', '18': '2 · Reference still 1', '19': '2 · Reference still 2',
                    '4': 'MiniMax H3 (ref2va, pruned int8)', '5': 'Text encoder (Qwen3-VL 32B, NVFP4)', '6': 'Video VAE', '7': 'Audio VAE',
                    '8': 'Reference to video: the prompt is the whole instruction', '13': 'Sample (20 steps)', '17': f'Reconstruction, window {w}'},
            notes=[
                (f'Reconstruction: El Tinterillo, stairs, window {w} ({rng})',
                 '## What this graph does\n\n'
                 'The shot survives only as a damaged 16mm print and a soft telecine. The **hybrid** window (`tools/make_hybrid.py`: the median-cleaned '
                 '16mm frame with the registered telecine inside it) is the **motion control**: it decides timing, camera, every silhouette and the '
                 'architecture. Three **reference stills** made from the hybrid (an image generator, prompt in `reference/reference_prompt.txt`) are the '
                 '**appearance** at frames ' + refs + '. **MiniMax H3** reconstructs the window through them.\n\n'
                 '**Output.** `stairs_' + w + '_*.mp4` at 768 × 432, 24 fps. Four such windows overlap and are joined by `tools/seam_blend.py` at cuts 200, 340 and 400.'),
                ('What should and should not happen',
                 '**Should.** All frames of the window in order and in the hybrid\'s exact motion phase; the rounded film aperture; correctly exposed '
                 'black-and-white with blacks that are black and plaster that is grey, not blown out; one look for the whole reel.\n\n'
                 '**Should not.** Holding, averaging, retiming or stabilising the movement; invented faces, props, people or text; scratches, dust or '
                 'flicker reproduced from the print; the washed-out tonality of the telecine reproduced as if it were the film. Small faces and lip '
                 'movement are the known limit at this resolution.\n\n'
                 '**What it is.** A reconstruction, with detail the film no longer holds, and labelled as one. The original scan and every raw window are kept.'),
                ('Hardware', 'MiniMax H3 at 768 × 432 for 243 frames wants an NVIDIA card with 24 GB of VRAM or more and about 40–60 GB of model files; '
                 'a window takes 20 to 45 minutes. The graph opens in Comfy Cloud for reading; running it there is a paid, long job.'),
                ('Reproduced result', 'The hybrid step reproduces identically (ΔE 0) and the seam blend within ΔE 1.07 of the approved shot. '
                 'The reference stills come from a closed image model, so they are published rather than regenerated.'),
            ])
print('done')
