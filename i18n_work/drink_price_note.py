# 가격을 확인하지 못한 술에 '(매장마다 달라요)' 붙이기(2026-11-11) → drink_view.js·drink_more.py, 번역 tr_61·zh_62·th_62
import re, sys
sys.path.insert(0, '/home/claude/i18n_work')
import drink_price_fix as F
NOTE = "매장마다 달라요"
F.NOTE[NOTE] = ("varies by shop", "店によって異なる", "varía según la tienda", "varie selon le magasin", "因店而异", "แตกต่างกันตามร้าน")
ORIG = ['나다·후시미 사케', '삿포로 클래식', '오토코야마·구니마레', '오타루 와인', '오리온 드래프트', '히다 다카야마 사케', '긴샤치 맥주', '사이조 사케', '세토우치 레몬 술', '고치 사케', '도고 맥주', '유자 술']
MORE = ['에비스 맥주', '미노오 맥주', '아마오 딸기 술', '도카치 와인', '아바시리 유빙 드래프트', '즈이센', '구메지마노 구메센', '시콰사 술', '히다 다카야마 맥주', '다케쓰루', '미야지마 맥주', '나루토타이', '스다치 술']
add = lambda p: p if p.endswith('(' + NOTE + ')') else p + ' (' + NOTE + ')'
LEMON = "캔 약 200~300엔, 병 약 1,000~2,000엔 (매장마다 달라요)"
LEMON_T = ("can approx. ¥200–300, bottle approx. ¥1,000–2,000 (varies by shop)", "缶 約200〜300円、瓶 約1,000〜2,000円（店によって異なる）", "lata aprox. 200–300 ¥, botella aprox. 1.000–2.000 ¥ (varía según la tienda)", "canette env. 200–300 ¥, bouteille env. 1 000–2 000 ¥ (varie selon le magasin)", "罐约200~300日元，瓶约1,000~2,000日元（因店而异）", "กระป๋องประมาณ 200–300 เยน ขวดประมาณ 1,000–2,000 เยน (แตกต่างกันตามร้าน)")
def main():
    rows = {}
    p = '/home/claude/sitegen/drink_view.js'; s = open(p, encoding='utf-8').read()
    for n in ORIG:
        m = re.search(r'\{k:"[a-z]+", n:"' + re.escape(n) + r'",.*?p:"([^"]*)"', s); assert m, n
        v = LEMON if n == '세토우치 레몬 술' else add(m.group(1))
        s = s[:m.start(1)] + v + s[m.end(1):]
        rows[v] = list(LEMON_T) if v == LEMON else [F.tr(v, L) for L in range(6)]
    open(p, 'w', encoding='utf-8').write(s)
    p = '/home/claude/i18n_work/drink_more.py'; s = open(p, encoding='utf-8').read()
    for n in MORE:
        m = re.compile(r'(\("' + re.escape(n) + r'",.*?\n  \'[a-z]+\', ")([^"]+)(")', re.S).search(s); assert m, n
        s = s[:m.start(2)] + add(m.group(2)) + s[m.end(2):]
    if 'drink_price_note' not in s:
        s = s.replace("import json, re, sys; sys.path.insert(0, '/home/claude/i18n_work')", "import json, re, sys; sys.path.insert(0, '/home/claude/i18n_work'); import drink_price_note")
    open(p, 'w', encoding='utf-8').write(s)
    B = '/home/claude/i18n_work/'
    open(B + 'tr_61.tsv', 'w', encoding='utf-8').write(''.join('\t'.join([k] + r[:4]) + '\n' for k, r in rows.items()))
    open(B + 'zh_62.tsv', 'w', encoding='utf-8').write(''.join(k + '\t' + r[4] + '\n' for k, r in rows.items()))
    open(B + 'th_62.tsv', 'w', encoding='utf-8').write(''.join(k + '\t' + r[5] + '\n' for k, r in rows.items()))
    print('ok', len(rows))
if __name__ == '__main__': main()
