"""易アプリのアイコン(太極図)を作る。使い方: python tools/make-icons.py  (Pillow が必要: pip install pillow)
icon-512.png / icon-192.png / apple-touch-icon.png / icon.svg を、リポジトリ直下に書き出す。
背景は全面を塗る(OSが角を丸める。maskable に対応するため、図は中央の約65%に収める)。"""
from pathlib import Path
from PIL import Image, ImageDraw

BG, GOLD = (0x12, 0x14, 0x1d), (0xd6, 0xb2, 0x6a)
ROOT = Path(__file__).resolve().parent.parent
S = 8  # 作図は8倍の大きさで行い、縮小してなめらかにする

def render(size):
    n = 512 * S
    im = Image.new('RGB', (n, n), BG)
    d = ImageDraw.Draw(im)
    def circle(cx, cy, r, fill=None, outline=None, width=0):
        d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill, outline=outline, width=width * S)
    circle(256, 256, 160, outline=GOLD, width=8)                       # 外の輪
    d.pieslice([(256 - 140) * S, (256 - 140) * S, (256 + 140) * S, (256 + 140) * S], -90, 90, fill=GOLD)  # 右半分
    circle(256, 326, 70, fill=GOLD)                                     # 下のふくらみ(金)
    circle(256, 186, 70, fill=BG)                                       # 上のふくらみ(紺)
    circle(256, 186, 22, fill=GOLD)                                     # 上の点
    circle(256, 326, 22, fill=BG)                                       # 下の点
    return im.resize((size, size), Image.LANCZOS)

SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" fill="#{BG[0]:02x}{BG[1]:02x}{BG[2]:02x}"/><circle cx="256" cy="256" r="160" fill="none" stroke="#{GOLD[0]:02x}{GOLD[1]:02x}{GOLD[2]:02x}" stroke-width="8"/><path d="M256 116 a140 140 0 0 1 0 280 a70 70 0 0 1 0 -140 a70 70 0 0 0 0 -140 Z" fill="#{GOLD[0]:02x}{GOLD[1]:02x}{GOLD[2]:02x}"/><circle cx="256" cy="186" r="22" fill="#{GOLD[0]:02x}{GOLD[1]:02x}{GOLD[2]:02x}"/><circle cx="256" cy="326" r="22" fill="#{BG[0]:02x}{BG[1]:02x}{BG[2]:02x}"/></svg>
'''

if __name__ == '__main__':
    for name, size in (('icon-512.png', 512), ('icon-192.png', 192), ('apple-touch-icon.png', 180)):
        render(size).save(ROOT / name, optimize=True)
        print('wrote', name, size)
    (ROOT / 'icon.svg').write_text(SVG, encoding='utf-8')
    print('wrote icon.svg')
