# 여행 추천(첫 화면) '여행하기 좋은 도시': '추천 1/2' 표시를 빼고, 도시마다 그달에 가면 좋은 축제·관광지 이름(누르면 자세히)을 붙여요 (2026-11 사용자 요청)
# 이름은 MONTH_PICKS의 추천 장소 + 그 도시의 그달 축제(최대 5개). html·backup pre에 같이 적용, 여러 번 돌려도 안전.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
A = '    const rec = (MONTH_PICKS[M-1]||[]).map(([k,why],i)=>`<li><button type="button" class="pick" data-rec="${i}"><b>${CITIES[k].ko}</b><em class="pm">추천 ${i+1}</em><span class="pd">${esc(why)}</span></button></li>`).join("");'
B = ('    const recX = (k,t) => { const ids=[...((t&&t.ids)||[]), ...FESTS.filter(f=>f.city===k&&f.month===M).map(f=>f.id)]; return [...new Set(ids)].map(byId).filter(Boolean).slice(0,5); };\n'
     '    const rec = (MONTH_PICKS[M-1]||[]).map(([k,why,t],i)=>{ const xs=recX(k,t); return `<li><button type="button" class="pick" data-rec="${i}"><b>${CITIES[k].ko}</b><span class="pd">${esc(why)}</span></button>'
     '${xs.length?`<span class="rxs">${xs.map(x=>`<button type="button" data-open="${x.id}" class="rx${x.type==="fest"?" f":""}">${esc(x.name)}</button>`).join("")}</span>`:""}</li>`; }).join("");')
CSS = """/*BCCSS_BEGIN*/
.brief.ball .bcity .picks .pick b{grid-column:2/-1}
.brief.ball .bcity .picks .pd{grid-column:2/-1;margin:0;white-space:normal}
.brief .bcity .rxs{grid-column:2/-1;display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 14px}
.brief .bcity .rx{display:inline-block;flex:none;width:auto;white-space:nowrap;font:inherit;font-size:13px;line-height:1.4;border:1px solid var(--line);border-radius:999px;padding:3px 10px;background:var(--surface,#fff);color:var(--ink);cursor:pointer}
.brief .bcity .rx::before{content:"⛩️ ";counter-increment:none;font:inherit;font-size:11px;color:inherit;font-weight:400;grid-row:auto}.brief .bcity .rx.f::before{content:"🏮 "}
.brief .bcity .rx:hover{border-color:var(--shu);color:var(--shu)}
/*BCCSS_END*/
"""
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    if B not in s: assert s.count(A) == 1, f; s = s.replace(A, B)
    s = block(s, '/*BCCSS_BEGIN*/', '/*BCCSS_END*/', CSS, '/*BRCSS_BEGIN*/')
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
