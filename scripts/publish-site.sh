#!/usr/bin/env bash
# Build the Jekyll site from docs/ locally and publish it to the gh-pages branch
# (GitHub Pages serves that branch; no GitHub Actions involved).
# Needs Ruby + Bundler. Gems are installed outside docs/ so Jekyll does not read them.
set -euo pipefail
cd "$(dirname "$0")/.."
root=$(pwd)
export BUNDLE_PATH="${BUNDLE_PATH:-$HOME/.efr-bundle}"
out=$(mktemp -d)
(cd docs && bundle install --quiet && JEKYLL_ENV=production bundle exec jekyll build -d "$out")
touch "$out/.nojekyll"
[ -f docs/CNAME ] && cp docs/CNAME "$out/CNAME"
src=$(git rev-parse --short HEAD)
cd "$out"
git init -q -b gh-pages
git add -A
git -c user.name="$(git -C "$root" config user.name)" -c user.email="$(git -C "$root" config user.email)" commit -q -m "Publish site from main@$src"
git push -q --force "$(git -C "$root" remote get-url origin)" gh-pages:gh-pages
echo "Published main@$src to gh-pages."
rm -rf "$out"
