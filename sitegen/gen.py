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
LANGS = ['ko', 'en', 'ja', 'es', 'fr']
OG_LOCALE = {'ko': 'ko_KR', 'en': 'en_US', 'ja': 'ja_JP', 'es': 'es_ES', 'fr': 'fr_FR'}
HOME_DESC = {
    'ko': '도쿄·오사카·나고야·히로시마·시코쿠·후쿠오카·홋카이도·오키나와와 근교 도시의 관광지, 축제, 맛집, 교통, 쇼핑 정보와 실시간 날씨',
    'en': 'Sights, festivals, restaurants, transport and shopping in Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa and nearby cities, with live weather.',
    'ja': '東京・大阪・名古屋・広島・四国・福岡・北海道・沖縄と近郊都市の観光地、祭り、グルメ、交通、ショッピング情報とリアルタイムの天気。',
    'es': 'Lugares, festivales, restaurantes, transporte y compras en Tokio, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa y ciudades cercanas, con el tiempo en directo.',
    'fr': 'Sites, fêtes, restaurants, transports et shopping à Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa et dans les villes voisines, avec la météo en direct.',
}
GA_ID = 'G-07B266GQNY'   # Google Analytics 4 측정 ID (공개 값, 비밀 키 아님)
GA = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
      f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>")
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
var cur=(r.match(/^(en|ja|es|fr)(\/|$)/)||[])[1]||"ko",q=(location.search.match(/[?&]lang=(ko|en|ja|es|fr)\b/)||[])[1],s=null;
try{s=localStorage.getItem("tabishiori-lang")}catch(e){} if(q){try{localStorage.setItem("tabishiori-lang",q)}catch(e){}}
var want=q||(cur==="ko"&&/^(en|ja|es|fr)$/.test(s||"")&&!/bot|crawl|spider|slurp|yeti|daum|bing/i.test(navigator.userAgent)?s:null);
if(want&&want!==cur){var bare=cur==="ko"?r:r.replace(/^(en|ja|es|fr)\/?/,"");location.replace(B+(want==="ko"?"":want+"/")+bare+location.hash);return;}
window.NT_LANG=cur;document.documentElement.lang=cur;
if(cur!=="ko")document.write('<script src="'+B+'i18n/'+cur+'.js"><\/script><script src="'+B+'engine.js"><\/script>');})();</script>''' % json.dumps(BASE)


def page_html(lang, title, desc, path, body, fonts, icon, alternates=True, index=True, home=False, ld=None):
    esc = lambda x: html.escape(x, quote=True)
    url = ORIGIN + BASE + ('' if lang == 'ko' else lang + '/') + path
    h = ['<!doctype html>', f'<html lang="{lang}">', '<head>', '<meta charset="utf-8">',
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
            h.append(f'<link rel="alternate" hreflang="{l}" href="{ORIGIN}{BASE}{"" if l == "ko" else l + "/"}{path}">')
        h.append(f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{BASE}{path}">')
    h += ['<meta property="og:type" content="website">', '<meta property="og:site_name" content="Go Nihon Trip">',
          f'<meta property="og:title" content="{esc(title)}">', f'<meta property="og:description" content="{esc(desc)}">',
          f'<meta property="og:url" content="{url}">', f'<meta property="og:locale" content="{OG_LOCALE[lang]}">',
          f'<meta property="og:image" content="{ORIGIN}{BASE}og-{lang}.png">', '<meta property="og:image:width" content="1200">',
          '<meta property="og:image:height" content="630">', '<meta property="og:image:alt" content="Go Nihon Trip">',
          '<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:image" content="{ORIGIN}{BASE}og-{lang}.png">', icon]
    h.append(GA)
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
                sm.append(f'    <xhtml:link rel="alternate" hreflang="{l2}" href="{ORIGIN}{BASE}{"" if l2 == "ko" else l2 + "/"}{path}"/>')
            sm.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN}{BASE}{path}"/>')
            sm.append('  </url>')
    sm.append('</urlset>')
    open(f'{OUT}/sitemap.xml', 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
    open(f'{OUT}/CNAME', 'w').write(DOMAIN + '\n')
    open(f'{OUT}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
    print('total pages', len(pages), 'sitemap urls', len(paths) * len(LANGS))


if __name__ == '__main__':
    main()
