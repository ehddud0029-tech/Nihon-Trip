# 페이지별 맨 위 요약 칸에서 날씨·시내 이동을 빼고 주제 내용만 (2026-11 사용자 요청)
# - 관광지: 추천 관광지 TOP 3(짧은 설명 2줄) · 추천 여행 경로
# - 맛집·축제·쇼핑·나의 여행: 주제 칸 두 개(추천 목록 · 주제별 안내)
# - 교통: 날씨만 빼고 공항 가는 법 · 교통카드 · 시내 이동 (교통 페이지는 '한눈에 보기' 탭에서만 보임)
# - 도시를 고른 화면에선 날씨 출처 안내 줄도 숨겨요
# html·backup pre에 같이 적용 (여러 번 돌려도 안전, patch_ttabs.py 다음에 돌리기)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
CSS = """/*BRCSS_BEGIN*/
.brief .picks .pdx{grid-column:2/-1;color:var(--ink-2);font-size:14px;font-weight:400;line-height:1.55;margin:0 0 10px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;text-align:left}
body.nowx #wxnote{display:none}
.brief .bspot .picks{grid-template-columns:auto auto minmax(0,1fr);row-gap:3px}.brief .bspot .picks .pick b{grid-column:2/-1}.brief .bspot .picks .pm{grid-column:2;justify-self:start;min-width:0;margin:0}.brief .bspot .picks .pd{grid-column:3;white-space:normal}
/*BRCSS_END*/
"""
R = [
 ('    const cells = st.view==="spots" ? [wxCell, topicCell, courseCell, moveCell]\n      : st.view==="transport" ? [wxCell, apCell, icBrief, moveCell]\n      : [wxCell, extraCell, topicCell, moveCell];',
  '    const cells = st.view==="spots" ? [topicCell, courseCell]\n      : st.view==="transport" ? [apCell, icBrief, moveCell]\n      : [topicCell, extraCell];\n    document.body.classList.add("nowx");'),
 # 관광지 TOP 3에 짧은 설명
 ('${pickList(items, x=>SPOT_CAT[x.cat].ko, x=>x.area||"")}',
  '${pickList(items, x=>SPOT_CAT[x.cat].ko, x=>x.area||"").replace(/<\\/button><\\/li>/g,"</button></li>").replace(/(<button type="button" class="pick" data-open="([^"]+)">[\\s\\S]*?)<\\/button>/g,(m,a,id)=>{ const it=byId(id); return a+(it&&it.desc?`<span class="pdx">${esc(it.desc)}</span>`:"")+"</button>"; })}'),
 # 도시를 안 고른 화면에선 날씨 안내 줄 다시 보이게
 ('  document.body.classList.toggle("tsub",', '  document.body.classList.remove("nowx");\n  document.body.classList.toggle("tsub",'),
]
def patch(s):
    s = block(s, '/*BRCSS_BEGIN*/', '/*BRCSS_END*/', CSS, 'footer{border-top:1px solid var(--line);')
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (a[:60], s.count(a))
        s = s.replace(a, b)
    return s
if __name__ == '__main__':
    for f in FILES:
        s = patch(open(f, encoding='utf-8').read())
        open(f, 'w', encoding='utf-8').write(s); print('patched', f)
