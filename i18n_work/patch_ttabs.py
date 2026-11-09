# 교통 페이지를 탭 4개로 (2026-11 사용자 요청): 한눈에 보기 / 이동별 걸리는 시간 / 공항에서 시내 가는 법 / 교통카드 안내
# 주소: transport/, <도시>/<지역>/transport/ 뒤에 times/ · airport/ · ic/
# 원래 교통 화면(V.transport)은 그대로 두고, 그 결과에서 탭에 맞는 부분만 골라 보여 줘요(다른 패치 규칙을 건드리지 않게).
# 맨 위 요약 칸(날씨·공항·교통카드·시내 이동)은 '한눈에 보기' 탭에서만 보여요.
# patch_tabs.py의 subOk/subFromSeg/subMeta에 교통 탭을 더해요. html·backup pre에 같이 적용 (여러 번 돌려도 안전, patch_tabs 다음에 돌리기)
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s2tw import s2tw
from patch_weather import block
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
TM = {
 'ko': {"times": ["{a} 교통 – 이동별 걸리는 시간", "{a}에서 주요 구간을 기차·지하철·버스로 이동할 때 걸리는 시간과 노선을 정리했어요."],
        "airport": ["{a} 공항에서 시내 가는 법 – 기차·버스·걸리는 시간", "{a}의 공항에서 시내와 관광지까지 가는 가장 빠른 방법과 걸리는 시간을 정리했어요."],
        "ic": ["{a} 교통카드 안내 – 어디서 사고 어떻게 쓰나", "{a}에서 쓰는 교통카드 종류와 사는 곳, 충전·환불 방법, 전국 호환 여부를 정리했어요."]},
 'en': {"times": ["{a} Transport – Travel Times by Route", "Travel times and lines for the main routes around {a} by train, subway and bus."],
        "airport": ["{a} Airport to City – Trains, Buses & Times", "The fastest ways from the airport to the city and sights in {a}, with travel times."],
        "ic": ["{a} IC Card Guide – Where to Buy & How to Use", "Which IC card to use in {a}, where to buy it, how to top up and get a refund, and where it works."]},
 'ja': {"times": ["{a}の交通 – 区間ごとの所要時間", "{a}の主な区間を電車・地下鉄・バスで移動するときの所要時間と路線をまとめました。"],
        "airport": ["{a}の空港から市内への行き方 – 電車・バス・所要時間", "{a}の空港から市内や観光地へのいちばん早い行き方と所要時間をまとめました。"],
        "ic": ["{a}の交通系ICカード案内 – 買える場所と使い方", "{a}で使える交通系ICカードの種類と買える場所、チャージ・払い戻し、全国での相互利用をまとめました。"]},
 'es': {"times": ["Transporte en {a} – Tiempos por trayecto", "Tiempos y líneas de los principales trayectos en {a} en tren, metro y autobús."],
        "airport": ["Del aeropuerto al centro en {a} – Trenes, autobuses y tiempos", "Las formas más rápidas de ir del aeropuerto al centro y a los lugares de interés en {a}, con tiempos."],
        "ic": ["Tarjetas IC en {a} – Dónde comprarlas y cómo usarlas", "Qué tarjeta IC usar en {a}, dónde comprarla, cómo recargarla y pedir el reembolso, y dónde funciona."]},
 'fr': {"times": ["Transports à {a} – Durées par trajet", "Durées et lignes des principaux trajets à {a} en train, métro et bus."],
        "airport": ["De l'aéroport au centre de {a} – Trains, bus et durées", "Les moyens les plus rapides de l'aéroport vers le centre et les sites de {a}, avec les durées."],
        "ic": ["Cartes IC à {a} – Où les acheter et comment les utiliser", "Quelle carte IC utiliser à {a}, où l'acheter, comment la recharger et se faire rembourser, et où elle fonctionne."]},
 'zh': {"times": ["{a}交通 – 各区间所需时间", "整理了{a}主要区间乘坐电车、地铁、巴士所需的时间和线路。"],
        "airport": ["{a}机场到市区的交通 – 电车·巴士·所需时间", "整理了从{a}的机场到市区和景点最快的方法与所需时间。"],
        "ic": ["{a}交通卡指南 – 在哪买·怎么用", "整理了{a}使用的交通卡种类、购买地点、充值与退款方法，以及全国通用情况。"]},
 'th': {"times": ["การเดินทางใน{a} – เวลาเดินทางแต่ละเส้นทาง", "เวลาและสายของเส้นทางหลักใน{a} ทั้งรถไฟ รถไฟใต้ดิน และรถบัส"],
        "airport": ["จากสนามบินเข้าเมือง{a} – รถไฟ รถบัส และเวลา", "วิธีที่เร็วที่สุดจากสนามบินเข้าเมืองและไปสถานที่ท่องเที่ยวใน{a} พร้อมเวลาเดินทาง"],
        "ic": ["คู่มือบัตร IC ใน{a} – ซื้อที่ไหนและใช้อย่างไร", "บัตร IC ที่ใช้ใน{a} ซื้อได้ที่ไหน วิธีเติมเงินและขอคืนเงิน และใช้ได้ที่ไหนบ้าง"]},
}
TM['tw'] = {k: [s2tw(x) for x in v] for k, v in TM['zh'].items()}
CORE = """/*TTABS_BEGIN*/
const TTABS = [["","한눈에 보기"],["times","이동별 걸리는 시간"],["airport","공항에서 시내 가는 법"],["ic","교통카드 안내"]];
const TTABM = """ + json.dumps(TM, ensure_ascii=False, separators=(',', ':')) + """;
const _vTransport = V.transport;
V.transport = function(){
  const html = _vTransport.call(this), t = TTABS.some(x=>x[0]===st.sub)?st.sub:"";
  const tp = document.createElement("template"); tp.innerHTML = html;
  const pick = sel => { const e = tp.content.querySelector(sel); return e ? e.outerHTML : ""; };
  const notes = [...tp.content.children].filter(e=>e.classList.contains("notes")).map(e=>e.outerHTML).join("");
  const keys = st.city==="all" ? Object.keys(CITIES) : [st.city];
  let body;
  if(t==="times") body = pick(".tgrid");
  else if(t==="ic") body = pick("#icguide") + notes;
  else if(t==="airport"){
    const aps = Object.keys(APS).filter(a=>keys.includes(apRegion(a)));
    body = aps.map(a=>`<section class="apsec"><h3 class="sgh"><span>${apA(a,"",esc(apName(a)))}</span></h3><ul class="apmini">${apDests(a).map(k2=>{ const o=apOpts(a,k2)[0]; return o?`<li>${apA(a,k2,`<b>${esc(AREA[k2].ko)}</b><span class="mode m-${o[0].mode}">${o[0].mode}</span><span class="aptm">${apMin(apSum(o))}</span><i class="apgo">›</i>`,"apm")}</li>`:""; }).join("")}</ul>
       ${apA(a,"",`모든 목적지와 방법 보기<i> →</i>`,"btn ghost")}</section>`).join("")   // 요약만, 자세한 내용은 공항 페이지 (2026-11 중복 정리)
       || pick(".apsec");
  } else {
    const ic = st.city!=="all" && IC_CARDS.find(x=>x.cities.includes(st.city));
    const icOv = ic ? `<section class="ovic"><h3 class="sgh"><span>교통카드</span></h3><div class="ovic-card"><div class="icrow">${ic.img?`<img src="${ic.img}" alt="" loading="lazy" referrerpolicy="no-referrer">`:""}<span><b>${esc(ic.name)}</b><small>${esc(ic.area)}</small></span></div><p>${esc(ic.cities[0]===st.city?ic.buy[0]:(ICBUY[st.city]||ic.buy[0]))}</p><a class="more" href="${ROUTED?window.NT_BASE+LPRE+pathOf({...st,sub:"ic"}):"#"}" data-subtab="ic">교통카드 안내<i> →</i></a></div></section>` : "";
    body = icOv + notes;   // 아래 탭 이동 버튼은 위 탭과 같아서 뺌 (2026-11 중복 정리)
  }
  return `<div class="sechead"><div><h2>교통</h2><p>공항에서 시내까지, 그리고 도시 안에서 이동하는 방법</p></div></div>
   ${subTabs(TTABS,t)}
   ${body}`;
};
/*TTABS_END*/
"""
CSS = """/*TTCSS_BEGIN*/
body.tsub #brief{display:none}
.ovic{margin:0 0 22px}.ovic-card{background:var(--card,#fff);border:1px solid var(--line);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;gap:8px;max-width:640px}
.ovic .icrow{display:flex;align-items:center;gap:12px}.ovic .icrow img{width:72px;height:46px;object-fit:contain;border-radius:6px;background:#fff;border:1px solid var(--line)}.ovic .icrow span{display:flex;flex-direction:column}.ovic .icrow small{font-size:13px;color:var(--ink-2)}.ovic p{margin:0;color:var(--ink-2);font-size:14px}.ovic .more{font-weight:600;font-size:14px}
.ttlinks{margin-top:20px}
.apmini{list-style:none;padding:0;margin:8px 0 12px;display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:6px 14px}.apmini li{display:block}.apmini .apm{display:grid;grid-template-columns:minmax(0,1fr) 4.8em 6.4em 10px;gap:8px;align-items:center;padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:var(--surface,#fff);color:var(--ink);text-decoration:none}.apmini .apm:hover{border-color:var(--shu)}.apmini .apgo{font-style:normal;color:var(--ink-2);font-size:18px;line-height:1}.apmini b{flex:1;font-weight:600;font-size:14.5px}.apmini .aptm{color:var(--shu);font-weight:600;font-size:14px;white-space:nowrap;text-align:left}.apmini .mode{justify-self:start;margin:0;white-space:nowrap}html:not([lang=ko]) .apmini .apm{grid-template-columns:minmax(0,1fr) 5.4em 8.8em 10px}
.apsec{margin-bottom:24px}
/*TTCSS_END*/
"""
R = [
 # 주소: 교통은 어느 도시·지역이든 탭 3개
 ('  if(s.view==="airport") return APS[s.ap]', '  if(s.view==="transport") return ["times","airport","ic"].includes(t)?t:"";\n  if(s.view==="airport") return APS[s.ap]'),
 ('  if(seg[0]==="airport"&&n===3&&APS[seg[1]]', '  if(seg[n-2]==="transport"&&["times","airport","ic"].includes(l)) return l;\n  if(seg[0]==="airport"&&n===3&&APS[seg[1]]'),
 # 탭별 검색 제목
 ('  else if(st.view==="airport"){ key=`airport:a:${st.sub}`; o.ap=T(apName(st.ap)); }',
  '  else if(st.view==="airport"){ key=`airport:a:${st.sub}`; o.ap=T(apName(st.ap)); }\n  else if(st.view==="transport"){ const tm=(TTABM[L]||TTABM.ko)[st.sub]; if(!tm) return null; const A=curArea(); const a=st.city==="all"?T("일본"):A?T(A.ko):T(CITIES[st.city].ko); return {title:f(tm[0],{a})+" | Go Nihon Trip", desc:f(tm[1],{a})}; }'),
 # 한눈에 보기 탭이 아니면 위 요약 칸 숨김
 ('  renderCities(); setNav();\n', '  document.body.classList.toggle("tsub", st.view==="transport" && !!subOk(st));\n  renderCities(); setNav();\n'),
]
def patch(s):
    s = block(s, '/*TTABS_BEGIN*/', '/*TTABS_END*/', CORE, 'V.place = function(){')
    s = block(s, '/*TTCSS_BEGIN*/', '/*TTCSS_END*/', CSS, 'footer{border-top:1px solid var(--line);')
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (a[:60], s.count(a))
        s = s.replace(a, b)
    return s
if __name__ == '__main__':
    for f in FILES:
        s = patch(open(f, encoding='utf-8').read())
        open(f, 'w', encoding='utf-8').write(s); print('patched', f)
