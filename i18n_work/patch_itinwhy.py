# 추천 일정 보강 (2026-11-16, 사용자 요청)
# 1) 일정마다 '이 일정을 추천하는 이유'(블로그식 추천 글, itin_why_text.py) — 제목 아래
# 2) 일정 장소 옆 휴무 표시(SPOT_INFO의 요일·계절 휴무만, 연말연시·점검·부정기는 빼고)
# 3) 동선·중복 고침(도쿄 3박 4일 셋째 날 순서, 벳푸 우미지고쿠 중복, 나고야 셋째 날 메이지무라 먼저)과 새 팁
# html·backup pre·itin_view.js에 같이 적용, 여러 번 돌려도 안전. region_inject 뒤에도 다시 돌려 주세요(ITIN 줄 바로 아래 블록).
import json, sys
sys.path.insert(0, '/home/claude/i18n_work')
from itin_why_text import WHY, TIPS, UI
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
VIEW = f'{W}/sitegen/itin_view.js'

why_ko = {k: v[0] for k, v in WHY.items()}
tips_ko = [[k, t[0]] for k, *t in TIPS]
BLOCK = '''/*ITINWHY_BEGIN*/
/* 추천 일정 보강: 추천 이유 글·동선 고침·새 팁 (i18n_work/patch_itinwhy.py, 2026-11-16) */
const ITIN_WHY = %s;
(()=>{ const f=k=>ITIN.find(x=>x.key===k), set=(k,d,s)=>{ const c=f(k); if(c&&c.plan[d]) c.plan[d].s=s; };
  set("tokyo-3n4d",2,["s_toyosu","s_teamlab","s_odaiba","s_hamarikyu"]);
  { const c=f("kyushu-3n4d"); if(c&&c.plan[2]) c.plan[2].s=c.plan[2].s.filter(x=>x!=="s_umijigoku"); }
  set("nagoya-2n3d",2,["n_meijimura","n_inuyamajo","n_jokamachi"]);
  for(const [k,t] of %s){ const cs = k==="*kokyo" ? ITIN.filter(c=>c.plan.some(d=>d.s.includes("s_kokyo"))) : [f(k)].filter(Boolean);
    for(const c of cs) if(!c.tips.includes(t)) c.tips.push(t); }
})();
function itinWhy(c){ const w=ITIN_WHY[c.key]; return w?`<div class="gblk iwhy"><h4><span class="gbi">${gsvg("torii")}</span>이 일정을 추천하는 이유</h4><p>${esc(w)}</p></div>`:""; }
/* 일정 장소 휴무: 요일·계절 휴무만 (연중무휴·연말연시·점검·부정기 휴무는 표시하지 않음) */
function itinClosed(id){
  const si=SPOT_INFO[id]; if(!si||!si.c) return "";
  const r=SIV.rows(id), cl=r&&r.rows.find(x=>x[0]==="closed"); if(!cl) return "";
  const ny=d=>d.every(([m,dd])=>(m===12&&dd>=20)||(m===1&&dd<=5));
  const keep=si.c.map(c=>typeof c==="string" ? /^(mon|tue|wed|thu|fri)\\+?$|^mkt$/.test(c) : c.d ? !ny(c.d) : true);
  const txt=cl[1].filter((_,i)=>keep[i]); if(!txt.length) return "";
  return `<small class="iclo"><b>휴무</b> ${esc(txt.join(" · "))}</small>`;
}
/*ITINWHY_END*/''' % (json.dumps(why_ko, ensure_ascii=False), json.dumps(tips_ko, ensure_ascii=False))

CSS = '/*ITINWHYCSS*/.iwhy p{margin:4px 0 0;line-height:1.85;font-size:15px}.isn small.iclo{display:block;white-space:normal;overflow:visible;color:#B5452B;margin-top:2px;line-height:1.4}.iclo b{font-weight:700}/*ITINWHYCSS_END*/'

R = [
 ('<p itemprop="description">${esc(c.sum)}</p></div>\n   ${(ieSeen=new Set(),"")}',
  '<p itemprop="description">${esc(c.sum)}</p></div>\n   ${itinWhy(c)}${(ieSeen=new Set(),"")}'),
 ('${fee?` · <span class="ifee">${esc(fee[1][0])}</span>`:""}</small>',
  '${fee?` · <span class="ifee">${esc(fee[1][0])}</span>`:""}</small>${itinClosed(id)}'),
 ('${fee?` · <span class="ifee">${esc(fee[1][0])}</span>`:""}${itinClosed(id)}</small>',
  '${fee?` · <span class="ifee">${esc(fee[1][0])}</span>`:""}</small>${itinClosed(id)}'),
]

def rules(s, fn):
    for a, b in R:
        if b in s or a not in s: continue
        assert s.count(a) == 1, (fn, a[:50], s.count(a)); s = s.replace(a, b)
    assert 'itinWhy(c)' in s and '</small>${itinClosed(id)}' in s, fn
    return s

for fn in FILES:
    s = open(fn, encoding='utf-8').read()
    s = rules(s, fn)
    if '/*ITINWHY_BEGIN*/' in s:
        i = s.index('/*ITINWHY_BEGIN*/'); j = s.index('/*ITINWHY_END*/') + len('/*ITINWHY_END*/')
        s = s[:i] + BLOCK + s[j:]
    else:
        i = s.index('\nconst ITIN = '); j = s.index('\n', i + 1)
        s = s[:j + 1] + BLOCK + '\n' + s[j + 1:]
    if '/*ITINWHYCSS*/' in s:
        i = s.index('/*ITINWHYCSS*/'); j = s.index('/*ITINWHYCSS_END*/') + len('/*ITINWHYCSS_END*/')
        s = s[:i] + CSS + s[j:]
    else:
        a = '</style>'; i = s.index(a); s = s[:i] + CSS + '\n' + s[i:]
    open(fn, 'w', encoding='utf-8').write(s); print('ok', fn)

v = open(VIEW, encoding='utf-8').read(); v = rules(v, VIEW); open(VIEW, 'w', encoding='utf-8').write(v); print('ok view')

rows = [(v[0], v[1], v[2], v[3], v[4], v[5], v[6]) for v in WHY.values()] + [tuple(t) for k, *t in TIPS] + list(UI)
for r in rows: assert len(r) == 7 and all(r), r[0][:30]
D = f'{W}/i18n_work'
open(f'{D}/tr_64.tsv', 'w', encoding='utf-8').write(''.join('\t'.join(r[:5]) + '\n' for r in rows))
open(f'{D}/zh_65.tsv', 'w', encoding='utf-8').write(''.join(f'{r[0]}\t{r[5]}\n' for r in rows))
open(f'{D}/th_65.tsv', 'w', encoding='utf-8').write(''.join(f'{r[0]}\t{r[6]}\n' for r in rows))
print('rows', len(rows), 'why', len(WHY))
