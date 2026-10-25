#!/usr/bin/env bash
# Local checks (formerly run on GitHub Actions). Run from the repo root.
set -euo pipefail
cd "$(dirname "$0")/.."
# New-file guard: reject archives, raw scans, model files and anything over 1 MiB (8 MiB for docs/media/*.mp4)
base="${BASE:-$(git merge-base origin/main HEAD 2>/dev/null || git rev-parse HEAD~1)}"
[ "$base" = "$(git rev-parse HEAD)" ] && base=$(git rev-parse HEAD~1)
echo "Comparing new files against $base"
bad=0
while IFS= read -r f; do
  [ -f "$f" ] || continue
  case "${f,,}" in
    *.zip|*.tar|*.gz|*.7z|*.exr|*.dpx|*.mkv|*.safetensors|*.ckpt|*.npy|*.npz)
      echo "New archive, raw scan or model file: $f"; bad=1;;
  esac
  size=$(wc -c < "$f")
  limit=1048576
  case "$f" in docs/media/*.mp4) limit=8388608;; esac
  if [ "$size" -gt "$limit" ]; then echo "File over the limit: $f ($size bytes)"; bad=1; fi
done < <(git diff --name-only --diff-filter=A "$base" HEAD)
[ "$bad" = 0 ] || exit 1
# Internal links and assets (needs pyyaml)
python3 tools/site-check/audit_links.py . --strict
echo "All checks passed."
