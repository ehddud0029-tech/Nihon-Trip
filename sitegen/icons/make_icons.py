# 사이트 아이콘 파일 만들기 (tabishiori.html의 SVG 아이콘 → favicon.ico·PNG). python3 sitegen/icons/make_icons.py
import os, re, urllib.parse
from playwright.sync_api import sync_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
s = open('/home/claude/site/index.html', encoding='utf-8').read()
href = re.search(r'<link rel="icon" href="data:image/svg\+xml,([^"]+)"', s).group(1)
svg = urllib.parse.unquote(href)
open(f'{D}/icon.svg', 'w', encoding='utf-8').write(svg)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 512, 'height': 512})
    big = svg.replace('<svg ', '<svg width="512" height="512" ', 1)
    pg.set_content('<html><body style="margin:0;background:transparent">' + big + '</body></html>')
    pg.screenshot(path=f'{D}/icon-512.png', omit_background=True, clip={'x': 0, 'y': 0, 'width': 512, 'height': 512}); b.close()
im = Image.open(f'{D}/icon-512.png').convert('RGBA')
for n in [192, 180, 48, 32]:
    im.resize((n, n), Image.LANCZOS).save(f'{D}/icon-{n}.png')
im.save(f'{D}/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
print('ok')
