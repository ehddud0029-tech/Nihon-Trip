# 여행 추천(첫 화면) 오늘 날씨 칸을 작게(아이콘·기온 한 줄) + 여행 메모 소제목을 크게 (2026-11 사용자 요청)
# html·backup pre에 같이 적용, 여러 번 돌려도 안전 (CSS 블록만).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
CSS = """/*TCCSS_BEGIN*/
.brief .tcity{display:grid;grid-template-columns:auto auto;grid-template-areas:"b b" "i t" "c c" "h h";justify-content:center;align-items:center;column-gap:4px;row-gap:0;padding:5px 4px}
.brief .tcity b{grid-area:b;text-align:center;font-size:13.5px}
.brief .tcity .ticon{grid-area:i;font-size:18px;line-height:1}
.brief .tcity .tavg{grid-area:t;font-size:19px;line-height:1.2}
.brief .tcity .tcond{grid-area:c;text-align:center;font-size:11.5px;line-height:1.35}
.brief .tcity .thl,.brief .tcity .thum,.brief .tcity .tnow{grid-area:h;text-align:center;font-size:11.5px;line-height:1.35;margin:0}
.brief .tcities{gap:5px}
@media (max-width:480px){.brief .tcity .ticon{font-size:16px}.brief .tcity .tavg{font-size:17px}.brief .tcity b{font-size:12px}}
.brief .mood{gap:12px}
.brief .mood p span{font-size:15px;font-weight:700;color:var(--shu);margin-bottom:3px;padding-left:9px;border-left:3px solid var(--shu);line-height:1.3}
/*TCCSS_END*/
"""
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    s = block(s, '/*TCCSS_BEGIN*/', '/*TCCSS_END*/', CSS, '/*BRCSS_BEGIN*/')
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
