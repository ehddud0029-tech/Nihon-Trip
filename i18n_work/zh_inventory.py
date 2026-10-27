# 중국어 번역 대상 목록 만들기: zh_src/chunk_NN.tsv (번호 \t 한국어 \t 영어 \t 일본어)
# 이미 zh_*.tsv 에 번역이 있는 한국어는 건너뛰어요.  python3 zh_inventory.py [chunk크기]
import re, json, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build
W = os.path.dirname(os.path.abspath(__file__))
H = re.compile('[가-힣]')

def done():
    d = {}
    for f in glob.glob(f'{W}/zh_*.tsv'):
        for l in open(f, encoding='utf-8'):
            p = l.rstrip('\n').split('\t')
            if len(p) == 2: d[p[0]] = p[1]
    return d

def inventory():
    items, seen = [], set()
    def add(ko, en='', ja=''):
        if not ko or ko in seen or not H.search(ko): return
        seen.add(ko); items.append((ko, en, ja))
    jp = {}
    for s, k, j in json.load(open(f'{W}/atoms2.json')):
        if j: jp.setdefault(k, j)
    for f in sorted(glob.glob(f'{W}/tr_*.tsv')) + [f'{W}/ui.tsv']:
        for p in build.rows(f, 5): add(p[0], p[1], p[2])
    for ko, en in build.rows(f'{W}/names_en.tsv', 2): add(ko, en, jp.get(ko, ''))
    s = open('/home/claude/tabishiori.html', encoding='utf-8').read()
    q = r'"((?:[^"\\]|\\.)*)"'
    for m in re.finditer(r'W\(' + q + ',' + q + ',' + q, s): add(*[json.loads('"%s"' % x) for x in m.groups()])
    for m in re.finditer(r'\{"?ko"?:\s*' + q + r',\s*"?en"?:\s*' + q + r',\s*"?ja"?:\s*' + q, s): add(*[json.loads('"%s"' % x) for x in m.groups()])
    return items

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    d = done(); items = [x for x in inventory() if x[0] not in d]
    os.makedirs(f'{W}/zh_src', exist_ok=True)
    for f in glob.glob(f'{W}/zh_src/chunk_*.tsv'): os.remove(f)
    clean = lambda x: x.replace('\t', ' ').replace('\n', ' ')
    for c in range(0, len(items), n):
        with open(f'{W}/zh_src/chunk_{c//n:02d}.tsv', 'w', encoding='utf-8') as o:
            for i, (ko, en, ja) in enumerate(items[c:c+n]):
                o.write(f'{c+i}\t{clean(ko)}\t{clean(en)}\t{clean(ja)}\n')
    print(len(items), 'to translate,', sum(len(x[0]) for x in items), 'ko chars,', (len(items)+n-1)//n, 'chunks')
