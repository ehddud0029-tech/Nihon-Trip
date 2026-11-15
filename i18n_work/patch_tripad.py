# Trip.com 호텔 제휴 링크 광고 칸 (2026-11-15)
# 도시 숙소 '추천 숙소' 탭, 숙소 전체 '추천 숙소' 탭, 숙소 동네 페이지에 넣어요. 한국어·영어에서만(stayShowHotels).
# sitegen/stay_view.js를 고치고, 그 STAY 블록을 html·backup pre에 그대로 옮겨요. 여러 번 돌려도 안전.
W = '/home/claude'
VIEW = f'{W}/sitegen/stay_view.js'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']

TRIP = r'''/*TRIPAD_BEGIN*/
/* Trip.com 호텔 제휴 링크 (2026-11-15, 사용자 제공). 도시 키 → [이름, 주소] */
const TRIP_LINKS = {
 tokyo:[["도쿄","https://www.trip.com/t/30BKzQBdAX2"]],
 osaka:[["오사카","https://www.trip.com/t/VfjGSLDdAX2"],["교토","https://www.trip.com/t/jVdM5pDdAX2"]],
 nagoya:[["나고야","https://www.trip.com/t/SLSPyREdAX2"]],
 hokkaido:[["삿포로","https://www.trip.com/t/nk7WKaFdAX2"]],
 fukuoka:[["후쿠오카","https://www.trip.com/t/frLQ2FGdAX2"]]
};
/* 동네 페이지: 동네 키 → 보여 줄 링크 이름 (없으면 도시 첫 링크, null이면 안 보임) */
const TRIP_NB = {kyotoeki:"교토",kawaramachi:"교토",namba:"오사카",umeda:"오사카",tennoji:"오사카",hakodate:null,takayama:null};
function tripBox(list){
  if(!list || !list.length || !stayShowHotels()) return "";
  return `<aside class="tripad"><div class="tpt"><span class="tptag">광고</span><b>Trip.com</b></div>
   <p class="tpd">날짜를 고르면 여러 호텔 요금을 한 번에 비교할 수 있어요.</p>
   <div class="tpbs">${list.map(([n,u])=>`<a class="btn tpbtn" href="${u}" target="_blank" rel="sponsored noopener">Trip.com에서 ${esc(n)} 호텔 보기 ↗</a>`).join("")}</div></aside>`;
}
const tripCity = c => TRIP_LINKS[c] || [];
const tripNb = (c,k) => { if(k in TRIP_NB){ const n=TRIP_NB[k]; return n ? tripCity(c).filter(x=>x[0]===n) : []; } return tripCity(c).slice(0,1); };
const tripAll = () => STAY_CITIES.flatMap(k=>tripCity(k));
/* Trip.com 할인 예약 링크 (2026-11-15, 사용자 제공, 한국어 원화 페이지라 한국어에서만): 숙소 '예약 방법' 맨 위 */
const TRIP_DEAL = "https://kr.trip.com/sale/w/27435/holidaydeals2025.html?locale=ko-kr&curr=krw&transparentBar=1&Allianceid=11318805&SID=335739587&trip_sub1=&trip_sub3=P21198942";
function tripDeal(){
  if(((window.I18N&&window.I18N.lang)||"ko")!=="ko") return "";
  return `<aside class="tripad tpdeal"><div class="tpt"><span class="tptag">광고</span><b>Trip.com</b><span class="tpdt">할인 예약</span></div>
   <p class="tpd">Trip.com 할인 페이지에서 숙소를 할인된 요금으로 예약할 수 있어요. 할인 조건과 기간은 페이지에서 확인하세요.</p>
   <div class="tpbs"><a class="btn tpbtn" href="${TRIP_DEAL}" target="_blank" rel="sponsored noopener">할인 받고 예약하기 ↗</a></div></aside>${STAY_AD}`;
}
/*TRIPAD_END*/'''

RULES = [
  # 숙소 전체 '추천 숙소' 탭: 맨 위에 도시별 Trip.com 버튼
  ('if(t==="hotels") body = `${STAY_CITIES.map(k=>{',
   'if(t==="hotels") body = `${tripBox(tripAll())}${STAY_CITIES.map(k=>{'),
  # 도시 '추천 숙소' 탭: 호텔 카드 아래
  ('if(t==="hotels") body = `${hs.length?`<div class="hgrid">${hs.map(hotelCard).join("")}</div>${STAY_AD}`:`<p class="stsub">추천 숙소를 준비하고 있어요.</p>`}`;',
   'if(t==="hotels") body = `${hs.length?`<div class="hgrid">${hs.map(hotelCard).join("")}</div>`:(tripCity(c).length?"":`<p class="stsub">추천 숙소를 준비하고 있어요.</p>`)}${tripBox(tripCity(c))}${hs.length||tripCity(c).length?STAY_AD:""}`;'),
  # 동네 페이지 '추천 숙소'
  ('const booking = `<section id="booking">${stayList("예약 사이트 고르기", STAY_SITES)}',
   'const booking = `<section id="booking">${tripDeal()}${stayList("예약 사이트 고르기", STAY_SITES)}'),
 ('${hs.length?`<section class="stsec"><h3 class="sgh"><span>추천 숙소</span></h3><div class="hgrid">${hs.map(hotelCard).join("")}</div>${STAY_AD}</section>`:""}',
   '${hs.length||tripBox(tripNb(c,o.key))?`<section class="stsec"><h3 class="sgh"><span>추천 숙소</span></h3>${hs.length?`<div class="hgrid">${hs.map(hotelCard).join("")}</div>`:""}${tripBox(tripNb(c,o.key))}${STAY_AD}</section>`:""}'),
]

CSS = ('/*TRIPCSS*/.tripad{margin:16px 0 0;background:var(--surface);border:1px solid var(--line);border-left:4px solid #287DFA;border-radius:var(--r);padding:14px 16px}'
       '.tpt{display:flex;align-items:center;gap:8px}.tpt b{font-size:17px;color:#287DFA}.tpdt{font-weight:700;font-size:15px}.tpdeal{margin:0 0 6px}.tpdeal+.sisrc{margin:0 0 14px}'
       '.tptag{font-size:11px;font-weight:700;color:var(--ink-2);border:1px solid var(--line);border-radius:4px;padding:1px 6px}'
       '.tpd{margin:6px 0 10px;color:var(--ink-2);font-size:14px;line-height:1.6}'
       '.tpbs{display:flex;flex-wrap:wrap;gap:8px}.tpbtn{margin:0;background:#287DFA;border-color:#287DFA;color:#fff;white-space:nowrap}'
       '@media (max-width:599px){.tpbtn{width:100%;justify-content:center}}/*TRIPCSS_END*/')

v = open(VIEW, encoding='utf-8').read()
if '/*TRIPAD_BEGIN*/' in v:
    i = v.index('/*TRIPAD_BEGIN*/'); j = v.index('/*TRIPAD_END*/') + len('/*TRIPAD_END*/')
    v = v[:i] + TRIP + v[j:]
else:
    a = 'function hotelCard(h){'
    assert v.count(a) == 1
    v = v.replace(a, TRIP + '\n' + a)
for old, new in RULES:
    if new in v: continue
    assert v.count(old) == 1, old[:60]
    v = v.replace(old, new)
open(VIEW, 'w', encoding='utf-8').write(v)
blk = v.strip()

for fn in FILES:
    s = open(fn, encoding='utf-8').read()
    i = s.index('/*STAY_BEGIN*/'); j = s.index('/*STAY_END*/') + len('/*STAY_END*/')
    s = s[:i] + blk + s[j:]
    if '/*TRIPCSS*/' in s:
        i = s.index('/*TRIPCSS*/'); j = s.index('/*TRIPCSS_END*/') + len('/*TRIPCSS_END*/')
        s = s[:i] + CSS + s[j:]
    else:
        a = '.hcard{background:var(--surface)'
        assert s.count(a) == 1
        s = s.replace(a, CSS + '\n' + a)
    open(fn, 'w', encoding='utf-8').write(s)
    print('ok', fn)

# 번역 (5칸: 한·영·일·스·프), 간체·태국어
TR = [
 ("광고", "Ad", "広告", "Anuncio", "Publicité", "广告", "โฆษณา"),
 ("날짜를 고르면 여러 호텔 요금을 한 번에 비교할 수 있어요.", "Pick your dates to compare hotel prices in one place.", "日付を選ぶと、ホテルの料金をまとめて比較できます。",
  "Elige tus fechas para comparar precios de hoteles en un solo lugar.", "Choisissez vos dates pour comparer les prix des hôtels en un seul endroit.",
  "选择日期即可一次比较多家酒店的价格。", "เลือกวันที่เพื่อเปรียบเทียบราคาโรงแรมได้ในที่เดียว"),
]
CITY = [("도쿄","Tokyo","東京","Tokio","Tokyo","东京","โตเกียว"),("오사카","Osaka","大阪","Osaka","Osaka","大阪","โอซาก้า"),("교토","Kyoto","京都","Kioto","Kyoto","京都","เกียวโต"),
        ("나고야","Nagoya","名古屋","Nagoya","Nagoya","名古屋","นาโกย่า"),("삿포로","Sapporo","札幌","Sapporo","Sapporo","札幌","ซัปโปโร"),("후쿠오카","Fukuoka","福岡","Fukuoka","Fukuoka","福冈","ฟุกุโอกะ")]
for c in CITY:
    TR.append((f"Trip.com에서 {c[0]} 호텔 보기 ↗", f"See {c[1]} hotels on Trip.com ↗", f"Trip.comで{c[2]}のホテルを見る ↗", f"Ver hoteles en {c[3]} en Trip.com ↗",
               f"Voir les hôtels à {c[4]} sur Trip.com ↗", f"在Trip.com查看{c[5]}酒店 ↗", f"ดูโรงแรมใน{c[6]}บน Trip.com ↗"))
W2 = f'{W}/i18n_work'
open(f'{W2}/tr_63.tsv', 'w', encoding='utf-8').write(''.join('\t'.join(r[:5]) + '\n' for r in TR))
open(f'{W2}/zh_64.tsv', 'w', encoding='utf-8').write(''.join(f'{r[0]}\t{r[5]}\n' for r in TR))
open(f'{W2}/th_64.tsv', 'w', encoding='utf-8').write(''.join(f'{r[0]}\t{r[6]}\n' for r in TR))
print('tr', len(TR))
