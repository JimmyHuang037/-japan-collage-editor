"""Build full-frame previews and a local ID-based catalog; never change originals."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public/travel'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'thumbs').mkdir(exist_ok=True)
rows = json.loads((ROOT / 'data/reference/已下载照片索引.json').read_text())
by_id = {r['id']: r['original_name'] for r in rows}
current = ROOT / 'data/reference/drive-current.json'
if current.exists(): by_id.update({r['id']: r['name'] for r in json.loads(current.read_text())})
photos = OUT / 'photos'
if not photos.exists(): photos.symlink_to('../../data/originals', target_is_directory=True)
catalog = []
for path in sorted((ROOT / 'data/originals').glob('*.jpg')):
    with Image.open(path) as source:
        im = ImageOps.exif_transpose(source).convert('RGB')
        w, h = im.size
        im.thumbnail((480, 360))
        im.save(OUT / 'thumbs' / path.name, quality=86)
    catalog.append({'id': path.stem, 'originalName': by_id.get(path.stem, path.name),
        'src': f'/travel/photos/{path.name}', 'thumb': f'/travel/thumbs/{path.name}',
        'width': w, 'height': h, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'city': '待核实', 'reviewed': False})
(OUT / 'catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2))
font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 16)
contact_dir = ROOT / 'outputs/contact-sheets'
contact_dir.mkdir(parents=True, exist_ok=True)
for offset in range(0, len(catalog), 30):
    batch = catalog[offset:offset+30]
    sheet = Image.new('RGB', (1400, ((len(batch)+4)//5)*205), '#f8f5ef')
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(batch):
        im = Image.open(OUT / 'thumbs' / (row['id']+'.jpg'))
        im.thumbnail((265, 170))
        x, y = (i%5)*280, (i//5)*205
        sheet.paste(im,(x+(280-im.width)//2,y))
        draw.text((x+4,y+172),f"{offset+i+1:03d}  {row['originalName'].split('/')[-1][-23:]}",font=font,fill='#243e38')
    sheet.save(contact_dir/f'{offset//30+1:03d}.jpg',quality=88)
print(json.dumps({'photos':len(catalog),'contact_sheets':(len(catalog)+29)//30}))
