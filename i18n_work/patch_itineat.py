# 추천 일정 상세: 날마다 '이날 추천 식당' 1~2곳 (2026-11 사용자 요청)
# 그날 들르는 장소의 지역(가장 많이 들르는 지역 먼저)에서 맛집 목록(AutoReserve·구글 지도 추천) 1위 가게를 메뉴를 바꿔 가며 고름(일정 안 중복 없음).
# 누르면 그 지역·메뉴의 맛집 페이지. html·backup pre·sitegen/itin_view.js에 같이 적용, 여러 번 돌려도 안전 (patch_itincity.py·patch_aio.py 다음에).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
BLK = r'''/*ITINEAT_BEGIN*/
const IEAT_MENUS = ["local","ramen","washoku","izakaya","konamon","meat","cafe"];
function itinEat(d, i, city, seen){
  const subs = d.s.map(byId).filter(Boolean).map(x=>x.sub).filter(Boolean); if(!subs.length) return "";
  const cnt = {}; subs.forEach(s=>cnt[s]=(cnt[s]||0)+1);
  const areas = [...new Set(subs.map(s=>vgRep(s,"food")))].filter(k=>(window.AR_SLUG||{})[k]).sort((a,b)=>(cnt[b]||0)-(cnt[a]||0));
  const ms = IEAT_MENUS.slice(i % IEAT_MENUS.length).concat(IEAT_MENUS.slice(0, i % IEAT_MENUS.length)), out = [];
  const take = k => { for(const m of ms){ const x = arShops(k,m,1)[0]; if(x && !seen.has(x.n) && !out.some(o=>o.m===m)){ seen.add(x.n); out.push({...x, m, k}); return true; } } return false; };
  for(const k of areas){ if(out.length>=2) break; take(k); }
  if(out.length<2 && areas[0]) take(areas[0]);
  if(!out.length && areas[0]){ const x = ms.map(m=>({...(arShops(areas[0],m,1)[0]||{}), m})).find(x=>x.n); if(x) out.push({...x, k:areas[0]}); }   // 그 지역 가게가 이미 다 나왔으면 다시 보여 줌
  if(!out.length) return "";
  const href = (k,m) => typeof ROUTED!=="undefined" && ROUTED ? window.NT_BASE+LPRE+pathOf({...st, view:"food", city, area:k, sub:"", menu:m}) : "#";
  return `<div class="ieat"><span class="ieh">이날 추천 식당</span>${out.map(x=>`<a class="ieatc" href="${esc(shopHref(x)||href(x.k,x.m))}"${shopHref(x)?' target="_blank" rel="noopener"':` data-goarea="${x.k}" data-region="${city}" data-to="food" data-menu="${x.m}"`}><b>${esc(x.n)}</b><em class="pm">${esc(MENU[x.m].ko.split("·")[0])}</em><span>${esc(x.dish||"")}</span><i>›</i></a>`).join("")}</div>`;
}
/*ITINEAT_END*/
'''
CSS = """/*IECSS_BEGIN*/
.ieat{margin:10px 0 2px;padding:10px 12px;border:1px dashed var(--line);border-radius:10px;display:flex;flex-direction:column;gap:6px}
.ieat .ieh{font-size:13px;font-weight:700;color:var(--shu)}.ieat .ieh::before{content:"🍽️ "}
.ieat .ieatc{display:grid;grid-template-columns:minmax(0,max-content) auto minmax(0,1fr) 10px;gap:8px;align-items:center;color:var(--ink);text-decoration:none;font-size:14px}
.ieat .ieatc b{font-weight:600}.ieat .ieatc span{color:var(--ink-2);font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.ieat .ieatc i{font-style:normal;color:var(--ink-2)}
.ieat .ieatc:hover b{color:var(--shu)}
.ieat .pm{font-style:normal;font-size:11.5px;border:1px solid var(--shu);color:var(--shu);border-radius:4px;padding:0 6px;white-space:nowrap}
/*IECSS_END*/
"""
A = '<ol class="istops">${d.s.map(itinStop).join("")}</ol></li>`).join("")}</ol>'
B = '<ol class="istops">${d.s.map(itinStop).join("")}</ol>${itinEat(d,i,c.city,ieSeen)}</li>`).join("")}</ol>'
A2 = '<ol class="idays" itemprop="itinerary"'
B2 = '${(ieSeen=new Set(),"")}<ol class="idays" itemprop="itinerary"'
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html', f'{W}/sitegen/itin_view.js']:
    s = open(f, encoding='utf-8').read()
    if B not in s: assert s.count(A) == 1, (f, 'A'); s = s.replace(A, B)
    if B2 not in s: assert s.count(A2) == 1, (f, 'A2'); s = s.replace(A2, B2)
    if f.endswith('.html'):
        s = block(s, '/*ITINEAT_BEGIN*/', '/*ITINEAT_END*/', BLK.replace('function itinEat', 'let ieSeen = new Set();\nfunction itinEat'), 'const ALL = [...SPOTS')
        s = block(s, '/*IECSS_BEGIN*/', '/*IECSS_END*/', CSS, '/*BRCSS_BEGIN*/')
        a = '  if(ga){ st.city=ga.dataset.region; st.area=ga.dataset.goarea; st.focus=null; st.more=false; go(ga.dataset.to||st.homeTo); return; }'
        b = '  if(ga){ st.city=ga.dataset.region; st.area=ga.dataset.goarea; st.focus=null; st.more=false; if(ga.dataset.menu) st.menu=ga.dataset.menu; go(ga.dataset.to||st.homeTo); return; }'
        if b not in s: assert s.count(a) == 1, (f, 'ga'); s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
