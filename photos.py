# 사진 주소 미리 받기 (GitHub Actions에서 실행: 작업 공간은 위키 사이트에 못 붙어서)
# titles.json: 장소id -> 위키 문서 후보 ("ja:" 접두어는 일본어 위키백과)
# search.json: 장소id -> 일본어 이름 (사진이 없으면 위키미디어 공용에서 후보 검색)
# 결과: photo_cache.json (id -> src, file, page, lang, artist, license, commons), photo_candidates.json
import json, time, urllib.request, urllib.parse, re, html

UA = 'GoNihonTripPhotoBuild/1.0 (+https://gonihontrip.com/)'

def api(base, params):
    params = dict(params, format='json', formatversion='2')
    url = base + '?' + urllib.parse.urlencode(params)
    for k in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print('retry', k, e); time.sleep(3 * (k + 1))
    return {}

def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()

def page_images(lang, titles):
    out = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        q = api(f'https://{lang}.wikipedia.org/w/api.php', {'action': 'query', 'redirects': 1, 'prop': 'pageimages',
                'piprop': 'thumbnail|name', 'pithumbsize': 900, 'pilimit': 50, 'titles': '|'.join(chunk)}).get('query', {})
        alias = {n['from']: n['to'] for n in q.get('normalized', []) + q.get('redirects', [])}
        by = {p['title']: p for p in q.get('pages', []) if p.get('thumbnail') and p.get('pageimage')}
        for t in chunk:
            x = t
            for _ in range(4):
                if x in alias: x = alias[x]
            if x in by:
                p = by[x]
                out[t] = {'src': p['thumbnail']['source'], 'file': p['pageimage'].replace('_', ' '), 'page': p['title'], 'lang': lang}
        time.sleep(0.5)
    return out

def commons_meta(files):
    meta = {}
    files = list(files)
    for i in range(0, len(files), 40):
        chunk = ['File:' + f for f in files[i:i + 40]]
        q = api('https://commons.wikimedia.org/w/api.php', {'action': 'query', 'prop': 'imageinfo', 'iiprop': 'extmetadata|url',
                'iiurlwidth': 900, 'iiextmetadatafilter': 'Artist|LicenseShortName|ImageDescription', 'titles': '|'.join(chunk)}).get('query', {})
        for p in q.get('pages', []):
            ii = (p.get('imageinfo') or [{}])[0]
            m = ii.get('extmetadata') or {}
            if not m: continue
            meta[p['title'][5:]] = {'artist': strip(m.get('Artist', {}).get('value')), 'license': strip(m.get('LicenseShortName', {}).get('value')),
                                   'commons': True, 'thumb': ii.get('thumburl')}
        time.sleep(0.5)
    return meta

titles = json.load(open('titles.json', encoding='utf-8'))
search = json.load(open('search.json', encoding='utf-8'))
en_t = sorted({t for ts in titles.values() for t in ts if not t.startswith('ja:')})
ja_t = sorted({t[3:] for ts in titles.values() for t in ts if t.startswith('ja:')})
en = page_images('en', en_t); ja = page_images('ja', ja_t)
cache = {}
for k, ts in titles.items():
    for t in ts:
        hit = ja.get(t[3:]) if t.startswith('ja:') else en.get(t)
        if hit: cache[k] = dict(hit); break
meta = commons_meta({v['file'] for v in cache.values()})
for v in cache.values():
    if v['file'] in meta: v.update({k: meta[v['file']][k] for k in ('artist', 'license', 'commons')})
print('resolved', len(cache), 'commons', sum(1 for v in cache.values() if v.get('commons')))

# 사진이 없거나 공용 사진이 아닌 장소: 위키미디어 공용 파일 검색 후보
cand = {}
for pid, jp in search.items():
    if pid in cache and cache[pid].get('commons'): continue
    q = api('https://commons.wikimedia.org/w/api.php', {'action': 'query', 'generator': 'search', 'gsrsearch': f'{jp} filetype:bitmap',
            'gsrnamespace': 6, 'gsrlimit': 8, 'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata', 'iiurlwidth': 900,
            'iiextmetadatafilter': 'Artist|LicenseShortName|ImageDescription|DateTimeOriginal'}).get('query', {})
    lst = []
    for p in sorted(q.get('pages', []), key=lambda p: p.get('index', 99)):
        ii = (p.get('imageinfo') or [{}])[0]; m = ii.get('extmetadata') or {}
        lst.append({'file': p['title'][5:], 'thumb': ii.get('thumburl'), 'w': ii.get('width'), 'h': ii.get('height'),
                    'artist': strip(m.get('Artist', {}).get('value'))[:80], 'license': strip(m.get('LicenseShortName', {}).get('value')),
                    'desc': strip(m.get('ImageDescription', {}).get('value'))[:160], 'date': strip(m.get('DateTimeOriginal', {}).get('value'))[:20]})
    cand[pid] = {'jp': jp, 'files': lst}
    time.sleep(0.4)
json.dump(cache, open('photo_cache.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
json.dump(cand, open('photo_candidates.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('candidates for', len(cand), 'places')
