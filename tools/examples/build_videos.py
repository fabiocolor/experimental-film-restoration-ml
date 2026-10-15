#!/usr/bin/env python3
"""Build the site's comparison videos from the approved results in EXPERIMENT_RESULTS.

For each example: a web side-by-side (source | result, muted, H.264, <= 8 MiB) and a web
"reveal" (the result wipes across the source, then holds), plus a full-quality side-by-side
master for Drive / the examples release. Runs on the Cowork VM where the drive is mounted.
"""
import json, os, subprocess, sys
from pathlib import Path

H = Path.home()
ER = H / 'mnt/EXPERIMENT_RESULTS'
OUT = H / 'mnt/RESEARCH/_hub_work'
WEB = OUT / 'web'; MAS = OUT / 'masters'; FR = OUT / 'frames'
for d in (WEB, MAS, FR): d.mkdir(parents=True, exist_ok=True)

FPS_OUT = 24

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('FFMPEG ERROR', ' '.join(cmd)[:400], r.stderr[-1500:]); sys.exit(1)

def probe(p):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,nb_frames,r_frame_rate', '-of', 'json', str(p)], capture_output=True, text=True).stdout
    s = json.loads(o)['streams'][0]
    num, den = s['r_frame_rate'].split('/')
    return int(s['width']), int(s['height']), int(s.get('nb_frames') or 0), float(num) / float(den)

LUT = OUT / 'cineon_to_rec709.cube'   # log=True applies it; not used for the published videos (it made faded reds look hot)
STEPS = set(os.environ.get('STEPS','sbs,reveal,master,stills').split(','))

def av1(h264):
    """An AV1 twin of a web file (about a third smaller at the same quality); the page offers it first and
    falls back to the H.264 file in browsers that cannot play it."""
    out = h264.with_suffix('.av1.mp4')
    if 'libsvtav1' not in subprocess.run(['ffmpeg', '-v', 'quiet', '-encoders'], capture_output=True, text=True).stdout:
        print(f'  (no libsvtav1 in this ffmpeg; make {out.name} elsewhere)'); return
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(h264), '-c:v', 'libsvtav1', '-preset', '6', '-crf', '30', '-g', '48',
         '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', str(out)])

def build(slug, src, res, src_crop=None, res_crop=None, start=0.0, dur=None, web_w=1280, master_w=None, fps=None, log=False, register=True):
    """src/res: video paths. crops: (x, y, w, h) in the input. start/dur in seconds.
    With register=True the result crop and start are corrected so the result lands on the source exactly
    (see register.py); the hand-set res_crop is only the first guess."""
    sw, sh, sn, sfps = probe(src)
    fps = fps or sfps
    sc = src_crop or (0, 0, sw, sh)
    rc = res_crop or (0, 0, *probe(res)[:2])
    res_start = start
    if register:
        from register import measure
        same = Path(src).resolve() == Path(res).resolve()   # both halves cut from one file: simultaneous by construction
        sc, rc, res_start, rep = measure(src, sc, res, rc, start, dur or (sn / sfps), fps=fps, max_k=0 if same else 8)
        W = rep['warp']
        if sc != rep['sc_in']: print(f"  {slug}: source crop trimmed to what the result holds: {rep['sc_in']} -> {sc}")
        print(f"  {slug}: result moved {rep['k']:+d} frame(s); crop {rep['rc_in']} -> {rc}; "
              f"scale ({W[0][0]:.4f}, {W[1][1]:.4f}) shift ({W[0][2]:+.1f}, {W[1][2]:+.1f}) px at 960 wide; "
              f"frame offsets seen {rep['ks']}")
        if abs(rep['drift']) > 2:
            print(f"  WARNING {slug}: the frame offset drifts by {rep['drift']} over the clip (fps {rep['fps_src']} vs {rep['fps_res']}?)")
    aspect = sc[2] / sc[3]
    view = f',lut1d=file={LUT}' if log else ''
    half_w = web_w // 2
    half_h = int(round(half_w / aspect / 2)) * 2
    t = ['-ss', f'{start:.3f}'] if start else []
    tr = ['-ss', f'{res_start:.3f}'] if res_start else []
    d = ['-t', f'{dur:.3f}'] if dur else []
    # --- web side by side
    f = (f"[0:v]crop={sc[2]}:{sc[3]}:{sc[0]}:{sc[1]}{view},scale={half_w}:{half_h}:flags=lanczos,setsar=1[a];"
         f"[1:v]crop={rc[2]}:{rc[3]}:{rc[0]}:{rc[1]}{view},scale={half_w}:{half_h}:flags=lanczos,setsar=1[b];"
         f"[a][b]hstack=inputs=2,fps={fps},format=yuv420p[v]")
    web = WEB / f'{slug}-sbs.mp4'
    if 'sbs' in STEPS:
        run(['ffmpeg', '-v', 'error', '-y', *t, '-i', str(src), *tr, '-i', str(res), *d, '-filter_complex', f, '-map', '[v]', '-an',
             '-c:v', 'libx264', '-preset', 'slow', '-tune', 'film', '-g', '48', '-crf', '23', '-movflags', '+faststart', str(web)])
        av1(web)
    # --- web reveal: the result wipes over the source left -> right in 2.5 s, starting at 0.4 s, then holds
    WIPE_AT, WIPE = 0.4, 2.5
    rw = min(960, sc[2] if sc[2] % 2 == 0 else sc[2] - 1)
    rh = int(round(rw / aspect / 2)) * 2
    f = (f"[0:v]crop={sc[2]}:{sc[3]}:{sc[0]}:{sc[1]}{view},scale={rw}:{rh}:flags=lanczos,setsar=1,fps={fps}[a];"
         f"[1:v]crop={rc[2]}:{rc[3]}:{rc[0]}:{rc[1]}{view},scale={rw}:{rh}:flags=lanczos,setsar=1,fps={fps}[b];"
         f"[a][b]xfade=transition=wipeleft:duration={WIPE}:offset={WIPE_AT},format=yuv420p[v]")
    # xfade shows the second clip from its first frame at the moment the wipe starts, so the result is cut WIPE_AT
    # later than the source; otherwise it runs 0.4 s behind and the edge of the wipe tears on anything that moves
    reveal = WEB / f'{slug}-reveal.mp4'
    tr2 = ['-ss', f'{res_start + WIPE_AT:.3f}']
    d2 = ['-t', f'{dur - WIPE_AT:.3f}'] if dur else []
    if 'reveal' in STEPS:
        run(['ffmpeg', '-v', 'error', '-y', *t, *d, '-i', str(src), *tr2, *d2, '-i', str(res), '-filter_complex', f, '-map', '[v]', '-an',
             '-c:v', 'libx264', '-preset', 'slow', '-tune', 'film', '-g', '48', '-crf', '23', '-movflags', '+faststart', str(reveal)])
        av1(reveal)
    # --- master side by side at full input resolution
    mw = master_w or sc[2] * 2
    mh = int(round(mw / 2 / aspect / 2)) * 2
    f = (f"[0:v]crop={sc[2]}:{sc[3]}:{sc[0]}:{sc[1]}{view},scale={mw//2}:{mh}:flags=lanczos,setsar=1[a];"
         f"[1:v]crop={rc[2]}:{rc[3]}:{rc[0]}:{rc[1]}{view},scale={mw//2}:{mh}:flags=lanczos,setsar=1[b];"
         f"[a][b]hstack=inputs=2,fps={fps},format=yuv420p[v]")
    master = MAS / f'{slug}-sbs-{mw}x{mh}.mp4'
    # the master is the whole shot; only the frame offset is applied, by trimming the clip that starts early
    off = res_start - start
    ms = ['-ss', f'{-off:.3f}'] if off < 0 else []
    mr = ['-ss', f'{off:.3f}'] if off > 0 else []
    if 'master' in STEPS: run(['ffmpeg', '-v', 'error', '-y', *ms, '-i', str(src), *mr, '-i', str(res), '-filter_complex', f, '-map', '[v]', '-an',
         '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-movflags', '+faststart', str(master)])
    # --- stills for the site: three frames, source and result as separate JPEGs
    n_total = int((dur or (sn / sfps)) * sfps) if sn else 0
    for k, frac in (('a', 0.18), ('b', 0.5), ('c', 0.82)) if 'stills' in STEPS else ():
        tt = (dur or (sn / sfps)) * frac
        for tag, p, c, t0 in (('source', src, sc, start), ('result', res, rc, res_start)):
            run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0 + tt:.3f}', '-i', str(p), '-frames:v', '1', '-vf', f'crop={c[2]}:{c[3]}:{c[0]}:{c[1]}{view},scale=min(1280\\,iw):-2:flags=lanczos', '-q:v', '3', str(FR / f'{slug}-{k}-{tag}.jpg')])
    sizes = {p.name: p.stat().st_size // 1024 for p in (web, reveal, master) if p.exists()}
    print(slug, sizes)
    if register and web.exists():   # check the finished file: the two halves should now be on the same pixels
        from register import measure
        rep = measure(web, (0, 0, half_w, half_h), web, (half_w, 0, half_w, half_h), 0.3, max(1.0, (dur or 5) - 1), samples=7)[3]
        W = rep['warp']
        print(f"  check {web.name}: residual {rep['k']:+d} frame(s), scale ({W[0][0]:.4f}, {W[1][1]:.4f}), shift ({W[0][2]:+.1f}, {W[1][2]:+.1f}) px at 960 wide")

FADED = ER / 'FADED COLOR LORA RECOVERY/results/temporal_tests'
UP = ER / 'DIFFUSION UPSCALING/runs/outputs'
KOT = ER / 'KNIGHTS-SOURCE-INVENTORY-20260922/runs/KOT-SYNTH-002/v6/hub/out'
BW = ER / 'BLACK AND WHITE COLORIZATION/results/review_hub'
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else None  # optional folder with release/Drive videos

jobs = sys.argv[2:] or ['all']
def want(n): return 'all' in jobs or n in jobs

if want('obsession-ballroom'):
    v = FADED / 'OBSESSION_H3_T159/17_h3_semantic_anchor_ownership_cascade/00_overview/obsession_t160_source_raw_h3_sourceY_h3CbCr_full_overlap_3up.mp4'
    # 3 panels of 640 x 486; the label strip is the top 20 px of each panel
    build('obsession-ballroom', v, v, src_crop=(6, 49, 628, 360), res_crop=(1286, 49, 628, 360), start=0, dur=9.5, master_w=1280)  # shown as delivered, no log-to-709 view
if want('counter-attack-waterfront'):
    # approved T148 final (H3 base, TeleStyle on two spans of hand movement) against the full-size source frames
    src = OUT / 'src/waterfront_source_338f_30fps_1920x1440.mp4'   # ffmpeg from t124_t125.../01_source_fullshot/fanji_waterfront_f%06d_source.png
    fin = FADED / 'FANJI_FILM_COPY/t148_t147_base_independent_telestyle_detector_heal_20260808/05_final_composite/fanji_t148_t147_base_telestyle_fullframe_w1_338f_30fps_1920x1440.mp4'
    build('counter-attack-waterfront', src, fin, start=1.0, dur=9.0, master_w=1920)
if want('counter-attack-quarry'):
    # the final covers frames 1-681 of the full-size source sequence (matched on luminance); the source clip is
    # ffmpeg from FANJI_QUARRY_T133/six_reference_fullshot_20260726/review_bundle/01_source/frame_%06d.jpg
    src = OUT / 'src/quarry_source_681f_30fps_1920x1440.mp4'
    fin = FADED / 'FANJI_QUARRY_T157/h3_unbalanced_raw_full_overlap_palette_transition/05_final_composite/fanji_t157_h3_only_s2_s3_full_overlap_palette_transition_sourcey_681f_30fps_1920x1440.mp4'
    build('counter-attack-quarry', src, fin, start=4.0, dur=9.0, master_w=1920)
if want('tinterillo') or any(j.startswith('tinterillo-') for j in jobs):
    for fg, src, res, n in (('fg02', 'tinterillo_fg02_reel_r1_20260926/FG02_scan_review_f0001_f0410_768x432.mp4', 'tinterillo_fg02_reel_r1_20260926/seamblend/tinterillo_fg02_reel_r1_seamblend_f0001_f0410_24fps_768x432.mp4', 410),
                           ('fg03', 'tinterillo_fg03_reel_r1_20260926/FG03_scan_review_f0001_f0176_768x432.mp4', 'tinterillo_fg03_reel_r1_20260926/tinterillo_fg03_reel_r1_f0001_f0176_24fps_768x432.mp4', 176),
                           ('fg04', 'tinterillo_fg04_reel_r1_20260926/FG04_scan_review_f0001_f0422_768x432.mp4', 'tinterillo_fg04_reel_r1_20260926/seamblend/tinterillo_fg04_reel_r1_seamblend_f0001_f0422_24fps_768x432.mp4', 422)):
        if 'tinterillo' not in jobs and f'tinterillo-{fg}' not in jobs: continue
        dur = min(9.0, n / 24)
        build(f'el-tinterillo-{fg}', UP / src, UP / res, src_crop=(112, 40, 560, 392), res_crop=(112, 40, 560, 392), start=max(0, (n / 24 - dur) / 2), dur=dur, master_w=1120)
if want('kot'):
    build('knights-of-the-trail-gap', KOT / '01_nitrate_original.mp4', KOT / '02_v6_candidate.mp4', start=0, dur=9.4, master_w=1280)
    for k, n in (('gap748', 14), ('gap826', 92), ('gap871', 137), ('gap937', 203)):
        for tag, p in (('source', KOT / '01_nitrate_original.mp4'), ('result', KOT / '02_v6_candidate.mp4'), ('generated', KOT / '03_v6_generated_pixels_tinted.mp4')):
            run(['ffmpeg', '-v', 'error', '-y', '-i', str(p), '-vf', f"select='eq(n\\,{n})'", '-frames:v', '1', '-q:v', '3', str(FR / f'knights-of-the-trail-{k}-{tag}.jpg')])
if want('general'):
    build('the-general-garden', BW / 'garden/media/original.mp4', BW / 'garden/media/colorized.mp4', start=0, dur=5.17, master_w=2560, fps=24)
    build('the-general-train', BW / 'train_v3/media/original.mp4', BW / 'train_v3/media/colorized.mp4', start=0, dur=5.17, master_w=2560, fps=24)
if want('market'):
    build('market-street-1906', BW / 'market_v4/media/original.mp4', BW / 'market_v4/media/colorized.mp4', src_crop=(244, 0, 1432, 1080), res_crop=(244, 0, 1432, 1080), start=0, dur=5.17, master_w=2864, fps=24)
if SRC and want('release'):
    build('counter-attack-crowd', SRC / 'slide11.mp4', SRC / 'slide11.mp4', src_crop=(0, 65, 960, 719), res_crop=(960, 65, 960, 719), start=0, dur=9.5, master_w=1920)
    build('unman-wittering-zigo-choir', SRC / 'unman.mp4', SRC / 'unman.mp4', src_crop=(9, 74, 946, 709), res_crop=(974, 74, 946, 709), start=0, dur=6.8, master_w=1892)
    build('wong-flute-players', SRC / '16mm-flute-players-scan.mp4', SRC / '16mm-flute-players-reconstruction.mp4', start=0, dur=7.6, master_w=1536)
    build('folgers', SRC / 'source_shot.mkv', SRC / 'result_respect.mp4', start=0, dur=5.6, master_w=2048)
    build('candy-candy', SRC / 'candy.mp4', SRC / 'candy.mp4', src_crop=(82, 68, 554, 430), res_crop=(1260, 602, 578, 420), start=22.0, dur=9.0, master_w=1108)
print('done')
