#!/usr/bin/env python3
"""Static link and asset audit for the Jekyll site in docs/ (no build needed).

Usage: python3 tools/site-check/audit_links.py <repo root> [--strict] [--quiet]

Checks every relative_url, {% link %}, Markdown link and href/src in docs/ against the
pages, redirects and files that will exist in the built site. --strict exits non-zero
when anything is missing or points at a file excluded from the build.
"""
import os, re, sys, json, yaml
from pathlib import Path

args=[a for a in sys.argv[1:] if not a.startswith("--")]
flags=[a for a in sys.argv[1:] if a.startswith("--")]
ROOT = Path(args[0] if args else ".").resolve()
STRICT="--strict" in flags
QUIET="--quiet" in flags
DOCS = ROOT / "docs"
cfg = yaml.safe_load((DOCS / "_config.yml").read_text())
baseurl = cfg.get("baseurl", "")
excludes = cfg.get("exclude", [])

def excluded(rel):
    for e in excludes:
        e = e.strip("/")
        if rel == e or rel.startswith(e + "/"):
            return True
    return False

# Build permalink map: url path -> source file
pages = {}
redirects = {}
for md in list(DOCS.rglob("*.md")) + list(DOCS.rglob("*.html")):
    rel = md.relative_to(DOCS).as_posix()
    if rel.startswith(("_", ".jekyll", "_site")) or "/_" in rel or excluded(rel):
        continue
    txt = md.read_text(errors="replace")
    fm = {}
    if txt.startswith("---"):
        end = txt.find("\n---", 3)
        if end > 0:
            try:
                fm = yaml.safe_load(txt[3:end]) or {}
            except Exception as ex:
                fm = {"__yaml_error__": str(ex)}
    if not fm and md.suffix == ".md":
        continue  # no front matter → not a page
    if "permalink" in fm:
        url = fm["permalink"]
    else:
        stem = rel[:-len(md.suffix)]
        if stem.endswith("/index") or stem == "index":
            stem = stem[:-5] if stem != "index" else ""
        url = "/" + stem + "/" if stem else "/"
        if stem.lower() == "readme":
            url = "/" + stem + "/"
    url = url if url.endswith("/") or "." in url.rsplit("/", 1)[-1] else url + "/"
    pages[url] = rel
    rf = fm.get("redirect_from") or []
    if isinstance(rf, str):
        rf = [rf]
    for r in rf:
        if r:
            redirects[r if r.endswith("/") else r + "/"] = rel

def norm(u):
    u = u.split("#")[0].split("?")[0]
    if baseurl and u.startswith(baseurl + "/"):
        u = u[len(baseurl):]
    return u

issues = []
checked = 0
ext_links = set()
pat_rel = re.compile(r"""\{\{\s*['"]([^'"]+)['"]\s*\|\s*relative_url\s*\}\}""")
pat_link = re.compile(r"\{%\s*link\s+([^\s%]+)\s*%\}")
pat_md = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
pat_attr = re.compile(r"""(?:href|src|poster|data-src|data-full)=["']([^"']+)["']""")

def check_target(src_rel, raw, kind):
    global checked
    u = raw.strip()
    if u.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:", "data:")):
        if u.startswith("http"):
            ext_links.add(u)
        return
    if "{{" in u or "{%" in u:
        return  # liquid handled separately
    checked += 1
    u = norm(u)
    if u.startswith("/"):
        p = DOCS / u.lstrip("/")
        if u in pages or u in redirects:
            if u in redirects and u not in pages:
                issues.append((src_rel, kind, raw, "ok-via-redirect→" + redirects[u]))
            return
        if p.exists():
            if p.is_file() and excluded(p.relative_to(DOCS).as_posix()):
                issues.append((src_rel, kind, raw, "FILE EXISTS BUT EXCLUDED FROM BUILD"))
            return
        if (not u.endswith("/")) and (DOCS / (u.lstrip("/") + "/")).exists():
            return
        issues.append((src_rel, kind, raw, "MISSING"))
    else:
        # relative to source dir
        base = (DOCS / src_rel).parent
        p = (base / u).resolve()
        if p.exists():
            if p.is_file() and p.is_relative_to(DOCS) and excluded(p.relative_to(DOCS).as_posix()):
                issues.append((src_rel, kind, raw, "FILE EXISTS BUT EXCLUDED FROM BUILD"))
            return
        # maybe a page url relative
        rel_url = "/" + u.strip("./")
        if rel_url in pages:
            return
        issues.append((src_rel, kind, raw, "MISSING (relative)"))

for md in list(DOCS.rglob("*.md")) + list(DOCS.rglob("*.html")) + list(DOCS.rglob("*.yml")):
    rel = md.relative_to(DOCS).as_posix()
    if rel.startswith((".jekyll", "_site")) or excluded(rel):
        continue
    txt = md.read_text(errors="replace")
    for m in pat_rel.finditer(txt):
        check_target(rel, m.group(1), "relative_url")
    for m in pat_link.finditer(txt):
        tgt = m.group(1)
        if not (DOCS / tgt).exists():
            issues.append((rel, "link-tag", tgt, "MISSING"))
    for m in pat_md.finditer(txt):
        check_target(rel, m.group(1), "md")
    for m in pat_attr.finditer(txt):
        check_target(rel, m.group(1), "attr")

# README at repo root
readme = (ROOT / "README.md").read_text()
for m in pat_md.finditer(readme):
    u = m.group(1)
    if u.startswith("http"):
        ext_links.add(u)
        continue
    if not (ROOT / u.split("#")[0]).exists():
        issues.append(("README.md", "md", u, "MISSING"))

print(f"pages: {len(pages)}  redirects: {len(redirects)}  internal refs checked: {checked}")
if not QUIET:
    print("\nPAGES:")
    for u in sorted(pages):
        print(f"  {u:50s} {pages[u]}")
    print("\nREDIRECTS:")
    for u in sorted(redirects):
        print(f"  {u:50s} -> {redirects[u]}")
print("\nISSUES:")
seen = set()
for i in issues:
    if i in seen: continue
    seen.add(i)
    print("  ", " | ".join(i))
json.dump(sorted(ext_links), open(os.environ.get("EXT_OUT", "/dev/null"), "w"), indent=1)
print(f"\nexternal links: {len(ext_links)}")
hard=[i for i in seen if not i[3].startswith("ok-via-redirect")]
if STRICT and hard:
    print(f"\n{len(hard)} problem(s) found")
    sys.exit(1)
