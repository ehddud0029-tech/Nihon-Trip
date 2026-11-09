# 날씨 메뉴는 바로 도쿄 날씨부터 (2026-11 사용자 요청: 일본 전체 날씨 첫 화면 삭제).
# 날씨 화면에서 도시가 '전체'면 도쿄로, '전체' 도시 버튼은 숨김, weather/ · weather/<월>/ 주소는 gen.py MOVED로 tokyo/weather/…로 보냄.
# html·backup pre·gen.py에 같이 적용, 여러 번 돌려도 안전. region_inject 뒤에 다시 돌려 주세요.
W = '/home/claude'
R = [
 ('function render(){\n  if(st.view==="transport" && st.area!=="all")',
  'function render(){\n  if(st.view==="weather" && !(WXN[st.city] && st.city!=="all")) st.city = "tokyo";\n  if(st.view==="transport" && st.area!=="all")'),
 ('  const list = [["all","전체","日本"],...Object.entries(CITIES).map(([k,v])=>[k,v.ko,v.jp])];',
  '  const list = [...(st.view==="weather"?[]:[["all","전체","日本"]]),...Object.entries(CITIES).map(([k,v])=>[k,v.ko,v.jp])];'),
 ('  if(seg[0]==="weather"){ st.view="weather"; st.city="all";', '  if(seg[0]==="weather"){ st.view="weather"; st.city="tokyo";'),
 ('const wxHref = (c,m) => ROUTED ? window.NT_BASE + LPRE + (c==="all" ?', 'const wxHref = (c,m) => (c==="all"&&(c="tokyo"), ROUTED ? window.NT_BASE + LPRE + (c==="all" ?'),
 ('`${c}/weather/${m}/`:`${c}/weather/`)) : "#weather";', '`${c}/weather/${m}/`:`${c}/weather/`)) : "#weather");'),
 ('  const crumb = `<nav class="wxcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">${bc(1,wxA("all",0,"일본 월별 날씨와 옷차림"))}${c!=="all"?` <i>›</i> ${bc(2,wxA(c,0,esc(wxNm(c))))}`:""}</nav>`;',
  '  const crumb = `<nav class="wxcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">${c!=="all"?bc(1,wxA(c,0,esc(wxNm(c)))):""}</nav>`;'),
]
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (f, a[:60], s.count(a)); s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
G = f'{W}/sitegen/gen.py'; s = open(G, encoding='utf-8').read()
for a, b in [('r.push("weather/"); for(let m=1;m<=12;m++) r.push(`weather/${m}/`);', ''),
             ("sec('Weather and what to wear by month (all of Japan)', 'weather/')", "sec('Weather and what to wear by month (Tokyo; other cities from the city buttons)', 'tokyo/weather/')"),
             ("MOVED = {'guide/stay/': 'stay/'}", "MOVED = {'guide/stay/': 'stay/', 'weather/': 'tokyo/weather/', **{f'weather/{m}/': f'tokyo/weather/{m}/' for m in range(1, 13)}}   # 날씨 첫 화면은 도쿄 (patch_wxtokyo.py)")]:
    if a in s: s = s.replace(a, b)
open(G, 'w', encoding='utf-8').write(s); print('gen ok', "'weather/': 'tokyo/weather/'" in s)
