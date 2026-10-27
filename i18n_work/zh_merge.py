# zh_out/NN.txt (번호 \t 간체) 를 zh_src/chunk_NN.tsv 와 맞춰 zh_NN.tsv (한국어 \t 간체) 로 저장
import sys, os
W = os.path.dirname(os.path.abspath(__file__))
for n in sys.argv[1:]:
    src = {}
    for l in open(f'{W}/zh_src/chunk_{n}.tsv', encoding='utf-8'):
        p = l.rstrip('\n').split('\t'); src[p[0]] = p[1]
    out, miss = [], []
    got = {}
    for l in open(f'{W}/zh_out/{n}.txt', encoding='utf-8'):
        l = l.rstrip('\n')
        if not l.strip(): continue
        i, z = l.split('\t', 1)
        assert i in src, (n, i)
        got[i] = z.strip()
    for i, ko in src.items():
        if i in got: out.append(f'{ko}\t{got[i]}')
        else: miss.append(i)
    open(f'{W}/zh_{n}.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(n, len(out), 'rows', 'MISSING:' if miss else '', ' '.join(miss[:20]))
