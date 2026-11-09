# 숙소 동네별 페이지 <도시>/stay/<동네>/ (2026-11 사용자 요청: '오사카 숙소' 등 지역 검색 노출).
# 화면은 sitegen/stay_view.js의 stayNbPage (patch_stay.py가 넣음). 여기서는 주소(subOk·subFromSeg)·검색 제목(subMeta)·
# 숨은 h1(숙소·날씨·공항·술 화면은 검색 제목과 같게)·CSS·gen.py 경로·verify2를 고쳐요. html·pre에 같이, 여러 번 돌려도 안전. patch_stay.py·patch_tabs.py 다음에.
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
from s2tw import s2tw
W = '/home/claude'
NBM = {
 'ko': ["{n} 숙소 추천 – 장단점·공항 가는 법·근처 맛집 ({c})", "{pros} {cons}"],
 'en': ["Where to Stay in {n}, {c} – Pros, Cons & Airport Access", "{pros} {cons}"],
 'ja': ["{n}の宿泊ガイド（{c}）– メリット・デメリットと空港からのアクセス", "{pros}{cons}"],
 'zh': ["{c}{n}住宿指南 – 优缺点与机场交通", "{pros}{cons}"],
 'th': ["พักย่าน{n} {c} – ข้อดีข้อเสียและการเดินทางจากสนามบิน", "{pros} {cons}"],
 'es': ["Dónde alojarse en {n} ({c}) – Ventajas, desventajas y acceso desde el aeropuerto", "{pros} {cons}"],
 'fr': ["Loger à {n} ({c}) – Avantages, inconvénients et accès depuis l'aéroport", "{pros} {cons}"],
}
NBM['tw'] = [s2tw(x) for x in NBM['zh']]
R = [
 ('  if(s.view==="stay") return (t==="booking"||(t==="hotels"&&typeof stayShowHotels==="function"&&stayShowHotels()))?t:"";',
  '  if(s.view==="stay") return (t==="booking"||(t==="hotels"&&typeof stayShowHotels==="function"&&stayShowHotels())||(typeof stayNb==="function"&&stayNb(STAY_CITIES.includes(s.city)?s.city:"",t)))?t:"";'),
 ('  if(CITIES[seg[0]]&&seg[1]==="stay"&&n===3&&["hotels","booking"].includes(l)) return l;',
  '  if(CITIES[seg[0]]&&seg[1]==="stay"&&n===3&&(["hotels","booking"].includes(l)||(typeof stayNb==="function"&&stayNb(seg[0],l)))) return l;'),
 ('  if(st.view==="stay"){ const c=STAY_CITIES.includes(st.city)?st.city:""; key=`stay:${c?"c":"i"}:${st.sub}`; if(c) o.a=T(CITIES[c].ko); }',
  '  if(st.view==="stay"){ const c=STAY_CITIES.includes(st.city)?st.city:"", nb=stayNb(c,st.sub); if(nb){ const M=NBM_[L]||NBM_.ko, f=(s,x)=>s.replace(/\\{(\\w+)\\}/g,(_,k)=>x[k]!=null?x[k]:""), x={n:T(nb.name), c:T(stayAreas(c).h||CITIES[c].ko), pros:T(nb.pros), cons:T(nb.cons)}; return {title:f(M[0],x)+" | Go Nihon Trip", desc:f(M[1],x)}; } key=`stay:${c?"c":"i"}:${st.sub}`; if(c) o.a=T(CITIES[c].ko); }'),
 ('  const pm = subMeta() || pageMeta(); document.title = pm.title; setMeta(\'meta[property="og:title"]\',pm.title);\n',
  '  const pm = subMeta() || pageMeta(); document.title = pm.title; setMeta(\'meta[property="og:title"]\',pm.title);\n  if(["stay","weather","airport","drink"].includes(st.view)){ const h1=document.getElementById("heroTitle"); if(h1) h1.textContent = pm.title.replace(/ \\| Go Nihon Trip$/,""); }   // 숨은 h1을 검색 제목과 같게 (patch_staynb.py)\n'),
]
BLK = "/*NBMETA_BEGIN*/\nconst NBM_ = " + json.dumps(NBM, ensure_ascii=False, separators=(',', ':')) + ";\n/*NBMETA_END*/\n"
CSS = """/*NBCSS_BEGIN*/
.stnb .starea{margin-top:4px}.stnb .stjump{margin:14px 0 18px}
.stnear{list-style:none;margin:8px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:8px}
.stnear a{display:flex;flex-direction:column;gap:3px;padding:10px 14px;border:1px solid var(--line);border-radius:10px;background:var(--surface,#fff);color:var(--ink);text-decoration:none;height:100%;box-sizing:border-box}
.stnear a:hover{border-color:var(--shu)}.stnear b{font-size:15px;font-weight:600;line-height:1.4}.stnear span{font-size:13.5px;line-height:1.55;color:var(--ink-2);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.stgrid .starea{display:flex;flex-direction:column}.stgrid .starea .stmore{margin-top:auto;padding-top:10px}.starea h4 a{color:inherit;text-decoration:none}.starea h4 a:hover{color:var(--shu)}.starea .stmore{margin:10px 0 0}
/*NBCSS_END*/
"""
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    for a, b in R:
        if b in s: continue
        if s.count(a) == 0 and f.endswith('pre.html'): print('  (pre에 없음)', a[:50]); continue
        assert s.count(a) == 1, (f, a[:60]); s = s.replace(a, b)
    s = block(s, '/*NBMETA_BEGIN*/', '/*NBMETA_END*/', BLK, 'const ALL = [...SPOTS')
    s = block(s, '/*NBCSS_BEGIN*/', '/*NBCSS_END*/', CSS, '/*BRCSS_BEGIN*/')
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
G = f'{W}/sitegen/gen.py'; s = open(G, encoding='utf-8').read()
a = 'for(const c of STAY_CITIES) for(const t of sts) r.push(`${c}/stay/${t?t+"/":""}`);'
b = 'for(const c of STAY_CITIES){ for(const t of sts) r.push(`${c}/stay/${t?t+"/":""}`); for(const o of stayAreas(c).opts) r.push(`${c}/stay/${o.key}/`); }'
if b not in s: assert s.count(a) == 1, 'gen'; s = s.replace(a, b)
open(G, 'w', encoding='utf-8').write(s); print('gen ok')
V = f'{W}/i18n_work/verify2.py'; s = open(V, encoding='utf-8').read()
a = 'for(const c of ["all",...STAY_CITIES]) for(const t of ["","hotels","booking"]){ st.view="stay"; st.city=c; st.sub=t; await R(); } st.sub="";'
b = 'for(const c of ["all",...STAY_CITIES]) for(const t of ["","hotels","booking",...(c==="all"?[]:stayAreas(c).opts.map(o=>o.key))]){ st.view="stay"; st.city=c; st.sub=t; await R(); } st.sub="";'
if b not in s: assert s.count(a) == 1, 'verify'; s = s.replace(a, b)
open(V, 'w', encoding='utf-8').write(s); print('verify ok')
