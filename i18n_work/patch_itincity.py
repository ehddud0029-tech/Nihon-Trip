# 도시별 추천 일정 페이지 itinerary/<도시>/ (2026-11, 사용자 요청: 상단 도시 버튼 → 도시 페이지, 검색 노출용 고유 안내·FAQ)
# 데이터·화면: sitegen/itin_city.js (ICITY_INFO, itinCityPage). html·backup pre·itin_view.js·gen.py·verify2.py에 같이 적용, 여러 번 돌려도 안전.
# patch_itinjump.py 다음에 돌리기 (목록 위 도시 버튼을 도시 페이지 링크로 바꿈). region_inject 뒤에도 다시 돌려 주세요.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
HTML = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
VIEW = f'{W}/sitegen/itin_view.js'
CITY = open(f'{W}/sitegen/itin_city.js', encoding='utf-8').read().strip() + '\n'
CSS = """/*ICCSS_BEGIN*/
.icity .ijump{margin:14px 0 6px}.icity .sgh{margin-top:26px}.icity .ifr{margin:-4px 0 12px;color:var(--ink-2);line-height:1.6}.icity .faq{margin-top:28px}.icity .faq dd a{font-weight:700}
.itin .igrp .sgh a{color:inherit;text-decoration:none}.itin .igrp .sgh a:hover{text-decoration:underline}.itin .igrp .imore{margin:10px 0 0;font-size:14px;font-weight:600}
/*ICCSS_END*/
"""
# 목록 페이지: 도시 버튼 → 도시 페이지, 도시 제목 → 도시 페이지 링크, 도시 묶음 아래 '모든 일정 보기'
V = [
 ('<nav class="wxmon stjump ijump">${ICITY_ORDER.filter(k=>ITIN.some(x=>x.city===k)).map(k=>`<a href="#st-${k}" data-stjump="${k}">${esc(CITIES[k].ko)}</a>`).join("")}</nav>',
  '<nav class="wxmon ijump">${ICITY_ORDER.filter(k=>ITIN.some(x=>x.city===k)).map(k=>`<a href="${itinHref(k)}" data-itin="${k}">${esc(CITIES[k].ko)}</a>`).join("")}</nav>'),
 ('<section class="igrp" id="st-${k}"><h3 class="sgh"><span>${esc(CITIES[k].ko)}</span><small>${esc(CITIES[k].jp)}</small></h3><div class="igrid">${g.map(itinCard).join("")}</div></section>',
  '<section class="igrp" id="st-${k}"><h3 class="sgh"><span><a href="${itinHref(k)}" data-itin="${k}">${esc(CITIES[k].ko)}</a></span><small>${esc(CITIES[k].jp)}</small></h3><div class="igrid">${g.map(itinCard).join("")}</div><p class="imore"><a href="${itinHref(k)}" data-itin="${k}">${esc(CITIES[k].ko)} 일정 안내 보기<i> →</i></a></p></section>'),
 # 도시 페이지로 분기
 ('V.itin = function(){\n  const c = ITIN.find(x=>x.key===st.itin);',
  'V.itin = function(){\n  if(ICITY_ORDER.includes(st.itin)) return itinCityPage(st.itin);\n  const c = ITIN.find(x=>x.key===st.itin);'),
 # 일정 상세: 도시 일정 링크
 ('<a class="iback" href="${itinHref("")}" data-itin=""><i>← </i>전체 일정</a>\n   <div class="ghead"><div class="ich">',
  '<a class="iback" href="${itinHref("")}" data-itin=""><i>← </i>전체 일정</a> <a class="iback" href="${itinHref(c.city)}" data-itin="${c.city}">${esc(CITIES[c.city].ko)} 일정 안내</a>\n   <div class="ghead"><div class="ich">'),
]
# html만: 주소 처리·검색 제목
H = [
 ('  if(s.view==="itin") return IKEYS.includes(s.itin) ? `itinerary/${s.itin}/` : "itinerary/";',
  '  if(s.view==="itin") return (IKEYS.includes(s.itin)||ICITY_ORDER.includes(s.itin)) ? `itinerary/${s.itin}/` : "itinerary/";'),
 ('  if(seg[0]==="itinerary"){ st.view="itin"; st.itin=IKEYS.includes(seg[1])?seg[1]:""; return; }',
  '  if(seg[0]==="itinerary"){ st.view="itin"; st.itin=(IKEYS.includes(seg[1])||ICITY_ORDER.includes(seg[1]))?seg[1]:""; return; }'),
 ('    const c=ITIN.find(x=>x.key===st.itin); return c ?',
  '    if(ICITY_ORDER.includes(st.itin)){ const L=(window.I18N&&window.I18N.lang)||"ko", T=window.__tr||(x=>x), k=st.itin, cn=T(CITIES[k].ko), ns=[...new Set(ITIN.filter(x=>x.city===k).map(x=>x.n))].sort((a,b)=>a-b).map(n=>n===0?T("당일치기"):nightsLabel(n)).join(L==="ko"||L==="ja"||L==="zh"||L==="tw"?"·":", "); const TT={ko:"{c} 여행 추천 일정 – {d} 코스",en:"{c} Itineraries – {d} Trip Plans",ja:"{c}旅行のモデルコース – {d}",es:"Itinerarios por {c} – {d}",fr:"Itinéraires à {c} – {d}",zh:"{c}旅行推荐行程 – {d}",tw:"{c}旅行推薦行程 – {d}",th:"แผนเที่ยว{c}แนะนำ – {d}"}[L]||"{c} – {d}"; return {title:TT.replace("{c}",cn).replace("{d}",ns)+" | Go Nihon Trip", desc:T((ICITY_INFO[k]||{}).intro||"")}; }\n    const c=ITIN.find(x=>x.key===st.itin); return c ?'),
]
def rep(s, rules, f):
    for a, b in rules:
        if b in s: continue
        assert s.count(a) == 1, (f, a[:70], s.count(a))
        s = s.replace(a, b)
    return s
for f in HTML:
    s = open(f, encoding='utf-8').read()
    s = block(s, '/*ICITY_BEGIN*/', '/*ICITY_END*/', CITY, 'V.itin = function(){')
    s = block(s, '/*ICCSS_BEGIN*/', '/*ICCSS_END*/', CSS, 'footer{border-top:1px solid var(--line);')
    s = rep(s, V + H, f)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
s = open(VIEW, encoding='utf-8').read()
s = block(s, '/*ICITY_BEGIN*/', '/*ICITY_END*/', CITY, 'V.itin = function(){')
s = rep(s, V, VIEW); open(VIEW, 'w', encoding='utf-8').write(s); print('patched', VIEW)
# 페이지 생성·번역 검사 경로
G = f'{W}/sitegen/gen.py'; s = open(G, encoding='utf-8').read()
a = 'r.push("itinerary/"); for(const k of IKEYS) r.push(`itinerary/${k}/`);'
b = 'r.push("itinerary/"); for(const k of IKEYS) r.push(`itinerary/${k}/`); for(const k of ICITY_ORDER) if(ITIN.some(x=>x.city===k)) r.push(`itinerary/${k}/`);'
if b not in s: assert s.count(a) == 1; s = s.replace(a, b); open(G, 'w', encoding='utf-8').write(s)
print('gen ok')
Vf = f'{W}/i18n_work/verify2.py'; s = open(Vf, encoding='utf-8').read()
a = 'for(const k of IKEYS){ st.itin=k; await R(); } st.itin=null;'
b = 'for(const k of IKEYS){ st.itin=k; await R(); } for(const k of ICITY_ORDER){ st.itin=k; await R(); } st.itin=null;'
if b not in s: assert s.count(a) == 1; s = s.replace(a, b); open(Vf, 'w', encoding='utf-8').write(s)
print('verify ok')
