# 주차장 정보 2차: 검색(DuckDuckGo HTML)으로 '<일본어 이름> <동네> 駐車場' 상위 결과 페이지에서 '駐車' 주변 글 모으기
# park2.json id -> {q: 검색어} → park2_candidates.json id -> {results:[url...], snips:[{src,text}]}
import json, re, time, random, urllib.parse
from parking import fetch, text_of, snips
SKIP = re.compile(r'tabelog|instagram|facebook|twitter|x\.com|youtube|tiktok|pinterest|wikipedia')
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
Q = json.load(open('park2.json', encoding='utf-8')); out = {}
for i, (k, v) in enumerate(Q.items()):
    us = ddg(v['q']); res = {'q': v['q'], 'results': us, 'snips': []}
    for u in us:
        fin, h = fetch(u)
        if h: res['snips'] += snips(text_of(h), fin, 2)
    out[k] = res
    if i % 20 == 0:
        print(i, k, len(us), len(res['snips']), flush=True)
        json.dump(out, open('park2_candidates.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    time.sleep(1.5 + random.random())
json.dump(out, open('park2_candidates.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('done', len(out), sum(1 for v in out.values() if v['snips']))
