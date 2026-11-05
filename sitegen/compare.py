# 수정 전·후 비교 이미지 만들기
#   python3 sitegen/compare.py <비교 이름> <주소1> [<주소2> ...] [--ref main] [--mobile]
#   예: python3 sitegen/compare.py faq ko:tokyo/weather/11/ en:airport/kansai/dotonbori/ --ref HEAD~1
# 수정 전 = 배포된 사이트(main 브랜치, --ref로 커밋 지정 가능), 수정 후 = 지금 작업 공간의 원본으로 그린 화면.
# 결과: sitegen/compare_out/<이름>_<번호>.png (왼쪽 수정 전 · 오른쪽 수정 후)
import os, re, sys, shutil, subprocess, threading, socketserver, http.server, functools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

ROOT = '/home/claude'
SITE_REPO = f'{ROOT}/nihon-trip'
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compare_out')
TMP = '/tmp/nt_compare'
REAL_IMG = False   # 작업 공간에서는 위키 사진 서버에 못 붙어서 빈 사진으로 대신해요

def args():
    a = sys.argv[1:]; ref = 'main'; mobile = False
    if '--ref' in a: i = a.index('--ref'); ref = a[i + 1]; del a[i:i + 2]
    if '--mobile' in a: a.remove('--mobile'); mobile = True
    name, paths = a[0], [p if ':' in p else 'ko:' + p for p in a[1:]]
    return name, paths, ref, mobile

def serve(directory, handler=None):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = handler or functools.partial(Quiet, directory=directory)
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', 0), h)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f'http://127.0.0.1:{httpd.server_address[1]}/'

def before_dir(ref):
    d = f'{TMP}/before'
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(['git', 'fetch', '-q', 'origin', 'main'], cwd=SITE_REPO)
    subprocess.run(['git', 'worktree', 'prune'], cwd=SITE_REPO)
    subprocess.run(['git', 'worktree', 'add', '-q', '--detach', d, 'origin/main' if ref == 'main' else ref], cwd=SITE_REPO, check=True)
    return d

def after_dir():
    d = f'{TMP}/after'; gen.OUT = d
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    engine, app, css, body, fonts, icon = gen.split_source()
    for f in ['areas.js', 'autoreserve.js', 'google_picks.js', 'geo.js']: shutil.copy(f'{gen.SITE}/{f}', d)
    shutil.copytree(f'{gen.SITE}/i18n', f'{d}/i18n')
    open(f'{d}/app.css', 'w').write(css); open(f'{d}/engine.js', 'w').write(engine); open(f'{d}/app.js', 'w').write(app)
    gen.VER = 'cmp'
    open(f'{d}/404.html', 'w').write(gen.page_html('ko', 'x', 'x', '', body, fonts, icon, alternates=False, index=False))
    return d

def fake_wx(route):
    import json, datetime, urllib.parse
    q = urllib.parse.parse_qs(urllib.parse.urlparse(route.request.url).query)
    n = len(q.get('latitude', ['0'])[0].split(','))
    jst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    days = [(jst + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    hrs = [f'{d}T{h:02d}:00' for d in days for h in range(24)]
    temps = [12 + 6 * __import__('math').sin((i % 24 - 9) / 24 * 6.28) for i in range(len(hrs))]
    one = {"current": {"time": jst.strftime('%Y-%m-%dT%H:00'), "temperature_2m": 15, "apparent_temperature": 14, "weather_code": 2, "relative_humidity_2m": 60},
           "hourly": {"time": hrs, "temperature_2m": temps, "weather_code": [0, 1, 2, 3, 61, 2] * 28, "precipitation_probability": [10] * 168, "wind_speed_10m": [3] * 168, "relative_humidity_2m": [60] * 168},
           "daily": {"time": days, "weather_code": [0, 2, 3, 61, 1, 2, 3], "temperature_2m_max": [18, 17, 19, 15, 16, 18, 17], "temperature_2m_min": [10, 9, 11, 8, 9, 10, 9], "precipitation_probability_max": [10, 20, 5, 80, 10, 20, 30]}}
    route.fulfill(status=200, content_type='application/json', body=json.dumps([one] * n), headers={'Access-Control-Allow-Origin': '*'})

def shoot(br, url, out, mobile, grab=None):
    vp = {'width': 390, 'height': 844} if mobile else {'width': 1300, 'height': 900}
    pg = br.new_page(viewport=vp, device_scale_factor=2 if mobile else 1)
    pg.route(re.compile(r'^https?://(?!127\.0\.0\.1)'), lambda r: r.abort())
    pg.route(re.compile(r'^https://api\.open-meteo\.com/'), fake_wx)   # 날씨는 예시 값으로 (화면 비교용)
    pg.route(re.compile(r'^https://(upload|thumb)\.wikimedia\.org/'), lambda r: r.continue_() if REAL_IMG else r.fulfill(status=200, content_type='image/png', body=gen.PNG1))   # 위키 사진은 빈 이미지로 대신 (작업 공간에서 못 받아서)
    if grab:
        pg.goto(grab[0], wait_until='load'); pg.wait_for_timeout(400); pg.evaluate(gen.GRAB, grab[1])
    else:
        pg.goto(url, wait_until='load')
    pg.wait_for_timeout(1500)
    pg.screenshot(path=out, full_page=True); pg.close()

def side(a, b, out, label):
    A, B = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
    w = max(A.width, B.width); h = max(A.height, B.height); bar = 70; gap = 24
    im = Image.new('RGB', (w * 2 + gap, h + bar), '#FFFFFF')
    try: f = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 34)
    except Exception: f = ImageFont.load_default()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, bar], fill='#5A6272'); d.rectangle([w + gap, 0, w * 2 + gap, bar], fill='#C4452C')
    d.text((20, 14), f'수정 전 · {label}', fill='#FFFFFF', font=f); d.text((w + gap + 20, 14), f'수정 후 · {label}', fill='#FFFFFF', font=f)
    im.paste(A, (0, bar)); im.paste(B, (w + gap, bar)); im.save(out)

def main():
    name, paths, ref, mobile = args()
    os.makedirs(OUTDIR, exist_ok=True)
    bdir, adir = before_dir(ref), after_dir()
    hb, rb = serve(bdir)
    gen.OUT = adir; ha, ra = serve(adir, gen.Handler)
    outs = []
    with sync_playwright() as p:
        br = p.chromium.launch()
        for i, lp in enumerate(paths, 1):
            lang, path = lp.split(':', 1); pre = '' if lang == 'ko' else lang + '/'
            b, a = f'{TMP}/b{i}.png', f'{TMP}/a{i}.png'
            shoot(br, rb + pre + path, b, mobile)
            shoot(br, None, a, mobile, grab=(ra + pre, gen.BASE + pre + path))
            o = f'{OUTDIR}/{name}_{i}.png'; side(b, a, o, f'/{pre}{path}'); outs.append(o)
        br.close()
    hb.shutdown(); ha.shutdown()
    subprocess.run(['git', 'worktree', 'remove', '--force', bdir], cwd=SITE_REPO)
    print('\n'.join(outs))

if __name__ == '__main__':
    main()
