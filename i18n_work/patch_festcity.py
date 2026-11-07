# 축제 화면은 도시 단위: 하위 지역 버튼 숨김, 제목은 도시만, 주소는 도시의 첫 지역(<도시>/<첫 지역>/festivals/) 하나로 (2026-11 사용자 요청)
# 축제 목록은 원래 도시 기준이라 지역을 눌러도 내용이 같았어요. gen.py는 다른 지역 축제 주소를 만들지 않고 MOVED로 대표 주소에 보내요.
# html·backup pre·gen.py에 같이 적용, 여러 번 돌려도 안전. region_inject 뒤에 다시 돌려 주세요.
W = '/home/claude'
HTML = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
R = [
 ('const cityName = () => curArea() ?', 'const cityName = () => curArea() && st.view!=="festivals" ?'),
 ('  const c = CITIES[st.city], A = curArea();\n  $("#areas").hidden = !c;\n',
  '  const c = CITIES[st.city], A = st.view==="festivals" ? null : curArea();\n  $("#areas").hidden = !c || st.view==="festivals";\n'),
 ('  return `${s.city}/${s.area}/${s.view}/`;\n}',
  '  if(s.view==="festivals" && areasOf(s.city)[0]) return `${s.city}/${areasOf(s.city)[0].key}/festivals/`;\n  return `${s.city}/${s.area}/${s.view}/`;\n}'),
]
def rep(s, f):
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (f, a[:60], s.count(a)); s = s.replace(a, b)
    return s
for f in HTML:
    s = rep(open(f, encoding='utf-8').read(), f); open(f, 'w', encoding='utf-8').write(s); print('patched', f)
G = f'{W}/sitegen/gen.py'; s = open(G, encoding='utf-8').read()
a = 'if(v!=="transport"||tgRep(a.key)===a.key){ r.push(`${c}/${a.key}/${v}/`);'
b = 'if((v!=="transport"||tgRep(a.key)===a.key)&&(v!=="festivals"||a.key===areasOf(c)[0].key)){ r.push(`${c}/${a.key}/${v}/`);'
if b not in s: assert s.count(a) == 1; s = s.replace(a, b)
a = "              return r; }''')\n"
b = a + "            if not any(k.endswith('/festivals/') for k in MOVED): MOVED.update(dict(pg.evaluate('''()=>Object.keys(CITIES).flatMap(c=>areasOf(c).slice(1).map(a=>[`${c}/${a.key}/festivals/`,`${c}/${areasOf(c)[0].key}/festivals/`]))''')))   # 축제는 도시 단위 (i18n_work/patch_festcity.py)\n"
if b not in s: assert s.count(a) == 1; s = s.replace(a, b)
open(G, 'w', encoding='utf-8').write(s); print('gen ok')
