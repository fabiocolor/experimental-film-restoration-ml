#!/usr/bin/env python3
"""Cut source|result pairs for the site from the published videos and stills.

Every output is a plain JPEG (q86, <= 1280 px wide, well under 1 MiB) in
docs/images_kebab/examples/<slug>-f<NNN>-{source,result,reference,model}.jpg so the
pages can show them with one figure grammar (figure.pair) and the compare wipe.
"""
import io, os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('src')  # the examples-2026-10 release videos and the Drive comparisons, downloaded locally
DOCS = Path(__file__).resolve().parents[2] / 'docs'
K = DOCS / 'images_kebab'
OUT = K / 'examples'
OUT.mkdir(exist_ok=True)
MAXW = 1280

def frame(path, n):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vf', f"select='eq(n\\,{n})'", '-vframes', '1',
                          '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(out)).convert('RGB')

def save(im, name):
    im = im.convert('RGB')
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    p = OUT / f'{name}.jpg'
    im.save(p, quality=86, optimize=True, progressive=True)
    sz = p.stat().st_size
    assert sz < 1048576, (p, sz)
    print(f'{p.name:60s} {im.width}x{im.height} {sz//1024} KB')

def pair_from_video(slug, n, src_video, res_video, crop=None, label=None):
    a = frame(src_video, n); b = frame(res_video, n)
    if crop:
        a = a.crop(crop); b = b.crop(crop)
    save(a, f'{slug}-f{n:03d}-source'); save(b, f'{slug}-f{n:03d}-result')

def pair_from_sbs_video(slug, n, video, left, right, suffix=('source', 'result')):
    f = frame(video, n)
    save(f.crop(left), f'{slug}-f{n:03d}-{suffix[0]}'); save(f.crop(right), f'{slug}-f{n:03d}-{suffix[1]}')

def split_composite(slug, path, top=0, label='f062'):
    im = Image.open(path).convert('RGB'); w, h = im.size
    half = w // 2
    save(im.crop((0, top, half, h)), f'{slug}-{label}-source'); save(im.crop((half, top, w, h)), f'{slug}-{label}-result')

# 1. Faded colour recovery -------------------------------------------------------------
# Counter Attack, waterfront (T148): the published composite, minus the burned-in label bar
split_composite('counter-attack-waterfront', K / 'colour-recovery/counter-attack-waterfront-t148-f160.jpg', top=62, label='f160')
# Counter Attack, crowd (T182, the default-base route): the FIAT/IFTA comparison video, 308 distinct frames
for n in (40, 230):
    pair_from_sbs_video('counter-attack-crowd', n, SRC / 'slide11.mp4', (0, 65, 960, 784), (960, 65, 1920, 784))
# Folgers (balanced kit): the published source and approved result
for n in (20, 67, 110):
    pair_from_video('folgers', n, SRC / 'source_shot.mkv', SRC / 'result_respect.mp4')
# Single-frame route (SEAPAVAA 2026): Juggernaut auditorium, Reptilicus beach, FANJI/Counter Attack anchor
jug = K / 'seapavaa2026/originals/jug_auditorium'
# The trailer-reel stills are shown as delivered (no log-to-display view: it made the faded reds look hot).
save(Image.open(jug / '01_source_juggernaut_tlr_000066-ed2dda29.jpg'), 'juggernaut-auditorium-f066-source')
save(Image.open(jug / '05_final_composite_juggernaut_tlr_r5_v1_10_auditorium_c-9d2f7cbe.png'), 'juggernaut-auditorium-f066-result')
save(Image.open(jug / '04_inference_frame_000000_test-feb2c14f.png'), 'juggernaut-auditorium-f066-model')
rep = K / 'seapavaa2026/originals/reptilicus_beach'
save(Image.open(rep / '01_source_reptilicus_tlr_000025-40689881.jpg'), 'reptilicus-beach-f025-source')
save(Image.open(rep / '04_inference_frame_000000_seed_0_cfg_1.000_Belak-0c1f0329.png'), 'reptilicus-beach-f025-model')
save(Image.open(rep / '05_final_composite_reptilicus_tlr_05_beach_woman_source-38de94d1.png'), 'reptilicus-beach-f025-result')
fan = K / 'seapavaa2026/originals'
src = Image.open(fan / 'fanji_waterfront_top3_fullframe/fanji_film_copy_000007.png').convert('RGB')
anc = Image.open(fan / 'fanji_waterfront_top3/04_clara_anchor.png').convert('RGB')
save(src, 'counter-attack-waterfront-f007-source')
save(anc, 'counter-attack-waterfront-f007-model')
# A source-luma composite of the anchor (Y from the scan, CbCr from the model), the same idea as the kit's
# composite step, for the kit page preview. The kit's own composite_still.py is the reference implementation.
def ycc(im):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = (b - y) * 0.564 + 0.5; cr = (r - y) * 0.713 + 0.5
    return y, cb, cr
def from_ycc(y, cb, cr):
    r = y + 1.403 * (cr - 0.5); b = y + 1.773 * (cb - 0.5); g = (y - 0.299 * r - 0.114 * b) / 0.587
    a = np.clip(np.stack([r, g, b], -1), 0, 1)
    return Image.fromarray((a * 255 + 0.5).astype(np.uint8))
anc_r = anc.resize(src.size, Image.LANCZOS)
y, _, _ = ycc(src); _, cb, cr = ycc(anc_r)
save(from_ycc(y, cb, cr), 'counter-attack-waterfront-f007-result')

# 2. Temporal CbCr ------------------------------------------------------------------------
# Unman, Wittering and Zigo, choir: the published adapter video (faded | adapter), 1920 x 850
for n in (30, 120):
    pair_from_sbs_video('unman-wittering-zigo-choir', n, SRC / 'unman.mp4', (9, 74, 955, 783), (974, 74, 1920, 783))
# Frontier Experience: the comparison GIF (scan | result, video reference below)
g = Image.open(K / 'frontier-experience/frontier-experience-comparison-preview.gif')
for n in (20, 55):
    g.seek(n); f = g.convert('RGB')
    save(f.crop((0, 0, 445, 320)), f'frontier-experience-f{n:03d}-source')
    save(f.crop((485, 0, 930, 320)), f'frontier-experience-f{n:03d}-result')
    save(f.crop((362, 360, 600, 540)), f'frontier-experience-f{n:03d}-reference')
# Candy Candy: the four-way comparison video (original scan | balanced | DVD reference | result)
for n in (600, 1200):
    f = frame(SRC / 'candy.mp4', n)
    save(f.crop((1260, 6, 1838, 596)), f'candy-candy-f{n:04d}-balanced')
    save(f.crop((1260, 602, 1838, 1022)), f'candy-candy-f{n:04d}-result')
    save(f.crop((83, 602, 584, 1022)), f'candy-candy-f{n:04d}-reference')
    save(f.crop((82, 68, 636, 498)), f'candy-candy-f{n:04d}-source')

# 3. Diffusion healing -------------------------------------------------------------------
for n in (30, 95, 160):
    pair_from_video('wong-flute-players', n, SRC / '16mm-flute-players-scan.mp4', SRC / '16mm-flute-players-reconstruction.mp4')

# 4. Diffusion reconstruction ----------------------------------------------------------------
def content_box(im, thr=16):
    a = np.asarray(im.convert('L')); cols = np.where((a > thr).mean(axis=0) > 0.05)[0]; rows = np.where((a > thr).mean(axis=1) > 0.05)[0]
    return (int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1)
for w, n in (('w1', 120), ('w3', 60), ('w2b', 150)):
    a = frame(SRC / f'{w}_source.mp4', n); b = frame(SRC / f'{w}.mp4', n)
    ba, bb = content_box(a), content_box(b)
    box = (min(ba[0], bb[0]), min(ba[1], bb[1]), max(ba[2], bb[2]), max(ba[3], bb[3]))
    save(a.crop(box), f'el-tinterillo-stairs-{w}-f{n:03d}-source'); save(b.crop(box), f'el-tinterillo-stairs-{w}-f{n:03d}-result')

# 5. Black-and-white colourization: the seven published composites, split
for f in sorted((K / 'black-and-white-colourization').glob('*-f062.jpg')):
    split_composite(f.stem.replace('-f062', ''), f)

print('done')
