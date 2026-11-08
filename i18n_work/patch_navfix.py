# 메뉴(상단·하단 탭) 링크가 지금 보고 있는 상태를 따라가지 않게: '추천 일정'은 항상 일정 목록, '여행 준비'는 첫 섹션으로
# (전에는 정적 페이지 생성 때 마지막으로 그린 일정이 남아 모든 장소 페이지의 '추천 일정' 링크가 오키나와 일정으로 가 있었어요)
# html과 backup pre에 같이 적용 (여러 번 돌려도 안전)
FILES = ['/home/claude/tabishiori.html', '/home/claude/i18n_work/backup/tabishiori.pre.html']
A = 'if(ROUTED) a.setAttribute("href", window.NT_BASE + LPRE + pathOf({...st, view:a.dataset.view, city:a.dataset.view==="home"?"all":st.city}));'
B = 'if(ROUTED) a.setAttribute("href", window.NT_BASE + LPRE + pathOf({...st, view:a.dataset.view, city:a.dataset.view==="home"?"all":st.city, itin:a.dataset.view==="itin"?null:st.itin, gsec:a.dataset.view==="guide"&&st.view!=="guide"?null:st.gsec}));'
for f in FILES:
    s = open(f, encoding='utf-8').read()
    if B not in s and 'view:a.dataset.view, city:"all"' not in s:  # 아래 MENU_RESET로 이미 바뀐 줄이면 건너뜀
        assert s.count(A) == 1, (f, s.count(A))
        s = s.replace(A, B)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)

# 추천 일정의 장소 버튼을 장소 페이지 링크(<a>)로: 누르면 지금처럼 상세 창이 열리고, 검색엔진은 장소 페이지로 따라갈 수 있어요
A2 = '<li><button type="button" class="istop" data-open="${id}" style="--c:var(${colorOf(it)})">'
B2 = '<li><a class="istop" href="${PLACE_TYPES.includes(it.type)?placeHref(id):"#"}" data-open="${id}" style="--c:var(${colorOf(it)})">'
A3 = '<span class="iar">›</span></button></li>`;'
B3 = '<span class="iar">›</span></a></li>`;'
CSS = '/*ISTOPA*/a.istop{text-decoration:none;color:inherit}\n'
for f in FILES + ['/home/claude/sitegen/itin_view.js']:
    s = open(f, encoding='utf-8').read()
    for a, b in [(A2, B2), (A3, B3)]:
        if b in s: continue
        assert s.count(a) == 1, (f, a[:40], s.count(a))
        s = s.replace(a, b)
    if f.endswith('.html') and '/*ISTOPA*/' not in s:
        anc = 'footer{border-top:1px solid var(--line);'
        assert s.count(anc) == 1; s = s.replace(anc, CSS + anc)
    open(f, 'w', encoding='utf-8').write(s); print('itin links', f)

# 장소 페이지 → 그 장소가 들어간 추천 일정 링크 (내부 링크 강화)
FN = ('/*PITIN*/function placeItins(it){ if(typeof ITIN==="undefined"||!it) return "";\n'
      '  const L=ITIN.filter(c=>c.plan.some(d=>d.s.includes(it.id))); if(!L.length) return "";\n'
      '  return `<div class="gblk pitin"><h4>이 장소가 들어간 추천 일정</h4><ul class="gul">${L.map(c=>`<li><a href="${itinHref(c.key)}" data-itin="${c.key}">${esc(c.title)}</a></li>`).join("")}</ul></div>`; }\n')
A4 = '   ${typeof shopPlus==="function"?shopPlus(it):""}'
B4 = '   ${typeof placeItins==="function"?placeItins(it):""}\n' + A4
for f in FILES:
    s = open(f, encoding='utf-8').read()
    if '/*PITIN*/' not in s:
        anc = 'function detailHTML('; assert s.count(anc) == 1; s = s.replace(anc, FN + anc)
    if B4 not in s:
        assert s.count(A4) == 1, (f, s.count(A4)); s = s.replace(A4, B4)
    open(f, 'w', encoding='utf-8').write(s); print('place itins', f)

# 메뉴를 누르면 어느 메뉴든 항상 첫 페이지(전체)로: 보고 있던 도시·동네·날씨 월·공항 선택을 넘기지 않아요 (2026-11)
MENU_RESET = 'city:"all", area:"all", itin:null, gsec:null, ap:"", apk:"", wm:0, sub:""'   # 여행 추천의 '이달 추천'(focus)은 남겨 둠 (patch_focus.py)
OLD_RESET2 = 'city:"all", area:"all", itin:null, gsec:null, ap:"", apk:"", wm:0, focus:null, sub:""'
OLD_RESET = 'city:"all", area:"all", itin:null, gsec:null, ap:"", apk:"", wm:0, focus:null'
B4 = 'if(ROUTED) a.setAttribute("href", window.NT_BASE + LPRE + pathOf({...st, view:a.dataset.view, ' + MENU_RESET + '}));'
A5 = 'if(v){ e.preventDefault(); if(v.dataset.view==="itin") st.itin=""; go(v.dataset.view); return; }'
B5 = 'if(v){ e.preventDefault(); if(!v.classList.contains("brand")) Object.assign(st, {' + MENU_RESET + '}); if(v.dataset.view==="itin") st.itin=""; go(v.dataset.view); return; }'
for f in FILES:
    s = open(f, encoding='utf-8').read()
    s = s.replace(B4.replace(MENU_RESET, OLD_RESET2), B4).replace(B5.replace(MENU_RESET, OLD_RESET2), B5)
    s = s.replace(B4.replace(MENU_RESET, OLD_RESET), B4).replace(B5.replace(MENU_RESET, OLD_RESET), B5)  # 예전 MENU_RESET 줄 업그레이드
    if B4 not in s:
        assert s.count(B) == 1, (f, 'B', s.count(B)); s = s.replace(B, B4)
    if B5 not in s:
        assert s.count(A5) == 1, (f, 'A5', s.count(A5)); s = s.replace(A5, B5)
    open(f, 'w', encoding='utf-8').write(s); print('menu reset', f)
