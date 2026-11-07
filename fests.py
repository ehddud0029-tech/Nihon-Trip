# 축제 공식 사이트·사진 후보 받기. fest_search.json: id -> {"wiki": [ja 문서 제목...], "q": [공용 검색어...]}
# → fest_candidates.json: id -> {"wiki": 찾은 문서, "official": [위키데이터 P856], "lead": 문서 대표 사진, "cands": [공용 검색 결과]}
import json, time, urllib.request, urllib.parse, re, html
UA = 'GoNihonTripPhotoBuild/1.0 (+https://gonihontrip.com/)'
def api(base, params):
    url = base + '?' + urllib.parse.urlencode(dict(params, format='json', formatversion='2'))
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r: return json.load(r)
        except Exception as e: print('retry', k, e); time.sleep(3 * (k + 1))
    return {}
strip = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()
def info(files):
    if not files: return {}
    r = api('https://commons.wikimedia.org/w/api.php', {'action': 'query', 'titles': '|'.join('File:' + f for f in files), 'prop': 'imageinfo',
            'iiprop': 'url|size|extmetadata', 'iiurlwidth': 600, 'iiextmetadatafilter': 'Artist|LicenseShortName|ImageDescription'}).get('query', {})
    out = {}
    for p in r.get('pages', []):
        ii = (p.get('imageinfo') or [{}])[0]; m = ii.get('extmetadata') or {}
        if not ii: continue
        out[p['title'][5:]] = {'file': p['title'][5:], 'thumb': ii.get('thumburl'), 'w': ii.get('width'), 'h': ii.get('height'),
                              'artist': strip(m.get('Artist', {}).get('value'))[:80], 'license': strip(m.get('LicenseShortName', {}).get('value')),
                              'desc': strip(m.get('ImageDescription', {}).get('value'))[:160]}
    return out
q = json.load(open('fest_search.json', encoding='utf-8'))
out = {}
for k, spec in q.items():
    res = {'wiki': None, 'official': [], 'lead': None, 'imgs': [], 'cands': []}
    for t in spec.get('wiki', []):
        lang, title = (t.split(':', 1) if ':' in t[:4] else ('ja', t))
        r = api(f'https://{lang}.wikipedia.org/w/api.php', {'action': 'query', 'titles': title, 'redirects': 1,
                'prop': 'pageprops|pageimages|images|extlinks', 'piprop': 'original', 'imlimit': 30, 'ellimit': 40}).get('query', {})
        pg = (r.get('pages') or [{}])[0]
        if pg.get('missing') or not pg.get('pageid'): continue
        res['wiki'] = f"{lang}:{pg.get('title')}"
        qid = (pg.get('pageprops') or {}).get('wikibase_item')
        if qid:
            w = api('https://www.wikidata.org/w/api.php', {'action': 'wbgetclaims', 'entity': qid, 'property': 'P856'})
            res['official'] = [c['mainsnak']['datavalue']['value'] for c in w.get('claims', {}).get('P856', []) if c.get('mainsnak', {}).get('datavalue')]
        res['extlinks'] = [e.get('url') for e in pg.get('extlinks', [])][:40]
        if pg.get('original'): res['lead'] = pg['original'].get('source')
        files = [i['title'].split(':', 1)[1] for i in pg.get('images', []) if re.search(r'\.(jpe?g|png)$', i['title'], re.I)][:20]
        res['imgs'] = list(info(files).values())
        break
    seen = set(x['file'] for x in res['imgs'])
    for s in spec.get('q', []):
        r = api('https://commons.wikimedia.org/w/api.php', {'action': 'query', 'generator': 'search', 'gsrsearch': s + ' filetype:bitmap',
                'gsrnamespace': 6, 'gsrlimit': 8, 'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata', 'iiurlwidth': 600,
                'iiextmetadatafilter': 'Artist|LicenseShortName|ImageDescription'}).get('query', {})
        for p in sorted(r.get('pages', []), key=lambda p: p.get('index', 99)):
            f = p['title'][5:]
            if f in seen: continue
            seen.add(f); ii = (p.get('imageinfo') or [{}])[0]; m = ii.get('extmetadata') or {}
            res['cands'].append({'q': s, 'file': f, 'thumb': ii.get('thumburl'), 'w': ii.get('width'), 'h': ii.get('height'),
                                 'artist': strip(m.get('Artist', {}).get('value'))[:80], 'license': strip(m.get('LicenseShortName', {}).get('value')),
                                 'desc': strip(m.get('ImageDescription', {}).get('value'))[:160]})
        time.sleep(0.3)
    out[k] = res
    time.sleep(0.3)
json.dump(out, open('fest_candidates.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('done', {k: (v['wiki'], len(v['official']), len(v['imgs']), len(v['cands'])) for k, v in out.items()})
