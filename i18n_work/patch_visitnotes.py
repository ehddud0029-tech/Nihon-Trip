# 장소 페이지 '직접 다녀온 이야기' 칸 (2026-11-22). 글은 i18n_work/visit_notes.py.
# html·backup pre에 같이 적용, 여러 번 돌려도 안전. 번역 tr_65·zh_66·th_66. 글이 있는 장소는 site/place_keep.json에도 더해 검색에 내놓아요.
import json, sys
sys.path.insert(0, '/home/claude/i18n_work')
from visit_notes import NOTES, UI
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
byid = {}
for k, (ids, t) in NOTES.items():
    for i in ids: byid.setdefault(i, []).append(t[0])
BLOCK = '''/*VISITNOTE_BEGIN*/
const VISIT_NOTES = %s;
function visitNote(it){ const n=it&&VISIT_NOTES[it.id]; if(!n) return "";
  return `<div class="vnote"><h4>직접 다녀온 이야기</h4>${n.map(x=>`<p>${esc(x)}</p>`).join("")}<small>Go Nihon Trip 운영자가 직접 다녀와서 쓴 글이에요.</small></div>`; }
/*VISITNOTE_END*/''' % json.dumps(byid, ensure_ascii=False)
CSS = '/*VNCSS*/.vnote{margin:14px 0;padding:14px 16px;background:var(--surface,#fff);border:1px solid var(--line,#E3E6EC);border-left:4px solid #2E7D5B;border-radius:10px}.vnote h4{margin:0 0 6px;font-size:15px}.vnote p{margin:0 0 6px;line-height:1.8}.vnote small{color:var(--mute,#5A6272);font-size:12px}/*VNCSS_END*/'
A = '<div class="jpn">${esc(it.jp)}</div><p>${esc(it.desc)}</p>'
B = A + '${typeof visitNote==="function"?visitNote(it):""}'
for fn in FILES:
    s = open(fn, encoding='utf-8').read()
    if B not in s:
        assert s.count(A) >= 1, fn; s = s.replace(A, B)   # 상세 화면 두 곳(창·페이지)
    for beg, end, new, anchor in (('/*VISITNOTE_BEGIN*/', '/*VISITNOTE_END*/', BLOCK, '/*PITIN*/'), ('/*VNCSS*/', '/*VNCSS_END*/', CSS, '</style>')):
        if beg in s:
            i = s.index(beg); j = s.index(end) + len(end); s = s[:i] + new + s[j:]
        else:
            i = s.index(anchor); s = s[:i] + new + '\n' + s[i:]
    open(fn, 'w', encoding='utf-8').write(s); print('ok', fn)
rows = [t for ids, t in NOTES.values()] + UI
D = f'{W}/i18n_work'
open(f'{D}/tr_65.tsv', 'w', encoding='utf-8').write(''.join('\t'.join(r[:5]) + '\n' for r in rows))
open(f'{D}/zh_66.tsv', 'w', encoding='utf-8').write(''.join(f'{r[0]}\t{r[5]}\n' for r in rows))
open(f'{D}/th_66.tsv', 'w', encoding='utf-8').write(''.join(f'{r[0]}\t{r[6]}\n' for r in rows))
pk = f'{W}/site/place_keep.json'; cur = set(json.load(open(pk)))
slug = lambda i: i.replace('_', '-')
cur |= {slug(i) for i in byid}
json.dump(sorted(cur), open(pk, 'w'), ensure_ascii=False, indent=0)
print('notes', len(NOTES), 'places', len(byid))
