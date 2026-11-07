# 술 여행 페이지(drink/, <도시>/drink/) 추가. html·backup pre에 같이 적용 (여러 번 돌려도 안전). 화면 코드·데이터는 sitegen/drink_view.js
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s2tw import s2tw
from patch_weather import block
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
VIEW = open(f'{W}/sitegen/drink_view.js', encoding='utf-8').read().strip()
CSS = """/*DRCSS_BEGIN*/
.dtypes{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-bottom:12px}.dtypes p{margin:0;line-height:1.6}
.dgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.dcard{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px 18px;display:flex;flex-direction:column;gap:8px}
.dcard h3{margin:0;font-family:var(--f-display);font-size:19px;line-height:1.35}.dcard .dd{margin:0;line-height:1.65}
.dcard dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:5px 12px;font-size:14px}.dcard dt{color:var(--ink-2);font-weight:700;white-space:nowrap}.dcard dd{margin:0}
.dcard .more{margin-top:auto}.dtop{display:flex;gap:6px;flex-wrap:wrap}
.dkind{display:inline-block;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:700;color:#fff;background:var(--ink-2)}
.dk-shochu{background:#6b5b95}.dk-umeshu{background:#b5536b}.dk-wine{background:#7a2e45}.dk-liqueur{background:#c2701a}
.dbuyl{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:8px 0 0;font-size:14px}.dbuyl b{margin-right:4px}.dbuyl span{background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:3px 10px}
.dk-sake{background:#3d6f8e}.dk-beer{background:#c08a1e}.dk-whisky{background:#8a4b2a}.dk-awamori{background:#2f7d6b}
.dlist{display:flex;flex-direction:column;gap:6px}.dmini{display:flex;align-items:center;gap:8px;flex-wrap:wrap;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:10px 12px}
.dmini b{font-size:15px}.dmini small{color:var(--ink-2);font-size:13px}
/*DRCSS_END*/
"""
DM = {
 'ko': {"i": ["일본 술 여행 – 지역별 사케·맥주·위스키 양조장 견학 가이드", "일본 사케·소주·아와모리·맥주·위스키 종류와 라벨 읽는 법, 도쿄·오사카·교토·후쿠오카·홋카이도·오키나와 등 지역별로 견학·시음할 수 있는 양조장과 증류소, 한국에 술을 가져올 때 면세 규칙까지 정리했어요."],
        "c": ["{a} 술 여행 – 사케·맥주·위스키 양조장 견학과 시음", "{a}에서 견학·시음할 수 있는 곳({list})의 요금·예약·가는 길을 2026년 11월 공식 정보로 정리했어요."]},
 'en': {"i": ["Japan Sake, Beer & Whisky Guide – Breweries and Distilleries to Visit by Region", "Types of Japanese alcohol and how to read sake labels, breweries and distilleries you can tour in Tokyo, Osaka, Kyoto, Fukuoka, Hokkaido, Okinawa and more, plus rules for flying home with alcohol."],
        "c": ["{a} Sake, Beer & Whisky – Brewery and Distillery Tours", "Fees, booking and access for places you can tour and taste in {a} ({list}), checked against official sites in November 2026."]},
 'ja': {"i": ["日本のお酒旅 – 地域別の酒蔵・ビール工場・蒸溜所見学ガイド", "日本酒・焼酎・泡盛・ビール・ウイスキーの種類とラベルの読み方、東京・大阪・京都・福岡・北海道・沖縄などで見学・試飲できる酒蔵や蒸溜所、お酒の持ち帰りルールまで。"],
        "c": ["{a}のお酒旅 – 酒蔵・ビール工場・蒸溜所の見学と試飲", "{a}で見学・試飲できる場所（{list}）の料金・予約・アクセスを2026年11月の公式情報でまとめました。"]},
 'es': {"i": ["Guía de sake, cerveza y whisky en Japón – Fábricas y destilerías para visitar por región", "Tipos de alcohol japonés y cómo leer las etiquetas de sake, fábricas y destilerías que se pueden visitar en Tokio, Osaka, Kioto, Fukuoka, Hokkaido, Okinawa y más, y normas para llevar alcohol en el avión."],
        "c": ["Sake, cerveza y whisky en {a} – Visitas a fábricas y destilerías", "Precios, reservas y cómo llegar a los lugares de visita y degustación en {a} ({list}), según las webs oficiales en noviembre de 2026."]},
 'fr': {"i": ["Guide du saké, de la bière et du whisky au Japon – Brasseries et distilleries à visiter par région", "Les types d'alcool japonais et comment lire une étiquette de saké, les brasseries et distilleries à visiter à Tokyo, Osaka, Kyoto, Fukuoka, Hokkaido, Okinawa et ailleurs, et les règles pour rapporter de l'alcool en avion."],
        "c": ["Saké, bière et whisky à {a} – Visites de brasseries et distilleries", "Tarifs, réservations et accès des lieux de visite et de dégustation à {a} ({list}), d'après les sites officiels en novembre 2026."]},
 'zh': {"i": ["日本酒类之旅 – 各地区酒藏·啤酒厂·威士忌蒸馏所参观指南", "介绍日本清酒、烧酒、泡盛、啤酒、威士忌的种类和清酒酒标的看法，东京、大阪、京都、福冈、北海道、冲绳等地可参观试饮的酒藏和蒸馏所，以及带酒回国的规定。"],
        "c": ["{a}酒类之旅 – 酒藏·啤酒厂·蒸馏所参观与试饮", "整理了{a}可参观试饮的地方（{list}）的费用、预约和交通，依据2026年11月官网信息。"]},
 'th': {"i": ["เที่ยวสายเหล้าญี่ปุ่น – โรงสาเก โรงเบียร์ และโรงกลั่นวิสกี้แยกตามภูมิภาค", "ประเภทเหล้าญี่ปุ่นและวิธีอ่านฉลากสาเก โรงสาเกและโรงกลั่นที่เข้าชมและชิมได้ในโตเกียว โอซาก้า เกียวโต ฟุกุโอกะ ฮอกไกโด โอกินาว่า และที่อื่น ๆ พร้อมกฎการนำเหล้าขึ้นเครื่อง"],
        "c": ["เที่ยวสายเหล้าใน{a} – ทัวร์โรงสาเก โรงเบียร์ และโรงกลั่น", "ค่าเข้าชม การจอง และการเดินทางของสถานที่เข้าชมและชิมใน{a} ({list}) อ้างอิงเว็บไซต์ทางการ ณ พฤศจิกายน 2026"]},
}
DM['tw'] = {k: [s2tw(x) for x in v] for k, v in DM['zh'].items()}
META_JS = """/*DRMETA_BEGIN*/
function drinkMeta(L,T){
  const M=(""" + json.dumps(DM, ensure_ascii=False, separators=(',', ':')) + """)[L]||""" + json.dumps(DM['ko'], ensure_ascii=False, separators=(',', ':')) + """;
  const c=DRINK_CITIES.includes(st.city)?st.city:"", sep=(L==="ja"||L==="zh"||L==="tw")?"、":", ";
  const f=(s,o)=>s.replace(/\\{(\\w+)\\}/g,(_,k)=>o[k]!=null?o[k]:"");
  if(!c) return {title:M.i[0]+" | Go Nihon Trip", desc:M.i[1]};
  const o={a:T(CITIES[c].ko), list:DRINKS.filter(v=>v.city===c).map(v=>T(v.n)).join(sep)};
  return {title:f(M.c[0],o)+" | Go Nihon Trip", desc:f(M.c[1],o)};
}
/*DRMETA_END*/
"""
ICON = '<path d="M7 3h10l-1.2 6.5a3.9 3.9 0 0 1-7.6 0z"/><path d="M12 13.5V20M8.5 20.5h7"/>'
NAV = ('<a href="#drink" data-view="drink"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
       + ICON + '</svg><span>술</span></a>\n      ')
MTAB = ('<a href="#drink" data-view="drink"><i><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
        + ICON + '</svg></i>술</a>\n')
R = [
 ('"weather","airport","stay"];\nconst INFO_VIEWS', '"weather","airport","stay","drink"];\nconst INFO_VIEWS'),
 ('  if(s.view==="stay") return', '  if(s.view==="drink") return DRINK_CITIES.includes(s.city) ? `${s.city}/drink/` : "drink/";\n  if(s.view==="stay") return'),
 ('  if(seg[0]==="stay"){', '  if(seg[0]==="drink"){ st.view="drink"; st.city="all"; return; }\n  if(CITIES[seg[0]]&&seg[1]==="drink"){ st.view="drink"; st.city=seg[0]; return; }\n  if(seg[0]==="stay"){'),
 ('||st.view==="stay");', '||st.view==="stay"||st.view==="drink");'),
 ('  if(st.view==="stay") return stayMeta(L,T);', '  if(st.view==="stay") return stayMeta(L,T);\n  if(st.view==="drink") return drinkMeta(L,T);'),
 ('  const stl = e.target.closest("[data-stayc]"); if(stl){', '  const drl = e.target.closest("[data-drc]"); if(drl){ e.preventDefault(); st.view="drink"; st.city=drl.dataset.drc; render(); window.scrollTo({top:0}); return; }\n  const stl = e.target.closest("[data-stayc]"); if(stl){'),
 ('<a href="#guide" data-view="guide"><svg', NAV + '<a href="#guide" data-view="guide"><svg'),
 ('  <a href="#guide" data-view="guide"><i>', MTAB + '  <a href="#guide" data-view="guide"><i>'),
]
def patch(s):
    s = block(s, '/*DRCSS_BEGIN*/', '/*DRCSS_END*/', CSS, 'footer{border-top:1px solid var(--line);')
    s = block(s, '/*DRINK_BEGIN*/', '/*DRINK_END*/', VIEW, 'V.place = function(){')
    s = block(s, '/*DRMETA_BEGIN*/', '/*DRMETA_END*/', META_JS, 'function setMeta(sel,val)')
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (a[:60], s.count(a))
        s = s.replace(a, b)
    return s
if __name__ == '__main__':
    for f in FILES:
        s = patch(open(f, encoding='utf-8').read())
        open(f, 'w', encoding='utf-8').write(s); print('patched', f)
