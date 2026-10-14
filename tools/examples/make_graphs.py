#!/usr/bin/env python3
"""Generate the public ComfyUI graphs (UI format, laid out, with notes) for the two colour-recovery kits."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wfbuild import Graph

OI = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'object_info.json'))  # GET /object_info from a running ComfyUI
DOCS = str(Path(__file__).resolve().parents[2] / 'docs')

CLARA = ("Recover integrated RGB chroma for this faded film frame with a source-preserving C-anchor personality. "
         "Use image2 as a soft non-spatial calibration field for period film hue relationships, natural skin, believable material colors, clean neutrals, and restrained saturation. "
         "Use image3 as source-derived control so chroma boundaries stay aligned to source luma. "
         "Preserve the same source shot, people, faces, clothing, objects, foreground/background layout, framing, broad pixel geometry, luminance relationships, grain, scratches, softness, and visible detail. "
         "Keep color integrated into the original light and shadows, not pasted on top. "
         "Reduce warm, reddish, brown, and magenta drift without swinging into cold blue, cyan, gray, or black-and-white. "
         "Maintain a minimum useful chroma level in wide scenery, faces, walls, signs, clothing, shadows, and red/magenta probes. "
         "Whites and grays should stay neutral, blues should remain blue, greens should remain green, and reds or magentas should appear only where supported. "
         "Avoid copied chart patterns, chart layout leakage, reference-content takeover, invented objects, redesigned faces, sharpening, denoising, or beautification.")

PALETTE = ("Colorize this black-and-white film frame as a 1970s Eastmancolor television commercial. "
           "Use image1 as the source shot and preserve its exact content, geometry, people, clothing, objects, framing, silhouettes, foreground/background layout, and spatial boundaries. "
           "image2 is the same frame from a faded, colour-neutralized print: its colours are washed out and shifted toward cyan. "
           "Use image2 only as a weak hint of which hue family each object had (for example which garments or products were red, blue or green); do not copy its washed-out saturation or its cyan cast. "
           "Give skin a warm, healthy, natural colour and every garment, painted surface, product and prop a full, believable film colour, with clean whites and true neutral greys. "
           "Use image3 as a hard source-derived edge map in the same geometry space as image1: follow those edges and boundaries closely so the recovered chroma stays aligned to the original luma after inverse mapping. "
           "Do not move faces, bodies, objects, buildings, sky lines, vehicles, or foreground/background borders. "
           "Do not redesign faces, add new objects, change the location, replace the scene, invent detail in blank skies, or copy visible chart content.")

MODELS = {
    'fp8mixed': dict(unet='qwen_image_edit_2511_fp8mixed.safetensors', label='the published model (fp8mixed)'),
    'bf16':     dict(unet='qwen_image_edit_2511_bf16.safetensors',     label='the bf16 model in Comfy Cloud\'s library'),
}
CLIP = 'qwen_2.5_vl_7b_fp8_scaled.safetensors'
VAE = 'qwen_image_vae.safetensors'
LORA = 'Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors'

PAPER = '#2b2b2b'

def build(kind, variant, out_path):
    """kind: 'single' (unbalanced single frame, Clara) or 'palette' (balanced palette still)."""
    m = MODELS[variant]
    g = Graph(OI)
    single = kind == 'single'
    name = 'Faded colour recovery: single frame' if single else 'Faded colour recovery: palette still (balanced scan)'
    cfg = 0.9 if single else 1.0
    prefix = 'colour_recovery_single_frame' if single else 't185_palette'

    # --- Column 0: inputs ---------------------------------------------------------------------
    x0, x1, x2, x3, x4 = 0, 560, 1120, 1740, 2300
    if single:
        intro = (f"## {name}\n\n"
                 "One faded frame in, one colour frame out, with the frame's own brightness kept.\n\n"
                 "1. **Source frame**: your faded frame (PNG). The test frame is `source.png` from *Counter Attack* (1976).\n"
                 "2. **Colour chart**: `chart.png`, a softly blurred colour chart. Keep it; it guides the colour and gives the model nothing else to copy.\n"
                 "3. **Edge map**: `control.png`, the Canny edges of the source. For your own frame, connect **Detect Edges** below instead "
                 "(right-click the Edge map input of both *Encode* nodes' image3, or just drag the Canny output into *Scale edge map*).\n\n"
                 f"Model: {m['label']}. Lightning 4-step LoRA, cfg {cfg}, seed 0, shift 3.1.\n\n"
                 "Outputs: **model output** (1184 × 880, the raw proposal) and **composite** (the proposal's colour on the source's brightness, at source size). "
                 "Review both against the source: altered faces, invented objects, colour across an edge, clipped highlights.\n\n"
                 "Research by Fabio Bedoya. Generated colour is an interpretation, not evidence of the original colour. "
                 "fabiocolor.github.io/experimental-film-restoration-ml/colour-recovery/")
    else:
        intro = (f"## {name}\n\n"
                 "The first step of the balanced-source route: one colour frame for the shot, made from the scan's own brightness.\n\n"
                 "Make the three inputs with `tools/prepare_still_inputs.py frame.png still/` (or upload the kit's `example/` files):\n"
                 "1. **Source Y**: the frame's brightness as grey (`source_y.png`).\n"
                 "2. **Faded frame**: the frame itself (`faded_frame.png`), only a hint of which hue each object had.\n"
                 "3. **Edge map**: Canny 80/160 of the frame (`canny.png`).\n\n"
                 f"Model: {m['label']}. Lightning 4-step LoRA, cfg {cfg}, seed 0, shift 3.1.\n\n"
                 "Outputs: **model output** (the raw palette proposal) and a **composite** preview on the source brightness. "
                 "For the shot, use `tools/composite_still.py` on the model output; it is the reference composite (inverse Kontext geometry and shadow gate) and what the H3 step expects.\n\n"
                 "Research by Fabio Bedoya. fabiocolor.github.io/experimental-film-restoration-ml/downloads/faded-colour-recovery-t185/")
    g.note(intro, pos=(x0, -40), size=(480, 520), title=name)

    src = g.node('LoadImage', title='1 · Source frame' if single else '1 · Source Y (grey)',
                 widgets={'image': 'source.png' if single else 'source_y.png'}, pos=(x0, 520), size=(320, 360))
    hint = g.node('LoadImage', title='2 · Colour chart (soft)' if single else '2 · Faded frame (hint)',
                  widgets={'image': 'chart.png' if single else 'faded_frame.png'}, pos=(x0, 920), size=(320, 320))
    ctl = g.node('LoadImage', title='3 · Edge map (Canny 80/160)', widgets={'image': 'control.png' if single else 'canny.png'},
                 pos=(x0, 1280), size=(320, 320))
    canny = g.node('Canny', title='Detect edges here instead (for your own frame)', widgets={'low_threshold': 0.31, 'high_threshold': 0.63},
                   pos=(x0, 1640), size=(320, 110))
    g.link(src, 0, canny, 'image')
    g.note("For a new frame: upload it as the source, then drag **Detect edges → IMAGE** into *Scale edge map* (replacing the uploaded edge map). "
           "The in-graph detector (kornia) is close to OpenCV's Canny 80/160 but not identical; the uploaded `control.png` reproduces the published test exactly.",
           pos=(x0, 1780), size=(320, 150), title='Own frames')

    # --- Column 1: scaling and models ---------------------------------------------------------
    scale_src = g.node('FluxKontextImageScale', title='Scale source to the model grid', pos=(x1, 520), size=(300, 60))
    scale_ctl = g.node('FluxKontextImageScale', title='Scale edge map', pos=(x1, 1280), size=(300, 60))
    g.link(src, 0, scale_src, 'image'); g.link(ctl, 0, scale_ctl, 'image')

    unet = g.node('UNETLoader', title='Qwen Image Edit 2511', widgets={'unet_name': m['unet'], 'weight_dtype': 'default'}, pos=(x1, 0), size=(420, 90))
    clip = g.node('CLIPLoader', title='Text encoder', widgets={'clip_name': CLIP, 'type': 'qwen_image', 'device': 'default'}, pos=(x1, 120), size=(420, 110))
    vae = g.node('VAELoader', title='VAE', widgets={'vae_name': VAE}, pos=(x1, 260), size=(420, 60))
    shift = g.node('ModelSamplingAuraFlow', title='Shift 3.1', widgets={'shift': 3.1, 'sampling': 'flow'}, pos=(x1, 350), size=(300, 80))
    norm = g.node('CFGNorm', title='CFG norm', widgets={'strength': 1.0, 'pre_cfg': False}, pos=(x1, 640), size=(300, 80))
    lora = g.node('LoraLoaderModelOnly', title='Lightning 4-step LoRA', widgets={'lora_name': LORA, 'strength_model': 1.0}, pos=(x1, 750), size=(420, 90))
    g.link(unet, 0, shift, 'model'); g.link(shift, 0, norm, 'model'); g.link(norm, 0, lora, 'model')

    # --- Column 2: conditioning ---------------------------------------------------------------
    pos_enc = g.node('TextEncodeQwenImageEditPlus', title='Encode: prompt + source + chart + edges',
                     widgets={'prompt': CLARA if single else PALETTE}, pos=(x2, 0), size=(520, 420))
    neg_enc = g.node('TextEncodeQwenImageEditPlus', title='Encode: empty prompt (negative)', widgets={'prompt': ''}, pos=(x2, 470), size=(520, 220))
    for enc in (pos_enc, neg_enc):
        g.link(clip, 0, enc, 'clip'); g.link(vae, 0, enc, 'vae')
        g.link(scale_src, 0, enc, 'image1'); g.link(hint, 0, enc, 'image2'); g.link(scale_ctl, 0, enc, 'image3')
    pos_ref = g.node('FluxKontextMultiReferenceLatentMethod', title='Reference method', widgets={'reference_latents_method': 'index_timestep_zero'}, pos=(x2, 730), size=(420, 60))
    neg_ref = g.node('FluxKontextMultiReferenceLatentMethod', title='Reference method', widgets={'reference_latents_method': 'index_timestep_zero'}, pos=(x2, 820), size=(420, 60))
    g.link(pos_enc, 0, pos_ref, 'conditioning'); g.link(neg_enc, 0, neg_ref, 'conditioning')
    enc = g.node('VAEEncode', title='Encode source', pos=(x2, 920), size=(300, 60))
    g.link(scale_src, 0, enc, 'pixels'); g.link(vae, 0, enc, 'vae')

    # --- Column 3: sampling ---------------------------------------------------------------------
    ks = g.node('KSampler', title=f'Sample: 4 steps, cfg {cfg}, seed 0',
                widgets={'seed': 0, 'steps': 4, 'cfg': cfg, 'sampler_name': 'euler', 'scheduler': 'simple', 'denoise': 1.0}, pos=(x3, 0), size=(400, 300))
    g.link(lora, 0, ks, 'model'); g.link(pos_ref, 0, ks, 'positive'); g.link(neg_ref, 0, ks, 'negative'); g.link(enc, 0, ks, 'latent_image')
    dec = g.node('VAEDecode', title='Decode', pos=(x3, 340), size=(300, 60))
    g.link(ks, 0, dec, 'samples'); g.link(vae, 0, dec, 'vae')
    save_raw = g.node('SaveImage', title='Model output (raw proposal)', widgets={'filename_prefix': prefix + '/model_output'}, pos=(x3, 440), size=(400, 380))
    g.link(dec, 0, save_raw, 'images')

    # --- Column 4: composite on the source's own brightness -----------------------------------------
    g.note("**Composite.** The model returns a reduced picture (1184 × 880 for 4:3). Only its colour is used: the result is scaled back to the "
           "source size, its U and V (colour) are joined to the source's Y (brightness). Grain, detail and damage are the source's. "
           "Plain scaling and a shadow gate (right); the kit's `composite_still.py` is the reference, with the exact inverse of the Kontext crop and a smoothstep gate.",
           pos=(x4, 0), size=(440, 190), title='Composite')
    size = g.node('GetImageSize', title='Source size', pos=(x4, 230), size=(260, 90))
    g.link(src, 0, size, 'image')
    rescale = g.node('ImageScale', title='Scale result to source size', widgets={'upscale_method': 'lanczos', 'crop': 'disabled'}, pos=(x4, 360), size=(360, 130))
    g.link(dec, 0, rescale, 'image'); g.link(size, 0, rescale, 'width'); g.link(size, 1, rescale, 'height')
    yuv_src = g.node('ImageRGBToYUV', title='Source -> Y U V', pos=(x4, 530), size=(260, 90))
    yuv_res = g.node('ImageRGBToYUV', title='Result -> Y U V', pos=(x4, 660), size=(260, 90))
    g.link(src, 0, yuv_src, 'image'); g.link(rescale, 0, yuv_res, 'image')
    # Shadow gate: below a source brightness of 32/255 the generated colour is replaced by neutral, with a ramp to 96/255
    # (the kit's composite_still.py does the same with a smoothstep). weight = clamp(4 * (Y - 0.125)).
    x5 = x4 + 520
    g.note("**Shadow gate.** Generated colour is unreliable in deep shadows, so below a source brightness of 32/255 the colour is "
           "made neutral, with a ramp up to 96/255. The weight is built from the source Y with mask arithmetic: "
           "weight = clamp(4 x (Y - 0.125)). Delete these nodes and feed the result U and V straight into *Source Y + result U V* "
           "if you want the ungated colour.", pos=(x5, 0), size=(420, 190), title='Shadow gate')
    ymask = g.node('ImageToMask', title='Y as mask', widgets={'channel': 'red'}, pos=(x5, 230), size=(260, 60))
    g.link(yuv_src, 0, ymask, 'image')
    thr = g.node('SolidMask', title='0.125 (= 32/255)', widgets={'value': 0.125}, pos=(x5, 330), size=(260, 110))
    g.link(size, 0, thr, 'width'); g.link(size, 1, thr, 'height')
    sub = g.node('MaskComposite', title='Y - 0.125', widgets={'x': 0, 'y': 0, 'operation': 'subtract'}, pos=(x5, 480), size=(300, 110))
    g.link(ymask, 0, sub, 'destination'); g.link(thr, 0, sub, 'source')
    dbl1 = g.node('MaskComposite', title='x 2', widgets={'x': 0, 'y': 0, 'operation': 'add'}, pos=(x5, 630), size=(300, 110))
    g.link(sub, 0, dbl1, 'destination'); g.link(sub, 0, dbl1, 'source')
    dbl2 = g.node('MaskComposite', title='x 2 again = weight', widgets={'x': 0, 'y': 0, 'operation': 'add'}, pos=(x5, 780), size=(300, 110))
    g.link(dbl1, 0, dbl2, 'destination'); g.link(dbl1, 0, dbl2, 'source')
    neutral = g.node('EmptyImage', title='Neutral colour (grey)', widgets={'batch_size': 1, 'color': 8421504}, pos=(x5, 930), size=(300, 130))
    g.link(size, 0, neutral, 'width'); g.link(size, 1, neutral, 'height')
    ug = g.node('ImageCompositeMasked', title='U, gated', widgets={'x': 0, 'y': 0, 'resize_source': False}, pos=(x5, 1100), size=(300, 150))
    vg = g.node('ImageCompositeMasked', title='V, gated', widgets={'x': 0, 'y': 0, 'resize_source': False}, pos=(x5, 1290), size=(300, 150))
    for node, idx in ((ug, 1), (vg, 2)):
        g.link(neutral, 0, node, 'destination'); g.link(yuv_res, idx, node, 'source'); g.link(dbl2, 0, node, 'mask')
    merge = g.node('ImageYUVToRGB', title='Source Y + result U V', pos=(x4, 790), size=(300, 90))
    g.link(yuv_src, 0, merge, 'Y'); g.link(ug, 0, merge, 'U'); g.link(vg, 0, merge, 'V')
    save_comp = g.node('SaveImage', title='Composite (colour on the source brightness)', widgets={'filename_prefix': prefix + '/composite'}, pos=(x4, 920), size=(440, 400))
    g.link(merge, 0, save_comp, 'images')

    g.group('Inputs', (x0 - 20, 480, 400, 1480), '#3f5f3f')
    g.group('Models', (x1 - 20, -60, 500, 920), '#3f3f5f')
    g.group('Conditioning', (x2 - 20, -60, 560, 1060), '#5f3f3f')
    g.group('Sampling', (x3 - 20, -60, 480, 900), '#5f5f3f')
    g.group('Composite on the source brightness', (x4 - 20, -60, 980, 1500), '#3f5f5f')

    g.save(out_path)
    return g

if __name__ == '__main__':
    import os
    out = {}
    sf = f'{DOCS}/downloads/colour-recovery-single-frame/graphs'; os.makedirs(sf, exist_ok=True)
    out['single-fp8'] = build('single', 'fp8mixed', f'{sf}/colour-recovery-single-frame-fp8mixed.json')
    out['single-bf16'] = build('single', 'bf16', f'{sf}/colour-recovery-single-frame-bf16-cloud.json')
    pk = f'{DOCS}/downloads/faded-colour-recovery-t185/graphs'
    out['palette-fp8'] = build('palette', 'fp8mixed', f'{pk}/1_palette_still_fp8mixed_ui.json')
    out['palette-bf16'] = build('palette', 'bf16', f'{pk}/1_palette_still_bf16_cloud_ui.json')
    # API-format twins, for validation and for people who script ComfyUI
    for k, g in out.items():
        print(k, len(g.nodes), 'nodes', len(g.links), 'links')
    json.dump(out['single-fp8'].to_api(), open(f'{sf}/colour-recovery-single-frame-fp8mixed_api.json', 'w'), indent=1)
    json.dump(out['single-bf16'].to_api(), open(f'{sf}/colour-recovery-single-frame-bf16-cloud_api.json', 'w'), indent=1)
