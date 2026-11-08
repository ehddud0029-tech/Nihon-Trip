# 여행 추천 '여행하기 좋은 도시'로 들어간 뒤 보이는 'N월 추천' 칸(st.focus)을 계속 남겨요 (2026-11 사용자 요청)
# 전에는 메뉴·도시·지역·분류·달을 누르면 지워졌어요. 이제 같은 화면 종류(관광지/축제)라면 그 도시나 일본 전체 화면에서 계속 보여요.
# 첫 화면(여행 추천)으로 돌아가거나 다른 추천을 누르면 바뀌어요. html·backup pre에 같이 적용, 여러 번 돌려도 안전 (patch_navfix.py 다음에).
W = '/home/claude'
R = [
 ('    return `<div class="sechead"><div><h2>관광지</h2><p>지역과 하위 지역을', '    return `${focusBox()}<div class="sechead"><div><h2>관광지</h2><p>지역과 하위 지역을'),
 ('  const f = st.focus; if(!f || f.city!==st.city) return "";', '  const f = st.focus; if(!f || (f.view && f.view!==st.view) || (st.city!=="all" && f.city!==st.city)) return "";'),
 ('st.focus={ids:t.ids||[],why,city:k,m:st.hm||NOW_M};', 'st.focus={ids:t.ids||[],why,city:k,m:st.hm||NOW_M,view:st.view};'),
 ('  if(e.target.closest("[data-city],[data-area],[data-view],[data-chip],[data-month]")) st.focus=null;\n', ''),
]
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    for a, b in R:
        if b and b in s: continue
        if not b and a not in s: continue
        assert s.count(a) == 1, (f, a[:50]); s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
