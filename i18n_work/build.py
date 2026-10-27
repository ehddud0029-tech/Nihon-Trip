import json, glob, re, sys, os
from functools import lru_cache
W = os.path.dirname(os.path.abspath(__file__))
LANGS = ['en', 'ja', 'es', 'fr']
ZH = ['zh', 'tw']          # 간체(zh)는 zh_*.tsv·zhtpl.tsv, 번체(tw)는 s2tw로 자동 변환
ALL_LANGS = LANGS + ZH
IDX = {l: i for i, l in enumerate(ALL_LANGS)}
H = re.compile('[가-힣]')

def rows(path, n):
    out = []
    for l in open(path, encoding='utf-8'):
        l = l.rstrip('\n')
        if not l.strip():
            continue
        p = l.split('\t')
        if len(p) != n:
            print('BAD ROW', path, l[:60], file=sys.stderr)
            continue
        out.append(p)
    return out

def load():
    D = {l: {} for l in LANGS}
    # names: en from names_en, ja from atoms2 jp, es/fr = en
    jp = {}
    for s, k, j in json.load(open(f'{W}/atoms2.json')):
        if j:
            jp.setdefault(k, j)
    for ko, en in rows(f'{W}/names_en.tsv', 2):
        D['en'][ko] = en; D['es'][ko] = en; D['fr'][ko] = en
        D['ja'][ko] = jp.get(ko, en)
    for f in ['arnames_1.tsv', 'arnames_2.tsv', 'arnames_3.tsv', 'arnames_4.tsv']:
        R = rows(f'{W}/{f}', 3)
        for i, (ko, ja, en) in enumerate(R):
            guess = f == 'arnames_3.tsv' and i >= 325
            D['en'][ko] = en; D['es'][ko] = en; D['fr'][ko] = en
            D['ja'][ko] = en if guess else ja
    for f in sorted(glob.glob(f'{W}/tr_*.tsv')) + [f'{W}/ui.tsv']:
        for p in rows(f, 5):
            for l in LANGS:
                D[l][p[0]] = p[1 + IDX[l]]
    # 중국어: 가게 이름(arnames)은 일본어 원래 이름, 나머지는 zh_*.tsv
    from s2tw import s2tw
    D['zh'] = {}; D['tw'] = {}
    keep = set()
    for f in ['arnames_1.tsv', 'arnames_2.tsv', 'arnames_3.tsv', 'arnames_4.tsv']:
        for ko, ja, en in rows(f'{W}/{f}', 3):
            v = D['ja'].get(ko, ja); D['zh'][ko] = v; keep.add(ko)
    for f in sorted(glob.glob(f'{W}/zh_*.tsv')):
        for ko, zh in rows(f, 2):
            D['zh'][ko] = zh
            if zh == D['ja'].get(ko): keep.add(ko)
            else: keep.discard(ko)
    for ko, zh in D['zh'].items():
        D['tw'][ko] = zh if ko in keep else s2tw(zh)
    for f in sorted(glob.glob(f'{W}/tw_fix*.tsv')):   # 번체 수동 보정 (한국어 \t 번체)
        for ko, tw in rows(f, 2): D['tw'][ko] = tw
    for l in ALL_LANGS:
        for k in [k for k in D[l] if re.fullmatch(r'\d+월', k)]:
            del D[l][k]
    T = []
    zt = dict(rows(f'{W}/zhtpl.tsv', 2))
    for p in rows(f'{W}/tpl.tsv', 5):
        z = zt.get(p[0], p[3])
        T.append([p[0]] + p[1:] + [z, s2tw(z)])
    return D, T

MON = {
 'en': ['January','February','March','April','May','June','July','August','September','October','November','December'],
 'es': ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'],
 'fr': ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'],
}
MS = {
 'en': ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
 'es': ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'],
 'fr': ['janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.'],
}

def compile_tpl(p):
    toks = re.split(r'(\{x\}|\{n\})', p)
    return [t for t in toks if t != '']

def fmt(out, g, lang):
    def rep(m):
        s = m.group(0)[1:-1]
        mm = re.fullmatch(r'(\d+)\?([^|]*)\|(.*)', s)
        if mm:
            k = int(mm.group(1))
            r = mm.group(2) if g[k] == '1' else mm.group(3)
            return r.replace('{%d}' % k, g[k])
        mm = re.fullmatch(r'(M|MC|MS|MSC)(\d+)', s)
        if mm:
            k = int(mm.group(2)); n = int(g[k]) - 1
            if lang in ('ja', 'zh', 'tw'):
                return g[k] + '月'
            if not 0 <= n < 12:
                return g[k]
            if mm.group(1) in ('MS', 'MSC'):
                v = MS[lang][n]
                return v[0].upper() + v[1:] if mm.group(1) == 'MSC' else v
            v = MON[lang][n]
            return v[0].upper() + v[1:] if mm.group(1) == 'MC' else v
        if s.isdigit():
            return g[int(s)]
        return m.group(0)
    r = re.sub(r'\{[^{}]*\}', rep, out)
    if lang == 'fr':
        r = re.sub(r"\b([dD])e ([AEIOUaeiouÉé])", r"\1'\2", r).replace('du 1 ', 'du 1er ')
    return r

def make(D, T, lang):
    TT = [(compile_tpl(t[0]), t[1 + IDX[lang]]) for t in T]
    d = D[lang]

    @lru_cache(None)
    def tr(s):
        if not H.search(s):
            return s
        if s in d:
            return d[s]
        st = s.strip()
        if st != s and st:
            r = tr(st)
            if r is not None:
                return s[:len(s) - len(s.lstrip())] + r + s[len(s.rstrip()):]
        for toks, out in TT:
            lits = [t for t in toks if t not in ('{x}', '{n}')]
            if any(l not in s for l in lits):
                continue
            g = match(toks, 0, s, 0)
            if g is not None:
                return fmt(out, g, lang)
        for pre in ['· ', '📍 ', '↳ ']:
            if s.startswith(pre):
                r = tr(s[len(pre):]); return None if r is None else pre + r
        for suf in [' ↗', ' ↓', ' →', ' ·', ':']:
            if s.endswith(suf):
                r = tr(s[:-len(suf)]); return None if r is None else r + suf
        for sep in [' · ', ' → ', '→', ' / ']:
            if sep in s:
                parts = [tr(p) for p in s.split(sep)]
                if all(p is not None for p in parts):
                    return sep.join(parts)
        return None

    def match(toks, i, s, pos):
        if i == len(toks):
            return [] if pos == len(s) else None
        t = toks[i]
        if t == '{n}':
            m = re.match(r'\d+', s[pos:])
            if not m:
                return None
            r = match(toks, i + 1, s, pos + m.end())
            return None if r is None else [m.group(0)] + r
        if t == '{x}':
            nxt = toks[i + 1] if i + 1 < len(toks) else None
            ends = []
            if nxt is None:
                ends = [len(s)]
            elif nxt in ('{x}', '{n}'):
                ends = range(pos + 1, len(s))
            else:
                k = s.find(nxt, pos + 1)
                while k != -1:
                    ends.append(k); k = s.find(nxt, k + 1)
            for e in ends:
                sub = s[pos:e]
                if not sub or sub == s:
                    continue
                v = tr(sub)
                if v is None:
                    continue
                r = match(toks, i + 1, s, e)
                if r is not None:
                    return [v] + r
            return None
        if s.startswith(t, pos):
            return match(toks, i + 1, s, pos + len(t))
        return None
    return tr

def emit(outdir):
    D, T = load()
    os.makedirs(outdir, exist_ok=True)
    for l in ALL_LANGS:
        o = {'lang': l, 'ar': {'en': 'en', 'ja': 'ja', 'zh': 'zh-cn', 'tw': 'zh-tw'}.get(l, 'en'), 'D': D[l],
             'T': [[t[0], t[1 + IDX[l]]] for t in T],
             'MON': MON.get(l, []), 'MS': MS.get(l, [])}
        js = '/* Go Nihon Trip — ' + l + ' dictionary (generated) */\nwindow.I18N=' + json.dumps(o, ensure_ascii=False, separators=(',', ':')) + ';\n'
        open(f'{outdir}/{l}.js', 'w', encoding='utf-8').write(js)
        print(l, len(js.encode()))

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'emit':
    emit(sys.argv[2]); sys.exit()
if __name__ == '__main__':
    D, T = load()
    S = json.load(open(f'{W}/strings.json'))
    for l in LANGS:
        tr = make(D, T, l)
        un = [s for s in S if tr(s) is None]
        print(l, 'dict', len(D[l]), 'unresolved', len(un))
        if l == 'en':
            for s in un[:80]:
                print('   ', repr(s))
