"""브랜드 이름 Nihon Trip → Go Nihon Trip, 로고 B안(도장 안 GO + Nihon Trip + 도메인)"""
import re, sys, urllib.parse
SEAL_RE = re.compile(r'<span class="seal" title="Nihon Trip"><svg.*?</svg></span><span><b>Nihon Trip</b><small>일본 여행 가이드</small></span>', re.S)
SEAL_NEW = '<span class="seal seal-go" title="Go Nihon Trip" aria-hidden="true">GO</span><span><b>Nihon Trip</b><small>gonihontrip.com</small></span>'
CSS_A = '.brand b{font-family:var(--f-display);font-size:19px;letter-spacing:.01em}'
CSS_B = CSS_A + '\n.seal.seal-go{font-family:var(--f-display);font-weight:700;font-size:16px;letter-spacing:.02em}'
NAME = re.compile(r'(?<!Go )Nihon Trip(?!</b><small>gonihontrip)')

def html(p):
    s = open(p, encoding='utf-8').read()
    if 'seal-go' not in s:
        assert len(SEAL_RE.findall(s)) == 1, p
        s = SEAL_RE.sub(SEAL_NEW, s)
        assert s.count(CSS_A) == 1; s = s.replace(CSS_A, CSS_B)
    s = NAME.sub('Go Nihon Trip', s)
    open(p, 'w', encoding='utf-8').write(s)

def text(p):
    s = open(p, encoding='utf-8').read(); n = len(NAME.findall(s))
    open(p, 'w', encoding='utf-8').write(NAME.sub('Go Nihon Trip', s)); return n

FAV = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#C4452C"/>'
       '<text x="32" y="43" text-anchor="middle" font-family="Georgia,\'Times New Roman\',serif" font-weight="700" font-size="30" fill="#fff" letter-spacing="1">GO</text></svg>')
def favicon(p):
    s = open(p, encoding='utf-8').read()
    new = '<link rel="icon" href="data:image/svg+xml,' + urllib.parse.quote(FAV, safe='') + '">'
    s2 = re.sub(r'<link rel="icon"[^>]*>', new, s, count=1)
    open(p, 'w', encoding='utf-8').write(s2); return s2 != s

if __name__ == '__main__':
    for p in sys.argv[1:]:
        if p.endswith('.html') and 'tabishiori' in p: html(p); print('html', p)
        elif p.endswith('index.html'): print('favicon', p, favicon(p))
        else: print('text', p, text(p))
