# 장소 상세 '주차장' 줄 (2026-11)
# - site/parking_curated.json: 공식 안내를 읽고 직접 정리한 곳 (전용 주차장 있음·대수·요금 / 없음 / 근처 공영)
# - photo-job osm_park.json → site/parking_osm.json: 정리본이 없는 곳은 오픈스트리트맵 주변 주차장(가장 가까운 거리)
# 입장료·운영 시간과 같은 facts dl 줄, 8개 언어 문장은 코드에서 만듦. html·pre, 여러 번 돌려도 안전
import json, re
FILES = ['/home/claude/tabishiori.html', '/home/claude/i18n_work/backup/tabishiori.pre.html']
cur = json.load(open('/home/claude/site/parking_curated.json'))
cur = {k: v for k, v in cur.items() if not k.startswith('_')}
try: osm = json.load(open('/home/claude/site/parking_osm.json'))
except Exception: osm = {}
# 주변 주차장: 가장 가까운 곳 거리(10m 단위)와 600m 안 개수(최대 10+)
PO = {}
for k, rows in osm.items():
    if k.startswith('ar') or k in cur or not rows: continue
    PO[k] = [int(round(rows[0]['d'] / 10.0) * 10) or 10, min(len(rows), 10)]

BLOCK = '/*PARK_BEGIN*/\nconst PARK = ' + json.dumps(cur, ensure_ascii=False, separators=(',', ':')) + ';\nconst PARK_OSM = ' + json.dumps(PO, separators=(',', ':')) + ';\n' + r'''const PARK_T = {
 ko:{o:"전용 주차장 있음",n:"전용 주차장 없음 · 주변 유료 주차장 이용",m:"근처 공영·제휴 주차장 이용",cap:"약 {c}대",free:"무료",paid:"유료",r:"{m}분 {y}엔",v:"1회 {y}엔",d:"하루 최대 {y}엔",osm:"주변 주차장 있음 · 가장 가까운 곳 약 {d}m",map:"지도에서 주차장 찾기 ↗",src:"주차장: 공식 안내 기준(2026년 11월), 주변 주차장 위치 © OpenStreetMap contributors · 행사·성수기에는 만차·이용 제한이 있을 수 있어요."},
 en:{o:"On-site parking",n:"No on-site parking · use nearby paid lots",m:"Use nearby public / partner parking",cap:"approx. {c} spaces",free:"free",paid:"paid",r:"¥{y} / {m} min",v:"¥{y} per visit",d:"max ¥{y}/day",osm:"Parking nearby · nearest approx. {d} m",map:"Find parking on the map ↗",src:"Parking: based on official info (Nov 2026); nearby lots © OpenStreetMap contributors · Lots can fill up or close during events and peak season."},
 ja:{o:"専用駐車場あり",n:"専用駐車場なし・周辺の有料駐車場を利用",m:"近くの公営・提携駐車場を利用",cap:"約{c}台",free:"無料",paid:"有料",r:"{m}分{y}円",v:"1回{y}円",d:"1日最大{y}円",osm:"周辺に駐車場あり・最寄り約{d}m",map:"地図で駐車場を探す ↗",src:"駐車場：公式案内に基づく（2026年11月）、周辺駐車場の位置 © OpenStreetMap contributors・行事や繁忙期は満車・利用制限の場合があります。"},
 es:{o:"Aparcamiento propio",n:"Sin aparcamiento propio · usa los de pago cercanos",m:"Usa aparcamientos públicos o concertados cercanos",cap:"aprox. {c} plazas",free:"gratis",paid:"de pago",r:"{y} ¥ / {m} min",v:"{y} ¥ por visita",d:"máx. {y} ¥/día",osm:"Aparcamientos cerca · el más cercano a unos {d} m",map:"Buscar aparcamiento en el mapa ↗",src:"Aparcamiento: información oficial (nov. 2026); ubicaciones cercanas © OpenStreetMap contributors · En eventos y temporada alta puede llenarse o cerrarse."},
 fr:{o:"Parking sur place",n:"Pas de parking sur place · parkings payants à proximité",m:"Parkings publics ou partenaires à proximité",cap:"env. {c} places",free:"gratuit",paid:"payant",r:"{y} ¥ / {m} min",v:"{y} ¥ par visite",d:"max {y} ¥/jour",osm:"Parkings à proximité · le plus proche à env. {d} m",map:"Trouver un parking sur la carte ↗",src:"Parking : informations officielles (nov. 2026) ; parkings à proximité © OpenStreetMap contributors · Complet ou fermé possible lors des événements et en haute saison."},
 zh:{o:"有专用停车场",n:"无专用停车场・请使用周边收费停车场",m:"请使用附近的公营・合作停车场",cap:"约{c}个车位",free:"免费",paid:"收费",r:"{m}分钟{y}日元",v:"每次{y}日元",d:"每天最高{y}日元",osm:"周边有停车场・最近约{d}米",map:"在地图上查找停车场 ↗",src:"停车场：根据官方信息（2026年11月），周边停车场位置 © OpenStreetMap contributors・活动和旺季时可能满位或限制使用。"},
 tw:{o:"有專用停車場",n:"無專用停車場・請使用周邊收費停車場",m:"請使用附近的公營・合作停車場",cap:"約{c}個車位",free:"免費",paid:"收費",r:"{m}分鐘{y}日圓",v:"每次{y}日圓",d:"每天最高{y}日圓",osm:"周邊有停車場・最近約{d}公尺",map:"在地圖上尋找停車場 ↗",src:"停車場：根據官方資訊（2026年11月），周邊停車場位置 © OpenStreetMap contributors・活動和旺季時可能客滿或限制使用。"},
 th:{o:"มีที่จอดรถของสถานที่",n:"ไม่มีที่จอดรถของสถานที่ · ใช้ที่จอดแบบเสียเงินใกล้เคียง",m:"ใช้ที่จอดรถสาธารณะหรือที่จอดพันธมิตรใกล้เคียง",cap:"ประมาณ {c} คัน",free:"ฟรี",paid:"เสียเงิน",r:"{y} เยน / {m} นาที",v:"ครั้งละ {y} เยน",d:"สูงสุด {y} เยน/วัน",osm:"มีที่จอดรถใกล้เคียง · ใกล้สุดประมาณ {d} ม.",map:"หาที่จอดรถบนแผนที่ ↗",src:"ที่จอดรถ: อ้างอิงข้อมูลทางการ (พ.ย. 2026) ตำแหน่งที่จอดใกล้เคียง © OpenStreetMap contributors · ช่วงเทศกาลและฤดูท่องเที่ยวอาจเต็มหรือปิดใช้"}
};
function parkRow(it){
  if(it.type!=="spot" && it.type!=="shop") return "";
  const l=(window.I18N&&window.I18N.lang)||"ko", T=PARK_T[l]||PARK_T.ko, n=x=>Number(x).toLocaleString("en-US");
  const p=PARK[it.id], o=PARK_OSM[it.id], g=(window.GEO||{})[it.id];
  let main="", sub=[];
  if(p){
    main=T[p.t];
    if(p.c) sub.push(T.cap.replace("{c}",n(p.c)));
    if(p.f) sub.push(T[p.f==="f"?"free":"paid"]);
    if(p.r) sub.push(T.r.replace("{m}",p.r[0]).replace("{y}",n(p.r[1])));
    if(p.v) sub.push(T.v.replace("{y}",n(p.v)));
    if(p.d) sub.push(T.d.replace("{y}",n(p.d)));
  } else if(o){ main=T.osm.replace("{d}",o[0]); }
  else return "";
  const mapU = g ? `https://www.google.com/maps/search/${encodeURIComponent("駐車場")}/@${g[0]},${g[1]},16z` : "https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(it.jp+" 駐車場");
  return `<dt>주차장</dt><dd class="si pk"><span>${esc(main)}</span>${sub.length?`<span>${esc(sub.join(" · "))}</span>`:""}<a class="pkmap" href="${mapU}" target="_blank" rel="noopener">${esc(T.map)}</a></dd>`;
}
function parkSrc(it){ if(!(PARK[it.id]||PARK_OSM[it.id])||(it.type!=="spot"&&it.type!=="shop")) return ""; const l=(window.I18N&&window.I18N.lang)||"ko"; return `<p class="sisrc pksrc">${esc((PARK_T[l]||PARK_T.ko).src)}</p>`; }
/*PARK_END*/'''

CSS = '/*PARKCSS_BEGIN*/.facts dd.pk .pkmap{font-size:12px;color:var(--ai,#2563eb);text-decoration:none;margin-top:2px;align-self:flex-start}.facts dd.pk .pkmap:hover{text-decoration:underline}.pksrc{margin-top:2px}/*PARKCSS_END*/'

RULES = [
 ('.join(""):""}</dl>\n   ${si?`${si.note?', '.join(""):""}${typeof parkRow==="function"?parkRow(it):""}</dl>\n   ${si?`${si.note?'),
 ('${typeof shopNote==="function"?shopNote(it):""}', '${typeof shopNote==="function"?shopNote(it):""}${typeof parkSrc==="function"?parkSrc(it):""}'),
]

def block(s, b, e, new, anchor):
    if b in s:
        i = s.index(b); j = s.index(e, i) + len(e); return s[:i] + new + s[j:]
    assert s.count(anchor) == 1, anchor[:40]
    return s.replace(anchor, new + '\n' + anchor)

for fn in FILES:
    s = open(fn, encoding='utf-8').read()
    for old, new in RULES:
        if new in s: continue
        assert s.count(old) == 1, (fn, old[:50], s.count(old))
        s = s.replace(old, new)
    s = block(s, '/*PARK_BEGIN*/', '/*PARK_END*/', BLOCK, 'function pageMeta(){')
    s = block(s, '/*PARKCSS_BEGIN*/', '/*PARKCSS_END*/', CSS, '.facts dd.si.warn{')
    open(fn, 'w', encoding='utf-8').write(s)
    print('ok', fn, 'curated', len(cur), 'osm', len(PO))
