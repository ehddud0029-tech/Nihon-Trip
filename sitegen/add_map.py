import json
p = '/home/claude/tabishiori.html'
s = open(p, encoding='utf-8').read()
js = open('/home/claude/sitegen/map_view.js', encoding='utf-8').read()
anchor = '\n/* 화면별 주소 (배포 사이트에서만)'
assert anchor in s and 'V.map = ' not in s
s = s.replace(anchor, '\n' + js + anchor, 1)
old = '''function render(){
  if(st.view==="home"){ st.city="all"; }'''
new = '''function render(){
  document.body.classList.toggle("is-map", st.view==="map");
  if(st.view!=="map" && MAP){ try{ MAP.remove(); }catch(_){} MAP=null; MAPREADY=false; }
  if(st.view==="map"){ setNav(); if(!$("#mapwrap")){ $("#main").innerHTML = V.map(); mapMount(); } syncUrl(); return; }
  if(st.view==="home"){ st.city="all"; }'''
assert old in s
s = s.replace(old, new, 1)
a = '  if(s.view==="saved") return "saved/";\n  if(s.city==="all")'
assert a in s
s = s.replace(a, '  if(s.view==="saved") return "saved/";\n  if(s.view==="map") return "map/";\n  if(s.city==="all")', 1)
a = '  if(seg[0]==="saved"){ st.view="saved"; return; }'
assert a in s
s = s.replace(a, a + '\n  if(seg[0]==="map"){ st.view="map"; return; }', 1)
a = 'st.view=VIEWS.includes(seg[2])&&seg[2]!=="home"&&seg[2]!=="saved"?seg[2]:"spots";'
assert a in s
s = s.replace(a, 'st.view=VIEWS.includes(seg[2])&&!["home","saved","map"].includes(seg[2])?seg[2]:"spots";')
a = 'const key = st.view==="saved" ? "saved" :'
assert a in s
s = s.replace(a, 'const key = st.view==="saved" ? "saved" : st.view==="map" ? "map" :')
add = {'ko': ('일본 여행 지도 – 관광지·축제·맛집·쇼핑 위치', '관광지·축제·맛집·쇼핑 장소를 일본 지도에서 한눈에 보세요. 지역과 종류를 골라 위치와 정보를 확인할 수 있어요.'),
       'en': ('Japan Travel Map – Sights, Festivals, Restaurants & Shopping', 'See sights, festivals, restaurants and shopping spots on a map of Japan. Filter by area and type to check locations and details.'),
       'ja': ('日本旅行マップ – 観光地・祭り・グルメ・ショッピング', '観光地・祭り・グルメ・ショッピングの場所を日本地図で一目で。地域と種類を選んで位置と情報を確認できます。'),
       'es': ('Mapa de viaje de Japón – Lugares, festivales, restaurantes y compras', 'Ve lugares, festivales, restaurantes y tiendas en un mapa de Japón. Filtra por zona y tipo para ver ubicaciones y detalles.'),
       'fr': ('Carte de voyage du Japon – Sites, fêtes, restaurants et shopping', 'Voyez sites, fêtes, restaurants et adresses shopping sur une carte du Japon. Filtrez par zone et par type pour voir emplacements et détails.')}
for L, (t, d) in add.items():
    key = f' {L}:{{t:{{'
    i = s.index(key)
    j = i + len(key)
    s = s[:j] + f'map:{json.dumps(t, ensure_ascii=False)},' + s[j:]
    k = s.index('d:{', j)
    s = s[:k + 3] + f'map:{json.dumps(d, ensure_ascii=False)},' + s[k + 3:]
open(p, 'w', encoding='utf-8').write(s)
print('ok')
