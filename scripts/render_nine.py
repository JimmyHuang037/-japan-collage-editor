"""Render composites through Kuaitu's actual browser export; generate full-frame previews."""
import json
from pathlib import Path
from PIL import Image, ImageOps
from playwright.sync_api import sync_playwright

ROOT = Path('/app')
OUT = ROOT / 'outputs/draft-nine'
EVIDENCE = ROOT / 'outputs/browser-acceptance'
EVIDENCE.mkdir(parents=True, exist_ok=True)
entries = json.loads((ROOT / 'public/travel/projects/index.json').read_text())
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1700, 'height': 1100}, device_scale_factor=1)
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto('http://127.0.0.1:3077/', wait_until='networkidle', timeout=90000)
    page.wait_for_function('window.__travelEditor?.canvas.getObjects().some(o => o.photoId)', timeout=90000)
    rendered = []
    for entry in entries:
        doc = json.loads((ROOT / 'public/travel/projects' / (entry['id'] + '.json')).read_text())
        ids = [o['photoId'] for o in doc['objects'] if o['type'] == 'image']
        page.locator('[data-project="' + entry['id'] + '"]').click()
        page.wait_for_function('(ids) => JSON.stringify(window.__travelEditor.canvas.getObjects().filter(o=>o.type==="image").map(o=>o.photoId)) === JSON.stringify(ids)', arg=ids, timeout=90000)
        page.wait_for_function('!document.querySelector("[data-project]").disabled', timeout=90000)
        page.evaluate('document.fonts.ready')
        if entry['kind'] == 'composite':
            with page.expect_download(timeout=90000) as event:
                page.get_by_test_id('export-png').click()
            path = OUT / 'images' / (entry['id'] + '.png')
            event.value.save_as(str(path))
        else:
            path = OUT / 'images' / (entry['id'] + '.jpg')
        with Image.open(path) as raw:
            preview = ImageOps.exif_transpose(raw).convert('RGB')
            preview.thumbnail((800, 800))
            preview.save(ROOT / 'public/travel/projects' / (entry['id'] + '.jpg'), quality=90)
            rendered.append({'id': entry['id'], 'size': ImageOps.exif_transpose(raw).size, 'photos': len(ids)})
        print(entry['id'], flush=True)
    page.locator('[data-project="04-uji"]').click()
    page.wait_for_function('window.__travelEditor.canvas.getObjects().filter(o=>o.type==="image").length===6')
    page.screenshot(path=str(EVIDENCE / 'editor-nine.png'), full_page=True)
    assert not errors, errors
    (EVIDENCE / 'render-report.json').write_text(json.dumps({'renders': rendered, 'page_errors': errors}, ensure_ascii=False, indent=2))
    browser.close()
