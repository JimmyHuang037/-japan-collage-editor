"""A compact delivery for the two refined, fully editable scrapbooks."""
import json
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DEST = Path(sys.argv[1])
KEYS = ('04-uji', '08-birthday')
font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 27)
preview = Image.new('RGB', (1660, 920), '#f5f0e4')
draw = ImageDraw.Draw(preview)
draw.text((30, 16), '日本旅行 · 参考图手账细化版', font=font, fill='#294435')
for i, (key, title) in enumerate(zip(KEYS, ('宇治 · 夏日碎片', '生日 · 和一点童心'))):
    with Image.open(DEST / 'images' / (key+'.png')) as raw:
        thumb = raw.convert('RGB')
        thumb.thumbnail((790, 790))
        preview.paste(thumb, (30+i*820, 72))
    draw.text((30+i*820, 875), title, font=font, fill='#294435')
preview.save(DEST / '两张拼贴预览.jpg', quality=95)
readme = '''# 日本旅行 · 两张拼贴细化版

依据 2026-10-01 提供的参考图，将宇治和生日页改为旅行手账排版：错落相框、撕纸故事卡、半透明胶带、植物纸花、手写文字及手绘图案。

images/ 中两张 PNG 均为 2400×2400；projects/ 中两份 JSON 内嵌全部原片，支持保存重开。原片字节、完整比例、Drive ID、原文件名及 SHA-256 保留，未裁切、拉伸、调色或重绘。

打开 http://127.0.0.1:3077/，在“九图”选 04 宇治或 08 生日；也可使用“文件 → 导入文件”导入 JSON。相框、文字、撕纸、胶带、植物、纸花和手绘图案均可独立编辑。切换作品或刷新前点击“保存工程”。

本机编辑器已配置旅行楷体和 TravelHand 字体；其他编辑器缺少这些字体时文字外观可能不同。系统字体文件仅保留在本机，不随 ZIP 分发。

真实浏览器已验证图层编辑、等比换图、撤销重做、保存重开及 PNG 导出；原片字节验证通过。旧版已保留在项目 outputs/history/before-reference-refinement-2026-10-01/ 中。
'''
(DEST / '拼贴细化说明.md').write_text(readme)
verification = json.loads((DEST / 'source-verification.json').read_text())
verification['sources'] = [r for r in verification['sources'] if r['project'] in KEYS]
verification['distinct_originals'] = len({r['sha256'] for r in verification['sources']})
archive_path = DEST / '两张拼贴_成图与可编辑工程.zip'
with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=2) as archive:
    for key in KEYS:
        for folder, suffix in (('images', '.png'), ('projects', '.json')):
            p = DEST / folder / (key+suffix)
            archive.write(p, p.relative_to(DEST))
    archive.write(DEST / '两张拼贴预览.jpg', '两张拼贴预览.jpg')
    archive.writestr('README.md', readme)
    archive.writestr('source-verification.json', json.dumps(verification, ensure_ascii=False, indent=2))
with zipfile.ZipFile(archive_path) as archive:
    assert archive.testzip() is None
print(json.dumps({'refined_projects': list(KEYS), 'verified_originals': verification['distinct_originals'],
                  'zip_bytes': archive_path.stat().st_size}, ensure_ascii=False))
