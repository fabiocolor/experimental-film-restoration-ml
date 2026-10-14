#!/usr/bin/env python3
"""Stairs example: four H3 windows (w1, w2b, w3b, w3) joined at cuts 200, 340, 400.

Put the four window MP4s in CWC_INPUT_DIR as w1.mp4, w2b.mp4, w3b.mp4 and w3.mp4
(the files in example/ are ready to use), then:

  CWC_INPUT_DIR=example CWC_OUTPUT_DIR=out python tools/run_blend_example.py

Window global starts: w1=1, w2b=128, w3b=300, w3=382. Half-pool 12, dissolve 12.
For your own shot, change the windows and cuts below.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seam_blend  # noqa: E402

sys.argv = [
    'seam_blend.py',
    '--window', 'w1:1:.',
    '--window', 'w2b:128:.',
    '--window', 'w3b:300:.',
    '--window', 'w3:382:.',
    '--cut', '200:w1:w2b',
    '--cut', '340:w2b:w3b',
    '--cut', '400:w3b:w3',
    '--half', '12',
    '--dissolve', '12',
    '--label', 'stairs',
]
# seam_blend resolves NAME:START:SUBDIR via (inp/sub).glob('*.mp4') - one mp4 per subdir.
# Flat example/ has four mp4s, so stage into temp subdirs named by window.
import os, tempfile, shutil
inp = Path(os.environ.get('CWC_INPUT_DIR', 'example')).resolve()
staging = Path(tempfile.mkdtemp(prefix='stairs_blend_'))
try:
    for name in ('w1', 'w2b', 'w3b', 'w3'):
        src = inp / f'{name}.mp4'
        if not src.is_file():
            raise SystemExit(f'missing {src}')
        d = staging / name
        d.mkdir()
        os.symlink(src, d / src.name)
    os.environ['CWC_INPUT_DIR'] = str(staging)
    sys.argv = [
        'seam_blend.py',
        '--window', 'w1:1:w1',
        '--window', 'w2b:128:w2b',
        '--window', 'w3b:300:w3b',
        '--window', 'w3:382:w3',
        '--cut', '200:w1:w2b',
        '--cut', '340:w2b:w3b',
        '--cut', '400:w3b:w3',
        '--half', '12',
        '--dissolve', '12',
        '--label', 'stairs',
    ]
    seam_blend.main()
finally:
    shutil.rmtree(staging, ignore_errors=True)
