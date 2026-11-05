# 숙소 페이지(stay/, <도시>/stay/) 추가. html·backup pre에 같이 적용 (여러 번 돌려도 안전). 화면 코드는 sitegen/stay_view.js
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s2tw import s2tw
from patch_weather import block
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
VIEW = open(f'{W}/sitegen/stay_view.js', encoding='utf-8').read().strip()
CSS = """/*STCSS_BEGIN*/
body.is-wx .hero{display:none}
.stgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.stsec{margin-top:30px}.stsec .sgh{margin-top:0}.stsub{color:var(--ink-2);margin:0 0 12px;line-height:1.6}.stho{margin:12px 0 0}.stmore{margin:10px 0 0}
.starea dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:6px 12px}.starea dt{font-size:13px;font-weight:700;color:var(--ink-2)}.starea dd{margin:0;line-height:1.6}
.hgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.hcard{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px 18px;display:flex;flex-direction:column;gap:8px}
.hcard h3{margin:0;font-family:var(--f-display);font-size:19px;line-height:1.35}.hja{margin:0;font-size:13px;color:var(--ink-2)}
.harea{display:inline-block;padding:3px 10px;border-radius:999px;background:var(--ai-soft);color:var(--ai);font-size:12px;font-weight:700}
.hst{margin:0;font-size:14px;font-weight:600}.hcard .gul li{font-size:14px}
.hbtn{margin-top:auto;justify-content:center;background:var(--shu);border-color:var(--shu);color:#fff}
/*STCSS_END*/
"""
SM = {
 'ko': {"i": ["일본 숙소 추천 – 지역별 묵기 좋은 동네와 예약 방법", "도쿄·오사카·교토·후쿠오카·삿포로·오키나와·나고야에서 묵기 좋은 동네와 추천 숙소, 예약 사이트 고르는 법과 숙박세·취소 기한 등 예약 전에 확인할 점을 정리했어요."],
        "c": ["{a} 숙소 추천 – 묵기 좋은 동네·추천 호텔·예약 팁", "{a}에서 묵기 좋은 동네({list})의 장단점과 추천 숙소, 예약할 때 확인할 점을 정리했어요."]},
 'en': {"i": ["Where to Stay in Japan – Best Areas by Region and How to Book", "The best neighborhoods and hotel picks in Tokyo, Osaka, Kyoto, Fukuoka, Sapporo, Okinawa and Nagoya, plus how to choose a booking site and what to check before you book (accommodation tax, cancellation deadlines and more)."],
        "c": ["Where to Stay in {a} – Best Areas, Hotel Picks & Booking Tips", "Pros and cons of the best areas to stay in {a} ({list}), hotel picks and what to check before booking."]},
 'ja': {"i": ["日本の宿泊エリアガイド – 地域別のおすすめエリアと予約のコツ", "東京・大阪・京都・福岡・札幌・沖縄・名古屋の泊まりやすいエリアと、予約サイトの選び方、宿泊税やキャンセル期限など予約前の確認ポイント。"],
        "c": ["{a}の宿泊エリアガイド – 泊まりやすいエリアと予約のコツ", "{a}で泊まりやすいエリア（{list}）の長所・短所と、予約前に確認したいポイント。"]},
 'es': {"i": ["Dónde alojarse en Japón – Mejores zonas por región y cómo reservar", "Los mejores barrios para alojarse en Tokio, Osaka, Kioto, Fukuoka, Sapporo, Okinawa y Nagoya, cómo elegir web de reservas y qué revisar antes de reservar (impuesto de alojamiento, plazos de cancelación y más)."],
        "c": ["Dónde alojarse en {a} – Mejores zonas y consejos para reservar", "Ventajas e inconvenientes de las mejores zonas para alojarse en {a} ({list}) y qué revisar antes de reservar."]},
 'fr': {"i": ["Où loger au Japon – Meilleurs quartiers par région et conseils de réservation", "Les meilleurs quartiers où loger à Tokyo, Osaka, Kyoto, Fukuoka, Sapporo, Okinawa et Nagoya, comment choisir un site de réservation et quoi vérifier avant de réserver (taxe de séjour, délais d'annulation, etc.)."],
        "c": ["Où loger à {a} – Meilleurs quartiers et conseils de réservation", "Avantages et inconvénients des meilleurs quartiers où loger à {a} ({list}) et quoi vérifier avant de réserver."]},
 'zh': {"i": ["日本住宿指南 – 各地区推荐住宿区域与预订方法", "整理东京、大阪、京都、福冈、札幌、冲绳、名古屋适合住宿的区域，以及预订网站的选择方法和住宿税、取消期限等预订前须知。"],
        "c": ["{a}住宿指南 – 推荐住宿区域与预订技巧", "{a}适合住宿的区域（{list}）的优缺点，以及预订前需要确认的事项。"]},
 'th': {"i": ["พักที่ไหนดีในญี่ปุ่น – ย่านที่พักแนะนำแต่ละภูมิภาคและวิธีจอง", "ย่านที่พักแนะนำในโตเกียว โอซาก้า เกียวโต ฟุกุโอกะ ซัปโปโร โอกินาว่า และนาโกย่า พร้อมวิธีเลือกเว็บจองและสิ่งที่ควรเช็กก่อนจอง เช่น ภาษีที่พักและกำหนดยกเลิกฟรี"],
        "c": ["พักที่ไหนดีใน{a} – ย่านที่พักแนะนำและเคล็ดลับการจอง", "ข้อดีข้อเสียของย่านที่พักแนะนำใน{a} ({list}) และสิ่งที่ควรเช็กก่อนจอง"]},
}
SM['tw'] = {k: [s2tw(x) for x in v] for k, v in SM['zh'].items()}
META_JS = """/*STMETA_BEGIN*/
function stayMeta(L,T){
  const M=(""" + json.dumps(SM, ensure_ascii=False, separators=(',', ':')) + """)[L]||""" + json.dumps(SM['ko'], ensure_ascii=False, separators=(',', ':')) + """;
  const c=STAY_CITIES.includes(st.city)?st.city:"", sep=(L==="ja"||L==="zh"||L==="tw")?"、":", ";
  const f=(s,o)=>s.replace(/\\{(\\w+)\\}/g,(_,k)=>o[k]!=null?o[k]:"");
  if(!c) return {title:M.i[0]+" | Go Nihon Trip", desc:M.i[1]};
  const o={a:T(CITIES[c].ko), list:stayAreas(c).opts.map(x=>T(x.name)).join(sep)};
  return {title:f(M.c[0],o)+" | Go Nihon Trip", desc:f(M.c[1],o)};
}
/*STMETA_END*/
"""
NAV = ('<a href="#stay" data-view="stay"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
       '<path d="M3 18V7M3 14h18v4M21 14v-2.5A2.5 2.5 0 0 0 18.5 9H11v5"/><circle cx="7" cy="11" r="1.8"/></svg><span>숙소</span></a>\n      ')
MTAB = ('<a href="#stay" data-view="stay"><i><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M3 18V7M3 14h18v4M21 14v-2.5A2.5 2.5 0 0 0 18.5 9H11v5"/><circle cx="7" cy="11" r="1.8"/></svg></i>숙소</a>\n')
R = [
 ('"weather","airport"];\nconst INFO_VIEWS', '"weather","airport","stay"];\nconst INFO_VIEWS'),
 ('  if(s.view==="saved") return "saved/";', '  if(s.view==="stay") return STAY_CITIES.includes(s.city) ? `${s.city}/stay/` : "stay/";\n  if(s.view==="saved") return "saved/";'),
 ('  if(seg[0]==="guide"){', '  if(seg[0]==="stay"){ st.view="stay"; st.city="all"; return; }\n  if(CITIES[seg[0]]&&seg[1]==="stay"){ st.view="stay"; st.city=seg[0]; return; }\n  if(seg[0]==="guide"){'),
 ('document.body.classList.toggle("is-wx", st.view==="weather"||st.view==="airport");', 'document.body.classList.toggle("is-wx", st.view==="weather"||st.view==="airport"||st.view==="stay");'),
 ('  if(st.view==="airport") return apMeta(L,T);', '  if(st.view==="airport") return apMeta(L,T);\n  if(st.view==="stay") return stayMeta(L,T);'),
 ('  const gs = e.target.closest("[data-gsec]");', '  const stl = e.target.closest("[data-stayc]"); if(stl){ e.preventDefault(); st.view="stay"; st.city=stl.dataset.stayc; render(); window.scrollTo({top:0}); return; }\n  const gs = e.target.closest("[data-gsec]");'),
 ('<a href="#guide" data-view="guide"><svg', NAV + '<a href="#guide" data-view="guide"><svg'),
 ('  <a href="#guide" data-view="guide"><i>', MTAB + '  <a href="#guide" data-view="guide"><i>'),
 ('const GKEYS = GUIDE.secs.map(s=>s.key);', 'const GKEYS = GUIDE.secs.filter(s=>s.key!=="stay").map(s=>s.key);   // 숙소는 숙소 페이지(stay/)로 옮김'),
 ('  const tabs = GUIDE.secs.map(s=>', '  const tabs = GUIDE.secs.filter(s=>s.key!=="stay").map(s=>'),
 ('GUIDE.secs.filter(s=>s.key!==sec.key).map(s=>`<a href="${gsecHref(s.key)}"', 'GUIDE.secs.filter(s=>s.key!==sec.key&&s.key!=="stay").map(s=>`<a href="${gsecHref(s.key)}"'),
 ('  if(seg[0]==="guide"){', '  if(seg[0]==="guide"&&seg[1]==="stay"){ st.view="stay"; st.city="all"; return; }\n  if(seg[0]==="guide"){'),
 ('grid-template-columns:repeat(10,minmax(0,1fr))}', 'grid-template-columns:repeat(11,minmax(0,1fr))}'),
]
def patch(s):
    s = s.replace('${sec.key==="stay"&&typeof stayGuideBlocks==="function"?stayGuideBlocks(sec,blocks):blocks.map(gBlock).join("")}', '${blocks.map(gBlock).join("")}')
    s = block(s, '/*STCSS_BEGIN*/', '/*STCSS_END*/', CSS, 'footer{border-top:1px solid var(--line);')
    s = block(s, '/*STAY_BEGIN*/', '/*STAY_END*/', VIEW, 'V.place = function(){')
    s = block(s, '/*STMETA_BEGIN*/', '/*STMETA_END*/', META_JS, 'function setMeta(sel,val)')
    for a, b in R:
        if b in s: continue
        add = b.replace(a, '', 1).strip() if a in b else ''
        if add and add.split('\n')[0][:60] in s: continue
        if s.count(a) == 0: continue
        assert s.count(a) == 1, (a[:60], s.count(a))
        s = s.replace(a, b)
    return s
if __name__ == '__main__':
    for f in FILES:
        s = patch(open(f, encoding='utf-8').read())
        open(f, 'w', encoding='utf-8').write(s); print('patched', f)
