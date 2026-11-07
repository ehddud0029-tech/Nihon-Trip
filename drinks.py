# 술 사진 후보 받기 (위키미디어 공용). drink_search.json: id -> [검색어, ...] → drink_candidates.json
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
q = json.load(open('drink_search.json', encoding='utf-8'))
out = {}
for k, qs in q.items():
    seen, lst = set(), []
    for s in qs:
        r = api('https://commons.wikimedia.org/w/api.php', {'action': 'query', 'generator': 'search', 'gsrsearch': s + ' filetype:bitmap',
                'gsrnamespace': 6, 'gsrlimit': 10, 'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata', 'iiurlwidth': 600,
                'iiextmetadatafilter': 'Artist|LicenseShortName|ImageDescription'}).get('query', {})
        for p in sorted(r.get('pages', []), key=lambda p: p.get('index', 99)):
            f = p['title'][5:]
            if f in seen: continue
            seen.add(f); ii = (p.get('imageinfo') or [{}])[0]; m = ii.get('extmetadata') or {}
            lst.append({'q': s, 'file': f, 'thumb': ii.get('thumburl'), 'w': ii.get('width'), 'h': ii.get('height'),
                        'artist': strip(m.get('Artist', {}).get('value'))[:80], 'license': strip(m.get('LicenseShortName', {}).get('value')),
                        'desc': strip(m.get('ImageDescription', {}).get('value'))[:160]})
        time.sleep(0.4)
    out[k] = lst
json.dump(out, open('drink_candidates.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('done', {k: len(v) for k, v in out.items()})
