#!/usr/bin/env python3
"""Render only the two local drafts. No publishing, inference or remote CI.

python -m pip install -r requirements.txt
python build.py --chromium /usr/bin/chromium
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
from pathlib import Path
import pymupdf as fitz
import qrcode
import qrcode.image.svg
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chromium', default=shutil.which('chromium') or shutil.which('google-chrome'))
    args = parser.parse_args()
    urls = json.loads((HERE / 'urls.json').read_text())
    for key, url in urls.items():
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        qr.make_image(image_factory=qrcode.image.svg.SvgPathImage).save(HERE / 'assets' / f'qr-{key}.svg')
        qr.make_image(fill_color='black', back_color='white').save(HERE / 'assets' / f'qr-{key}.png')
    report = {'renderer': 'Chromium via Playwright; CSS page size; scale 1', 'documents': {}}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.chromium, headless=True, args=['--no-sandbox'])
        report['chromium_version'] = browser.version
        for stem, inches in [('poster', (36, 36)), ('handout', (8.5, 11))]:
            page = browser.new_page(viewport={'width': round(inches[0]*96), 'height': round(inches[1]*96)}, device_scale_factor=1)
            page.emulate_media(media='print')
            page.goto((HERE / f'{stem}.html').as_uri(), wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            layout = page.evaluate('''() => {
              const page = document.querySelector('[data-page]'), r = page.getBoundingClientRect();
              const outside = [...page.querySelectorAll('*')].filter(e => { const b=e.getBoundingClientRect(); return b.width && b.height && (b.left<r.left-.5 || b.right>r.right+.5 || b.top<r.top-.5 || b.bottom>r.bottom+.5); }).map(e=>({element:e.tagName, text:e.textContent.trim().slice(0,100), rect:e.getBoundingClientRect().toJSON()}));
              const text = [...page.querySelectorAll('*')].filter(e => [...e.childNodes].some(n=>n.nodeType===Node.TEXT_NODE && n.textContent.trim()));
              return {width:r.width,height:r.height,scrollWidth:page.scrollWidth,scrollHeight:page.scrollHeight,outside,minTextPt:Math.min(...text.map(e=>parseFloat(getComputedStyle(e).fontSize)*.75)),images:[...page.querySelectorAll('img')].map(e=>({src:e.getAttribute('src'),loaded:e.complete&&e.naturalWidth>0}))};
            }''')
            if layout['outside'] or any(not i['loaded'] for i in layout['images']):
                # Keep the report on failure, so a layout problem can be inspected.
                report['documents'][stem] = layout
                (HERE/'validation.json').write_text(json.dumps(report, indent=2)+'\n')
                raise RuntimeError(f'{stem}: overflow or missing image; see validation.json')
            page.pdf(path=str(HERE/f'{stem}.pdf'), prefer_css_page_size=True, print_background=True, display_header_footer=False, scale=1)
            page.close()
            doc = fitz.open(HERE/f'{stem}.pdf')
            assert len(doc)==1, f'{stem}: expected one page, got {len(doc)}'
            dims = [round(doc[0].rect.width, 3), round(doc[0].rect.height, 3)]
            assert all(abs(a-b*72)<.1 for a,b in zip(dims,inches)), (stem,dims)
            layout['pdf_points']=dims
            layout['pdf_pages']=len(doc)
            layout['pdf_bytes']=(HERE/f'{stem}.pdf').stat().st_size
            layout['pdf_sha256']=hashlib.sha256((HERE/f'{stem}.pdf').read_bytes()).hexdigest()
            if stem=='poster':
                # A small review image, rendered FROM the PDF, not an HTML screenshot.
                doc[0].get_pixmap(matrix=fitz.Matrix(1200/2592,1200/2592), alpha=False).save(HERE/'poster-preview.png')
                assert layout['minTextPt']>=24, layout['minTextPt']
            report['documents'][stem]=layout
        browser.close()
    (HERE/'validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:{x:v[x] for x in ['pdf_points','pdf_pages','pdf_bytes','minTextPt','outside']} for k,v in report['documents'].items()},indent=2))

if __name__=='__main__':
    main()
