# 월별 날씨·옷차림 페이지(weather/, weather/<월>/, <도시>/weather/, <도시>/weather/<월>/) 추가
# tabishiori.html 과 backup/tabishiori.pre.html 두 곳에 같은 패치를 적용해요. 다시 돌려도 블록만 새로 바꿔요.
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s2tw import s2tw
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
VIEW = open(f'{W}/sitegen/weather_view.js', encoding='utf-8').read().strip()

CSS = """/*WXCSS_BEGIN*/
.wx{max-width:960px;margin:0 auto;padding-top:24px;display:flex;flex-direction:column;gap:16px}
body.is-wx .hero{display:none}
.wxcrumb{font-size:13px;color:var(--ink-2)}.wxcrumb a{color:var(--ink-2)}.wxcrumb i{font-style:normal;margin:0 4px}
.wxmon{display:flex;flex-wrap:wrap;gap:6px}
.wxmon a{padding:7px 12px;border:1px solid var(--line);border-radius:999px;background:var(--surface);text-decoration:none;color:var(--ink);font-size:14px}
.wxmon a.on{background:var(--ai);border-color:var(--ai);color:#fff;font-weight:700}
.wxsts{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px}
.wxst{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:10px 12px;display:flex;flex-direction:column;gap:2px}
.wxst span{font-size:12.5px;color:var(--ink-2)}.wxst b{font-size:22px;font-variant-numeric:tabular-nums}
.wxsts.big .wxst b{font-size:30px}.wxst.hi b{color:var(--shu)}.wxst.lo b{color:var(--ai)}
.wxtwo{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:760px){.wxtwo{grid-template-columns:1fr}}
.wxout{font-size:18px;font-weight:700;margin:0 0 14px;line-height:1.55}
.wxchart{width:100%;height:auto;display:block}
.wxchart text{font-size:12px;fill:var(--ink-2);font-variant-numeric:tabular-nums}.wxchart text.th{fill:var(--shu)}.wxchart text.tl{fill:var(--ai)}
.wxleg{display:flex;gap:14px;margin:6px 0 0;font-size:12.5px;color:var(--ink-2)}
.wxleg span::before{content:"";display:inline-block;width:14px;height:3px;border-radius:2px;margin-right:6px;vertical-align:middle;background:var(--ai)}
.wxleg .hi::before{background:var(--shu)}
.wxgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.wxcard{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.wxcard h3{margin:0;font-family:var(--f-display);font-size:19px}
.wxcard .wxsts{grid-template-columns:repeat(3,1fr);gap:6px}.wxcard .wxst{padding:6px 8px}.wxcard .wxst b{font-size:18px}
.wxfeel{margin:0;color:var(--ink-2);font-size:14px}
.wxo{margin:0;font-size:14.5px;line-height:1.55}.wxo span{display:block;font-size:12px;color:var(--ink-2)}
.wxcard .more{margin-top:auto;font-weight:700;color:var(--ai);text-decoration:none;font-size:14px}.wxcard .more i{font-style:normal}
.wxtblw{overflow-x:auto}
.wxtbl{border-collapse:collapse;width:100%;font-size:13.5px;background:var(--surface)}
.wxtbl th,.wxtbl td{border:1px solid var(--line);padding:6px 6px;text-align:center;white-space:nowrap}
.wxtbl a{text-decoration:none;color:var(--ink);display:block}
.wxtbl td b{display:block;color:var(--shu)}.wxtbl td small{color:var(--ai)}
.wxtbl tbody th{text-align:left}
.wxrows td.o{text-align:left;white-space:normal;min-width:220px}
.wxmemo{margin:0;display:grid;grid-template-columns:auto 1fr;gap:6px 14px}.wxmemo dt{font-weight:700;color:var(--ink-2);font-size:13.5px}.wxmemo dd{margin:0;line-height:1.6}
.wxlinks{display:flex;flex-wrap:wrap;gap:8px}.wxlinks i{font-style:normal}
/*WXCSS_END*/
"""

WM = {
 'ko': {"cm": ["{a} {m} 날씨와 옷차림 – 평균 기온·강수량", "{a} {m} 평균 최고 {hi}°, 최저 {lo}°, 강수량 {p}mm. 추천 옷차림: {o}. 챙기면 좋은 것과 여행 메모까지 정리했어요."],
        "am": ["일본 {m} 날씨와 옷차림 – 도쿄·오사카·후쿠오카·홋카이도·오키나와 기온 비교", "일본 {m} 도시별 평균 기온·강수량과 옷차림을 비교해 보세요. {list}."],
        "c": ["{a} 월별 날씨와 옷차림 – 1월~12월 평균 기온·강수량", "{a}의 1월부터 12월까지 평균 최고·최저 기온, 강수량, 습도와 달마다 추천 옷차림을 한눈에 정리했어요."],
        "i": ["일본 월별 날씨와 옷차림 – 지역별 평균 기온 한눈에", "도쿄·오사카·나고야·히로시마·시코쿠·후쿠오카·홋카이도·오키나와의 월별 평균 기온과 강수량, 옷차림을 기상청 평년값으로 비교해요."]},
 'en': {"cm": ["{a} Weather in {m} & What to Wear – Average Temperature and Rainfall", "{a} in {m}: average high {hi}°C, low {lo}°C, rainfall {p} mm. What to wear – {o}. Plus what to pack and travel notes."],
        "am": ["Japan Weather in {m} & What to Wear – Tokyo, Osaka, Fukuoka, Hokkaido, Okinawa Compared", "Average temperatures, rainfall and what to wear across Japan in {m}. {list}."],
        "c": ["{a} Weather by Month & What to Wear – Average Temperatures January–December", "Average highs and lows, rainfall, humidity and what to wear in {a} for every month from January to December."],
        "i": ["Japan Weather by Month & What to Wear – Average Temperatures by Region", "Compare monthly average temperatures, rainfall and what to wear in Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido and Okinawa, based on Japan Meteorological Agency normals."]},
 'ja': {"cm": ["{a}の{m}の天気と服装 – 平均気温・降水量", "{a}の{m}は平均最高{hi}℃、最低{lo}℃、降水量{p}mm。おすすめの服装：{o}。持ち物と旅のメモも。"],
        "am": ["日本の{m}の天気と服装 – 東京・大阪・福岡・北海道・沖縄の気温比較", "{m}の日本各地の平均気温・降水量と服装。{list}。"],
        "c": ["{a}の月別の天気と服装 – 1月〜12月の平均気温・降水量", "{a}の1月から12月までの平均最高・最低気温、降水量、湿度と、月ごとのおすすめの服装。"],
        "i": ["日本の月別の天気と服装 – 地域別の平均気温", "東京・大阪・名古屋・広島・四国・福岡・北海道・沖縄の月別平均気温と降水量、服装を気象庁の平年値で比較。"]},
 'es': {"cm": ["El tiempo en {a} en {m} y qué ropa llevar – Temperaturas y lluvias medias", "{a} en {m}: máxima media {hi} °C, mínima {lo} °C, lluvia {p} mm. Qué ponerse – {o}. Además, qué llevar y notas de viaje."],
        "am": ["El tiempo en Japón en {m} y qué ropa llevar – Tokio, Osaka, Fukuoka, Hokkaido y Okinawa", "Temperaturas medias, lluvias y ropa recomendada en Japón en {m}. {list}."],
        "c": ["El tiempo en {a} mes a mes y qué ropa llevar – Temperaturas de enero a diciembre", "Máximas y mínimas medias, lluvia, humedad y ropa recomendada en {a} para cada mes, de enero a diciembre."],
        "i": ["El tiempo en Japón mes a mes y qué ropa llevar – Temperaturas por región", "Compara temperaturas medias, lluvias y ropa recomendada por mes en Tokio, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido y Okinawa, según los valores normales de la Agencia Meteorológica de Japón."]},
 'fr': {"cm": ["Météo à {a} en {m} et comment s'habiller – Températures et pluies moyennes", "{a} en {m} : maximale moyenne {hi} °C, minimale {lo} °C, pluie {p} mm. Tenue conseillée – {o}. Avec quoi emporter et notes de voyage."],
        "am": ["Météo au Japon en {m} et comment s'habiller – Tokyo, Osaka, Fukuoka, Hokkaido, Okinawa", "Températures moyennes, pluies et tenues conseillées au Japon en {m}. {list}."],
        "c": ["Météo à {a} mois par mois et comment s'habiller – Températures de janvier à décembre", "Maximales et minimales moyennes, pluie, humidité et tenue conseillée à {a} pour chaque mois, de janvier à décembre."],
        "i": ["Météo au Japon mois par mois et comment s'habiller – Températures par région", "Comparez les températures moyennes, les pluies et les tenues conseillées par mois à Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido et Okinawa, d'après les normales de l'Agence météorologique du Japon."]},
 'zh': {"cm": ["{a}{m}天气与穿衣指南 – 平均气温·降水量", "{a}{m}平均最高{hi}℃、最低{lo}℃，降水量{p}毫米。推荐穿着：{o}。另附携带物品和旅行备忘。"],
        "am": ["日本{m}天气与穿衣指南 – 东京·大阪·福冈·北海道·冲绳气温对比", "日本各地{m}的平均气温、降水量和穿衣建议。{list}。"],
        "c": ["{a}各月天气与穿衣指南 – 1月至12月平均气温·降水量", "{a}1月至12月的平均最高·最低气温、降水量、湿度以及每月推荐穿着。"],
        "i": ["日本各月天气与穿衣指南 – 各地区平均气温", "根据日本气象厅平年值，比较东京、大阪、名古屋、广岛、四国、福冈、北海道、冲绳每月的平均气温、降水量和穿衣建议。"]},
 'th': {"cm": ["สภาพอากาศ{a}เดือน{m}และการแต่งตัว – อุณหภูมิเฉลี่ยและปริมาณฝน", "{a}เดือน{m}: อุณหภูมิสูงสุดเฉลี่ย {hi}°C ต่ำสุด {lo}°C ปริมาณฝน {p} มม. การแต่งตัวแนะนำ: {o} พร้อมของที่ควรพกและบันทึกการเดินทาง"],
        "am": ["สภาพอากาศญี่ปุ่นเดือน{m}และการแต่งตัว – เทียบโตเกียว โอซาก้า ฟุกุโอกะ ฮอกไกโด โอกินาว่า", "อุณหภูมิเฉลี่ย ปริมาณฝน และการแต่งตัวทั่วญี่ปุ่นในเดือน{m} {list}"],
        "c": ["สภาพอากาศ{a}รายเดือนและการแต่งตัว – อุณหภูมิเฉลี่ยมกราคม–ธันวาคม", "อุณหภูมิสูงสุดและต่ำสุดเฉลี่ย ปริมาณฝน ความชื้น และการแต่งตัวแนะนำใน{a} ทุกเดือนตั้งแต่มกราคมถึงธันวาคม"],
        "i": ["สภาพอากาศญี่ปุ่นรายเดือนและการแต่งตัว – อุณหภูมิเฉลี่ยแต่ละภูมิภาค", "เปรียบเทียบอุณหภูมิเฉลี่ย ปริมาณฝน และการแต่งตัวแนะนำรายเดือนในโตเกียว โอซาก้า นาโกย่า ฮิโรชิม่า ชิโกกุ ฟุกุโอกะ ฮอกไกโด และโอกินาว่า จากค่าปกติของสำนักงานอุตุนิยมวิทยาญี่ปุ่น"]},
}
WM['tw'] = {k: [s2tw(x) for x in v] for k, v in WM['zh'].items()}

META_JS = """/*WXMETA_BEGIN*/
function wxMeta(L,T){
  const WM=""" + json.dumps(WM, ensure_ascii=False, separators=(',', ':')) + """[L]||null; const M0=WM||null;
  const W=M0||""" + json.dumps(WM['ko'], ensure_ascii=False, separators=(',', ':')) + """;
  const c=WXN[st.city]?st.city:"all", m=st.wm>=1&&st.wm<=12?st.wm:0;
  const mon=k=> L==="ko"?k+"월":(L==="ja"||L==="zh"||L==="tw")?k+"月":((window.I18N&&window.I18N.MON[k-1])||k);
  const f=(s,o)=>s.replace(/\\{(\\w+)\\}/g,(_,k)=>o[k]!=null?o[k]:"");
  const sep=(L==="ja"||L==="zh"||L==="tw")?"、":", ";
  let k,o={};
  if(c==="all"&&!m) k="i";
  else if(c==="all"){ k="am"; o={m:mon(m), list:["tokyo","osaka","fukuoka","hokkaido","okinawa"].map(x=>{const d=wxData(x,m); return T(CITIES[x].ko)+" "+wxR(d.hi)+"°/"+wxR(d.lo)+"°";}).join(sep)}; }
  else if(!m){ k="c"; o={a:T(CITIES[c].ko)}; }
  else { k="cm"; const d=wxData(c,m); o={a:T(CITIES[c].ko), m:mon(m), hi:wxR(d.hi), lo:wxR(d.lo), p:d.pr, o:T(wxOutfit(c,m))}; }
  return {title:f(W[k][0],o)+" | Go Nihon Trip", desc:f(W[k][1],o)};
}
/*WXMETA_END*/
"""

NAV = ('<a href="#weather" data-view="weather"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" '
       'stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="3.2"/><path d="M9 2.5v1.3M3.8 4.8l.9.9M2.5 9h1.3M14.2 4.8l-.9.9"/>'
       '<path d="M8 19.5h9.5a3.5 3.5 0 0 0 .3-7 5 5 0 0 0-9.4 1.3A2.9 2.9 0 0 0 8 19.5z"/></svg><span>날씨</span></a>\n      ')

def block(s, begin, end, new, anchor):
    """begin~end 블록을 new로 바꾸고, 없으면 anchor 앞에 넣어요"""
    if begin in s:
        i = s.index(begin); j = s.index(end, i) + len(end)
        return s[:i] + new.strip() + s[j:]
    assert s.count(anchor) == 1, anchor[:50]
    return s.replace(anchor, new.strip() + '\n' + anchor)

R = [
 ('"about","contact","privacy"];\nconst INFO_VIEWS', '"about","contact","privacy","weather"];\nconst INFO_VIEWS'),
 ('  if(s.view==="saved") return "saved/";', '  if(s.view==="weather"){ const c=WXN[s.city]?s.city:"all", m=s.wm>=1&&s.wm<=12?s.wm:0; return c==="all"?(m?`weather/${m}/`:"weather/"):(m?`${c}/weather/${m}/`:`${c}/weather/`); }\n  if(s.view==="saved") return "saved/";'),
 ('  if(seg[0]==="guide"){', '  if(seg[0]==="weather"){ st.view="weather"; st.city="all"; st.wm=+seg[1]>=1&&+seg[1]<=12?+seg[1]:0; return; }\n  if(CITIES[seg[0]]&&seg[1]==="weather"){ st.view="weather"; st.city=seg[0]; st.wm=+seg[2]>=1&&+seg[2]<=12?+seg[2]:0; return; }\n  if(seg[0]==="guide"){'),
 ('  document.body.classList.toggle("is-info", INFO_VIEWS.includes(st.view));\n  if(st.view==="place")', '  document.body.classList.toggle("is-info", INFO_VIEWS.includes(st.view));\n  document.body.classList.toggle("is-wx", st.view==="weather");\n  if(st.view==="place")'),
 ('  if(INFO_VIEWS.includes(st.view)) return {title:IT[st.view]', '  if(st.view==="weather") return wxMeta(L,T);\n  if(INFO_VIEWS.includes(st.view)) return {title:IT[st.view]'),
 ('  const gs = e.target.closest("[data-gsec]");', '  const wxl = e.target.closest("[data-wxc]"); if(wxl){ e.preventDefault(); st.view="weather"; st.city=wxl.dataset.wxc; st.wm=+wxl.dataset.wxm||0; render(); window.scrollTo({top:0}); return; }\n'
  '  const wxf = e.target.closest("[data-wxfest]"); if(wxf){ e.preventDefault(); const c=wxf.dataset.wxfest; st.month=+wxf.dataset.m; st.city=c; if(c!=="all") st.area=areasOf(c)[0].key; st.view="festivals"; render(); window.scrollTo({top:0}); return; }\n'
  '  const gs = e.target.closest("[data-gsec]");'),
 ('<a href="#guide" data-view="guide"><svg', NAV + '<a href="#guide" data-view="guide"><svg'),
]

def patch(s):
    s = block(s, '/*WXCSS_BEGIN*/', '/*WXCSS_END*/', CSS, 'footer{border-top:1px solid var(--line);')
    s = block(s, '/*WX_BEGIN*/', '/*WX_END*/', VIEW, 'V.place = function(){')
    s = block(s, '/*WXMETA_BEGIN*/', '/*WXMETA_END*/', META_JS, 'function setMeta(sel,val)')
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (a[:60], s.count(a))
        s = s.replace(a, b)
    return s

if __name__ == '__main__':
    for f in FILES:
        s = open(f, encoding='utf-8').read()
        s = patch(s)
        open(f, 'w', encoding='utf-8').write(s)
        print('patched', f)
