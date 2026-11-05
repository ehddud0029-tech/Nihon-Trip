# 쇼핑 장소 영업시간·공식 사이트(층별 안내) + 장소 페이지 검색 설명 순서(소개 문장 먼저)
# html과 backup pre 파일에 같이 적용 (여러 번 돌려도 안전). 데이터는 sitegen/shop_info.js
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
VIEW = open(f'{W}/sitegen/shop_info.js', encoding='utf-8').read().strip() + '\n'
PTH = ('const PTH={ko:"{n} – 영업시간·추천 쇼핑·가는 길 ({a})",en:"{n} – Opening Hours, What to Buy & Access ({a})",'
       'ja:"{n} – 営業時間・おすすめの買い物・アクセス（{a}）",es:"{n} – Horario, qué comprar y cómo llegar ({a})",'
       'fr:"{n} – Horaires, quoi acheter et accès ({a})",zh:"{n} – 营业时间·推荐购物·交通（{a}）",tw:"{n} – 營業時間·推薦購物·交通（{a}）",'
       'th:"{n} – เวลาเปิด ของน่าซื้อ และการเดินทาง ({a})"};')
OLD_DESC = '    let desc=[facts.join(" | "),[T(it.desc),picks||T(it.tip||"")].filter(Boolean).join(" ")].filter(Boolean).join((L==="ja"||L==="zh"||L==="tw")?"。":" – "); if(desc.length>160) desc=desc.slice(0,157)+"…";'
NEW_DESC = ('    const rest=[facts.join(" | "), picks||(facts.length?"":T(it.tip||""))].filter(Boolean).join(" | ");   // 검색 설명: 소개 문장 먼저, 실용 정보는 뒤에\n'
            '    let desc=[T(it.desc),rest].filter(Boolean).join((L==="ja"||L==="zh"||L==="tw")?"":" "); if(desc.length>160) desc=desc.slice(0,157)+"…";\n    ' + PTH)
CSS = ('/*PPLUS*/.pplus{margin-top:14px;display:flex;flex-direction:column;gap:12px}.pmore{margin:0;line-height:1.7}'
       '.pfloor dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0}.pfloor dt{font-weight:700;color:var(--ink-2);white-space:nowrap}.pfloor dd{margin:0}'
       '.ptax{border-left:4px solid var(--ai)}.pplus .faq dl{margin:0}'
       '.psgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}.psub h4{margin:0 0 4px}.psw{margin:0 0 6px;font-size:13px;color:var(--ink-2)}.psub p{line-height:1.6}'
       '.psub dl{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;margin:8px 0;font-size:14px}.psub dt{color:var(--ink-2)}.psub dd{margin:0;white-space:nowrap}\n')
R = [
 ('footer{border-top:1px solid var(--line);', CSS + 'footer{border-top:1px solid var(--line);'),
 ('   <div class="actions"><button class="btn${isSaved?"":" primary"}" type="button" data-psave', '   ${typeof shopPlus==="function"?shopPlus(it):""}\n   <div class="actions"><button class="btn${isSaved?"":" primary"}" type="button" data-psave'),
 ('  if(it.station) facts.push(["가는 길",it.station]);', '  if(it.station) facts.push(["가는 길",it.station]);\n  if(typeof shopFacts==="function") shopFacts(it, facts);'),
 ('   ${SHOP_PICKS[it.id]&&it.type==="shop"?`<div class="picks2">', '   ${typeof shopNote==="function"?shopNote(it):""}\n   ${SHOP_PICKS[it.id]&&it.type==="shop"?`<div class="picks2">'),
 ('   <a class="btn" href="https://www.google.com/maps/search/?api=1&query=${mq}"', '   ${typeof shopBtn==="function"?shopBtn(it):""}\n   <a class="btn" href="https://www.google.com/maps/search/?api=1&query=${mq}"'),
 ('    if((it.type==="spot"||it.type==="shop")&&it.station) facts.push(DL[2]+col+T(it.station));', '    const shi=typeof shopInfo==="function"?shopInfo(it):null; if(shi&&shi.h) facts.push(DL[1]+col+shi.h);\n    if((it.type==="spot"||it.type==="shop")&&it.station) facts.push(DL[2]+col+T(it.station));'),
 (OLD_DESC, NEW_DESC),
 ('return {title:(PT[L]||PT.ko)[it.type].replace("{n}",n)', 'return {title:((it.type==="shop"&&shi&&shi.h&&PTH[L])||(PT[L]||PT.ko)[it.type]).replace("{n}",n)'),
 ('address:{"@type":"PostalAddress",addressCountry:"JP",addressRegion:T(CITIES[it.city].ko)}};', 'address:{"@type":"PostalAddress",addressCountry:"JP",addressRegion:T(CITIES[it.city].ko)},...(shi&&shi.u?{url:shi.u}:{}),...(shi&&shi.h?{openingHours:"Mo-Su "+shi.h.replace("–","-")}:{})};'),
]
def block(s, b, e, body, anchor):
    if b in s:
        i = s.index(b); j = s.index(e, i) + len(e)
        return s[:i] + body.strip() + s[j:]
    assert s.count(anchor) == 1, anchor
    return s.replace(anchor, body + anchor)
for f in FILES:
    s = open(f, encoding='utf-8').read()
    s = block(s, '/*SHOPINFO_BEGIN*/', '/*SHOPINFO_END*/', VIEW, 'function detailHTML(')
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (f, a[:70], s.count(a))
        s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s)
    print('patched', f)
