# 주차장 정보 2차: 검색(DuckDuckGo HTML)으로 '<일본어 이름> <동네> 駐車場' 상위 결과 페이지에서 '駐車' 주변 글 모으기
# park2.json id -> {q: 검색어} → park2_candidates.json id -> {results:[url...], snips:[{src,text}]}
import json, re, time, random, urllib.parse
from html import unescape as html_unescape
from parking import fetch, text_of, snips
SKIP = re.compile(r'tabelog|instagram|facebook|twitter|x\.com|youtube|tiktok|pinterest|wikipedia|support\.yahoo|times-info|akippa|navitime\.co\.jp/parking|parkinggod|earth-car|parking\.|toku-p|tripadvisor|ameblo|note\.com|hatena')
def yahoo(q):
    _, h = fetch('https://search.yahoo.co.jp/search?' + urllib.parse.urlencode({'p': q, 'ei': 'UTF-8'}))
    us = []
    for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"', h):
        u = html_unescape(m.group(1))
        if re.search(r'yahoo\.co\.jp|yimg|yahoo\.com', u) or SKIP.search(u): continue
        if u not in us: us.append(u)
    return us[:3], len(h)
def bing(q):
    _, h = fetch('https://www.bing.com/search?' + urllib.parse.urlencode({'q': q, 'setlang': 'ja', 'cc': 'JP'}))
    us = []
    for m in re.finditer(r'<h2[^>]*><a[^>]+href="(https?://[^"]+)"', h):
        u = html_unescape(m.group(1))
        if re.search(r'bing\.com|microsoft', u) or SKIP.search(u): continue
        if u not in us: us.append(u)
    return us[:3], len(h)
def ddg(q):
    for k in range(3):
        _, h = fetch('https://html.duckduckgo.com/html/?' + urllib.parse.urlencode({'q': q, 'kl': 'jp-jp'}))
        us = []
        for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"', h):
            u = m.group(1)
            if 'uddg=' in u: u = urllib.parse.unquote(re.search(r'uddg=([^&]+)', u).group(1))
            if u.startswith('http') and not SKIP.search(u) and 'duckduckgo' not in u and u not in us: us.append(u)
        if us or h: return us[:3]
        time.sleep(5 * (k + 1))
    return []
Q = json.load(open('park2.json', encoding='utf-8'))
try: out = json.load(open('park2_candidates.json', encoding='utf-8'))
except Exception: out = {}
from concurrent.futures import ThreadPoolExecutor
import threading
T0 = time.time(); LIM = 290 * 60; lock = threading.Lock()
def one(item):
    k, v = item
    if time.time() - T0 > LIM: return None
    us, n1 = yahoo(v['q']); eng = 'yahoo'
    if not us: us, n1 = bing(v['q']); eng = 'bing'
    res = {'q': v['q'], 'results': us, 'snips': [], 'eng': eng}
    for u in us[:3]:
        fin, h = fetch(u, 300000)
        if h: res['snips'] += snips(text_of(h), fin, 2)
    time.sleep(1 + random.random())
    return k, res
todo = [(k, v) for k, v in Q.items() if k not in out]
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(one, todo):
        if r:
            with lock: out[r[0]] = r[1]
rest = {k: v for k, v in Q.items() if k not in out}
json.dump(out, open('park2_candidates.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
json.dump(rest, open('park2.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('done', len(out), 'left', len(rest), sum(1 for v in out.values() if v['snips']))
