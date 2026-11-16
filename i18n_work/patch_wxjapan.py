# 일본 전체 월별 날씨 페이지 되살리기 (2026-11-16, 사용자 결정).
# 11월 7일 patch_wxtokyo.py로 weather/·weather/<월>/을 도쿄로 보냈는데, 검색 노출이 많던 페이지('日本3月天氣' 등)라 다시 살려요.
# 메뉴 '날씨'는 그대로 도쿄 날씨로 가고, weather/·weather/<월>/ 주소와 '전체' 도시 버튼·이동 경로 첫 칸만 되살려요.
# patch_wxtokyo.py 다음에 돌려요(html·backup pre·gen.py, 여러 번 돌려도 안전). region_inject 뒤에도 patch_wxtokyo → 이 스크립트 순서로.
W = '/home/claude'
R = [
 # 날씨 화면: 도시가 잘못된 값일 때만 도쿄로 ('all'은 일본 전체 화면)
 ('  if(st.view==="weather" && !(WXN[st.city] && st.city!=="all")) st.city = "tokyo";',
  '  if(st.view==="weather" && st.city!=="all" && !WXN[st.city]) st.city = "tokyo";'),
 # 메뉴를 누르면 날씨는 도쿄로 (주소 weather/는 일본 전체)
 ('Object.assign(st, {month:NOW_M, city:"all", area:"all", itin:null, gsec:null, ap:"", apk:"", wm:0, sub:""});',
  'Object.assign(st, {month:NOW_M, city:v.dataset.view==="weather"?"tokyo":"all", area:"all", itin:null, gsec:null, ap:"", apk:"", wm:0, sub:""});'),
 ('  if(seg[0]==="weather"){ st.view="weather"; st.city="tokyo";', '  if(seg[0]==="weather"){ st.view="weather"; st.city="all";'),
 ('  const list = [...(st.view==="weather"?[]:[["all","전체","日本"]]),...Object.entries(CITIES).map(([k,v])=>[k,v.ko,v.jp])];',
  '  const list = [["all","전체","日本"],...Object.entries(CITIES).map(([k,v])=>[k,v.ko,v.jp])];'),
 ('const wxHref = (c,m) => (c==="all"&&(c="tokyo"), ROUTED ? window.NT_BASE + LPRE + (c==="all" ?', 'const wxHref = (c,m) => (ROUTED ? window.NT_BASE + LPRE + (c==="all" ?'),
 ('  const crumb = `<nav class="wxcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">${c!=="all"?bc(1,wxA(c,0,esc(wxNm(c)))):""}</nav>`;',
  '  const crumb = `<nav class="wxcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">${bc(1,wxA("all",0,"일본 월별 날씨와 옷차림"))}${c!=="all"?` <i>›</i> ${bc(2,wxA(c,0,esc(wxNm(c))))}`:""}</nav>`;'),
]
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (f, a[:60], s.count(a)); s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)

G = f'{W}/sitegen/gen.py'; s = open(G, encoding='utf-8').read()
for a, b in [
    ("MOVED = {'guide/stay/': 'stay/', 'weather/': 'tokyo/weather/', **{f'weather/{m}/': f'tokyo/weather/{m}/' for m in range(1, 13)}}   # 날씨 첫 화면은 도쿄 (patch_wxtokyo.py)",
     "MOVED = {'guide/stay/': 'stay/'}   # 일본 전체 날씨(weather/)는 2026-11-16 되살림 (patch_wxjapan.py)"),
    ("sec('Weather and what to wear by month (Tokyo; other cities from the city buttons)', 'tokyo/weather/')",
     "sec('Weather and what to wear by month (all of Japan)', 'weather/')"),
    ('r.push("airport/"); for(const a of Object.keys(APS))',
     'r.push("weather/"); for(let m=1;m<=12;m++) r.push(`weather/${m}/`); r.push("airport/"); for(const a of Object.keys(APS))'),
]:
    if b in s: continue
    assert s.count(a) == 1, ('gen', a[:60]); s = s.replace(a, b)
open(G, 'w', encoding='utf-8').write(s); print('gen ok')
