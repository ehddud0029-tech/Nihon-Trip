import json,sys
sys.path.insert(0,'.')
from itin_data import COURSES, UI
from region_more import COURSES_ADD
COURSES = COURSES + COURSES_ADD
rows={}
def k(t):
    assert len(t)==5 and all(t), t
    rows.setdefault(t[0],t); return t[0]
out=[]
for c in COURSES:
    out.append({"key":c["key"],"city":c["city"],"n":c["n"],"title":k(c["title"]),"sum":k(c["sum"]),
                "plan":[{"t":k(d["t"]),"s":d["s"]} for d in c["plan"]],"tips":[k(t) for t in c["tips"]]})
for u in UI: k(u)
open('tr_27.tsv','w',encoding='utf-8').write(''.join('\t'.join(r)+'\n' for r in rows.values()))
open('/home/claude/sitegen/itin_data.js','w',encoding='utf-8').write('const ITIN = '+json.dumps(out,ensure_ascii=False)+';\n')
print(len(out),'courses',len(rows),'rows')
