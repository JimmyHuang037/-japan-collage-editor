"""Read-only Drive screening previews. Signed URLs stay in memory, never in manifests."""
import io
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont
from drive import service, FOLDER, ROOT


def main():
    api = service()
    rows, pending = [], [FOLDER]
    while pending:
        parent, token = pending.pop(), None
        while True:
            page = api.files().list(q=f"'{parent}' in parents and trashed=false", pageSize=1000,
                pageToken=token, fields='nextPageToken,files(id,name,mimeType,thumbnailLink)').execute()
            for row in page.get('files', []):
                if row['mimeType'] == 'application/vnd.google-apps.folder':
                    pending.append(row['id'])
                elif row['mimeType'].startswith('image/'):
                    rows.append(row)
            token = page.get('nextPageToken')
            if not token:
                break
    rows.sort(key=lambda r: (r['name'].split('/')[-1], r['id']))
    target = ROOT / 'data/screening/thumbs'
    target.mkdir(parents=True, exist_ok=True)
    thread = threading.local()

    def fetch(row):
        path = target / (row['id'] + '.jpg')
        if path.exists():
            return True
        url = row.get('thumbnailLink')
        if not url:
            return False
        url = re.sub(r'=s\d+$', '=s720', url)
        if not hasattr(thread, 'session'):
            thread.session = requests.Session()
        for _ in range(3):
            try:
                response = thread.session.get(url, timeout=40)
                response.raise_for_status()
                with Image.open(io.BytesIO(response.content)) as source:
                    im = ImageOps.exif_transpose(source).convert('RGB')
                    im.thumbnail((720, 720))
                    im.save(path, quality=90)
                return True
            except Exception:
                pass
        return False

    failed = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        tasks = {pool.submit(fetch, row): row for row in rows}
        for n, future in enumerate(as_completed(tasks), 1):
            row = tasks[future]
            if not future.result():
                failed.append(row['id'])
            if n % 100 == 0:
                print(f'Screening previews: {n}/{len(rows)}; unavailable: {len(failed)}', flush=True)
    safe = [{'number': n + 1, 'id': r['id'], 'name': r['name'],
             'preview_available': r['id'] not in failed} for n, r in enumerate(rows)]
    (ROOT / 'data/screening/index.json').write_text(json.dumps(safe, ensure_ascii=False, indent=2))
    sheets = ROOT / 'outputs/screening'
    sheets.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 15)
    for offset in range(0, len(safe), 48):
        batch = safe[offset:offset + 48]
        sheet = Image.new('RGB', (1680, ((len(batch) + 5) // 6) * 190), '#f8f5ef')
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(batch):
            x, y = (i % 6) * 280, (i // 6) * 190
            path = target / (row['id'] + '.jpg')
            if path.exists():
                im = Image.open(path)
                im.thumbnail((274, 156))
                sheet.paste(im, (x + (280 - im.width) // 2, y + (156 - im.height) // 2))
            draw.text((x + 3, y + 158), f"{row['number']:04d} {row['name'].split('/')[-1][-25:]}", font=font, fill='#243e38')
        sheet.save(sheets / f'{offset // 48 + 1:03d}.jpg', quality=90)
    print(json.dumps({'inventory': len(rows), 'previews': len(rows) - len(failed), 'failed_ids': failed}), flush=True)


if __name__ == '__main__':
    main()
