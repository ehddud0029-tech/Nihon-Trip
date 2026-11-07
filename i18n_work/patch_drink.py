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
.dph{margin:-16px -18px 4px;position:relative;background:var(--line)}.dph img{display:block;width:100%;height:190px;object-fit:cover;border-radius:var(--r) var(--r) 0 0}.dph figcaption{position:absolute;right:6px;bottom:6px;background:rgba(0,0,0,.55);color:#fff;font-size:10.5px;padding:2px 7px;border-radius:999px;max-width:90%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.dph figcaption a{color:#fff}
.dtaste{margin:0;font-size:14px;color:var(--ink-2);font-style:italic}
.dtabs{display:flex;gap:6px;overflow-x:auto;margin:14px 0 4px;padding-bottom:2px;border-bottom:1px solid var(--line)}.dtabs a{flex:0 0 auto;padding:9px 14px;border-radius:10px 10px 0 0;text-decoration:none;color:var(--ink-2);font-weight:600;font-size:14.5px;border-bottom:3px solid transparent}.dtabs a.on{color:var(--ink);border-bottom-color:var(--accent,#c0392b)}
.dwhere{margin:0;display:grid;grid-template-columns:auto 1fr;gap:6px 14px}.dwhere dt{font-weight:700}.dwhere dd{margin:0}
.dart{display:flex;align-items:center;justify-content:center;height:190px;border-radius:var(--r) var(--r) 0 0}.dart svg{display:block}.dmap{margin-top:6px}
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
TABM = {
 'ko': {"buy": ["{a}에서 사 갈 만한 술 – 추천 사케·맥주·위스키와 가격대", "{a}에서 사 가면 좋은 술({list})의 맛과 가격대, 살 수 있는 곳을 정리했어요."],
        "tips": ["{a} 술 살 때 팁 – 고르는 법과 가지고 오는 규칙", "{a}에서 술을 고르는 법, 사케 라벨 읽는 법, 비행기에 싣는 규칙과 면세 한도를 정리했어요."],
        "shops": ["{a} 술 파는 곳 – 백화점·주류점·공항 면세점 안내", "{a}에서 술을 살 수 있는 곳: 백화점 지하, 주류 할인점, 편의점, 공항 면세점, 양조장 직매장과 추천 술별 구매처."]},
 'en': {"buy": ["What to Buy in {a} – Sake, Beer & Whisky with Prices", "Taste, price range and where to buy the best drinks to bring home from {a} ({list})."],
        "tips": ["Tips for Buying Alcohol in {a} – Choosing, Labels & Flying Home", "How to choose alcohol in {a}, read sake labels, and the rules for flying home with bottles."],
        "shops": ["Where to Buy Alcohol in {a} – Department Stores, Liquor Shops & Duty-Free", "Where to buy alcohol in {a}: department store food halls, liquor discount stores, convenience stores, airport duty-free and brewery shops."]},
 'ja': {"buy": ["{a}で買って帰りたいお酒 – おすすめの日本酒・ビール・ウイスキーと価格帯", "{a}で買って帰りたいお酒（{list}）の味と価格帯、買える場所をまとめました。"],
        "tips": ["{a}でお酒を買うときのコツ – 選び方と持ち帰りのルール", "{a}でのお酒の選び方、日本酒ラベルの読み方、飛行機での持ち帰りルールをまとめました。"],
        "shops": ["{a}でお酒が買える店 – 百貨店・酒店・空港免税店", "{a}でお酒が買える場所：デパ地下、酒のディスカウント店、コンビニ、空港の免税店、酒蔵の直売所とおすすめ酒の購入先。"]},
 'es': {"buy": ["Qué comprar en {a} – Sake, cerveza y whisky con precios", "Sabor, precio aproximado y dónde comprar las mejores bebidas para llevar de {a} ({list})."],
        "tips": ["Consejos para comprar alcohol en {a} – Elegir, etiquetas y viajar con botellas", "Cómo elegir alcohol en {a}, leer etiquetas de sake y normas para llevar botellas en el avión."],
        "shops": ["Dónde comprar alcohol en {a} – Grandes almacenes, licorerías y duty free", "Dónde comprar alcohol en {a}: zonas de alimentación de grandes almacenes, licorerías, tiendas de conveniencia, duty free del aeropuerto y tiendas de bodegas."]},
 'fr': {"buy": ["Quoi acheter à {a} – Saké, bière et whisky avec les prix", "Goût, prix indicatif et où acheter les meilleurs alcools à rapporter de {a} ({list})."],
        "tips": ["Conseils pour acheter de l'alcool à {a} – Choisir, étiquettes et retour en avion", "Comment choisir un alcool à {a}, lire une étiquette de saké et les règles pour rapporter des bouteilles en avion."],
        "shops": ["Où acheter de l'alcool à {a} – Grands magasins, cavistes et duty-free", "Où acheter de l'alcool à {a} : sous-sols alimentaires des grands magasins, cavistes discount, supérettes, duty-free de l'aéroport et boutiques des brasseries."]},
 'zh': {"buy": ["{a}值得买的酒 – 推荐清酒·啤酒·威士忌与价格区间", "整理了{a}值得买回去的酒（{list}）的口味、价格区间和购买地点。"],
        "tips": ["{a}买酒小贴士 – 挑选方法与带酒回国规定", "整理了在{a}挑选酒的方法、清酒酒标的看法，以及带酒上飞机的规定。"],
        "shops": ["{a}哪里买酒 – 百货店·酒类商店·机场免税店", "{a}可以买酒的地方：百货店地下食品馆、酒类折扣店、便利店、机场免税店、酒藏直营店以及推荐酒的购买地点。"]},
 'th': {"buy": ["เหล้าที่น่าซื้อใน{a} – สาเก เบียร์ วิสกี้แนะนำพร้อมช่วงราคา", "รวมรสชาติ ช่วงราคา และที่ซื้อของเหล้าที่น่าซื้อกลับจาก{a} ({list})"],
        "tips": ["เคล็ดลับซื้อเหล้าใน{a} – วิธีเลือกและกฎการนำกลับ", "วิธีเลือกเหล้าใน{a} วิธีอ่านฉลากสาเก และกฎการนำเหล้าขึ้นเครื่องบิน"],
        "shops": ["ซื้อเหล้าที่ไหนใน{a} – ห้างสรรพสินค้า ร้านเหล้า ดิวตี้ฟรี", "ที่ซื้อเหล้าใน{a}: ชั้นอาหารใต้ดินของห้าง ร้านเหล้าราคาถูก ร้านสะดวกซื้อ ดิวตี้ฟรีในสนามบิน และร้านของโรงสาเก"]},
}
for L, v in TABM.items(): DM[L].update(v)
DM['tw'] = {k: [s2tw(x) for x in v] for k, v in DM['zh'].items()}
META_JS = """/*DRMETA_BEGIN*/
function drinkMeta(L,T){
  const M=(""" + json.dumps(DM, ensure_ascii=False, separators=(',', ':')) + """)[L]||""" + json.dumps(DM['ko'], ensure_ascii=False, separators=(',', ':')) + """;
  const c=DRINK_CITIES.includes(st.city)?st.city:"", sep=(L==="ja"||L==="zh"||L==="tw")?"、":", ";
  const f=(s,o)=>s.replace(/\\{(\\w+)\\}/g,(_,k)=>o[k]!=null?o[k]:"");
  if(!c) return {title:M.i[0]+" | Go Nihon Trip", desc:M.i[1]};
  const t=DRINK_TABS.includes(st.dtab)?st.dtab:"", C=(t&&M[t])||M.c;
  const o={a:T(CITIES[c].ko), list:(t==="buy"?(DRINK_BUY[c]||[]).map(v=>T(v.n)):DRINKS.filter(v=>v.city===c).map(v=>T(v.n))).join(sep)};
  return {title:f(C[0],o)+" | Go Nihon Trip", desc:f(C[1],o)};
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
R2 = [
 ('  if(s.view==="drink") return DRINK_CITIES.includes(s.city) ? `${s.city}/drink/` : "drink/";', '  if(s.view==="drink") return DRINK_CITIES.includes(s.city) ? `${s.city}/drink/${s.dtab&&DRINK_TABS.includes(s.dtab)?s.dtab+"/":""}` : "drink/";'),
 ('  if(seg[0]==="drink"){ st.view="drink"; st.city="all"; return; }\n  if(CITIES[seg[0]]&&seg[1]==="drink"){ st.view="drink"; st.city=seg[0]; return; }', '  if(seg[0]==="drink"){ st.view="drink"; st.city="all"; st.dtab=""; return; }\n  if(CITIES[seg[0]]&&seg[1]==="drink"){ st.view="drink"; st.city=seg[0]; st.dtab=DRINK_TABS.includes(seg[2])?seg[2]:""; return; }'),
 ('const drl = e.target.closest("[data-drc]"); if(drl){ e.preventDefault(); st.view="drink"; st.city=drl.dataset.drc;', 'const drl = e.target.closest("[data-drc]"); if(drl){ e.preventDefault(); st.view="drink"; st.city=drl.dataset.drc; st.dtab=drl.dataset.drt||"";'),
]
def patch(s):
    s = block(s, '/*DRCSS_BEGIN*/', '/*DRCSS_END*/', CSS, 'footer{border-top:1px solid var(--line);')
    s = block(s, '/*DRINK_BEGIN*/', '/*DRINK_END*/', VIEW, 'V.place = function(){')
    s = block(s, '/*DRMETA_BEGIN*/', '/*DRMETA_END*/', META_JS, 'function setMeta(sel,val)')
    for a, b in R:
        if b in s: continue
        if any(k in b and k in s for k in ('closest("[data-drc]")', 'if(s.view==="drink") return', 'if(seg[0]==="drink")')): continue  # R2가 이미 바꾼 규칙
        assert s.count(a) == 1, (a[:60], s.count(a))
        s = s.replace(a, b)
    for a, b in R2:
        if b in s: continue
        assert s.count(a) == 1, ('R2', a[:60], s.count(a))
        s = s.replace(a, b)
    return s
if __name__ == '__main__':
    for f in FILES:
        s = patch(open(f, encoding='utf-8').read())
        open(f, 'w', encoding='utf-8').write(s); print('patched', f)
