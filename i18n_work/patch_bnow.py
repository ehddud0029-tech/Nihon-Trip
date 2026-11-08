# 여행 추천(첫 화면) 'N월에만 즐길 수 있는 것': 다른 요약 칸처럼 이름 | 지역 | 기간 줄 맞춤 + 설명 2줄 (2026-11 사용자 요청)
# html·backup pre에 같이 적용, 여러 번 돌려도 안전 (patch_brief.py 다음에).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
A = '<ol class="picks">${only.map(o=>`<li><button type="button" class="pick" data-open="${o.x.id}"><b><span class="fcity">${cityOf(o.x)}</span>${esc(o.x.name)}<span class="fdate">${esc(o.when)}</span></b><span class="pd fd">${esc(o.desc)}</span></button></li>`).join("")}</ol>'
B = '<ol class="picks">${only.map(o=>`<li><button type="button" class="pick" data-open="${o.x.id}"><b>${esc(o.x.name)}</b><em class="pm">${cityOf(o.x)}</em><span class="pd">${esc(o.when)}</span><span class="pdx">${esc(o.desc)}</span></button></li>`).join("")}</ol>'
CSS = """/*BNCSS_BEGIN*/
.brief.ball .bnow .picks .pd{white-space:nowrap;color:var(--shu);font-weight:600;font-size:14px}
.brief.ball .bnow .picks .pdx{grid-column:2/-1}
@media (min-width:760px){.brief.ball .bnow .picks{grid-template-columns:auto minmax(0,max-content) auto minmax(0,1fr)}
 .brief.ball .bnow .picks .pick b{grid-column:2;border-right:1px solid var(--line);padding-right:12px;align-self:center}
 .brief.ball .bnow .picks .pm{grid-column:3;margin:0;align-self:center}
 .brief.ball .bnow .picks .pd{grid-column:4;border-left:1px solid var(--line);padding-left:12px;align-self:center;margin:0}}
/*BNCSS_END*/
"""
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    if B not in s: assert s.count(A) == 1, f; s = s.replace(A, B)
    s = block(s, '/*BNCSS_BEGIN*/', '/*BNCSS_END*/', CSS, '/*BRCSS_BEGIN*/')
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
