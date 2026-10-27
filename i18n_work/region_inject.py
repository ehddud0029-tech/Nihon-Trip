"""나고야·히로시마·시코쿠 지역 데이터를 tabishiori.html · areas.js · geo.js 에 넣어요.
항상 backup/ 의 원본에서 다시 만들기 때문에 여러 번 실행해도 같은 결과예요.
번역 줄은 tr_28.tsv 로 나가요."""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from region_nagoya import NAGOYA
from region_hiroshima import HIROSHIMA
from region_shikoku import SHIKOKU
from region_spotinfo import INFO
import region_extra as EX

H = '/home/claude/tabishiori.html'
SITE = '/home/claude/site'
BK = '/home/claude/i18n_work/backup'
os.makedirs(BK, exist_ok=True)
for src, name in [(H, 'tabishiori.pre.html'), (f'{SITE}/areas.js', 'areas.pre.js'), (f'{SITE}/geo.js', 'geo.pre.js'), ('/home/claude/sitegen/spot_info_view.js', 'spot_info_view.pre.js')]:
    if not os.path.exists(f'{BK}/{name}'):
        shutil.copy(src, f'{BK}/{name}')

PACKS = [NAGOYA, HIROSHIMA, SHIKOKU]
for P in PACKS:
    P["shops"] = P["shops"] + EX.SHOPS_ADD.get(P["key"], [])
    P["shop_picks"] = {**P["shop_picks"], **{k: v for k, v in EX.PICKS_ADD.items() if k in [x[0] for x in P["shops"]]}}
ORDER = ["tokyo", "osaka", "fukuoka", "hokkaido", "okinawa", "nagoya", "hiroshima", "shikoku"]
ROWS = {}
def tr(x):
    if isinstance(x, (tuple, list)) and len(x) == 5 and all(isinstance(v, str) for v in x):
        if x[0]:
            ROWS.setdefault(x[0], tuple(x))
        return x[0]
    return x
def route(r):
    return {"from": tr(r["from"]), "to": tr(r["to"]), "mode": r["mode"], "line": tr(r["line"]), "min": r["min"]}
J = lambda o: json.dumps(o, ensure_ascii=False)
GIFT_CAT = {"식품": "먹거리"}

cities, airport, icbuy, icmap, to_area, area_route, transport, hum, coord, in_city = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
sats, spots, foods, shops, fests, wiki, geo = [], [], [], [], [], {}, {}
guide, eats, gifts, souv, ashop, picks = {}, {}, [], {}, {}, {}
regions, areas = [], {}
ids = set()
def uid(i):
    assert i not in ids, i
    ids.add(i)
    return i

for P in PACKS:
    c = P["key"]
    regions.append([c, tr(P["ko"]), P["jp"]])
    areas[c] = [[k, tr(ko), jp, lat, lng] for k, ko, jp, lat, lng in P["areas"]]
    cities[c] = {"ko": tr(P["ko"]), "jp": P["jp"], "air": tr(P["air"]), "ic": tr(P["ic"]), "temp": P["temp"]}
    airport[c] = [route(r) for r in P["airport"]]
    icbuy[c] = tr(P["icbuy"])
    icmap[c] = [[tr(a), b] for a, b in P["icmap"]]
    for k, v in P["to_area"].items():
        to_area[k] = {kk: [route(r) for r in vv] for kk, vv in v.items()}
    for k, v in P["area_route"].items():
        area_route[k] = [route(r) for r in v]
    transport[c] = {"routes": [[tr(a), tr(b), tr(t)] for a, b, t in P["transport"]["routes"]], "tip": tr(P["transport"]["tip"])}
    hum[c] = P["hum"]; coord[c] = P["coord"]; in_city[c] = P["in_city"]; sats += P["satellites"]
    for (i, sub, cat, name, jp, desc, place, sta, tip, lat, lng, wk) in P["spots"]:
        spots.append({"id": uid(i), "type": "spot", "city": c, "sub": sub, "cat": cat, "k": "", "name": tr(name), "jp": jp, "desc": tr(desc), "area": tr(place), "station": tr(sta), "tip": tr(tip)})
        geo[i] = [lat, lng]
        if wk: wiki[i] = [wk]
    for (i, mon, name, jp, when, desc, place, tip, sub, lat, lng) in P["fests"]:
        fests.append({"id": uid(i), "type": "fest", "city": c, "month": mon, "k": "", "name": tr(name), "jp": jp, "when": tr(when), "desc": tr(desc), "area": tr(place), "tip": tr(tip), "sub": sub})
        geo[i] = [lat, lng]
    for (i, cat, name, jp, desc, sta, tip, sub, lat, lng) in P["shops"]:
        shops.append({"id": uid(i), "type": "shop", "city": c, "cat": tr(cat), "k": "", "name": tr(name), "jp": jp, "desc": tr(desc), "station": tr(sta), "tip": tr(tip), "sub": sub})
        geo[i] = [lat, lng]
    for (i, cat, name, jp, desc, place, price, tip, sub) in P["foods"]:
        foods.append({"id": uid(i), "type": "food", "city": c, "cat": cat, "k": "", "name": tr(name), "jp": jp, "desc": tr(desc), "area": tr(place), "price": price, "tip": tr(tip), "sub": sub})
    for (sub, cat, name, jp, desc, where) in P["gifts"]:
        gifts.append([c, sub, GIFT_CAT.get(tr(cat), tr(cat)), tr(name), jp, tr(desc), [[tr(a), q] for a, q in where]])
    souv[c] = tr(P["souvenir"])
    for k, (a, b) in P["area_shop"].items(): ashop[k] = [tr(a), tr(b)]
    for k, v in P["shop_picks"].items(): picks[k] = [tr(x) for x in v]
    for k, v in P["local_eats"].items(): eats[k] = [[tr(a), tr(b)] for a, b in v]
    for k, g in P["area_guide"].items():
        guide[k] = {"title": tr(g["title"]), "stops": [[i, tr(l)] for i, l in g["stops"]], "move": [[m, tr(t)] for m, t in g["move"]]}

# 모든 하위 지역에 안내·쇼핑·음식 정보가 있는지
allareas = [a[0] for v in areas.values() for a in v]
for k in allareas:
    for d, nm in [(guide, 'area_guide'), (ashop, 'area_shop'), (eats, 'local_eats'), (to_area, 'to_area')]:
        assert k in d, (k, nm)
for g in guide.values():
    for i, _ in g["stops"]: assert i in ids, i
for k in picks: assert k in ids, k
for x in shops: assert x['id'] in picks, ('picks', x['id'])
for k in allareas: assert any(x['sub']==k for x in shops), ('shop for', k)
for k in INFO: assert k in ids, ('spot_info', k)
missing = [s["id"] for s in spots if s["id"] not in INFO]
assert not missing, missing

# 교통카드
ic_add = [
 {"id": "manaca", "name": "manaca · TOICA", "area": tr(("나고야 (지하철·메이테쓰 / JR 도카이)", "Nagoya (subway & Meitetsu / JR Central)", "名古屋（地下鉄・名鉄／JR東海）", "Nagoya (metro y Meitetsu / JR Central)", "Nagoya (métro et Meitetsu / JR Central)")),
  "cities": ["nagoya"], "img": "", "credit": "", "file": "",
  "buy": [tr(("주부국제공항역·나고야역 발매기 (manaca는 지하철·메이테쓰, TOICA는 JR)", "Ticket machines at Centrair and Nagoya stations (manaca for subway and Meitetsu, TOICA for JR)", "中部国際空港駅・名古屋駅の券売機（manacaは地下鉄・名鉄、TOICAはJR）", "Máquinas de Centrair y Nagoya (manaca para metro y Meitetsu, TOICA para JR)", "Distributeurs de Centrair et de Nagoya (manaca pour métro et Meitetsu, TOICA pour JR)"))],
  "note": tr(("Suica·ICOCA 같은 다른 지역 카드도 그대로 쓸 수 있어요.", "Other regions' cards such as Suica and ICOCA work here too.", "SuicaやICOCAなど他地域のカードもそのまま使えます。", "También funcionan tarjetas de otras regiones como Suica o ICOCA.", "Les cartes d'autres régions comme Suica ou ICOCA fonctionnent aussi."))},
 {"id": "shikoku", "name": "IruCa · ICい～カード", "area": tr(("시코쿠 (다카마쓰 고토덴 / 마쓰야마 이요테쓰)", "Shikoku (Kotoden in Takamatsu / Iyotetsu in Matsuyama)", "四国（高松ことでん／松山伊予鉄）", "Shikoku (Kotoden en Takamatsu / Iyotetsu en Matsuyama)", "Shikoku (Kotoden à Takamatsu / Iyotetsu à Matsuyama)")),
  "cities": ["shikoku"], "img": "", "credit": "", "file": "",
  "buy": [tr(("고토덴·이요테쓰 역 창구", "Kotoden and Iyotetsu station counters", "ことでん・伊予鉄の駅窓口", "Taquillas de Kotoden e Iyotetsu", "Guichets Kotoden et Iyotetsu"))],
  "note": tr(("그 지역 전용 카드라 다른 지역에서는 못 쓰고, Suica 같은 카드도 이 노선에서는 대부분 못 써요. 여행자는 현금이나 1일 승차권이 편해요.", "These are local-only cards, and Suica-type cards mostly don't work on these lines. Visitors are better off with cash or a day pass.", "地域限定のカードで、Suicaなどもこれらの路線ではほぼ使えません。旅行者は現金か1日乗車券が便利です。", "Son tarjetas locales y las de tipo Suica casi no sirven en estas líneas: mejor efectivo o un pase de un día.", "Cartes locales uniquement ; les cartes type Suica ne marchent presque pas sur ces lignes. Mieux vaut espèces ou pass journée."))}]

# 사진: 위키백과 문서 (2026-10-26 확인, 이미지 있는 문서 우선)
wiki.update({
 "n_jokamachi": ["ja:犬山市"], "n_ghibli": ["ja:愛・地球博記念公園"], "n_asaichi": ["ja:宮川朝市"], "n_hidanosato": ["ja:飛騨民俗村", "Hida Folk Village"],
 "n_wada": ["ja:和田家住宅"], "n_sanmachi": ["ja:三町 (高山市)", "Takayama, Gifu"], "h_orizuru": ["ja:おりづるタワー"], "k_yashima": ["ja:屋島"],
 "h_ivy": ["ja:倉敷アイビースクエア"], "k_iepro": ["ja:家プロジェクト"], "h_shimanami": ["ja:多々羅大橋", "ja:来島海峡大橋"], "h_bikan": ["ja:倉敷美観地区", "Kurashiki"],
 "f_hitsumabushi": ["ja:ひつまぶし"], "f_misokatsu": ["ja:味噌カツ"], "f_tebasaki": ["ja:手羽先唐揚げ"], "f_hidagyu": ["ja:飛騨牛"],
 "f_hiroshimayaki": ["ja:広島風お好み焼き"], "f_oyster": ["ja:広島かき"], "f_onomichiramen": ["ja:尾道ラーメン"],
 "f_sanukiudon": ["ja:讃岐うどん"], "f_honetsuki": ["ja:骨付鳥"], "f_jakoten": ["ja:じゃこ天"],
 "g23": ["ja:ういろう (菓子)"], "g24": ["ja:海老煎餅"], "g25": ["ja:さるぼぼ"], "g26": ["ja:もみじ饅頭"], "g27": ["ja:熊野筆"],
 "g28": ["ja:一六本舗"], "g29": ["ja:今治タオル"], "g30": ["ja:讃岐うどん"],
 "p_meieki": ["ja:名駅"], "p_sakae": ["ja:栄 (名古屋市)"], "p_inuyamahonmachi": ["ja:犬山市"], "p_takayamasanmachi": ["ja:三町 (高山市)"],
 "p_shirakawaogimachi": ["ja:白川郷"], "p_hondori": ["ja:広島本通商店街"], "p_ekie": ["ja:広島駅"], "p_miyajimasando": ["ja:厳島"],
 "p_onomichihondori": ["Onomichi"], "p_kurashikihonmachi": ["ja:倉敷美観地区"], "p_dogohaikara": ["ja:道後温泉"], "p_okaido": ["ja:松山市"],
 "p_marugame": ["ja:高松中央商店街"], "p_kotohirasando": ["ja:金刀比羅宮"], "p_naoshimaport": ["Naoshima"],
 "f_nagoyamatsuri": ["ja:名古屋まつり"], "f_inuyamamatsuri": ["ja:犬山祭"], "f_takayama_spring": ["ja:高山祭"], "f_takayama_autumn": ["ja:高山祭"],
 "f_shirakawa_light": ["ja:白川郷"], "f_flowerfes": ["ja:ひろしまフラワーフェスティバル"], "f_toronagashi": ["Hiroshima Peace Memorial"],
 "f_dogoaki": ["ja:道後温泉"], "f_takamatsumatsuri": ["ja:さぬき高松まつり"], "f_konpiratai": ["ja:金刀比羅宮"]})
BLOCK1 = f"""/* 새 지역: 나고야·히로시마·시코쿠 (i18n_work/region_*.py 에서 만듦) */
Object.assign(CITIES,{J(cities)});
Object.assign(AIRPORT,{J(airport)}); Object.assign(ICBUY,{J(icbuy)}); Object.assign(ICMAP,{J(icmap)});
Object.assign(TO_AREA,{J(to_area)}); Object.assign(AREA_ROUTE,{J(area_route)}); Object.assign(TRANSPORT,{J(transport)});
Object.assign(HUM,{J(hum)}); Object.assign(COORD,{J(coord)}); Object.assign(IN_CITY,{J(in_city)}); SATELLITE.push(...{J(sats)});
SPOTS.push(...{J(spots)});
FOODS.push(...{J(foods)});
SHOPS.push(...{J(shops)});
FESTS.push(...{J(fests)});
Object.assign(WIKI,{J(wiki)});
{{ const o={J(ORDER)}, t={{...CITIES}}; o.forEach(k=>{{ delete CITIES[k]; CITIES[k]=t[k]; }}); }}
"""
BLOCK2 = f"""Object.assign(AREA_GUIDE,{J(guide)}); Object.assign(LOCAL_EATS,{J(eats)}); GIFTS.push(...{J(gifts)}.map(([city,sub,cat,name,jp,desc,where],i)=>({{id:"g"+(GIFTS.length+i),city,sub,cat,name,jp,desc,where}})));
Object.assign(SOUVENIR,{J(souv)}); Object.assign(AREA_SHOP,{J(ashop)}); Object.assign(SHOP_PICKS,{J(picks)});
IC_CARDS.find(x=>x.id==="icoca").cities.push("hiroshima"); IC_CARDS.push(...{J(ic_add)});
"""

def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a))
    return s.replace(a, b)

s = open(f'{BK}/tabishiori.pre.html', encoding='utf-8').read()
s = rep(s, '\nconst ALL = [', '\n' + BLOCK1 + 'const ALL = [')
i = s.index('\nconst IC_CARDS = '); j = s.index('\n', i + 1)
s = s[:j + 1] + BLOCK2 + s[j + 1:]
i = s.index('\nconst SPOT_INFO = {'); j = s.index('\n};\n', i) + 4
s = s[:j] + 'Object.assign(SPOT_INFO,' + J(INFO) + ');\n' + s[j:]
s = rep(s, 'const ICITY_ORDER = ["tokyo","osaka","fukuoka","hokkaido","okinawa"];', 'const ICITY_ORDER = ["tokyo","osaka","fukuoka","hokkaido","okinawa","nagoya","hiroshima","shikoku"];')
s = rep(s, 'const PHOTO_KEY = "tabishiori-photos-v7";', 'const PHOTO_KEY = "tabishiori-photos-v10";')
s = rep(s, '오키나와 OKICA를 빼면 서로 호환돼요.', '오키나와 OKICA와 시코쿠 지역 카드를 빼면 서로 호환돼요.')
# 음식: 하위 지역 지정 + 맛집 데이터가 없는 지역
s = rep(s, 'price:a[8],tip:a[9]}));', 'price:a[8],tip:a[9],...(a[10]?{sub:a[10]}:{})}));')
s = rep(s, '''  let body;
  if(curArea()){
    body = arBlock(st.area, st.menu);''', '''  let body;
  const noAR = !areasOf(st.city).some(A=>(window.AR_SLUG||{})[A.key]);
  if(noAR){
    const P = curArea()||CITIES[st.city];
    body = `<section class="arbox"><div class="arhead"><span class="arbadge">구글 지도</span><h3>${esc(P.ko)}</h3></div>
      <p class="credit">이 지역의 맛집 추천은 준비 중이에요. 아래 향토음식을 참고해 구글 지도에서 가게를 찾아보세요.</p>
      <a class="btn reserve" href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(P.jp.split("・")[0]+" グルメ")}" target="_blank" rel="noopener">구글 지도에서 맛집 찾기 ↗</a></section>`;
  }else if(curArea()){
    body = arBlock(st.area, st.menu);''')
s = rep(s, '''<p>${cityName()} · ${menuName} · ${st.menu==="konamon"?"구글 지도 인기 가게":"AutoReserve 추천 순서"}</p></div></div>
   ${menuChips}${body}''', '''<p>${noAR?`<span>${esc(cityName())}</span> · <span>꼭 먹어볼 향토음식</span>`:`${cityName()} · ${menuName} · ${st.menu==="konamon"?"구글 지도 인기 가게":"AutoReserve 추천 순서"}`}</p></div></div>
   ${noAR?"":menuChips}${body}''')

s = rep(s, """    const eatCell = `<div class="beat">""", """    const eatCell = (pa && !picks.length) ? `<div class="beat"><dt>${esc(AREA[pa]?.ko||"")} 추천 맛집</dt><dd class="sub">맛집 추천은 준비 중이에요</dd>
      <dd class="sub"><a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(AREA[pa].jp.split("・")[0]+" グルメ")}" target="_blank" rel="noopener">구글 지도에서 맛집 찾기 ↗</a></dd></div>` : `<div class="beat">""")
s = rep(s, '<dd class="sub">${esc(ic.buy[0])}</dd>', '<dd class="sub">${esc(ic.cities[0]===st.city?ic.buy[0]:(ICBUY[st.city]||ic.buy[0]))}</dd>')
# 입장료 표시: 라벨·메모를 바로 넣은 {ko,en,...} 객체도 받기
def siv(t):
    t = rep(t, 'const lbl = k => k ? t(LB[k]) : "";', 'const lbl = k => k ? (typeof k==="object" ? t(k) : t(LB[k])) : "";')
    t = rep(t, '(si.fx||[]).forEach(k=>out.push(t(TX[k])));', '(si.fx||[]).forEach(k=>out.push(typeof k==="object"?t(k):t(TX[k])));')
    t = rep(t, '(si.hx||[]).forEach(k=>out.push(t(TX[k])));', '(si.hx||[]).forEach(k=>out.push(typeof k==="object"?t(k):t(TX[k])));')
    return t
s = siv(s)
open('/home/claude/sitegen/spot_info_view.js', 'w', encoding='utf-8').write(siv(open(f'{BK}/spot_info_view.pre.js', encoding='utf-8').read()))
v = open('/home/claude/sitegen/itin_view.js', encoding='utf-8').read()
v = v.replace('const ICITY_ORDER = ["tokyo","osaka","fukuoka","hokkaido","okinawa"];', 'const ICITY_ORDER = ["tokyo","osaka","fukuoka","hokkaido","okinawa","nagoya","hiroshima","shikoku"];')
open('/home/claude/sitegen/itin_view.js', 'w', encoding='utf-8').write(v)

# 안내·일정 데이터 (guide_emit.py · itin_emit.py 결과)
for name in ['GUIDE', 'ITIN']:
    f = '/home/claude/sitegen/' + ('guide_data.js' if name == 'GUIDE' else 'itin_data.js')
    new = open(f, encoding='utf-8').read().strip()
    i = s.index(f'\nconst {name} = ') + 1; j = s.index('\n', i)
    s = s[:i] + new + s[j:]
open(H, 'w', encoding='utf-8').write(s)

# areas.js · geo.js
a = open(f'{BK}/areas.pre.js', encoding='utf-8').read()
a = a.rstrip()
assert a.endswith('};')
a += '\n/* 새 지역 */\nwindow.REGIONS.push(...' + J(regions) + ');\nObject.assign(window.AREAS,' + J(areas) + ');\n' + 'window.REGIONS.sort((x,y)=>' + J(ORDER) + '.indexOf(x[0])-' + J(ORDER) + '.indexOf(y[0]));\n'
open(f'{SITE}/areas.js', 'w', encoding='utf-8').write(a)
g = open(f'{BK}/geo.pre.js', encoding='utf-8').read().rstrip() + '\nObject.assign(window.GEO,' + J(geo) + ');\n'
open(f'{SITE}/geo.js', 'w', encoding='utf-8').write(g)
for f in ['areas.js', 'geo.js']:
    shutil.copy(f'{SITE}/{f}', f'/home/claude/{f}')

# 번역 줄
for u in EX.UI: tr(u)
for p in PACKS: pass
open('/home/claude/i18n_work/tr_28.tsv', 'w', encoding='utf-8').write(''.join('\t'.join(r) + '\n' for r in ROWS.values()))
print(len(spots), 'spots', len(fests), 'fests', len(shops), 'shops', len(foods), 'foods', len(gifts), 'gifts', len(ROWS), 'rows')

# 설명 문구에 새 지역 이름 넣기 (제목은 그대로)
PAIRS = [
 ("도쿄·오사카·후쿠오카·홋카이도·오키나와와", "도쿄·오사카·나고야·히로시마·시코쿠·후쿠오카·홋카이도·오키나와와"),
 ("Tokyo, Osaka, Fukuoka, Hokkaido, Okinawa and", "Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa and"),
 ("東京・大阪・福岡・北海道・沖縄と", "東京・大阪・名古屋・広島・四国・福岡・北海道・沖縄と"),
 ("Tokio, Osaka, Fukuoka, Hokkaido, Okinawa y", "Tokio, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa y"),
 ("Tokyo, Osaka, Fukuoka, Hokkaido, Okinawa et", "Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa et"),
 ("도쿄·오사카·교토·후쿠오카·홋카이도·오키나와의", "도쿄·오사카·교토·나고야·히로시마·시코쿠·후쿠오카·홋카이도·오키나와의"),
 ("Tokyo, Osaka, Kyoto, Fukuoka, Hokkaido and Okinawa", "Tokyo, Osaka, Kyoto, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido and Okinawa"),
 ("東京・大阪・京都・福岡・北海道・沖縄の", "東京・大阪・京都・名古屋・広島・四国・福岡・北海道・沖縄の"),
 ("Tokio, Osaka, Kioto, Fukuoka, Hokkaido y Okinawa", "Tokio, Osaka, Kioto, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido y Okinawa"),
 ("Tokyo, Osaka, Kyoto, Fukuoka, Hokkaido et Okinawa", "Tokyo, Osaka, Kyoto, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido et Okinawa"),
]
for f in [H, '/home/claude/sitegen/gen.py']:
    t = open(f, encoding='utf-8').read(); n = 0
    for a, b in PAIRS:
        n += t.count(a); t = t.replace(a, b)
    open(f, 'w', encoding='utf-8').write(t); print(f, n, 'region-name replacements')

# AutoReserve 맛집 (2026년 10월 26일 AutoReserve 지역·메뉴 페이지 순서)
import glob, re
SLUG = {"meieki": "aichi/nagoya-shi-naka-ku", "inuyama": "aichi/inuyama-shi", "takayama": "gifu/takayama-shi", "shirakawago": "gifu/ono-gun-shirakawa-mura",
        "hirocity": "hiroshima/hiroshima-shi-naka-ku", "miyajima": "hiroshima/hatsukaichi-shi", "onomichi": "hiroshima/onomichi-shi", "kurashiki": "okayama/kurashiki-shi",
        "matsuyama": "ehime/matsuyama-shi", "takamatsu": "kagawa/takamatsu-shi", "naoshima": "kagawa/kagawa-gun-naoshima-cho", "kotohira": "kagawa/nakatado-gun-kotohira-cho"}
for f in ['autoreserve.js', 'google_picks.js']:
    if not os.path.exists(f'{BK}/{f}'): shutil.copy(f'{SITE}/{f}', f'{BK}/{f}')
ar = open(f'{BK}/autoreserve.js', encoding='utf-8').read()
start = max(int(x) for x in re.findall(r'"(\d+)":\{"n"', ar)) + 1
rows = {}
for f in sorted(glob.glob('/home/claude/i18n_work/ar_new_shops_*.tsv')):
    for line in open(f, encoding='utf-8'):
        p = line.rstrip('\n').split('\t'); rows[p[0]] = p
LST = json.load(open('/home/claude/i18n_work/ar_new_lists.json', encoding='utf-8'))
num = {}
for k in sorted(rows):
    pass
order = []
for key, v in LST.items():
    for i in v:
        if i not in num: num[i] = str(start + len(num)); order.append(i)
shops_js = {num[i]: {"n": rows[i][1], "dish": rows[i][2], "feat": rows[i][3], "b": rows[i][4]} for i in order}
lists_js = {}
for key, v in LST.items():
    a, m = key.split('|')
    if v: lists_js.setdefault(SLUG[a], {})[m] = [num[i] for i in v]
argeo = {num[i]: [float(rows[i][5]), float(rows[i][6]), i] for i in order}
ar = ar.rstrip() + '\n/* 나고야·히로시마·시코쿠 (2026년 10월 26일 기준) */\nObject.assign(window.AR_SLUG,' + J(SLUG) + ');\nObject.assign(window.AR_LISTS,' + J(lists_js) + ');\nObject.assign(window.AR_SHOPS,' + J(shops_js) + ');\n'
open(f'{SITE}/autoreserve.js', 'w', encoding='utf-8').write(ar)
g = open(f'{SITE}/geo.js', encoding='utf-8').read().rstrip() + '\nObject.assign(window.AR_GEO,' + J(argeo) + ');\n'
open(f'{SITE}/geo.js', 'w', encoding='utf-8').write(g)
gp = open(f'{BK}/google_picks.js', encoding='utf-8').read().rstrip() + '\n/* 히로시마 오코노미야키 (AutoReserve에 등록 가게 없음) */\nObject.assign(window.GOOGLE_PICKS,' + J({
 "hiroshima/hiroshima-shi-naka-ku": {"konamon": [
  ["미짱 총본점 핫초보리 본점", "みっちゃん総本店 八丁堀本店", "히로시마 오코노미야키", "히로시마식 오코노미야키의 원조로 꼽히는 노포", "¥1,000~¥2,000"],
  ["핫쇼", "八昌 薬研堀", "히로시마 오코노미야키", "줄 서는 명점, 바삭한 면", "¥1,000~¥2,000"],
  ["오코노미무라", "お好み村 広島", "히로시마 오코노미야키", "오코노미야키 가게가 층마다 모인 건물", "¥1,000~¥2,000"],
  ["덴코세카 에키에점", "電光石火 ekie", "폭신한 오코노미야키", "히로시마역 안, 달걀로 감싼 스타일", "¥1,000~¥2,000"],
  ["레이짱 에키에점", "麗ちゃん ekie", "히로시마 오코노미야키", "히로시마역 안의 오래된 인기점", "¥1,000~¥2,000"]]}}) + ');\n'
open(f'{SITE}/google_picks.js', 'w', encoding='utf-8').write(gp)
for f in ['autoreserve.js', 'geo.js', 'google_picks.js']:
    shutil.copy(f'{SITE}/{f}', f'/home/claude/{f}')
print('AR shops', len(shops_js), 'from', start, 'lists', sum(len(v) for v in lists_js.values()))
