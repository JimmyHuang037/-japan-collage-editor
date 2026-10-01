"""Compose editable Fabric documents from screened, byte-preserved source photos."""
import base64
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public/travel/projects'
OUT = ROOT / 'outputs/draft-nine'
INDEX = {r['number']: r for r in json.loads((ROOT / 'data/screening/index.json').read_text())}
CATALOG = {r['id']: r for r in json.loads((ROOT / 'public/travel/catalog.json').read_text())}
CREAM, GREEN, BLUE, INK, RED = '#f6f1e7', '#233f3a', '#dcebf1', '#243e38', '#b8644c'


def shape(kind, **attrs):
    return {'type': kind, 'version': '5.3.0', 'originX': 'left', 'originY': 'top',
            'scaleX': 1, 'scaleY': 1, 'strokeWidth': 0, 'id': attrs.get('name', kind), **attrs}


def rect(x, y, w, h, color, name, **attrs):
    return shape('rect', left=x, top=y, width=w, height=h, fill=color, name=name, **attrs)


def text(content, x, y, size=36, color=INK, width=1800, name='文案', family='华康金刚黑', **attrs):
    return shape('textbox', text=content, left=x, top=y, width=width, fontSize=size,
                 fontFamily=family, fill=color, splitByGrapheme=True, lineHeight=attrs.pop('lineHeight', 1.3),
                 name=name, id=name + ':' + str(x) + ':' + str(y), **attrs)


def source(n):
    row = CATALOG[INDEX[n]['id']]
    path = ROOT / 'data/originals' / (row['id'] + '.jpg')
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    return row, path


def photo(n, x, y, w=None, h=None):
    row, path = source(n)
    with Image.open(path) as raw:
        width, height = ImageOps.exif_transpose(raw).size
    scale = min(w / width if w else 1, h / height if h else 1)
    if w and not h: scale = w / width
    if h and not w: scale = h / height
    return shape('image', left=x, top=y, width=width, height=height, scaleX=scale,
        scaleY=scale, src=row['src'], crossOrigin='anonymous', cropX=0, cropY=0,
        filters=[], photoId=row['id'], originalName=row['originalName'],
        sourceHash=row['sha256'], name='原片 · ' + row['originalName'].split('/')[-1],
        id='photo-' + row['id'])


def framed(objects, n, x, y, w=None, h=None, tape=False):
    image = photo(n, x, y, w, h)
    width, height = image['width'] * image['scaleX'], image['height'] * image['scaleY']
    objects.append(rect(x-16, y-16, width+32, height+32, '#fffdf9', '相框-'+str(n),
                        stroke='#ddd5c9', strokeWidth=2))
    objects.append(image)
    if tape:
        objects.append(rect(x+width*.35, y-40, min(210, width*.4), 24, '#d8c6a3', '胶带-'+str(n), angle=-4))
    return width, height


def document(width, height, objects, color=CREAM):
    return {'version': '5.3.0', 'objects': [rect(0, 0, width, height, color, '画布',
                id='workspace', selectable=False, hasControls=False, evented=False)] + objects}


def uji():
    from scrapbook import uji_scrapbook
    return uji_scrapbook()


def birthday():
    from scrapbook import birthday_scrapbook
    return birthday_scrapbook()


def portable(doc):
    doc = json.loads(json.dumps(doc))
    for obj in doc['objects']:
        if obj['type'] == 'image':
            _, path = source(next(n for n, row in INDEX.items() if row['id'] == obj['photoId']))
            obj['src'] = 'data:image/jpeg;base64,' + base64.b64encode(path.read_bytes()).decode()
    return doc


def main():
    PUBLIC.mkdir(parents=True, exist_ok=True)
    for folder in ('images', 'projects', 'sources'):
        (OUT / folder).mkdir(parents=True, exist_ok=True)
    entries = [
      ('01-usj', '01 · USJ，玩到尽兴', 'photo', 167, '飞天翼龙标识与游玩后自然的大笑；比普通打卡照更有情绪。'),
      ('02-nara', '02 · 奈良，和鹿同框', 'photo', 60, '鹿在前景、两人自然入镜，保留草坡与天空的开阔感。'),
      ('03-kyoto', '03 · 京都，金阁与夏云', 'photo', 284, '完整金阁寺、倒影与夏云，作为人像之间安静的一格。'),
      ('04-uji', '04 · 宇治，故事走到眼前', 'composite', None, '京吹必选巡礼、任天堂与三人夜爬分别讲清，夜爬照片保持原样。'),
      ('05-suwa', '05 · 诹访湖，花火盛开', 'photo', 1179, '比较多组花火后选三簇紫金烟花，结构清楚并保留湖岸夜色。'),
      ('06-fuji', '06 · 富士山，在云上', 'photo', 401, '清楚的山峰与云带，完整横向风景给整组留出呼吸。'),
      ('07-tokyo', '07 · 东京，日落与我们', 'photo', 1222, '选高分辨率版本，完整保留两人全身、涩谷落日与城市高度。'),
      ('08-birthday', '08 · 生日，和一点童心', 'composite', None, '以咖啡馆合照为主，串起任意门、道具、富士秋千和生日和牛。'),
      ('09-sea', '09 · 看海，笑得很大声', 'photo', 722, '自然的大笑与同伴、海面及铁路同框，适合以轻松情绪收尾。'),
    ]
    index, manifest = [], []
    for key, name, kind, n, reason in entries:
        if kind == 'photo':
            row, path = source(n)
            image = photo(n, 0, 0)
            doc = document(image['width'], image['height'], [image], '#ffffff')
            shutil.copyfile(path, OUT / 'images' / (key + '.jpg'))
        else:
            doc = uji() if key == '04-uji' else birthday()
        (PUBLIC / (key + '.json')).write_text(json.dumps(doc, ensure_ascii=False))
        (OUT / 'projects' / (key + '.json')).write_text(json.dumps(portable(doc), ensure_ascii=False))
        ids = [o['photoId'] for o in doc['objects'] if o['type'] == 'image']
        for photo_id in ids:
            shutil.copyfile(ROOT / 'data/originals' / (photo_id + '.jpg'), OUT / 'sources' / (photo_id + '.jpg'))
        index.append({'id': key, 'name': name, 'kind': kind, 'project': '/travel/projects/' + key + '.json',
                      'preview': '/travel/projects/' + key + '.jpg'})
        manifest.append({'id': key, 'title': name, 'kind': kind, 'selection_reason': reason,
            'photos': [CATALOG[i] for i in ids], 'photo_content_unchanged': True,
            'source_dates': '文件名不作为核实后的拍摄日期；故事依据用户原文与实际看图。'})
    (PUBLIC / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2))
    (OUT / 'selection.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    inventory = json.loads((ROOT / 'data/reference/drive-current.json').read_text())
    groups = {}
    for r in inventory:
        groups.setdefault(r.get('md5Checksum', r['id']), []).append(r['id'])
    report = {'total_contact_sheet_reviewed': len(INDEX), 'contact_sheets': 31,
        'full_resolution_candidates_compared': 33, 'single_photos': 7, 'composites': 2,
        'distinct_selected_sources': len({i for r in manifest for i in [p['id'] for p in r['photos']]}),
        'identical_byte_groups_in_drive': sum(len(v) > 1 for v in groups.values()),
        'duplicate_policy': '保留所有 Drive ID，不删除、不覆盖；只避免重复入选。',
        'visual_status': '参考图手账细化版，等待用户视觉审核',
        'refinement': '2026-10-01：宇治与生日页改为错落相框、撕纸、独立胶带、植物纸花与手绘图案；完整等比展示原片。',
        'limitations': ['夜爬自拍原片有雾感，未修图。', '和牛原片分辨率较低，仅作为拼贴小图。',
            '七张单图无法各自容纳全部景点，遗漏的细节放入配文与替补说明。',
            '没有找到可明确对应香港夫妇、上海家庭推孩子秋千的合照，不用其他照片冒充。']}
    (OUT / 'screening-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
