import json,re
H=re.compile('[가-힣]')
def make(D,T):
    def tr(s):
        if not H.search(s): return s
        if s in D: return D[s]
        for rx,out in T:
            m=rx.fullmatch(s)
            if m:
                g=[tr(x) if x is not None else '' for x in m.groups()]
                if all(x is not None for x in g):
                    return out(g) if callable(out) else out.format(*g)
        for pre in ['· ','📍 ','↳ ']:
            if s.startswith(pre):
                r=tr(s[len(pre):]); return None if r is None else pre+r
        for suf in [' ↗',' ↓',' →',' ·',':']:
            if s.endswith(suf):
                r=tr(s[:-len(suf)]); return None if r is None else r+suf
        for sep in [' · ',' → ','→']:
            if sep in s:
                parts=[tr(p) for p in s.split(sep)]
                if all(p is not None for p in parts): return sep.join(parts)
        return None
    return tr
