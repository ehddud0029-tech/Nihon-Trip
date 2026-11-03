# 공항에서 시내 가는 법 페이지(airport/, airport/<공항>/, airport/<공항>/<지역>/) 추가
# tabishiori.html 과 backup/tabishiori.pre.html 두 곳에 같은 패치를 적용해요. 다시 돌려도 블록만 새로 바꿔요.
# 경로 데이터는 사이트의 TO_AREA를 그대로 써요. 화면 코드는 sitegen/airport_view.js
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s2tw import s2tw
from patch_weather import block
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
VIEW = open(f'{W}/sitegen/airport_view.js', encoding='utf-8').read().strip()

CSS = """/*APCSS_BEGIN*/
body.is-wx .hero{display:none}
.apgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-bottom:8px}
.apcard{display:flex;flex-direction:column;gap:4px;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:12px 14px;text-decoration:none;color:var(--ink)}
.apcard b{font-size:16px}.apcard span{font-size:13px;color:var(--ink-2);line-height:1.5}.apcard small{font-size:12px;color:var(--ai);font-weight:700}
.aprt{margin:0;font-size:14px;line-height:1.55}.aptm{margin:0;font-size:20px;font-weight:700;color:var(--shu)}
.apopts{display:flex;flex-direction:column;gap:10px}
.apopt{position:relative}.apbest{display:inline-block;margin-bottom:8px;padding:3px 9px;border-radius:999px;background:var(--shu);color:#fff;font-size:12px;font-weight:700}
.apsteps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.apsteps li{display:flex;flex-direction:column;gap:3px}.apsteps .rt{font-size:15.5px;font-weight:600}.apsteps small{color:var(--ink-2);font-size:13.5px;padding-left:2px}
.apsteps .step{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:var(--ai);color:#fff;font-size:12px;margin-right:6px}
.apsteps .min{color:var(--shu);margin-left:4px}
.apnote{margin:10px 0 0;font-size:13.5px;color:var(--ink-2)}
.apic{margin:0 0 6px;font-size:17px}.aplbl{display:inline-block;font-size:12px;font-weight:700;color:var(--ink-2);margin-right:6px}
.aplinks{display:flex;flex-wrap:wrap;gap:6px 14px}.aplinks a{color:var(--ai);font-weight:600}
.apsec{margin-top:28px}
/*APCSS_END*/
"""

AM = {
 'ko': {"r": ["{ap}에서 {to} 가는 법 – {line} {min}", "{ap}에서 {to}까지 가는 방법을 정리했어요. 가장 빠른 길은 {line}({min}). 갈아타는 곳, 교통카드 사는 곳, 도착해서 가 볼 곳까지 한눈에."],
        "a": ["{ap}에서 시내 가는 법 – {list} 교통편과 걸리는 시간", "{ap}에서 {list} 등 {n}곳으로 가는 기차·버스와 걸리는 시간, 교통카드 사는 곳을 정리했어요."],
        "i": ["일본 공항에서 시내 가는 법 – 나리타·하네다·간사이·후쿠오카·신치토세·나하", "나리타·하네다·간사이·후쿠오카·신치토세·나하 등 일본 공항 {n}곳에서 시내와 관광지까지 가는 기차·버스와 걸리는 시간을 공항별로 정리했어요."]},
 'en': {"r": ["How to Get from {ap} to {to} – {line}, {min}", "Ways to get from {ap} to {to}. The fastest is {line} ({min}). Where to transfer, where to buy an IC card and what to see when you arrive."],
        "a": ["{ap} to the City – Trains & Buses to {list}", "Trains and buses from {ap} to {n} destinations including {list}, with travel times and where to buy an IC card."],
        "i": ["Getting from Japan's Airports to the City – Narita, Haneda, Kansai, Fukuoka, New Chitose, Naha", "Trains, buses and travel times from {n} Japanese airports, including Narita, Haneda, Kansai, Fukuoka, New Chitose and Naha, to cities and sights."]},
 'ja': {"r": ["{ap}から{to}への行き方 – {line}で{min}", "{ap}から{to}への行き方まとめ。最速は{line}で{min}。乗り換え場所、交通系ICカードの買える場所、着いてから行きたい場所も。"],
        "a": ["{ap}から市内への行き方 – {list}への電車・バスと所要時間", "{ap}から{list}など{n}か所への電車・バスと所要時間、ICカードの買える場所。"],
        "i": ["日本の空港から市内への行き方 – 成田・羽田・関西・福岡・新千歳・那覇", "成田・羽田・関西・福岡・新千歳・那覇など日本の空港{n}か所から市内・観光地への電車・バスと所要時間を空港別にまとめました。"]},
 'es': {"r": ["{ap} → {to}: cómo llegar – {line}, {min}", "Cómo llegar a {to} desde el aeropuerto ({ap}). La opción más rápida es {line} ({min}). Dónde hacer transbordo, dónde comprar la tarjeta IC y qué ver al llegar."],
        "a": ["{ap}: cómo llegar al centro – Trenes y autobuses a {list}", "Trenes y autobuses desde {ap} a {n} destinos, entre ellos {list}, con tiempos de viaje y dónde comprar la tarjeta IC."],
        "i": ["Cómo ir de los aeropuertos de Japón a la ciudad – Narita, Haneda, Kansai, Fukuoka, Nuevo Chitose, Naha", "Trenes, autobuses y tiempos de viaje desde {n} aeropuertos de Japón, como Narita, Haneda, Kansai, Fukuoka, Nuevo Chitose y Naha, hasta ciudades y lugares de interés."]},
 'fr': {"r": ["{ap} → {to} : comment y aller – {line}, {min}", "Comment rejoindre {to} depuis l'aéroport ({ap}). Le plus rapide : {line} ({min}). Où changer, où acheter une carte IC et que voir à l'arrivée."],
        "a": ["{ap} : comment rejoindre le centre – Trains et bus vers {list}", "Trains et bus depuis {ap} vers {n} destinations, dont {list}, avec temps de trajet et où acheter une carte IC."],
        "i": ["Des aéroports du Japon au centre-ville – Narita, Haneda, Kansai, Fukuoka, New Chitose, Naha", "Trains, bus et temps de trajet depuis {n} aéroports japonais, dont Narita, Haneda, Kansai, Fukuoka, New Chitose et Naha, vers les villes et les sites."]},
 'zh': {"r": ["{ap}到{to}怎么走 – {line}{min}", "{ap}到{to}的交通方式。最快是{line}，{min}。附换乘地点、交通卡购买地点和到达后可去的景点。"],
        "a": ["{ap}到市区怎么走 – 前往{list}的电车·巴士与所需时间", "从{ap}前往{list}等{n}处的电车·巴士、所需时间和交通卡购买地点。"],
        "i": ["日本机场到市区怎么走 – 成田·羽田·关西·福冈·新千岁·那霸", "按机场整理从成田、羽田、关西、福冈、新千岁、那霸等日本{n}座机场前往市区和景点的电车·巴士与所需时间。"]},
 'th': {"r": ["วิธีเดินทางจาก{ap}ไป{to} – {line} {min}", "วิธีเดินทางจาก{ap}ไป{to} เร็วที่สุดคือ{line} ({min}) พร้อมจุดเปลี่ยนรถ ที่ซื้อบัตร IC และที่เที่ยวเมื่อไปถึง"],
        "a": ["วิธีเดินทางจาก{ap}เข้าเมือง – รถไฟและรถบัสไป{list}", "รถไฟและรถบัสจาก{ap}ไป {n} จุดหมาย เช่น {list} พร้อมเวลาเดินทางและที่ซื้อบัตร IC"],
        "i": ["วิธีเดินทางจากสนามบินญี่ปุ่นเข้าเมือง – นาริตะ ฮาเนดะ คันไซ ฟุกุโอกะ ชินชิโตเสะ นาฮะ", "รถไฟ รถบัส และเวลาเดินทางจากสนามบินญี่ปุ่น {n} แห่ง เช่น นาริตะ ฮาเนดะ คันไซ ฟุกุโอกะ ชินชิโตเสะ และนาฮะ ไปยังตัวเมืองและที่เที่ยว จัดตามสนามบิน"]},
}
AM['tw'] = {k: [s2tw(x) for x in v] for k, v in AM['zh'].items()}

META_JS = """/*APMETA_BEGIN*/
function apMeta(L,T){
  const W=(""" + json.dumps(AM, ensure_ascii=False, separators=(',', ':')) + """)[L]||null;
  const M=W||""" + json.dumps(AM['ko'], ensure_ascii=False, separators=(',', ':')) + """;
  const a=APS[st.ap]?st.ap:"", k=a&&st.apk&&apOpts(a,st.apk).length?st.apk:"";
  const f=(s,o)=>s.replace(/\\{(\\w+)\\}/g,(_,x)=>o[x]!=null?o[x]:"");
  const sep=(L==="ja"||L==="zh"||L==="tw")?"、":", ";
  const strip=x=>x.replace(/\\s*[（(][^）)]*[）)]\\s*$/,"");
  let key,o={};
  if(!a){ key="i"; o={n:Object.keys(APS).length}; }
  else if(!k){ key="a"; const d=apDests(a); o={ap:T(apName(a)), n:d.length, list:d.slice(0,3).map(x=>T(AREA[x].ko)).join(sep)}; }
  else { key="r"; const p=apOpts(a,k)[0]; o={ap:T(apName(a)), to:T(AREA[k].ko), line:p.map(x=>strip(T(x.line))).join(" → "), min:T(apMin(apSum(p)))}; }
  return {title:f(M[key][0],o)+" | Go Nihon Trip", desc:f(M[key][1],o)};
}
/*APMETA_END*/
"""

R = [
 ('"privacy","weather"];\nconst INFO_VIEWS', '"privacy","weather","airport"];\nconst INFO_VIEWS'),
 ('  if(s.view==="saved") return "saved/";', '  if(s.view==="airport"){ const a=APS[s.ap]?s.ap:""; return "airport/"+(a?a+"/"+(s.apk&&apOpts(a,s.apk).length?s.apk+"/":""):""); }\n  if(s.view==="saved") return "saved/";'),
 ('  if(seg[0]==="guide"){', '  if(seg[0]==="airport"){ st.view="airport"; st.city="all"; st.ap=APS[seg[1]]?seg[1]:""; st.apk=st.ap&&seg[2]?seg[2]:""; return; }\n  if(seg[0]==="guide"){'),
 ('document.body.classList.toggle("is-wx", st.view==="weather");', 'document.body.classList.toggle("is-wx", st.view==="weather"||st.view==="airport");'),
 ('  if(st.view==="weather") return wxMeta(L,T);', '  if(st.view==="weather") return wxMeta(L,T);\n  if(st.view==="airport") return apMeta(L,T);'),
 ('  const gs = e.target.closest("[data-gsec]");', '  const apl = e.target.closest("[data-apa]"); if(apl){ e.preventDefault(); st.view="airport"; st.ap=apl.dataset.apa; st.apk=apl.dataset.apk; render(); window.scrollTo({top:0}); return; }\n'
  '  const aps = e.target.closest("[data-apspots]"); if(aps){ e.preventDefault(); const k=aps.dataset.apspots; st.city=AREA[k].region; st.area=k; st.view="spots"; render(); window.scrollTo({top:0}); return; }\n'
  '  const gs = e.target.closest("[data-gsec]");'),
 ('   ${icGuide}\n', '   ${apLinks(keys)}\n   ${icGuide}\n'),
]

def patch(s):
    s = block(s, '/*APCSS_BEGIN*/', '/*APCSS_END*/', CSS, 'footer{border-top:1px solid var(--line);')
    s = block(s, '/*AP_BEGIN*/', '/*AP_END*/', VIEW, 'V.place = function(){')
    s = block(s, '/*APMETA_BEGIN*/', '/*APMETA_END*/', META_JS, 'function setMeta(sel,val)')
    for a, b in R:
        if b in s: continue
        add = b.replace(a, '', 1).strip() if a in b else ''
        if add and add.split('\n')[0][:60] in s: continue   # 이미 넣은 줄 (다른 패치가 주변을 바꿨어도)
        if s.count(a) == 0: continue   # 이미 다른 패치가 이 줄을 바꿨어요
        assert s.count(a) == 1, (a[:60], s.count(a))
        s = s.replace(a, b)
    return s

if __name__ == '__main__':
    for f in FILES:
        s = patch(open(f, encoding='utf-8').read())
        open(f, 'w', encoding='utf-8').write(s)
        print('patched', f)
