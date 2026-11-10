# 사이트 점검(2026-11-10)에서 찾은 것 고치기. html·pre, 여러 번 돌려도 안전. patch_tabs·patch_navfix·patch_festcity 다음에.
# - 메뉴 '날씨' 주소를 안내(이동) 페이지 /weather/ 대신 /tokyo/weather/ 로
# - 교통 탭(걸리는 시간·공항·교통카드) 주소는 도시 첫 지역 주소로 (다른 지역 주소는 이동 페이지라서)
# - 메뉴를 누르면 축제 달도 이번 달로
FILES = ['/home/claude/tabishiori.html', '/home/claude/i18n_work/backup/tabishiori.pre.html']
RULES = [
 ('pathOf({...st, view:a.dataset.view, city:"all", area:"all", itin:null',
  'pathOf({...st, view:a.dataset.view, city:a.dataset.view==="weather"?"tokyo":"all", area:"all", itin:null'),
 ('window.NT_BASE+LPRE+pathOf({...st,sub:k}):"#"}" data-subtab=',
  'window.NT_BASE+LPRE+pathOf({...st,sub:k,area:(st.view==="transport"&&k&&CITIES[st.city]&&areasOf(st.city)[0])?areasOf(st.city)[0].key:st.area}):"#"}" data-subtab='),
 ('if(!v.classList.contains("brand")) Object.assign(st, {', 'if(!v.classList.contains("brand")) Object.assign(st, {month:NOW_M, '),
 ('pathOf({...st,sub:"ic"})', 'pathOf({...st,sub:"ic",area:(CITIES[st.city]&&areasOf(st.city)[0])?areasOf(st.city)[0].key:st.area})'),
]
for fn in FILES:
    s = open(fn, encoding='utf-8').read()
    for old, new in RULES:
        if new in s: continue
        assert s.count(old) == 1, (fn, old[:50], s.count(old))
        s = s.replace(old, new)
    open(fn, 'w', encoding='utf-8').write(s); print('ok', fn)
