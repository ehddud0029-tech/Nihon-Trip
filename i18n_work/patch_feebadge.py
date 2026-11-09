# 관광지 카드에 입장료 표시 (2026-11 사용자 요청): SPOT_INFO 요금 첫 줄을 카드 아래 배지로 —
# 유료(요금 숫자·'구간마다 다름' 등)는 주황 테두리(숫자로 시작하면 앞에 '입장료'), 무료는 초록, 휴관 중은 회색.
# 요금 문구는 SIV.rows()가 언어별로 만든 그대로. 비어 있던 곳 데이터는 FEEBDATA 블록.
# html·backup pre에 같이 적용, 여러 번 돌려도 안전.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
A = '''    <div class="meta"><span>${extra}</span>${isSaved?'<span class="saved-mark">저장됨</span>':''}</div></div></${tg[0]}>`;'''
B = '''    <div class="meta"><span>${extra}</span>${feeBadge(it)}${isSaved?'<span class="saved-mark">저장됨</span>':''}</div></div></${tg[0]}>`;'''
BLK = '''/*FEEB_BEGIN*/
function feePaid(id){ const si = SPOT_INFO[id]||{}, f = si.f; if(!f && si.fx && si.fx.length) return true; return Array.isArray(f) && f.some(x=>x[1]!=null ? x[1]!==0 : !/free/.test(x[0])); }
function feeBadge(it){
  if(it.type!=="spot") return "";
  const r = SIV.rows(it.id), st0 = r && r.rows.find(x=>x[0]==="status"), fee = r && r.rows.find(x=>x[0]==="fee");
  if(st0) return `<span class="feeb off">${esc(st0[1][0])}</span>`;
  if(!fee || !fee[1][0]) return "";
  const paid = feePaid(it.id);
  return `<span class="feeb${paid?" paid":""}" title="${esc(fee[1].join(" · "))}">${paid&&/^[0-9¥]/.test(fee[1][0])?"<b>입장료</b> ":""}${esc(fee[1][0])}</span>`;
}
/*FEEB_END*/
'''
DATA = '''/*FEEBDATA_BEGIN*/
/* 요금 정보가 비어 있던 곳 (2026-11 확인): 시키사이노오카는 7~9월만 입장료(어른 800엔), 랜드마크 스카이가든은 2025-12-31부터 공사로 휴관 */
SPOT_INFO.s_shikisai = Object.assign({f:[["adult",800,[7,9]]]}, SPOT_INFO.s_shikisai||{});
if(SPOT_INFO.s_landmark) SPOT_INFO.s_landmark.closed = 1;
/*FEEBDATA_END*/
'''
CSS = """/*FEEBCSS_BEGIN*/
.card .meta .feeb{font-size:11.5px;line-height:1.4;padding:1px 7px;border-radius:999px;border:1px solid #2e7d4f;color:#2e7d4f;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:62%}
.card .meta .feeb b{font-weight:600}.card .meta .feeb.off{border-color:#888;color:#666}.card .meta .feeb.paid{border-color:var(--shu);color:var(--shu)}
.card .meta{gap:6px;flex-wrap:wrap}
/*FEEBCSS_END*/
"""
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    if B not in s: assert s.count(A) == 1, f; s = s.replace(A, B)
    s = block(s, '/*FEEB_BEGIN*/', '/*FEEB_END*/', BLK, 'const ALL = [...SPOTS')
    s = block(s, '/*FEEBDATA_BEGIN*/', '/*FEEBDATA_END*/', DATA, 'const ITIN = [')
    s = block(s, '/*FEEBCSS_BEGIN*/', '/*FEEBCSS_END*/', CSS, '/*BRCSS_BEGIN*/')
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
