# 오픈스트리트맵(OSM) 주차장: 장소 좌표 주변의 amenity=parking (이름·거리·대수·요금 태그)
import json, time, math, urllib.request, urllib.parse
EPS = ['https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter', 'https://maps.mail.ru/osm/tools/overpass/api/interpreter']
items = json.load(open('osm.json'))
try: out = json.load(open('osm_park.json'))
except Exception: out = {}
def dist(a, b, c, d):
    R = 6371000; p1, p2 = math.radians(a), math.radians(c)
    x = math.radians(d - b) * math.cos((p1 + p2) / 2); y = p2 - p1
    return round(R * math.hypot(x, y))
def q(lat, lng, r):
    ql = f'[out:json][timeout:60];nwr["amenity"="parking"](around:{r},{lat},{lng});out center tags;'
    for i in range(6):
        ep = EPS[i % len(EPS)]
        try:
            req = urllib.request.Request(ep, data=urllib.parse.urlencode({'data': ql}).encode(), headers={'User-Agent': 'gonihontrip-parking/1.0 (travel site; contact via gonihontrip.com)'})
            return json.load(urllib.request.urlopen(req, timeout=90))['elements']
        except Exception as e:
            print('retry', ep, e, flush=True); time.sleep(5 + i * 5)
    return None
t0 = time.time()
for n, it in enumerate(items):
    if it['id'] in out: continue
    if time.time() - t0 > 280 * 60: break
    r = 300 if it['k'] == 'food' else 600
    el = q(it['lat'], it['lng'], r)
    if el is None: continue
    rows = []
    for e in el:
        tg = e.get('tags', {}); c = e.get('center') or e
        if tg.get('access') in ('private', 'no', 'customers_only_private'): continue
        if 'lat' not in c: continue
        rows.append({k: v for k, v in {'name': tg.get('name'), 'ja': tg.get('name:ja'), 'd': dist(it['lat'], it['lng'], c['lat'], c['lon']), 'cap': tg.get('capacity'), 'fee': tg.get('fee'), 'type': tg.get('parking'), 'acc': tg.get('access'), 'op': tg.get('operator'), 'hours': tg.get('opening_hours'), 'charge': tg.get('charge'), 'id': e['type'][0] + str(e['id'])}.items() if v})
    rows.sort(key=lambda x: x['d'])
    out[it['id']] = rows[:12]
    if n % 20 == 0:
        print(n, it['id'], len(rows), flush=True); json.dump(out, open('osm_park.json', 'w'), ensure_ascii=False)
    time.sleep(1.2)
json.dump(out, open('osm_park.json', 'w'), ensure_ascii=False)
print('done', len(out), '/', len(items))
