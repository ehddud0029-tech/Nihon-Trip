# th_out/NN.txt (번호 \t 태국어) 를 th_src/chunk_NN.tsv 와 맞춰 th_NN.tsv (한국어 \t 태국어) 로 저장
import sys, os, glob
W = os.path.dirname(os.path.abspath(__file__))
ns = sys.argv[1:] or sorted(os.path.basename(p)[:-4] for p in glob.glob(f'{W}/th_out/*.txt'))
for n in ns:
    src = {}
    for l in open(f'{W}/th_src/chunk_{n}.tsv', encoding='utf-8'):
        p = l.rstrip('\n').split('\t'); src[p[0]] = p[1]
    out, miss, got = [], [], {}
    for l in open(f'{W}/th_out/{n}.txt', encoding='utf-8'):
        l = l.rstrip('\n')
        if not l.strip(): continue
        i, z = l.split('\t', 1)
        assert i in src, (n, i)
        got[i] = z.rstrip()
    for i, ko in src.items():
        if i in got: out.append(f'{ko}\t{got[i]}')
        else: miss.append(i)
    open(f'{W}/th_{n}.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(n, len(out), 'MISSING:' if miss else '', ' '.join(miss[:20]))
