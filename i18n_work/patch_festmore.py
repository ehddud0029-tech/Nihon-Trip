# 축제·계절 행사 39개 추가 (fest_more.py) → html·backup pre에 FESTS.push·GEO 블록, 번역 tr_53·zh_54·th_54 생성.
# 여러 번 돌려도 안전 (블록만 교체). region_inject 뒤에 다시 돌려 주세요.
import os, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
from fest_more import F
W = '/home/claude'
items, geo = [], {}
for (i, c, sub, m, lat, lng, jp, name, when, desc, area, tip) in F:
    items.append({"id": i, "type": "fest", "city": c, "month": m, "k": "", "name": name[0], "jp": jp, "when": when[0],
                  "desc": desc[0], "area": area[0], "tip": tip[0], "sub": sub})
    geo[i] = [lat, lng]
J = lambda o: json.dumps(o, ensure_ascii=False)
BLK = f"/*FESTMORE_BEGIN*/\nFESTS.push(...{J(items)});\nwindow.GEO = Object.assign(window.GEO||{{}}, {J(geo)});\n/*FESTMORE_END*/\n"
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    s = block(s, '/*FESTMORE_BEGIN*/', '/*FESTMORE_END*/', BLK, 'const ALL = [...SPOTS')
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
# 번역 (이미 사전에 있는 한국어 문장은 건너뜀)
have = set()
for p in glob.glob(f'{W}/i18n_work/tr_*.tsv'):
    if p.endswith('tr_53.tsv'): continue
    for l in open(p, encoding='utf-8'): have.add(l.split('\t')[0])
seen = set()
with open(f'{W}/i18n_work/tr_53.tsv', 'w', encoding='utf-8') as a, open(f'{W}/i18n_work/zh_54.tsv', 'w', encoding='utf-8') as z, open(f'{W}/i18n_work/th_54.tsv', 'w', encoding='utf-8') as t:
    for f in F:
        for x in f[7:]:
            if x[0] in seen or x[0] in have: continue
            seen.add(x[0]); a.write('\t'.join(x[:5]) + '\n'); z.write(x[0] + '\t' + x[5] + '\n'); t.write(x[0] + '\t' + x[6] + '\n')
print('rows', len(seen), 'skipped (already translated)', sum(1 for f in F for x in f[7:] if x[0] in have))
