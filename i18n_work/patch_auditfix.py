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

# 2차(2026-11-10): 지역 이름이 도시 이름으로 시작하면 제목에 도시를 두 번 쓰지 않기, 날씨 안내 줄은 여행 추천(첫 화면)에서만,
# 다른 h1이 있는 화면(장소 상세·지도·소개 등)에서는 맨 위 제목을 h1 대신 div로
RULES2 = [
 ('A ? `${c.ko} · ${A.ko}, 무엇부터 볼까요?`', 'A ? (A.ko.startsWith(c.ko+" ") ? `${A.ko} 여행, 무엇부터 볼까요?` : `${c.ko} · ${A.ko}, 무엇부터 볼까요?`)'),
 ('  document.body.classList.remove("nowx");\n', '  document.body.classList.toggle("nowx", st.view!=="home" && st.view!=="saved");\n'),
 ('.hero h1{', '.hero h1,.hero #heroTitle{'),
 ('function setNav(){\n', 'function fixH1(){ const h=document.getElementById("heroTitle"); if(!h) return; const others=[...document.querySelectorAll("h1")].filter(x=>x!==h).length, want=others?"DIV":"H1"; if(h.tagName===want) return; const n=document.createElement(want); for(const a of h.attributes) n.setAttribute(a.name,a.value); n.textContent=h.textContent; h.replaceWith(n); }\nfunction setNav(){\n  setTimeout(fixH1,0);\n'),
]
for fn in FILES:
    s = open(fn, encoding='utf-8').read()
    for old, new in RULES2:
        if new in s: continue
        assert s.count(old) == 1, (fn, old[:50], s.count(old))
        s = s.replace(old, new)
    open(fn, 'w', encoding='utf-8').write(s); print('ok2', fn)

# 3차(2026-11-11): 장소 상세 창(drawer)을 뒤로 가기로 닫기 — 창을 열 때 기록을 하나 쌓고, 뒤로 가면 창만 닫음
RULES3 = [
 ('  $("#closeD").onclick=closeItem;\n}\nfunction closeItem(){', '  $("#closeD").onclick=closeDrawer;\n  try{ if(!(history.state&&history.state.drawer)) history.pushState({drawer:id},"",location.href) }catch(_){}\n}\nfunction closeDrawer(){ if(history.state&&history.state.drawer){ try{ history.back(); return }catch(_){} } closeItem(); }\nfunction closeItem(){'),
 ('$("#scrim").onclick=closeItem;', '$("#scrim").onclick=closeDrawer;'),
 ('if(e.key==="Escape"&&!$("#drawer").hidden) closeItem()', 'if(e.key==="Escape"&&!$("#drawer").hidden) closeDrawer()'),
 ('window.addEventListener("popstate",()=>{ if(ROUTED){', 'window.addEventListener("popstate",()=>{ const dr=document.getElementById("drawer"), ds=history.state&&history.state.drawer; if(dr&&!dr.hidden){ closeItem(); if(!ds) return; } if(ds){ try{history.replaceState(null,"",location.href)}catch(_){} } if(ROUTED){'),
]
for fn in FILES:
    s = open(fn, encoding='utf-8').read()
    for old, new in RULES3:
        if new in s: continue
        assert s.count(old) == 1, (fn, old[:50], s.count(old))
        s = s.replace(old, new)
    open(fn, 'w', encoding='utf-8').write(s); print('ok3', fn)
