#!/usr/bin/env python3
"""Run one step of the T185 route on your own machine.

  python run_step.py respect --source shot.mkv --recovered adapter_output.mp4 --out out/respect

Each step folder holds the exact code I ran, plus an example *_spec.json from my Folgers run.
The spec checks the SHA-256 of its inputs; update those fields (or pass --update-hashes) for your own shot.
prepare, respect: CPU is fine.  preview: CPU.  adapter: needs an NVIDIA GPU (PyTorch with CUDA).
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = {  # step: (entry script, spec file, {input flag: (folder, spec hash key)})
    'prepare': ('vod_prepare.py', 'prep_spec.json', {'source': ('source', 'source_sha256')}),
    'preview': ('vod_preview.py', 'preview_spec.json', {'source': ('source', 'source_sha256'), 'carrier': ('artifacts/donors', 'carrier_sha256'),
                                                       'h3': ('artifacts/donors', 'h3_sha256')}),
    'adapter': ('vod_adapter.py', 'adapter_spec.json', {'source': ('source', 'source_sha256'), 'targets': ('artifacts/donors', 'targets_sha256'),
                                                       'report': ('artifacts/donors', 'report_sha256')}),
    'respect': ('vod_respect.py', 'respect_spec.json', {'source': ('source', 'source_sha256'), 'recovered': ('artifacts/recovered', 'recovered_sha256')}),
}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('step', choices=STEPS)
    for flag in {f for s in STEPS.values() for f in s[2]}:
        ap.add_argument('--' + flag)
    ap.add_argument('--spec', help='spec JSON (default: the example in the step folder)')
    ap.add_argument('--update-hashes', action='store_true', help='write the SHA-256 of the given inputs into a copy of the spec')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    entry, spec_name, inputs = STEPS[a.step]
    work = Path(tempfile.mkdtemp(prefix=f't185_{a.step}_'))
    code, inp = work / 'code', work / 'input'
    shutil.copytree(HERE / 'steps' / a.step, code)
    spec = json.loads(Path(a.spec or code / spec_name).read_text())
    for flag, (folder, key) in inputs.items():
        path = getattr(a, flag)
        if not path:
            sys.exit(f'--{flag} is required for {a.step}')
        (inp / folder).mkdir(parents=True, exist_ok=True)
        link = 'context.mp4' if flag == 'carrier' else Path(path).name  # the preview step expects this name
        os.symlink(Path(path).resolve(), inp / folder / link)
        if a.update_hashes:
            spec[key] = sha(path)
            if a.step == 'preview' and flag == 'h3':
                spec['h3_filename'] = Path(path).name
    (code / spec_name).write_text(json.dumps(spec))
    out = Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, CWC_INPUT_DIR=str(inp), CWC_OUTPUT_DIR=str(out), CWC_EXPERIMENT_CODE_DIR=str(code))
    sys.exit(subprocess.call([sys.executable, str(code / entry)], cwd=code, env=env))


if __name__ == '__main__':
    main()
