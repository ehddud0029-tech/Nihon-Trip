# 간체 → 대만 번체(용어 포함) 변환. OpenCC(Apache-2.0) 사전 파일(opencc/)을 써요.
# 사용: from s2tw import s2tw; s2tw("东京塔")  →  "東京塔"
import os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opencc')

def _load(name):
    m = {}
    for line in open(os.path.join(D, name), encoding='utf-8'):
        line = line.rstrip('\n')
        if not line or line.startswith('#'):
            continue
        k, v = line.split('\t', 1)
        m.setdefault(k, v.split(' ')[0])
    return m

_ST_P = _load('STPhrases.txt'); _ST_C = _load('STCharacters.txt')
_TW_P = _load('TWPhrases.txt'); _TW_V = _load('TWVariants.txt')
_MAXP = max(len(k) for k in _ST_P); _MAXT = max(len(k) for k in _TW_P)
# 일본 여행 사이트에 맞춘 보정 (OpenCC 결과를 덮어씀)
FIX = {'日圆': '日圓', '臺': '台'}

def _mm(s, phrases, chars, maxlen):
    out, i, n = [], 0, len(s)
    while i < n:
        for L in range(min(maxlen, n - i), 1, -1):
            w = s[i:i + L]
            if w in phrases:
                out.append(phrases[w]); i += L; break
        else:
            c = s[i]; out.append(chars.get(c, c)); i += 1
    return ''.join(out)

def s2tw(s):
    s = _mm(s, _ST_P, _ST_C, _MAXP)
    s = _mm(s, _TW_P, {}, _MAXT)
    s = ''.join(_TW_V.get(c, c) for c in s)
    for a, b in FIX.items():
        s = s.replace(a, b)
    return s

if __name__ == '__main__':
    import sys
    for t in sys.argv[1:] or ['东京塔和浅草寺', '从机场乘坐地铁到酒店', '在便利店用信用卡支付', '后面的面条很好吃', '台湾的出租车', '网络信息', '一天里发生了很多事']:
        print(t, '→', s2tw(t))
