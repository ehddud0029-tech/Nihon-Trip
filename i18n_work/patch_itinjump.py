# 추천 일정 목록 맨 위에 도시 버튼(같은 페이지 안 그 도시 일정으로 이동, 숙소·술 전체 페이지의 stjump와 같은 방식)
# (patch_itincity.py가 이 버튼을 도시 페이지 링크로 바꿔요)
# html·backup pre·sitegen/itin_view.js에 같이 적용 (여러 번 돌려도 안전). region_inject 뒤에도 다시 돌려 주세요.
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html', f'{W}/sitegen/itin_view.js']
A = '장소를 누르면 입장료와 가는 길을 볼 수 있어요.</p></div>\n     ${ICITY_ORDER.map(k=>{ const g=ITIN.filter(x=>x.city===k); return g.length?`<section class="igrp">'
B = '장소를 누르면 입장료와 가는 길을 볼 수 있어요.</p></div>\n     <nav class="wxmon stjump ijump">${ICITY_ORDER.filter(k=>ITIN.some(x=>x.city===k)).map(k=>`<a href="#st-${k}" data-stjump="${k}">${esc(CITIES[k].ko)}</a>`).join("")}</nav>\n     ${ICITY_ORDER.map(k=>{ const g=ITIN.filter(x=>x.city===k); return g.length?`<section class="igrp" id="st-${k}">'
CSS_ANCHOR = 'footer{border-top:1px solid var(--line);'
CSS = '.itin .ijump{margin:14px 0 20px}.itin .igrp{scroll-margin-top:150px}@media (max-width:599px){.itin .igrp{scroll-margin-top:76px}}\n'
for f in FILES:
    s = open(f, encoding='utf-8').read()
    if B not in s and 'class="wxmon ijump"' not in s:
        assert s.count(A) == 1, (f, s.count(A)); s = s.replace(A, B)
    if f.endswith('.html') and CSS not in s:
        assert CSS_ANCHOR in s; s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
