# 가격 칸의 끝 메모 '(…)'를 다음 줄로(2026-11-11): 화면은 drink_view.js가 나누고, 여기서는 나뉜 앞부분·메모 번역 줄을 만듦 → tr_62·zh_63·th_63
import json, re, sys, subprocess
sys.path.insert(0, '/home/claude/i18n_work')
import drink_price_note, drink_price_fix as F
js = r'''global.window=global;const s=require('fs').readFileSync('/home/claude/sitegen/drink_view.js','utf8');const m=s.match(/const DRINK_BUY = (\{[\s\S]*?\n\});/);const B=eval('('+m[1]+')');const m2=s.match(/\/\*DRMORE_BEGIN\*\/Object\.entries\((\{.*?\})\)\.forEach/);const M=JSON.parse(m2[1]);const o=new Set();for(const k in B)for(const v of B[k].concat(M[k]||[]))for(const x of v.p.split(' · '))o.add(x);console.log(JSON.stringify([...o]))'''
P = json.loads(subprocess.check_output(['node', '-e', js]))
NOTES = {
 "상위 등급은 더 비싸요": F.NOTE["상위 등급은 더 비싸요"],
 "매장마다 달라요": F.NOTE["매장마다 달라요"],
 "실제로는 더 비싼 경우가 많아요": ("often sold for more", "実際はもっと高いことが多い", "a menudo se vende más caro", "souvent vendu plus cher", "实际常常更贵", "มักขายแพงกว่า"),
 "연수가 적힌 제품은 훨씬 비싸요": ("age-stated bottles cost far more", "年数表記のある商品はずっと高価", "las botellas con edad cuestan mucho más", "les versions avec âge coûtent bien plus", "标有年份的产品贵得多", "ขวดที่ระบุอายุแพงกว่ามาก"),
 "오래 숙성할수록 비싸요": ("older is pricier", "長期熟成ほど高価", "cuanto más añejo, más caro", "plus il est vieux, plus il est cher", "陈酿越久越贵", "ยิ่งบ่มนานยิ่งแพง"),
}
MAN = {
 "18년 약 67,100엔": ("18-year approx. ¥67,100", "18年 約67,100円", "18 años aprox. 67.100 ¥", "18 ans env. 67 100 ¥", "18年约67,100日元", "18 ปี ประมาณ 67,100 เยน"),
 "NV(숙성 연수 표기 없음) 700ml 정가 약 7,700엔": ("NV (no age statement) 700 ml list price approx. ¥7,700", "NV（年数表記なし）700ml 希望小売価格 約7,700円", "NV (sin edad) 700 ml, precio oficial aprox. 7.700 ¥", "NV (sans âge) 700 ml, prix conseillé env. 7 700 ¥", "NV（无年份）700ml 建议零售价约7,700日元", "NV (ไม่ระบุอายุ) 700 มล. ราคาตั้งประมาณ 7,700 เยน"),
 "캔 약 200~300엔, 병 약 1,000~2,000엔": ("can approx. ¥200–300, bottle approx. ¥1,000–2,000", "缶 約200〜300円、瓶 約1,000〜2,000円", "lata aprox. 200–300 ¥, botella aprox. 1.000–2.000 ¥", "canette env. 200–300 ¥, bouteille env. 1 000–2 000 ¥", "罐约200~300日元，瓶约1,000~2,000日元", "กระป๋องประมาณ 200–300 เยน ขวดประมาณ 1,000–2,000 เยน"),
}
rows = {}
for p in P:
    m = re.match(r'^(.*) \(([^()]+)\)$', p)
    if not m: continue
    base, note = m.groups()
    rows[base] = list(MAN[base]) if base in MAN else [F.tr(base, L) for L in range(6)]
    n = NOTES[note]
    rows['(' + note + ')'] = [f'({n[0]})', f'（{n[1]}）', f'({n[2]})', f'({n[3]})', f'（{n[4]}）', f'({n[5]})']
B = '/home/claude/i18n_work/'
open(B + 'tr_62.tsv', 'w', encoding='utf-8').write(''.join('\t'.join([k] + r[:4]) + '\n' for k, r in rows.items()))
open(B + 'zh_63.tsv', 'w', encoding='utf-8').write(''.join(k + '\t' + r[4] + '\n' for k, r in rows.items()))
open(B + 'th_63.tsv', 'w', encoding='utf-8').write(''.join(k + '\t' + r[5] + '\n' for k, r in rows.items()))
print('rows', len(rows))
