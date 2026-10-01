"""Current-editor smoke only; use check_travel.py for business acceptance."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

out = Path('/app/outputs/editor-smoke')
out.mkdir(parents=True, exist_ok=True)
errors, requests = [], []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1600, 'height': 1000}, device_scale_factor=1)
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('request', lambda r: requests.append({'method': r.method, 'url': r.url.split('?')[0]}))
    page.goto('http://127.0.0.1:3077/', wait_until='networkidle', timeout=90000)
    page.locator('#canvas').wait_for(state='visible', timeout=30000)
    page.screenshot(path=str(out/'editor.png'), full_page=True)
    result = {'title': page.title(), 'canvas_visible': page.locator('#canvas').is_visible(),
        'left_panel_visible': page.locator('.left-bar').is_visible(),
        'right_panel_visible': page.locator('.right-bar').is_visible(),
        'errors': errors, 'requests': requests}
    (out/'report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='requests'}, ensure_ascii=False))
    browser.close()
