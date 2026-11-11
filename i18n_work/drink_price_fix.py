# 술 가격 확인값 반영(2026-11-11, 판매 사이트 가격 기준) → drink_view.js(원래 술)·drink_more.py(추가 술) 가격 바꾸고 tr_60·zh_61·th_61 생성
import re, json, sys
sys.path.insert(0, '/home/claude/i18n_work')
NOTE = {"상위 등급은 더 비싸요": ("higher grades cost more", "上位グレードはさらに高価", "las gamas altas cuestan más", "les gammes supérieures coûtent plus", "高等级更贵", "เกรดสูงกว่าราคาแพงกว่า")}
UNIT = {"캔": ("can", "缶", "lata", "canette", "罐", "กระป๋อง"), "병": ("bottle", "瓶", "botella", "bouteille", "瓶", "ขวด")}
def tr(p, L):
    note = ''
    m = re.match(r'^(.*?) \((.+)\)$', p)
    if m: p, note = m.group(1), NOTE[m.group(2)][L]
    m = re.match(r'^(\d+)ml (?:(캔|병) )?약 ([\d,]+)(?:~([\d,]+))?엔$', p); assert m, p
    vol, u, a, b = m.groups(); uu = UNIT[u][L] if u else ''
    es = lambda x: x.replace(',', '.'); fr = lambda x: x.replace(',', ' ')
    if L == 0: out = ' '.join(x for x in [f'{vol} ml', uu, 'approx. ¥' + a + ('–' + b if b else '')] if x)
    elif L == 1: out = f'{vol}ml{uu} 約{a}' + ('〜' + b if b else '') + '円'
    elif L == 2: out = (f'{uu} de {vol} ml' if uu else f'{vol} ml') + ', aprox. ' + es(a) + ('–' + es(b) if b else '') + ' ¥'
    elif L == 3: out = (f'{uu} de {vol} ml' if uu else f'{vol} ml') + ', env. ' + fr(a) + ('–' + fr(b) if b else '') + ' ¥'
    elif L == 4: out = f'{vol}ml{uu} 约{a}' + ('~' + b if b else '') + '日元'
    else: out = ' '.join(x for x in [uu, f'{vol} มล.', 'ประมาณ ' + a + ('–' + b if b else '') + ' เยน'] if x)
    if note: out += {1: f'（{note}）', 4: f'（{note}）'}.get(L, f' ({note})')
    return out
def main():
    ORIG = {'사와노이': '720ml 약 1,100~1,700엔 (상위 등급은 더 비싸요)', '구로키리시마': '900ml 약 1,000~1,300엔', '이이치코': '720ml 약 1,000~1,100엔',
            '시게마스': '720ml 약 1,400~2,400엔 (상위 등급은 더 비싸요)', '잔파': '720ml 약 1,400엔', '구니자카리': '720ml 약 1,400~2,100엔 (상위 등급은 더 비싸요)',
            '긴료': '720ml 약 1,100~2,000엔 (상위 등급은 더 비싸요)'}
    MORE = {'다마지만': '720ml 약 1,300~2,500엔 (상위 등급은 더 비싸요)', '아키시카': '720ml 약 1,900~2,500엔 (상위 등급은 더 비싸요)', '하쿠타케 시로': '720ml 약 1,200~1,400엔',
            '다나카 로쿠주고': '720ml 약 2,200~3,100엔', '가미카와 다이세쓰': '720ml 약 1,900~3,200엔 (상위 등급은 더 비싸요)', '가모시비토 구헤이지': '720ml 약 2,300~3,000엔 (상위 등급은 더 비싸요)',
            '호라이센': '720ml 약 2,100~3,800엔', '우고노쓰키': '720ml 약 1,800~3,300엔', '이시즈치': '720ml 약 1,700~2,700엔 (상위 등급은 더 비싸요)'}
    p = '/home/claude/sitegen/drink_view.js'; s = open(p, encoding='utf-8').read()
    for n, v in ORIG.items():
        s, k = re.subn(r'(\{k:"[a-z]+", n:"' + re.escape(n) + r'",.*?p:")([^"]*)(")', lambda m: m.group(1) + v + m.group(3), s, count=1); assert k == 1, n
    open(p, 'w', encoding='utf-8').write(s)
    p = '/home/claude/i18n_work/drink_more.py'; s = open(p, encoding='utf-8').read()
    for n, v in MORE.items():
        m = re.compile(r'(\("' + re.escape(n) + r'",.*?\n  \'[a-z]+\', ")([^"]+)(")', re.S).search(s); assert m, n
        s = s[:m.start(2)] + v + s[m.end(2):]
    # drink_more.py의 price()가 범위·메모를 모두 처리하도록 tr로 바꿈
    s = s.replace("add(p, [price(p, L) for L in range(6)])", "add(p, [__import__('drink_price_fix').tr(p, L) for L in range(6)])")
    open(p, 'w', encoding='utf-8').write(s)
    rows = {v: [tr(v, L) for L in range(6)] for v in ORIG.values()}
    B = '/home/claude/i18n_work/'
    open(B + 'tr_60.tsv', 'w', encoding='utf-8').write(''.join('\t'.join([k] + r[:4]) + '\n' for k, r in rows.items()))
    open(B + 'zh_61.tsv', 'w', encoding='utf-8').write(''.join(k + '\t' + r[4] + '\n' for k, r in rows.items()))
    open(B + 'th_61.tsv', 'w', encoding='utf-8').write(''.join(k + '\t' + r[5] + '\n' for k, r in rows.items()))
    print('ok', len(rows))


if __name__=='__main__': main()
