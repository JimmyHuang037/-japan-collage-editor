"""Package only private user deliverables; never include OAuth or signed Drive URLs."""
import base64
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path('/app')
OUT = ROOT / 'outputs/draft-nine'
DEST = Path(sys.argv[1])
DEST.mkdir(parents=True, exist_ok=True)
report = json.loads((ROOT / 'outputs/browser-acceptance/report.json').read_text())
assert report['passed']
manifest = json.loads((OUT / 'selection.json').read_text())
inventory = {r['id']: r for r in json.loads((ROOT / 'data/reference/drive-current.json').read_text())}
verified, hashes = [], set()
for row in manifest:
    doc = json.loads((OUT / 'projects' / (row['id'] + '.json')).read_text())
    workspace = next(o for o in doc['objects'] if o['id'] == 'workspace')
    for photo in row['photos']:
        photo['reviewed'] = True
        raw = (OUT / 'sources' / (photo['id'] + '.jpg')).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        assert digest == photo['sha256']
        assert hashlib.md5(raw).hexdigest() == inventory[photo['id']]['md5Checksum']
        obj = next(o for o in doc['objects'] if o.get('photoId') == photo['id'])
        assert base64.b64decode(obj['src'].split(',', 1)[1]) == raw
        assert abs(obj['scaleX'] - obj['scaleY']) < 1e-10
        assert obj['cropX'] == obj['cropY'] == 0 and not obj['filters']
        hashes.add(digest)
        verified.append({'project': row['id'], 'drive_id': photo['id'], 'original_name': photo['originalName'], 'sha256': digest, 'md5_matches_drive': True})
    images = list((OUT / 'images').glob(row['id'] + '.*'))
    assert len(images) == 1
    if row['kind'] == 'photo':
        assert hashlib.sha256(images[0].read_bytes()).hexdigest() == row['photos'][0]['sha256']
    else:
        with Image.open(images[0]) as im: assert im.size == (2400, 2400)
assert len(hashes) == 18 and len(list((OUT / 'images').iterdir())) == 9
(OUT / 'selection.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
(OUT / 'source-verification.json').write_text(json.dumps({'passed': True, 'distinct_originals': 18, 'sources': verified}, ensure_ascii=False, indent=2))
shutil.copyfile(ROOT / 'outputs/browser-acceptance/report.json', OUT / 'browser-verification.json')

readme = '''# 日本旅行 · 八月存档 · 手账拼贴细化版

已完成 7 张原图直出和 2 张拼贴；每张都有可编辑工程。2026-10-01 按本次参考图细化宇治与生日拼贴：错落相框、撕纸故事卡、半透明胶带、植物纸花和手绘图案，中文使用本机楷体、英文使用本机手写字体。功能验收通过，等待你的视觉反馈。

## 文件与发布顺序

| 顺序 | 文件 | 内容 |
| --- | --- | --- |
| 1 | 01-usj.jpg | USJ，飞天翼龙前的笑脸 |
| 2 | 02-nara.jpg | 奈良，和鹿同框 |
| 3 | 03-kyoto.jpg | 京都，金阁与夏云 |
| 4 | 04-uji.png | 宇治：京吹巡礼、任天堂、三人夜爬大吉山 |
| 5 | 05-suwa.jpg | 诹访湖，紫金花火 |
| 6 | 06-fuji.jpg | 富士山，在云上 |
| 7 | 07-tokyo.jpg | 涩谷的日落与两人合照 |
| 8 | 08-birthday.png | 小马生日、和牛、富士秋千与哆啦 A 梦 |
| 9 | 09-sea.jpg | 镰仓，看海时的大笑 |

`images/` 恰好九张，适合按文件名顺序使用。七张 JPEG 与原片逐字节一致，保留原始尺寸和 EXIF；两张 PNG 为 2400 × 2400。预览总览只是展示排布，所有照片完整等比显示。

`projects/` 含九个快图 Fabric JSON；原片字节已内嵌，不依赖 Drive 临时网址、本地软链接或 blob 地址。`sources/` 是 18 张所用原片的额外备份，按 Drive ID 命名；`selection.json` 保留 ID、原文件名、哈希、尺寸与入选理由。

## 在原快图界面里修改

1. 打开 http://127.0.0.1:3077/，左侧“九图”选作品；也可在“文件 → 导入文件”选择 `projects/` 中任一个 JSON。
2. 点选文字后双击修改；选照片可移动、等比缩放、整体旋转。文字、相框、撕纸、胶带、植物、纸花、音符、箭头与蛋糕均为独立图层，可在“图层”面板选中。
3. 换原片：选中画布照片，左侧“照片”勾选“替换当前选中的照片”，再点本地素材；右侧“替换图片”可选自己的图片文件。横竖图互换保持完整比例，留白不会被强行填满。
4. 点击“保存工程”下载含原片的 JSON；重新导入可接着修改。切换作品或刷新前请保存，左侧打开的是这次固定初稿，不会自动覆盖初稿文件。
5. 点击“导出 PNG”输出当前画布；七张单图若要保持原文件字节，直接使用 `images/` 的 JPEG。

请在本项目编辑器打开；已有快图字体及新增的本机旅行楷体、TravelHand 均本地加载，不发送外部字体请求。其他 Fabric 环境若缺少字体，文本外观可能不同。系统字体只保留在本机编辑器，不打入交付 ZIP。

## 选片依据与取舍

已复核项目交接、最初《朋友圈创意编辑整理》原文，以及 9 月 21、22 日实施会话。按本次最新目标固定为 7+2。完整浏览 1,483 张图片的 31 张联系表，再比较 33 张候选原片，最终使用 18 张不同原片。

单图保留自然表情、同伴关系和风景的呼吸感；两张拼贴集中在最有个人兴趣与故事的宇治、生日和童心。宇治的京吹、三人夜爬与任天堂均已保留。

没有把全部景点塞进九格：京都其他建筑、鸭川聊天、甲府泡汤、河口湖骑行与音乐盒、东京其他观景点可留在配文或下一条记录。没有找到可明确对应香港夫妇、上海家庭的合照，不用别人的照片代替。

夜爬自拍原片有雾感；保留它是因为三人夜爬必须出现。和牛原片较小，放在拼贴的小图位，不做修复或生成。编号与文件名日期仅用于定位，不当作已经核实的拍摄时间。

## 验收

真实 Chromium 完成九图加载、独立图层拖动、横竖换片、撤销重做、Shift 缩放、旋转、边界、组合与拆组、文字编辑、保存刷新重导入、PNG 导出和网络核查。所用 18 张原片均通过 Drive MD5 与 SHA-256 校验，九个工程内嵌字节一致。具体报告见两个 verification JSON。功能测试通过不代替你的审美确认。
'''
(OUT / 'README.md').write_text(readme)
(OUT / '朋友圈配文.md').write_text('''# 配文草稿

八月存档。🎞️

从飞天翼龙到宇治的夜色，从花火到富士山，再到海边。
看了喜欢的风景，也遇见了很好的人。
谢谢小马一路同行，也谢谢路上的善意。

还有，哆啦 A 梦的九个隐藏道具，全都找到啦。

---

如果想多留一点旅行细节，可加在评论里：

鸭川边聊了一会儿天，和浙江兄弟一起夜爬大吉山。诹访湖边，香港夫妇用石头帮我们压好垫子；河口湖的骑行和音乐盒，也想再来一次。给小马庆祝生日，富士山下荡秋千，新宿吃和牛。

路上的几首歌也一起存档：花火时的 EVA、涩谷的 Stay With Me、海边的 If I Ain’t Got You。
''')

font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
board = Image.new('RGB', (1560, 1800), '#f6f1e7')
draw = ImageDraw.Draw(board)
draw.text((36, 20), '八月存档  ·  7 张原图 + 2 张故事拼贴', fill='#243e38', font=font)
for i, row in enumerate(manifest):
    x, y = 30 + (i % 3)*510, 90 + (i // 3)*560
    path = next((OUT / 'images').glob(row['id'] + '.*'))
    with Image.open(path) as raw:
        preview = ImageOps.exif_transpose(raw).convert('RGB')
        preview.thumbnail((480, 480))
        board.paste(preview, (x+(480-preview.width)//2, y+(480-preview.height)//2))
    draw.text((x, y+492), row['title'], fill='#243e38', font=font)
board.save(OUT / '九图总览.jpg', quality=94)
for folder in ('images', 'projects'):
    shutil.copytree(OUT / folder, DEST / folder, dirs_exist_ok=True)
for name in ('README.md', '朋友圈配文.md', '九图总览.jpg', 'selection.json', 'screening-report.json', 'source-verification.json', 'browser-verification.json'):
    shutil.copyfile(OUT / name, DEST / name)
for name, folders in [('日本旅行_九张成图.zip', ['images']), ('日本旅行_九图与可编辑工程.zip', ['images', 'projects', 'sources'])]:
    with zipfile.ZipFile(DEST / name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=2) as archive:
        for folder in folders:
            for path in sorted((OUT / folder).iterdir()): archive.write(path, path.relative_to(OUT))
        for path in OUT.iterdir():
            if path.is_file(): archive.write(path, path.name)
    with zipfile.ZipFile(DEST / name) as archive: assert archive.testzip() is None
print(json.dumps({'verified_sources': len(hashes), 'images': 9, 'destination': str(DEST), 'zips': {p.name: p.stat().st_size for p in DEST.glob('*.zip')}}, ensure_ascii=False), flush=True)
