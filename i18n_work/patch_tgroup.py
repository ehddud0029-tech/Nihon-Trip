# 교통 페이지에서 이동 방법이 거의 같은 하위 지역을 하나로 묶어 보여 주기 (2026-11 사용자 요청)
# 묶음 정보: site/tgroups.json (도시 -> [[이름, [지역 키 …]]], 첫 지역이 대표 주소)
# - 교통 화면의 지역 버튼은 묶음 하나로, 공항 가는 법·시내 이동은 묶인 지역 것을 합쳐서(중복 제거) 보여 줘요
# - 묶음 안 다른 지역을 고르면 대표 지역으로 바뀌고, 예전 주소(<도시>/<지역>/transport/)는 gen.py가 대표 주소로 보내요
# - 관광지·맛집 등 다른 화면은 그대로 세부 지역
# html·backup pre에 같이 적용 (여러 번 돌려도 안전)
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
G = json.load(open(f'{W}/site/tgroups.json', encoding='utf-8'))
CORE = """/*TGROUP_BEGIN*/
const TGROUPS = """ + json.dumps(G, ensure_ascii=False, separators=(',', ':')) + """;
const tgOf = k => { for(const c in TGROUPS) for(const [n,m] of TGROUPS[c]) if(m.includes(k)) return {name:n, members:m, rep:m[0]}; return null; };
const tgOn = () => st.view==="transport";
const tgRep = k => { const g=tgOf(k); return g?g.rep:k; };
function tgArea(A){ if(!A||!tgOn()) return A; const g=tgOf(A.key); return g?{...A, ko:g.name, tg:g.members}:A; }
function tgMerge(list, keyf, max){ const seen=new Set(), out=[]; for(const x of list){ const k=keyf(x); if(seen.has(k)) continue; seen.add(k); out.push(x); if(out.length>=max) break; } return out; }
function tgTo(A){
  const ta = A && TO_AREA[A.key]; if(!A||!A.tg||!ta) return ta;
  const all = A.tg.map(k=>TO_AREA[k]).filter(Boolean);
  const dir = all.flatMap(t=>t.direct||[]);
  return dir.length ? {direct: tgMerge(dir, r=>r.from+"|"+r.to, 5)} : ta;
}
function tgMove(pa){ const g=tgOn()&&tgOf(pa); if(!g) return (AREA_GUIDE[pa]||{}).move||[]; const n={}; return tgMerge(g.members.flatMap(k=>(AREA_GUIDE[k]||{}).move||[]), x=>x[1], 99).filter(x=>(n[x[0]]=(n[x[0]]||0)+1)<=2).slice(0,6); }
/*TGROUP_END*/
"""
R = [
 # 지금 지역: 교통 화면에선 묶음 이름·묶인 지역
 ('const curArea = () => st.area!=="all" ? AREA[st.area] : null;',
  'const curArea = () => st.area!=="all" ? tgArea(AREA[st.area]) : null;'),
 # 지역 버튼: 교통 화면에선 묶음 하나로
 ('  if(c) $("#areas").innerHTML = areasOf(st.city).map(a=>`<button class="area" type="button" data-area="${a.key}" aria-pressed="${st.area===a.key}">${a.ko}</button>`).join("");',
  '  if(c) $("#areas").innerHTML = areasOf(st.city).filter(a=>!tgOn()||tgRep(a.key)===a.key).map(a=>{ const g=tgOn()&&tgOf(a.key); return `<button class="area" type="button" data-area="${a.key}" aria-pressed="${st.area===a.key}">${g?g.name:a.ko}</button>`; }).join("");'),
 # 공항에서 가는 법: 묶인 지역 직행편을 합침
 ('    const ta = A && TO_AREA[A.key];', '    const ta = tgTo(A);'),
 # 시내 이동: 묶인 지역 것을 합침
 ('const moveCell = `<div class="bmove"><dt>${esc(AREA[pa]?.ko||c.ko)} 시내 이동</dt><dd class="mv">${(gd.move||[]).map(',
  'const moveCell = `<div class="bmove"><dt>${esc((tgOn()&&A?A.ko:AREA[pa]?.ko)||c.ko)} 시내 이동</dt><dd class="mv">${tgMove(pa).map('),
 # 교통 화면에서 묶음 안 다른 지역이면 대표 지역으로
 ('function render(){\n', 'function render(){\n  if(st.view==="transport" && st.area!=="all"){ const r=tgRep(st.area); if(r!==st.area) st.area=r; }\n'),
]
def patch(s):
    s = block(s, '/*TGROUP_BEGIN*/', '/*TGROUP_END*/', CORE, 'V.place = function(){')
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (a[:70], s.count(a))
        s = s.replace(a, b)
    return s
if __name__ == '__main__':
    for f in FILES:
        s = patch(open(f, encoding='utf-8').read())
        open(f, 'w', encoding='utf-8').write(s); print('patched', f)
