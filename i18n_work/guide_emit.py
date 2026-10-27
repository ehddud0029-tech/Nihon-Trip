import json,sys
sys.path.insert(0,'.')
from guide_data import PAGE, SECS
from stay_data import STAY
from region_more import STAY_ADD
STAY["blocks"] = STAY["blocks"] + STAY_ADD
SECS.insert([x['key'] for x in SECS].index('etiquette'), STAY)
from season_data import SEASON
SECS.insert([x['key'] for x in SECS].index('etiquette'), SEASON)
rows={}
def add(t):
    if isinstance(t,list) and len(t)==5 and isinstance(t[0],str):
        if all(t[1:]): rows.setdefault(t[0],t)
        return t[0]
    return t
def ko(o):
    if isinstance(o,list) and len(o)==5 and all(isinstance(x,str) for x in o) and o and not o[0].startswith('http'):
        return add(o)
    if isinstance(o,list): return [ko(x) for x in o]
    if isinstance(o,dict): return {k:ko(v) for k,v in o.items()}
    return o
G={"page":ko(PAGE),"secs":ko(SECS)}
extra=[["준비","Prep","準備","Prep.","Prép."],
       ["다른 준비 정보","More trip prep","ほかの準備情報","Más preparativos","Autres préparatifs"]]
for r in extra: rows[r[0]]=r
open('/home/claude/i18n_work/tr_25.tsv','w',encoding='utf-8').write(''.join('\t'.join(r)+'\n' for r in rows.values()))
open('/home/claude/sitegen/guide_data.js','w',encoding='utf-8').write('const GUIDE = '+json.dumps(G,ensure_ascii=False)+';\n')
print(len(rows),'rows')
