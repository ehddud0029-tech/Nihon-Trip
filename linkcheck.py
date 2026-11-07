# 공식 사이트 후보 확인: links.json id->[url...] → links_result.json id->[{url,status,final,title}]
import json, urllib.request, re, html, ssl
UA = 'Mozilla/5.0 (compatible; GoNihonTripLinkCheck/1.0; +https://gonihontrip.com/)'
ctx = ssl.create_default_context()
def get(u):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': UA, 'Accept-Language': 'ja,en;q=0.8'})
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            b = r.read(200000)
            cs = r.headers.get_content_charset() or ('shift_jis' if b'shift_jis' in b[:3000].lower() or b'sjis' in b[:3000].lower() else 'utf-8')
            t = b.decode(cs, 'replace'); m = re.search(r'<title[^>]*>(.*?)</title>', t, re.S | re.I)
            return {'url': u, 'status': r.status, 'final': r.geturl(), 'title': html.unescape(m.group(1).strip())[:120] if m else ''}
    except urllib.error.HTTPError as e: return {'url': u, 'status': e.code, 'final': u, 'title': ''}
    except Exception as e: return {'url': u, 'status': 0, 'final': u, 'title': str(e)[:100]}
L = json.load(open('links.json'))
out = {k: [get(u) for u in us] for k, us in L.items()}
json.dump(out, open('links_result.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print({k: [x['status'] for x in v] for k, v in out.items()})
