"""Reference-inspired scrapbooks; all decoration is editable native Fabric vector art."""
import math
import random

from build_nine import document, photo, rect, shape, text

PAPER, INK, MOSS, PINK = '#f5f0e4', '#294435', '#4a6849', '#c77c86'
SHADOW = {'color': 'rgba(40,47,32,0.19)', 'blur': 26, 'offsetX': 8, 'offsetY': 12}


def torn(x, y, width, height, color, name, angle=0, shadow=True):
    rng = random.Random(name)
    points = []
    for i in range(26):
        points.append({'x': width*i/25, 'y': rng.uniform(0, 13)})
    for i in range(1, 10):
        points.append({'x': width-rng.uniform(0, 10), 'y': height*i/10})
    for i in range(26):
        points.append({'x': width*(25-i)/25, 'y': height-rng.uniform(0, 13)})
    for i in range(9, 0, -1):
        points.append({'x': rng.uniform(0, 10), 'y': height*i/10})
    return shape('polygon', left=x, top=y, points=points, fill=color, angle=angle,
                 name=name, shadow=SHADOW if shadow else None)


def path(commands, x, y, color, name, stroke=None, sw=2, **attrs):
    return shape('path', path=commands, left=x, top=y, fill=color,
                 stroke=stroke, strokeWidth=sw if stroke else 0,
                 strokeLineCap='round', strokeLineJoin='round', name=name, **attrs)


def sprig(o, x, y, size=1, angle=0, color=MOSS, name='植物贴纸'):
    # A single compound path keeps the entire botanical sticker independently movable.
    commands = [['M', 70, 315], ['C', 52, 225, 89, 116, 75, 4]]
    for i in range(7):
        sy = 40+i*36
        cx = 74 + math.sin(i)*9
        for direction in (-1, 1):
            ex = cx + direction*(47+(i%3)*8)
            ey = sy-34
            commands += [['M', cx, sy+20],
                         ['C', cx+direction*40, sy+16, ex+direction*13, ey+18, ex, ey],
                         ['C', cx+direction*13, ey-4, cx+direction*3, sy-5, cx, sy+20],
                         ['Z']]
    o.append(path(commands, x, y, color, name, stroke=color, sw=2,
                  scaleX=size, scaleY=size, angle=angle))


def flower(o, x, y, size=1, color=PINK, name='花朵贴纸'):
    commands = []
    for i in range(5):
        a = i*math.tau/5-math.pi/2
        tip = (50+math.cos(a)*46, 50+math.sin(a)*46)
        c1 = (50+math.cos(a-.62)*52, 50+math.sin(a-.62)*52)
        c2 = (50+math.cos(a+.62)*52, 50+math.sin(a+.62)*52)
        commands += [['M', 50, 50], ['C', *c1, *tip, *tip], ['C', *tip, *c2, 50, 50], ['Z']]
    o.append(path(commands, x, y, color, name, scaleX=size, scaleY=size))
    o.append(shape('circle', left=x+39*size, top=y+39*size, radius=10*size,
                   fill='#dbba6b', name=name+'花心'))


def star(o, x, y, size=45, color='#b98b43', name='手绘星星'):
    pts = []
    for i in range(10):
        a = i*math.pi/5-math.pi/2
        r = size if i%2 == 0 else size*.4
        pts.append({'x': size+math.cos(a)*r, 'y': size+math.sin(a)*r})
    o.append(shape('polygon', left=x, top=y, points=pts, fill=None,
                   stroke=color, strokeWidth=4, name=name))


def tape(o, x, y, width, color, name, angle=-8):
    sticker = torn(x, y, width, 63, color, name, angle, shadow=False)
    sticker['opacity'] = .83
    o.append(sticker)


def card(o, n, x, y, width=None, height=None, angle=0, caption='', paper='#fffdf7'):
    image = photo(n, 0, 0, w=width, h=height)
    w, h = image['width']*image['scaleX'], image['height']*image['scaleY']
    a = math.radians(angle)

    def position(dx, dy):
        return x+dx*math.cos(a)-dy*math.sin(a), y+dx*math.sin(a)+dy*math.cos(a)

    o.append(rect(x, y, w+40, h+(112 if caption else 40), paper, '相框-'+str(n),
                  angle=angle, shadow=SHADOW))
    px, py = position(20, 20)
    image.update(left=px, top=py, angle=angle)
    o.append(image)
    if caption:
        tx, ty = position(27, h+42)
        caption_size = min(29, (w-12)/len(caption)*.94)
        o.append(text(caption, tx, ty, caption_size, INK, width=w-12,
                      name='照片说明-'+str(n), family='旅行楷体', angle=angle))
    return w, h


def base(color, tint):
    o = [rect(34, 34, 2332, 2332, PAPER, '手账底纸', shadow=SHADOW)]
    # Sparse local paper grain: independent vectors, no photograph or generated background.
    rng = random.Random(20261001)
    for i in range(160):
        o.append(shape('circle', left=rng.uniform(55, 2345), top=rng.uniform(55, 2345),
                       radius=rng.uniform(.8, 2.2), fill='#96896b', opacity=.11,
                       name='纸纹-'+str(i)))
    o.append(torn(1660, 90, 650, 2140, tint, '右侧衬纸', -1, shadow=False))
    for i in range(13):
        o.append(shape('line', left=1710, top=115+i*165, x1=0, y1=0, x2=540, y2=0,
                       stroke=color, strokeWidth=1, opacity=.13, name='笔记横线-'+str(i)))
    return o


def uji_scrapbook():
    o = base(MOSS, '#e4e8d5')
    sprig(o, 2020, 50, 1.13, -36, '#8a9b62', '右上橄榄枝')
    sprig(o, 57, 1290, .92, -4, '#668453', '左侧绿叶')
    o += [torn(120, 85, 970, 210, '#fffcf4', '宇治标题纸', -2),
          text('宇治 · 夏日碎片', 161, 105, 85, INK, width=1080,
               name='宇治标题', family='旅行楷体', angle=-2),
          text('a little summer in Uji', 172, 214, 33, MOSS, width=890,
               name='宇治英文标题', family='TravelHand', angle=-2),
          text('喜欢的故事，走到了眼前。', 1180, 172, 33, INK, width=850,
               name='宇治副标题', family='旅行楷体', angle=2)]
    card(o, 303, 118, 389, width=1340, angle=-3,
         caption='手里的画面，眼前的宇治。')
    tape(o, 650, 335, 268, '#c7b98e', '胶带-303', -7)
    card(o, 961, 1580, 305, width=610, angle=5,
         caption='先去任天堂玩一会儿。')
    tape(o, 1840, 287, 236, '#acc1a1', '胶带-961', 11)
    card(o, 298, 1675, 923, height=483, angle=-5,
         caption='这一帧，终于对上了。')
    tape(o, 1760, 883, 208, '#cabb98', '胶带-298', -10)
    o += [torn(2152, 988, 157, 450, '#f9f5e9', '巡礼窄纸', 1),
          text('跟\n着\n喜\n欢\n找\n到\n这\n里', 2190, 1015, 34, MOSS,
               width=95, name='巡礼小字', family='旅行楷体', lineHeight=1.14),
          text('SOUND! EUPHONIUM', 185, 1480, 29, MOSS, width=1300,
               name='宇治英文注脚', family='Georgia', charSpacing=100, angle=-2)]
    # Layer the paper edges while keeping every original photo fully visible.
    o.append(torn(86, 1600, 2200, 690, '#29493b', '夜色撕纸', -1.5))
    card(o, 324, 125, 1661, height=412, angle=-5, caption='京吹巡礼 · 夜色')
    card(o, 325, 535, 1600, height=436, angle=3, caption='和小马一起往山上走。')
    card(o, 327, 956, 1669, width=548, angle=-4, caption='三个人，同一片夜色。')
    tape(o, 211, 1600, 172, '#d5c39b', '胶带-324', -11)
    tape(o, 680, 1555, 178, '#afbc94', '胶带-325', 6)
    tape(o, 1112, 1624, 220, '#d5c39b', '胶带-327', -7)
    o += [torn(1610, 1660, 572, 449, '#f3eedc', '夜爬故事纸', 4),
          text('AFTER DARK', 1652, 1710, 28, MOSS, width=500,
               name='夜爬章节', family='Georgia', charSpacing=130, angle=4),
          text('三个人，\n同一片夜色。', 1640, 1780, 52, INK, width=540,
               name='夜爬标题', family='旅行楷体', angle=4),
          text('浙江兄弟、小马和我。\n动画之外，也有好故事。', 1630, 1951, 29, INK,
               width=530, name='夜爬故事', family='旅行楷体', angle=4),
          text('大吉山 / 把这个夜晚记住', 225, 2220, 33, '#efead8', width=1100,
               name='夜爬照片说明', family='旅行楷体', angle=-1),
          text('八月存档  /  GOOD COMPANY', 1310, 2320, 25, MOSS, width=950,
               name='宇治页脚', family='Georgia', charSpacing=90)]
    sprig(o, 2150, 1669, .56, -10, '#8da66c', '故事纸边枝叶')
    sprig(o, 2008, 2182, .48, -56, '#98ab73', '夜色绿叶')
    sprig(o, 55, 97, .60, 15, '#5f814d', '标题绿叶')
    flower(o, 1465, 690, .67, '#e7c997', '宇治纸花')
    star(o, 1456, 291, 34, MOSS, '宇治小星星')
    # Editable handwritten music mark in the free space between photos.
    o.append(path([['M', 14, 91], ['C', -16, 72, -9, 123, 20, 110],
                   ['L', 26, 9], ['L', 81, 0], ['L', 81, 86],
                   ['C', 52, 64, 51, 112, 83, 100]],
                  1515, 1270, None, '手绘音符', stroke=MOSS, sw=7, angle=8))
    return document(2400, 2400, o, '#405641')


def birthday_scrapbook():
    o = base('#729199', '#e3eceb')
    o.append(torn(82, 1580, 2175, 730, '#e9e2cb', '生日底部撕纸', -1.5))
    sprig(o, 2075, 55, .98, -30, '#9baa85', '生日右上枝叶')
    sprig(o, 51, 1300, .80, -3, '#7e9778', '生日左侧枝叶')
    o += [torn(123, 88, 1070, 202, '#fffcf4', '生日标题纸', -2),
          text('长大了，也可以很贪玩。', 164, 112, 72, INK, width=1390,
               name='童心标题', family='旅行楷体', angle=-2),
          text('good company, good days', 174, 218, 32, '#ad6f78', width=1000,
               name='生日英文标题', family='TravelHand', angle=-2),
          text('生日 / 富士山 / 一点童心', 1320, 183, 31, INK, width=900,
               name='生日副标题', family='旅行楷体', angle=2)]
    card(o, 1182, 116, 389, width=1340, angle=-3,
         caption='咖喱饭、大雄拿铁，快乐很具体。')
    tape(o, 660, 337, 275, '#a9c5cc', '胶带-1182', -7)
    card(o, 512, 1580, 318, width=605, angle=5,
         caption='如果有任意门，就再出发。')
    tape(o, 1810, 284, 254, '#d3b3b7', '胶带-512', 10)
    card(o, 837, 1730, 987, height=475, angle=-5,
         caption='九个道具，全部找到')
    tape(o, 1792, 944, 219, '#a9c5cc', '胶带-837', -12)
    o += [text('PLAY!', 1545, 1110, 31, '#a26f76', width=145,
               name='童心小字', family='TravelHand', angle=-4),
          text('旅行里的快乐，常常很幼稚，也很具体。', 173, 1490, 31, INK, width=1400,
               name='童心主照片说明', family='旅行楷体', angle=-2)]
    card(o, 1307, 137, 1661, height=480, angle=-4,
         caption='富士山下，两个人荡秋千。')
    card(o, 1105, 654, 1661, height=442, angle=4,
         caption='新宿和牛 · 小马生日')
    tape(o, 250, 1620, 218, '#d2b398', '胶带-1307', -9)
    tape(o, 721, 1620, 223, '#a9c5cc', '胶带-1105', 9)
    o += [torn(1182, 1692, 905, 439, '#fffaf0', '生日故事纸', -2),
          text('HAPPY BIRTHDAY', 1240, 1738, 30, '#ad6f78', width=800,
               name='生日英文', family='Georgia', charSpacing=110, angle=-2),
          text('一起玩，一起好好吃饭。', 1237, 1810, 58, INK, width=840,
               name='生日故事标题', family='旅行楷体', angle=-2),
          text('富士山下荡秋千。\n新宿吃一顿和牛，庆祝小马生日。\n把童心和好朋友都留在这一页。', 1240, 1935, 32, INK,
               width=835, name='生日故事', family='旅行楷体', angle=-2),
          text('八月存档 · 和小马的好日子', 1205, 2260, 32, INK, width=1090,
               name='生日页脚', family='旅行楷体', angle=-2)]
    # Botanical paper stickers sit on margins and paper, never across a face.
    sprig(o, 2190, 1010, .45, 1, '#7f9976', '道具纸边枝叶')
    sprig(o, 1970, 2110, .49, -60, '#889b7a', '生日底部枝叶')
    flower(o, 1485, 767, .71, '#c78692', '任意门纸花')
    flower(o, 2150, 770, .51, '#d49ca6', '任意门小花')
    flower(o, 2136, 2113, .73, '#c78692', '生日纸花')
    star(o, 1490, 335, 30, '#b88d48', '生日小星星')
    star(o, 1077, 1648, 27, '#b88d48', '生日许愿星')
    o.append(path([['M', 0, 0], ['Q', 35, 38, 95, 26],
                   ['M', 75, 8], ['L', 95, 26], ['L', 74, 43]],
                  1570, 1170, None, '道具手绘箭头', stroke='#a26f76', sw=4))
    # One native path forms an editable hand-drawn cake sticker.
    o.append(path([['M', 6, 90], ['L', 154, 90], ['L', 154, 171], ['L', 6, 171], ['Z'],
                   ['M', 6, 112], ['Q', 24, 141, 42, 112], ['Q', 60, 141, 78, 112],
                   ['Q', 96, 141, 114, 112], ['Q', 134, 141, 154, 112],
                   ['M', 79, 90], ['L', 79, 36],
                   ['M', 80, 4], ['C', 51, 38, 97, 44, 80, 4]],
                  2130, 1748, None, '手绘生日蛋糕', stroke='#b47979', sw=6, angle=7))
    return document(2400, 2400, o, '#8b9e8c')
