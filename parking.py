# 주차장 정보 후보 모으기: park.json id -> {jp, en:[en 위키 제목], url, type} 또는 {ar: AutoReserve id}
# → park_candidates.json id -> {wiki_ja, official:[...], snips:[{src, text}]}  ('駐車' 주변 글만, 사람이 읽고 정리)
import json, re, time, html, ssl, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
UA = 'Mozilla/5.0 (compatible; GoNihonTripInfo/1.0; +https://gonihontrip.com/)'
ctx = ssl.create_default_context()
def fetch(u, n=400000):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': UA, 'Accept-Language': 'ja,en;q=0.8'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            b = r.read(n); ct = r.headers.get_content_charset()
            if not ct:
                m = re.search(rb'charset=["\']?([\w-]+)', b[:4000]); ct = m.group(1).decode() if m else 'utf-8'
            if ct.lower() in ('shift_jis', 'sjis', 'x-sjis'): ct = 'cp932'
            return r.geturl(), b.decode(ct, 'replace')
    except Exception as e: return u, ''
def api(base, params):
    u = base + '?' + urllib.parse.urlencode(dict(params, format='json', formatversion='2'))
    _, t = fetch(u, 2000000)
    try: return json.loads(t)
    except Exception: return {}
def text_of(h):
    h = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', h)
    h = re.sub(r'(?i)<br\s*/?>|</(p|li|tr|div|dd|dt|h\d)>', '\n', h)
    h = re.sub(r'<[^>]+>', ' ', h); h = html.unescape(h)
    return re.sub(r'[ \t　]+', ' ', h)
KW = re.compile(r'駐車|パーキング|[Pp]arking')
def snips(t, src, k=6):
    out = []; last = -999
    for m in KW.finditer(t):
        if m.start() - last < 200: continue
        last = m.start(); s = t[max(0, m.start()-140): m.start()+220].replace('\n', ' / ')
        out.append({'src': src, 'text': re.sub(r'\s+', ' ', s).strip()})
        if len(out) >= k: break
    return out
def links(base, h):
    res = []
    for m in re.finditer(r'<a[^>]+href=["\']([^"\'#]+)["\'][^>]*>(.*?)</a>', h, re.S | re.I):
        href, label = m.group(1), re.sub('<[^>]+>', '', m.group(2))
        if re.search(r'アクセス|access|交通|駐車|parking|ご案内|guide|info|施設', href + label, re.I):
            u = urllib.parse.urljoin(base, href)
            if urllib.parse.urlparse(u).netloc == urllib.parse.urlparse(base).netloc and u not in res: res.append(u)
    return res[:4]
def place(item):
    k, v = item; res = {'wiki_ja': None, 'official': [], 'snips': []}
    if v.get('ar'):
        fin, h = fetch(f"https://autoreserve.com/ja/restaurants/{v['ar']}", 2000000)
        raw = h
        try: raw = h.encode('utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
        except Exception: pass
        res['snips'] = snips(text_of(h), 'ar', 3) or snips(re.sub(r'<[^>]+>', ' ', raw), 'ar-raw', 3)
        res['len'] = len(h); return k, res
    qid = None; jt = None
    for t in v.get('en', []):
        r = api('https://en.wikipedia.org/w/api.php', {'action': 'query', 'titles': t, 'redirects': 1, 'prop': 'pageprops'}).get('query', {})
        pg = (r.get('pages') or [{}])[0]; qid = (pg.get('pageprops') or {}).get('wikibase_item')
        if qid: break
    if not qid and v.get('jp'):
        for jpn in [v['jp']] + re.split(r'[・·（(]', v['jp'])[:1]:
            r = api('https://ja.wikipedia.org/w/api.php', {'action': 'query', 'titles': jpn, 'redirects': 1, 'prop': 'pageprops'}).get('query', {})
            pg = (r.get('pages') or [{}])[0]; qid = (pg.get('pageprops') or {}).get('wikibase_item')
            if qid: break
        if not qid:
            r = api('https://ja.wikipedia.org/w/api.php', {'action': 'query', 'generator': 'search', 'gsrsearch': v['jp'], 'gsrlimit': 1, 'prop': 'pageprops'}).get('query', {})
            pg = (r.get('pages') or [{}])[0]; qid = (pg.get('pageprops') or {}).get('wikibase_item'); res['wiki_guess'] = pg.get('title')
    if qid:
        w = api('https://www.wikidata.org/w/api.php', {'action': 'wbgetentities', 'ids': qid, 'props': 'claims|sitelinks'}).get('entities', {}).get(qid, {})
        res['official'] = [c['mainsnak']['datavalue']['value'] for c in w.get('claims', {}).get('P856', []) if c.get('mainsnak', {}).get('datavalue')][:2]
        jt = (w.get('sitelinks', {}).get('jawiki') or {}).get('title')
    if jt:
        res['wiki_ja'] = jt
        r = api('https://ja.wikipedia.org/w/api.php', {'action': 'query', 'titles': jt, 'prop': 'extracts', 'explaintext': 1}).get('query', {})
        res['snips'] += snips((r.get('pages') or [{}])[0].get('extract', ''), 'wiki', 3)
    urls = ([v['url']] if v.get('url') else []) + [u for u in res['official'] if u != v.get('url')]
    for u in urls[:2]:
        fin, h = fetch(u)
        if not h: continue
        res['snips'] += snips(text_of(h), fin, 3)
        for lu in links(fin, h):
            _, h2 = fetch(lu)
            if h2: res['snips'] += snips(text_of(h2), lu, 3)
    # 같은 글 빼기
    seen = set(); res['snips'] = [s for s in res['snips'] if not (s['text'][:80] in seen or seen.add(s['text'][:80]))][:10]
    return k, res
if __name__ == '__main__':
    Q = json.load(open('park.json', encoding='utf-8'))
    with ThreadPoolExecutor(8) as ex: out = dict(ex.map(place, Q.items()))
    json.dump(out, open('park_candidates.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('done', len(out), sum(1 for v in out.values() if v['snips']))
