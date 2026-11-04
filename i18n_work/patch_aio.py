# AI·검색 인용용 구조화 데이터: 추천 일정 상세에 TouristTrip 마이크로데이터 (html·backup pre·sitegen/itin_view.js에 같이 적용, 여러 번 돌려도 안전)
W = '/home/claude'
R = [
 ('''  return `<div class="itin">
   <a class="iback"''', '''  return `<div class="itin" itemscope itemtype="https://schema.org/TouristTrip">
   <a class="iback"'''),
 ('<h2>${esc(c.title)}</h2><p>${esc(c.sum)}</p>', '<h2 itemprop="name">${esc(c.title)}</h2><p itemprop="description">${esc(c.sum)}</p>'),
 ('<ol class="idays">${c.plan.map((d,i)=>`<li class="iday">', '<ol class="idays" itemprop="itinerary" itemscope itemtype="https://schema.org/ItemList">${c.plan.map((d,i)=>`<li class="iday" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem"><meta itemprop="position" content="${i+1}">'),
 ('<h3>${esc(d.t)}</h3>', '<h3 itemprop="name">${esc(d.t)}</h3>'),
]
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html', f'{W}/sitegen/itin_view.js']:
    s = open(f, encoding='utf-8').read(); n = 0
    for a, b in R:
        if b in s: continue
        if s.count(a) != 1: print('  not found', f.split('/')[-1], a[:50]); continue
        s = s.replace(a, b); n += 1
    open(f, 'w', encoding='utf-8').write(s); print(f.split('/')[-1], n, 'changes')
