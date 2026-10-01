"""Real Chromium acceptance: native controls, photo protection, portable round trip."""
import base64
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path('/app')
OUT = ROOT / 'outputs/browser-acceptance'
OUT.mkdir(parents=True, exist_ok=True)
catalog = json.loads((ROOT / 'public/travel/catalog.json').read_text())
entries = json.loads((ROOT / 'public/travel/projects/index.json').read_text())
errors, external, checks = [], [], []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1700, 'height': 1100}, locale='zh-CN')
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('dialog', lambda d: d.accept())
    page.on('request', lambda r: external.append({'method': r.method, 'url': r.url}) if urlparse(r.url).scheme in ('http', 'https') and urlparse(r.url).hostname not in ('localhost', '127.0.0.1') else None)
    page.goto('http://127.0.0.1:3077/', wait_until='networkidle', timeout=90000)
    page.wait_for_function('window.__travelEditor?.canvas.getObjects().filter(o=>o.type==="image").length===6')

    def state():
        return page.evaluate('window.__travelEditor.getJson()')

    def open_card(key):
        page.locator('.menu-item').filter(has_text='九图').click()
        page.evaluate('window.__qaBeforeWorkspace=window.__travelEditor.canvas.getObjects()[0]')
        page.locator('[data-project="' + key + '"]').click()
        expected = json.loads((ROOT / 'public/travel/projects' / (key + '.json')).read_text())
        ids = [o['photoId'] for o in expected['objects'] if o['type'] == 'image']
        page.wait_for_function('(ids) => JSON.stringify(window.__travelEditor.canvas.getObjects().filter(o=>o.type==="image").map(o=>o.photoId)) === JSON.stringify(ids)', arg=ids)
        page.wait_for_function('!document.querySelector("[data-project]").disabled')
        page.wait_for_function('window.__travelEditor.canvas.getObjects()[0]!==window.__qaBeforeWorkspace && !document.querySelector("[data-project]").disabled')

    def point(name, corner=None):
        return page.evaluate('''({name, corner}) => {
          const c=window.__travelEditor.canvas, o=c.getObjects().find(o=>o.name===name);
          const r=c.upperCanvasEl.getBoundingClientRect(), v=c.viewportTransform;
          const p=corner ? o.oCoords[corner] : o.getCenterPoint();
          return corner ? [r.left+p.x, r.top+p.y] : [r.left+p.x*v[0]+v[4],r.top+p.y*v[3]+v[5]];
        }''', {'name': name, 'corner': corner})

    def click(name):
        x, y = point(name)
        page.mouse.click(x, y)

    def drag(name, dx, dy, corner=None):
        x, y = point(name, corner)
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x+dx, y+dy, steps=12)
        page.mouse.up()
        page.wait_for_timeout(150)

    def photos(doc):
        output = []
        def walk(o):
            if o.get('type') == 'image': output.append(o)
            for child in o.get('objects', []): walk(child)
        walk(doc)
        return output

    def protected():
        return page.evaluate('''() => {
          const c=window.__travelEditor.canvas, w=window.__travelEditor.getWorkspase(), failures=[];
          const walk=o=>{if(o.type==='image'){
            if(Math.abs(o.scaleX-o.scaleY)>1e-8||o.cropX||o.cropY||o.flipX||o.flipY||o.clipPath||o.filters.length||o.opacity!==1||o.width!==o.getElement().naturalWidth||o.height!==o.getElement().naturalHeight)failures.push(o.name);
          }(o._objects||[]).forEach(walk)};
          c.getObjects().forEach(o=>{walk(o);if(o.type==='image'||o.type==='group'){
            const b=o.getBoundingRect(true,true);if(b.left<w.left-1||b.top<w.top-1||b.left+b.width>w.left+w.width+1||b.top+b.height>w.top+w.height+1)failures.push('bounds:'+o.name);
          }});return failures;
        }''')

    original = state()
    original_photos = photos(original)
    tape = '胶带-303'
    drag(tape, 25, -7)
    moved = state()
    assert photos(moved) == original_photos, 'Moving tape changed a photo'
    assert next(o for o in moved['objects'] if o.get('name') == tape)['left'] != next(o for o in original['objects'] if o.get('name') == tape)['left']
    page.keyboard.press('Control+z')
    page.wait_for_function('(x)=>window.__travelEditor.canvas.getObjects().find(o=>o.name==="胶带-303").left===x', arg=next(o for o in original['objects'] if o.get('name') == tape)['left'])
    page.keyboard.press('Control+Shift+z')
    page.wait_for_function('(x)=>window.__travelEditor.canvas.getObjects().find(o=>o.name==="胶带-303").left===x', arg=next(o for o in moved['objects'] if o.get('name') == tape)['left'])
    checks.append('Independent tape drag + native undo/redo; original photo transforms unchanged')

    # Use the local photo panel to replace a landscape with a portrait, and back.
    hero = original_photos[0]
    click(hero['name'])
    page.locator('.menu-item').filter(has_text='照片').click()
    page.get_by_text('替换当前选中的照片', exact=True).click()
    portrait = next(r for r in catalog if r['height'] > r['width'] and r['id'] != hero['photoId'])
    page.locator('[data-photo="' + portrait['id'] + '"]').click()
    page.wait_for_function('(id)=>window.__travelEditor.canvas.getObjects().find(o=>o.id==="'+hero['id']+'").photoId===id', arg=portrait['id'])
    assert not protected(), protected()
    page.keyboard.press('Control+z')
    page.wait_for_function('(id)=>window.__travelEditor.canvas.getObjects().find(o=>o.id==="'+hero['id']+'").photoId===id', arg=hero['photoId'])
    page.keyboard.press('Control+Shift+z')
    page.wait_for_function('(id)=>window.__travelEditor.canvas.getObjects().find(o=>o.id==="'+hero['id']+'").photoId===id', arg=portrait['id'])
    click(hero['name'])
    page.locator('[data-photo="' + hero['photoId'] + '"]').click()
    page.wait_for_function('(id)=>window.__travelEditor.canvas.getObjects().find(o=>o.id==="'+hero['id']+'").photoId===id', arg=hero['photoId'])
    assert not protected(), protected()
    checks.append('Landscape ↔ portrait replacement uses full-frame uniform scale; source metadata and undo/redo preserved')

    open_card('04-uji')
    click(hero['name'])
    # Native corner scaling with Shift must still preserve proportions.
    page.keyboard.down('Shift')
    drag(hero['name'], -45, -10, corner='br')
    page.keyboard.up('Shift')
    assert not protected(), protected()
    # Native rotation control, then drag toward the edge, must remain in frame.
    drag(hero['name'], 35, -30, corner='mtr')
    assert not protected(), protected()
    drag(hero['name'], -350, -220)
    assert not protected(), protected()
    checks.append('Native Shift corner resize, rotation and edge drag preserve full-frame photos')

    open_card('04-uji')
    click(hero['name'])
    page.keyboard.down('Shift')
    click(tape)
    page.keyboard.up('Shift')
    page.get_by_role('button', name='成组', exact=True).click()
    page.wait_for_function('window.__travelEditor.canvas.getActiveObject()?.type==="group"')
    grouped = state()
    assert sorted(p['photoId'] for p in photos(grouped)) == sorted(p['photoId'] for p in original_photos)
    assert all(p['sourceHash'] for p in photos(grouped))
    gname = page.evaluate('window.__travelEditor.canvas.getActiveObject().name')
    # Clone has no name; use active control directly for the native group scale.
    xy = page.evaluate('''()=>{const c=window.__travelEditor.canvas,r=c.upperCanvasEl.getBoundingClientRect(),p=c.getActiveObject().oCoords.br;return [r.left+p.x,r.top+p.y]}''')
    page.keyboard.down('Shift')
    page.mouse.move(*xy); page.mouse.down(); page.mouse.move(xy[0]-50,xy[1]-15,steps=10); page.mouse.up()
    page.keyboard.up('Shift')
    assert not protected(), protected()
    page.get_by_role('button', name='拆分组', exact=True).click()
    page.wait_for_function('!window.__travelEditor.canvas.getObjects().some(o=>o.type==="group")')
    assert all(p['sourceHash'] for p in photos(state()))
    checks.append('Native multi-select/group/Shift scale/ungroup preserves source IDs, hashes and full frame')

    # Edit an actual textbox, then save and reimport the downloaded portable project.
    open_card('04-uji')
    title = point('宇治标题')
    page.mouse.dblclick(*title)
    page.keyboard.press('Control+a'); page.keyboard.type('UJI / SUMMER MEMORY')
    page.keyboard.press('Escape')
    page.mouse.click(1355, 1040)
    page.wait_for_function('window.__travelEditor.canvas.getObjects().find(o=>o.name==="宇治标题").text==="UJI / SUMMER MEMORY"')
    saved_state = state()
    with page.expect_download(timeout=90000) as event:
        page.get_by_test_id('save-project').click()
    saved = OUT / 'roundtrip.json'
    event.value.save_as(str(saved))
    parsed = json.loads(saved.read_text())
    for photo in photos(parsed):
        assert photo['src'].startswith('data:image/')
        assert hashlib.sha256(base64.b64decode(photo['src'].split(',', 1)[1])).hexdigest() == photo['sourceHash']
    page.reload(wait_until='networkidle')
    page.wait_for_function('window.__travelEditor?.canvas.getObjects().filter(o=>o.type==="image").length===6')
    page.get_by_text('文件', exact=True).hover()
    with page.expect_file_chooser() as chooser:
        page.get_by_text('导入文件', exact=True).click()
    chooser.value.set_files(str(saved))
    page.wait_for_function('window.__travelEditor.canvas.getObjects().find(o=>o.name==="宇治标题")?.text==="UJI / SUMMER MEMORY"')
    for actual, before in zip(photos(state()), photos(saved_state)):
        diff = {k: [v, actual.get(k)] for k,v in before.items() if k not in ('src', 'crossOrigin') and v!=actual.get(k)}
        assert not diff, diff
    assert not protected(), protected()
    checks.append('Native text edit + downloaded self-contained JSON + refresh/file import preserves all photos and text')
    with page.expect_download() as event:
        page.get_by_test_id('export-png').click()
    exported = OUT / 'roundtrip.png'
    event.value.save_as(str(exported))
    with Image.open(exported) as im: assert im.size == (2400, 2400)
    checks.append('Native PNG export is 2400 × 2400')

    # Check all nine documents and the delivered embedded originals.
    for entry in entries:
        open_card(entry['id'])
        assert not protected(), (entry['id'], protected())
        assert page.locator('[data-project] img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)')
        doc = json.loads((ROOT / 'outputs/draft-nine/projects' / (entry['id'] + '.json')).read_text())
        for photo in photos(doc):
            assert hashlib.sha256(base64.b64decode(photo['src'].split(',',1)[1])).hexdigest() == photo['sourceHash']
    checks.append('All nine native projects and preview cards load; all 18 embedded originals match SHA-256')
    open_card('04-uji')
    page.screenshot(path=str(OUT / 'editor-nine.png'), full_page=True)
    assert not external, external
    assert not errors, errors
    checks.append('No external HTTP requests or browser page errors during acceptance')
    (OUT / 'report.json').write_text(json.dumps({'passed': True, 'checks': checks, 'page_errors': errors, 'external_requests': external}, ensure_ascii=False, indent=2))
    print(json.dumps({'passed': True, 'checks': checks}, ensure_ascii=False), flush=True)
    browser.close()
