# 장소 페이지 검색 제목·설명을 실용 정보 위주로 바꿔요 (html과 backup pre 파일에 같이 적용)
# - 관광지 제목의 지역 표시: 지역 묶음 이름 대신 실제 동네(it.area)를 써요 (예: 도쿄타워 → 시바코엔)
# - 관광지 설명 앞에 입장료 | 운영 시간 | 가는 길을 붙여요
# - 쇼핑 장소 제목을 '추천 쇼핑 목록·가는 길'로, 설명에 가는 길과 추천 쇼핑 목록을 넣어요
import sys
FILES = ['/home/claude/tabishiori.html', '/home/claude/i18n_work/backup/tabishiori.pre.html']

REPL = [
 ('shop:"{n} – 쇼핑 정보·추천 쇼핑 목록 ({a})"', 'shop:"{n} – 추천 쇼핑 목록·가는 길 ({a})"'),
 ('shop:"{n} – Shopping Guide & What to Buy ({a})"', 'shop:"{n} – What to Buy & How to Get There ({a})"'),
 ('shop:"{n} – ショッピング情報・おすすめの買い物（{a}）"', 'shop:"{n} – おすすめの買い物・アクセス（{a}）"'),
 ('shop:"{n} – Guía de compras y qué comprar ({a})"', 'shop:"{n} – Qué comprar y cómo llegar ({a})"'),
 ('shop:"{n} – Guide shopping et quoi acheter ({a})"', 'shop:"{n} – Quoi acheter et comment y aller ({a})"'),
 ('"shop":"{n} – 购物信息·推荐清单（{a}）"', '"shop":"{n} – 推荐购物清单·交通（{a}）"'),
 ('"shop":"{n} – 購物資訊·推薦清單（{a}）"', '"shop":"{n} – 推薦購物清單·交通（{a}）"'),
 ('const a=T((it.sub&&AREA[it.sub]?.ko.split("·")[0])||CITIES[it.city].ko), n=T(it.name);',
  'const a=(it.type==="spot"&&it.area) ? T(it.area).split(" · ")[0] : T((it.sub&&AREA[it.sub]?.ko.split("·")[0])||CITIES[it.city].ko), n=T(it.name);'),
 ('let desc=[T(it.desc),T(it.tip||"")].filter(Boolean).join(" "); if(desc.length>160) desc=desc.slice(0,157)+"…";',
  'const DL={ko:["입장료","운영","가는 길","추천 쇼핑"],en:["Admission","Open","Access","What to buy"],ja:["入場料","営業","アクセス","おすすめ"],es:["Entrada","Horario","Acceso","Qué comprar"],fr:["Entrée","Horaires","Accès","À acheter"],zh:["门票","开放","交通","推荐"],tw:["門票","開放","交通","推薦"]}[L]||["입장료","운영","가는 길","추천 쇼핑"];\n'
  '    const col=(L==="ja"||L==="zh"||L==="tw")?"：":L==="fr"?" : ":": ", sp=(L==="ja"||L==="zh"||L==="tw")?"、":", ";\n'
  '    const facts=[]; if(it.type==="spot"){ const si=SIV.rows(it.id); const fr=si&&si.rows.find(r=>r[0]==="fee"), hr=si&&si.rows.find(r=>r[0]==="hours"); if(fr) facts.push(DL[0]+col+fr[1][0]); if(hr) facts.push(DL[1]+col+hr[1][0]); }\n'
  '    if((it.type==="spot"||it.type==="shop")&&it.station) facts.push(DL[2]+col+T(it.station));\n'
  '    const picks=(it.type==="shop"&&SHOP_PICKS[it.id])?DL[3]+col+SHOP_PICKS[it.id].map(x=>T(x)).join(sp):"";\n'
  '    let desc=[facts.join(" | "),[T(it.desc),picks||T(it.tip||"")].filter(Boolean).join(" ")].filter(Boolean).join((L==="ja"||L==="zh"||L==="tw")?"。":" – "); if(desc.length>160) desc=desc.slice(0,157)+"…";'),
]

for f in FILES:
    s = open(f, encoding='utf-8').read()
    for a, b in REPL:
        if b in s:
            continue
        assert s.count(a) == 1, (f, a[:60], s.count(a))
        s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s)
    print('patched', f)
