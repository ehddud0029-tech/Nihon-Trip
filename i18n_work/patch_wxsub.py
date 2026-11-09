# 소도시 날씨(교토·나라·다카야마·하코다테·이시가키, 2026-11): 데이터·이름(wxNm)은 sitegen/weather_view.js.
# 여기서는 patch_weather·patch_wxtokyo·patch_tabs가 넣은 줄 중 CITIES[...]로 이름을 찾거나 주소를 읽는 곳을 WXN·wxNm으로 고쳐요.
# html·backup pre·gen.py에 같이, 여러 번 돌려도 안전. patch_weather.py → patch_wxtokyo.py → patch_tabs.py 다음에 돌려 주세요.
import re
W = '/home/claude'
R = [
 ('o={a:T(CITIES[c].ko), m:mon(m)', 'o={a:T(wxNm(c)), m:mon(m)'),
 ('  else if(!m){ k="c"; o={a:T(CITIES[c].ko)}; }', '  else if(!m){ k="c"; o={a:T(wxNm(c))}; }'),
 ('  if(CITIES[seg[0]]&&seg[1]==="weather"){ st.view="weather";', '  if((CITIES[seg[0]]||WXN[seg[0]])&&seg[1]==="weather"){ st.view="weather";'),
 ('  if(CITIES[seg[0]]&&seg[1]==="weather"&&n===3&&["outfit","faq"].includes(l)) return l;', '  if((CITIES[seg[0]]||WXN[seg[0]])&&seg[1]==="weather"&&n===3&&["outfit","faq"].includes(l)) return l;'),
 ('  else if(st.view==="weather"){ key=`weather:c:${st.sub}`; o.a=T(CITIES[st.city].ko); }', '  else if(st.view==="weather"){ key=`weather:c:${st.sub}`; o.a=T(wxNm(st.city)); }'),
 ('st.month=+wxf.dataset.m; st.city=c; st.area="all"; st.view="festivals";', 'st.month=+wxf.dataset.m; st.city=c; st.area=wxf.dataset.wxarea||"all"; st.view="festivals";'),
]
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    i, j = s.find('/*WX_BEGIN*/'), s.find('/*WX_END*/')
    if i > 0: s = s[:i] + s[i:j].replace('esc(CITIES[c].ko)', 'esc(wxNm(c))').replace('esc(CITIES[k].ko)', 'esc(wxNm(k))') + s[j:]
    for a, b in R:
        if b in s: continue
        if a not in s: print('  (없음)', f[-20:], a[:50]); continue
        s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
G = f'{W}/sitegen/gen.py'; s = open(G, encoding='utf-8').read()
a = "'okinawa/weather/', 'nagoya/weather/', 'hiroshima/weather/', 'shikoku/weather/']"
b = "'okinawa/weather/', 'nagoya/weather/', 'hiroshima/weather/', 'shikoku/weather/', 'kyoto/weather/', 'nara/weather/', 'takayama/weather/', 'hakodate/weather/', 'ishigaki/weather/']"
if b not in s and a in s: s = s.replace(a, b)
open(G, 'w', encoding='utf-8').write(s); print('gen', b in s)
