"""Go Nihon Trip 정적 페이지 생성기

tabishiori.html(원본 한 파일)에서 CSS·JS를 공용 파일로 빼고, 모든 화면(지역×주제, 월별 축제, 5개 언어)을
브라우저로 미리 그려 각자 주소의 index.html로 저장해요. 검색엔진은 이 HTML을 바로 읽고,
방문자는 열자마자 내용을 본 뒤 지금처럼 앱이 동작해요.

사용법: python3 gen.py  → /home/claude/sitegen/dist 에 사이트 전체가 생겨요.
"""
import html, json, os, re, shutil, socketserver, threading, http.server, sys, datetime
from playwright.sync_api import sync_playwright

SRC = '/home/claude/tabishiori.html'
SITE = '/home/claude/site'          # areas.js · i18n 등 기존 파일
OUT = '/home/claude/sitegen/dist'
ORIGIN = 'https://gonihontrip.com'
DOMAIN = 'gonihontrip.com'   # GitHub Pages 사용자 도메인 (CNAME 파일)
BASE = '/'
LANGS = ['ko', 'en', 'ja', 'zh', 'tw', 'th', 'es', 'fr']
HREFLANG = {'zh': 'zh-Hans', 'tw': 'zh-Hant'}   # 주소는 /zh/·/tw/, 언어 코드는 표준 표기
OG_LOCALE = {'ko': 'ko_KR', 'en': 'en_US', 'ja': 'ja_JP', 'es': 'es_ES', 'fr': 'fr_FR', 'zh': 'zh_CN', 'tw': 'zh_TW', 'th': 'th_TH'}
HOME_DESC = {
    'ko': '도쿄·오사카·나고야·히로시마·시코쿠·후쿠오카·홋카이도·오키나와와 근교 도시의 관광지, 축제, 맛집, 교통, 쇼핑 정보와 실시간 날씨',
    'en': 'Sights, festivals, restaurants, transport and shopping in Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa and nearby cities, with live weather.',
    'ja': '東京・大阪・名古屋・広島・四国・福岡・北海道・沖縄と近郊都市の観光地、祭り、グルメ、交通、ショッピング情報とリアルタイムの天気。',
    'es': 'Lugares, festivales, restaurantes, transporte y compras en Tokio, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa y ciudades cercanas, con el tiempo en directo.',
    'zh': '东京、大阪、名古屋、广岛、四国、福冈、北海道、冲绳及周边城市的景点、节庆、美食、交通、购物信息与实时天气。',
    'tw': '東京、大阪、名古屋、廣島、四國、福岡、北海道、沖繩及周邊城市的景點、節慶、美食、交通、購物資訊與即時天氣。',
    'th': 'ที่เที่ยว เทศกาล ร้านอาหาร การเดินทาง และช้อปปิ้งในโตเกียว โอซาก้า นาโกย่า ฮิโรชิม่า ชิโกกุ ฟุกุโอกะ ฮอกไกโด โอกินาว่า และเมืองใกล้เคียง พร้อมสภาพอากาศสด',
    'fr': 'Sites, fêtes, restaurants, transports et shopping à Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa et dans les villes voisines, avec la météo en direct.',
}
GA_ID = 'G-07B266GQNY'   # Google Analytics 4 측정 ID (공개 값, 비밀 키 아님)
GA = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
      f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>")
ADSENSE_ID = 'ca-pub-7250361561234920'   # 애드센스 게시자 ID (공개 값)
ADSENSE = (f'<meta name="google-adsense-account" content="{ADSENSE_ID}">'
           f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_ID}" crossorigin="anonymous"></script>')
GOOGLE_VERIFY = '<meta name="google-site-verification" content="rCU1knHQWui1umzcyPHVHmVVEYmbO0SjnEF1169ygRs">'
NAVER_VERIFY = '<meta name="naver-site-verification" content="a6df6739e6ce65fea96f38e4892385db40647698">'
TODAY = datetime.date.today().isoformat()
VER = '0'  # 파일 내용이 바뀌면 바뀌는 번호 → 브라우저가 옛 CSS·JS를 쓰지 않게 해요


def split_source():
    s = open(SRC, encoding='utf-8').read()
    scripts = list(re.finditer(r'<script>(.*?)</script>', s, re.S))
    engine = next(m.group(1) for m in scripts if '번역 엔진' in m.group(1))
    app = scripts[-1].group(1)
    css = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
    body = s[s.index('<header class="top">'):s.index('<script src="areas.js">')]
    fonts = re.findall(r'<link rel="(?:preconnect|stylesheet)"[^>]*>', s[:s.index('<style>')])
    old = open(f'{SITE}/index.html', encoding='utf-8').read()
    icon = re.search(r'<link rel="icon"[^>]*>', old).group(0)
    return engine, app, css, body, fonts, icon


BOOT = r'''<script>window.NT_BASE=%s;(function(){var B=NT_BASE,p=location.pathname,r=p.toLowerCase().indexOf(B.toLowerCase())===0?p.slice(B.length):p.replace(/^\//,"");
var cur=(r.match(/^(en|ja|zh|tw|th|es|fr)(\/|$)/)||[])[1]||"ko",q=(location.search.match(/[?&]lang=(ko|en|ja|zh|tw|th|es|fr)\b/)||[])[1],s=null;
try{s=localStorage.getItem("tabishiori-lang")}catch(e){} if(q){try{localStorage.setItem("tabishiori-lang",q)}catch(e){}}
var want=q||(cur==="ko"&&/^(en|ja|zh|tw|th|es|fr)$/.test(s||"")&&!/bot|crawl|spider|slurp|yeti|daum|bing/i.test(navigator.userAgent)?s:null);
if(want&&want!==cur){var bare=cur==="ko"?r:r.replace(/^(en|ja|zh|tw|th|es|fr)\/?/,"");location.replace(B+(want==="ko"?"":want+"/")+bare+location.hash);return;}
window.NT_LANG=cur;document.documentElement.lang=cur==="zh"?"zh-Hans":cur==="tw"?"zh-Hant":cur;
if(cur!=="ko")document.write('<script src="'+B+'i18n/'+cur+'.js"><\/script><script src="'+B+'engine.js"><\/script>');})();</script>''' % json.dumps(BASE)


def page_html(lang, title, desc, path, body, fonts, icon, alternates=True, index=True, home=False, ld=None):
    esc = lambda x: html.escape(x, quote=True)
    url = ORIGIN + BASE + ('' if lang == 'ko' else lang + '/') + path
    h = ['<!doctype html>', f'<html lang="{HREFLANG.get(lang, lang)}">', '<head>', '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
         f'<title>{esc(title)}</title>', f'<meta name="description" content="{esc(desc)}">']
    if not index:
        h.append('<meta name="robots" content="noindex">')
    if home and lang == 'ko':
        h.append(GOOGLE_VERIFY)
        h.append(NAVER_VERIFY)
    h.append(f'<link rel="canonical" href="{url}">')
    if ld:
        ld = dict(ld, url=url)
        h.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace('</', '<\\/') + '</script>')
    if alternates:
        for l in LANGS:
            h.append(f'<link rel="alternate" hreflang="{HREFLANG.get(l, l)}" href="{ORIGIN}{BASE}{"" if l == "ko" else l + "/"}{path}">')
        h.append(f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{BASE}{path}">')
    h += ['<meta property="og:type" content="website">', '<meta property="og:site_name" content="Go Nihon Trip">',
          f'<meta property="og:title" content="{esc(title)}">', f'<meta property="og:description" content="{esc(desc)}">',
          f'<meta property="og:url" content="{url}">', f'<meta property="og:locale" content="{OG_LOCALE[lang]}">',
          f'<meta property="og:image" content="{ORIGIN}{BASE}og-{lang}.png">', '<meta property="og:image:width" content="1200">',
          '<meta property="og:image:height" content="630">', '<meta property="og:image:alt" content="Go Nihon Trip">',
          '<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:image" content="{ORIGIN}{BASE}og-{lang}.png">', icon,
          f'<link rel="icon" type="image/png" sizes="32x32" href="{BASE}icon-32.png">', f'<link rel="apple-touch-icon" href="{BASE}icon-180.png">',
          f'<link rel="alternate" type="application/rss+xml" title="Go Nihon Trip" href="{ORIGIN}{BASE}rss.xml">']
    h.append(GA)
    h.append(ADSENSE)
    h += fonts
    h += ['<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>',
          f'<link rel="stylesheet" href="{BASE}app.css?v={VER}">', BOOT.replace('.js"><\\/script>', f'.js?v={VER}"><\\/script>')]
    if home:
        ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "Go Nihon Trip", "url": url,
              "inLanguage": lang, "description": desc}
        h.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')
    h += ['</head>', '<body>', body.strip(),
          f'<script src="{BASE}areas.js?v={VER}"></script>', f'<script src="{BASE}autoreserve.js?v={VER}"></script>',
          f'<script src="{BASE}google_picks.js?v={VER}"></script>', f'<script src="{BASE}geo.js?v={VER}"></script>', f'<script src="{BASE}app.js?v={VER}"></script>', '</body>', '</html>', '']
    return '\n'.join(h)


class Handler(http.server.SimpleHTTPRequestHandler):
    """BASE(/)… 를 dist에서 찾고, 화면 주소는 모두 404.html(앱 셸)로 돌려줘요"""
    def translate_path(self, path):
        p = path.split('?')[0].split('#')[0]
        if p.startswith(BASE):
            rel = p[len(BASE):]
            f = os.path.join(OUT, rel)
            if rel and os.path.isfile(f) and not rel.endswith('.html'):
                return f
        return os.path.join(OUT, '404.html')
    def log_message(self, *a):
        pass


GRAB = r'''async (url)=>{
  history.pushState(null,"",url);
  Object.assign(st,{q:"",more:false,focus:null,menu:"ramen",spotCat:"all",hm:null,month:NOW_M}); delete st.wxTab;
  readPath(); closeItem(); render(); window.scrollTo(0,0);
  await new Promise(r=>setTimeout(r,0));
  const b=document.body.cloneNode(true);
  b.querySelectorAll("script").forEach(x=>x.remove());
  b.querySelector("#langMenu")?.setAttribute("hidden","");
  const mm=b.querySelector("#mapmsg"); if(mm){ mm.removeAttribute("hidden"); mm.textContent=(window.__tr||(x=>x))("지도를 불러오는 중이에요"); }
  b.querySelector("#mapc")?.replaceChildren(); b.querySelector("#mapwrap")?.removeAttribute("data-live"); b.querySelector("#mapwrap")?.removeAttribute("style");
  return {title:document.title, desc:document.querySelector('meta[name="description"]').getAttribute("content"), body:b.innerHTML, path:location.pathname, ld:window.__ld||null};
}'''


RSS_PREFIX = ['itinerary/', 'weather/', 'airport/', 'guide/', 'festivals/', 'tokyo/weather/', 'osaka/weather/', 'fukuoka/weather/', 'hokkaido/weather/',
              'okinawa/weather/', 'nagoya/weather/', 'hiroshima/weather/', 'shikoku/weather/']

def write_rss(meta):
    """네이버 서치어드바이저용 RSS (한국어 페이지 중 일정·날씨·공항·여행 준비·축제 달력)"""
    from xml.sax.saxutils import escape
    import email.utils, time
    now = email.utils.formatdate(time.time(), localtime=False)
    meta = {p: v for (l, p), v in meta.items() if l == 'ko'}
    items = [p for p in meta if any(p.startswith(x) for x in RSS_PREFIX)]
    items.sort(key=lambda p: (p.count('/'), p))
    x = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">', '<channel>',
         '<title>Go Nihon Trip · 일본 여행 가이드</title>', f'<link>{ORIGIN}{BASE}</link>',
         f'<atom:link href="{ORIGIN}{BASE}rss.xml" rel="self" type="application/rss+xml"/>',
         f'<description>{escape(HOME_DESC["ko"])}</description>', '<language>ko</language>', f'<lastBuildDate>{now}</lastBuildDate>']
    for p in items:
        t, d = meta[p]; u = f'{ORIGIN}{BASE}{p}'
        x += ['<item>', f'<title>{escape(t.replace(" | Go Nihon Trip", ""))}</title>', f'<link>{u}</link>', f'<guid>{u}</guid>',
              f'<description>{escape(d)}</description>', f'<pubDate>{now}</pubDate>', '</item>']
    x += ['</channel>', '</rss>', '']
    open(f'{OUT}/rss.xml', 'w', encoding='utf-8').write('\n'.join(x))
    print('rss items', len(items))


INDEXNOW_KEY = '3df7fdd9ec42d1ae624f94732c4f09cf'   # IndexNow 키 (공개 값). 키 파일은 사이트 맨 위 <키>.txt

def write_llms(meta):
    """AI용 사이트 안내 (llms.txt): 사이트 소개와 주요 페이지 목록"""
    def sec(title, prefix, lang='en', depth=None):
        ps = sorted(p for (l, p) in meta if l == lang and p.startswith(prefix) and (depth is None or p.count('/') == depth))
        lp = '' if lang == 'ko' else lang + '/'
        return [f'## {title}', ''] + [f'- [{meta[(lang, p)][0].replace(" | Go Nihon Trip", "")}]({ORIGIN}{BASE}{lp}{p}): {meta[(lang, p)][1]}' for p in ps] + ['']
    x = ['# Go Nihon Trip', '',
         '> Japan travel guide organized by region: sights, festivals, restaurants, shopping, transport, airport-to-city routes, '
         'monthly weather and what to wear, and day-by-day itineraries for Tokyo, Osaka/Kyoto/Nara/Kobe, Nagoya, Hiroshima, Shikoku, '
         'Fukuoka, Hokkaido and Okinawa. Available in Korean (default, /), English (/en/), Japanese (/ja/), Simplified Chinese (/zh/), '
         'Traditional Chinese (/tw/), Thai (/th/), Spanish (/es/) and French (/fr/). Admission fees and hours were compiled from official '
         'sources (as of October 2026); weather figures are Japan Meteorological Agency normals (1991–2020).', '']
    x += sec('Suggested itineraries', 'itinerary/')
    x += sec('Airport to city', 'airport/')
    x += sec('Weather and what to wear by month (all of Japan)', 'weather/')
    x += sec('Travel preparation', 'guide/')
    x += ['## Other', '', f'- [Sitemap]({ORIGIN}{BASE}sitemap.xml): all pages in all languages', f'- [About]({ORIGIN}{BASE}en/about/): sources and contact', '']
    open(f'{OUT}/llms.txt', 'w', encoding='utf-8').write('\n'.join(x))
    print('llms.txt lines', len(x))

def write_indexnow():
    """IndexNow 키 파일과, main에 올라갈 때 바뀐 페이지를 빙 등에 알리는 GitHub Actions"""
    open(f'{OUT}/{INDEXNOW_KEY}.txt', 'w').write(INDEXNOW_KEY)
    os.makedirs(f'{OUT}/.github/workflows', exist_ok=True)
    open(f'{OUT}/.github/workflows/indexnow.yml', 'w').write(f"""name: IndexNow
on:
  push:
    branches: [main]
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - name: Send changed pages to IndexNow
        run: python3 .github/indexnow.py
        env:
          INDEXNOW_KEY: {INDEXNOW_KEY}
          SITE_ORIGIN: {ORIGIN}
""")
    open(f'{OUT}/.github/indexnow.py', 'w').write(INDEXNOW_PY)

INDEXNOW_PY = r'''# 바뀐 페이지만 IndexNow로 알려요 (스크립트·CSS 버전 번호만 바뀐 페이지는 빼요)
import json, os, re, subprocess, urllib.request
key, origin = os.environ['INDEXNOW_KEY'], os.environ['SITE_ORIGIN'].rstrip('/')
if subprocess.run(['git', 'rev-parse', 'HEAD~1'], capture_output=True).returncode:
    print('no previous commit'); raise SystemExit
out = subprocess.run(['git', 'diff', '-U0', 'HEAD~1', 'HEAD', '--', '*.html'], capture_output=True, text=True).stdout
ver = re.compile(r'\?v=[0-9a-f]+')
changed, cur = set(), None
for line in out.split('\n'):
    if line.startswith('+++ '):
        cur = line[6:] if line.startswith('+++ b/') else None
    elif line.startswith('--- '):
        continue
    elif cur and line[:1] in '+-' and not ver.search(line):
        changed.add(cur)
urls = []
for f in sorted(changed):
    if f == '404.html' or not f.endswith('index.html'): continue
    urls.append(origin + '/' + f[:-len('index.html')])
print(len(urls), 'changed pages')
host = origin.split('://')[1]
for i in range(0, len(urls), 10000):
    body = json.dumps({'host': host, 'key': key, 'keyLocation': f'{origin}/{key}.txt', 'urlList': urls[i:i + 10000]}).encode()
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: print('IndexNow', r.status)
    except Exception as e:
        print('IndexNow error', e)
'''


def main():
    engine, app, css, body, fonts, icon = split_source()
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for f in ['areas.js', 'autoreserve.js', 'google_picks.js', 'geo.js']:
        shutil.copy(f'{SITE}/{f}', OUT)
    shutil.copytree(f'{SITE}/i18n', f'{OUT}/i18n')
    shutil.copytree(f'{SITE}/photos', f'{OUT}/photos')
    shutil.copy(f'{SITE}/README.md', OUT)
    for f in ['favicon.ico', 'icon-32.png', 'icon-48.png', 'icon-180.png', 'icon-192.png', 'icon-512.png']:   # 사이트 아이콘 (icons/make_icons.py)
        shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', f), OUT)
    for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'og')):
        if f.endswith('.png'):
            shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'og', f), OUT)
    open(f'{OUT}/app.css', 'w', encoding='utf-8').write(css.strip() + '\n')
    open(f'{OUT}/engine.js', 'w', encoding='utf-8').write(engine.strip() + '\n')
    open(f'{OUT}/app.js', 'w', encoding='utf-8').write(app.strip() + '\n')
    global VER
    import hashlib, glob
    h = hashlib.sha1()
    for f in sorted(glob.glob(f'{OUT}/*.js') + glob.glob(f'{OUT}/*.css') + glob.glob(f'{OUT}/i18n/*.js')):
        h.update(open(f, 'rb').read())
    VER = h.hexdigest()[:8]
    # 앱 셸(없는 주소용): 언어는 주소 앞부분에서 정해요
    open(f'{OUT}/404.html', 'w', encoding='utf-8').write(
        page_html('ko', 'Go Nihon Trip · 일본 여행 가이드', HOME_DESC['ko'], '', body, fonts, icon, alternates=False, index=False))

    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    root = f'http://127.0.0.1:{port}{BASE}'

    pages = []
    META = {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        for lang in LANGS:
            pg = br.new_page(viewport={'width': 1300, 'height': 900})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.route(re.compile(r'^https?://(?!127\.0\.0\.1)'), lambda r: r.abort())
            lp = '' if lang == 'ko' else lang + '/'
            pg.goto(root + lp, wait_until='load')
            pg.wait_for_timeout(300)
            routes = pg.evaluate('''()=>{ const r=["","saved/","map/"]; for(const g of GKEYS) r.push(`guide/${g}/`); r.push("about/","contact/","privacy/"); r.push("itinerary/"); for(const k of IKEYS) r.push(`itinerary/${k}/`); for(const v of ["spots","food","transport","shopping"]) r.push(v+"/");
              for(let m=1;m<=12;m++) r.push(`festivals/${m}/`);
              r.push("airport/"); for(const a of Object.keys(APS)){ r.push(`airport/${a}/`); for(const k of apDests(a)) r.push(`airport/${a}/${k}/`); } r.push("weather/"); for(let m=1;m<=12;m++) r.push(`weather/${m}/`); for(const c of WX_ORDER){ r.push(`${c}/weather/`); for(let m=1;m<=12;m++) r.push(`${c}/weather/${m}/`); }
              for(const c of Object.keys(CITIES)) for(const a of areasOf(c)) for(const v of ["spots","festivals","food","transport","shopping"]) r.push(`${c}/${a.key}/${v}/`);
              for(const x of ALL) if(PLACE_TYPES.includes(x.type)) r.push(`place/${placeSlug(x.id)}/`);
              return r; }''')
            for path in routes:
                d = pg.evaluate(GRAB, BASE + lp + path)
                want = BASE + lp + path
                if d['path'] != want:
                    print('PATH MISMATCH', want, d['path'])
                home = path == ''
                desc = HOME_DESC[lang] if home else d['desc']
                pages.append((lang, path))
                if lang in ('ko', 'en'): META[(lang, path)] = (d['title'], desc or '')
                out = page_html(lang, d['title'], desc, path, d['body'], fonts, icon,
                                index=path != 'saved/', home=home, ld=d.get('ld'))
                fp = os.path.join(OUT, lp + path, 'index.html')
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                open(fp, 'w', encoding='utf-8').write(out)
            print(lang, len(routes), 'pages', 'errors:', errs[:3])
            pg.close()
        br.close()
    httpd.shutdown()

    # 사이트맵: 언어별 주소를 서로 연결
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    paths = sorted({p for l, p in pages if p != 'saved/'}, key=lambda x: (x.count('/'), x))
    for path in paths:
        for lang in LANGS:
            sm.append('  <url>')
            sm.append(f'    <loc>{ORIGIN}{BASE}{"" if lang == "ko" else lang + "/"}{path}</loc>')
            sm.append(f'    <lastmod>{TODAY}</lastmod>')
            for l2 in LANGS:
                sm.append(f'    <xhtml:link rel="alternate" hreflang="{HREFLANG.get(l2, l2)}" href="{ORIGIN}{BASE}{"" if l2 == "ko" else l2 + "/"}{path}"/>')
            sm.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN}{BASE}{path}"/>')
            sm.append('  </url>')
    sm.append('</urlset>')
    open(f'{OUT}/sitemap.xml', 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
    write_rss(META)
    write_llms(META)
    write_indexnow()
    open(f'{OUT}/CNAME', 'w').write(DOMAIN + '\n')
    open(f'{OUT}/ads.txt', 'w').write(f"google.com, {ADSENSE_ID.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")
    open(f'{OUT}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
    print('total pages', len(pages), 'sitemap urls', len(paths) * len(LANGS))


if __name__ == '__main__':
    main()
