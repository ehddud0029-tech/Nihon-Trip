# 페이지 안 중복 정리 (2026-11 사용자 요청, 1·4번)
# - 쇼핑: 맨 위 요약 칸의 '쇼핑 명소'(아래 카드와 같음) → '사 갈 만한 선물' 3개(아래 특산물·선물로 이동),
#         '면세·쇼핑 안내'에서 면세 설명(아래 TAX FREE 칸과 같음)·기념품을 빼고 '쇼핑 팁'(팁·영업시간·결제)
# - 맛집: 요약 칸 '추천 맛집'은 지금 보는 메뉴를 뺀 다른 메뉴 1위(누르면 그 메뉴로), AutoReserve 예약 링크는 아래 목록에만
# (교통 2건은 patch_ttabs.py) html·backup pre에 같이 적용, 여러 번 돌려도 안전 (patch_brief.py·patch_festcity.py 다음에).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
import json as _j, re as _re, subprocess as _sp
def _arjp():
    js = r'''global.window={};require("/home/claude/site/autoreserve.js");require("/home/claude/i18n/ja.js");const D=window.I18N.D,S=window.AR_SHOPS,L=window.AR_LISTS,G={};
      const pref={tokyo:"東京",osaka:"大阪",kyoto:"京都",hyogo:"兵庫",nara:"奈良",fukuoka:"福岡",oita:"大分",hokkaido:"北海道",okinawa:"沖縄",aichi:"愛知",gifu:"岐阜",hiroshima:"広島",okayama:"岡山",ehime:"愛媛",kagawa:"香川",kanagawa:"神奈川"};
      for(const [slug,l] of Object.entries(L)) for(const ids of Object.values(l)) for(const i of ids) if(!G[i]) G[i]=pref[slug.split("/")[0]]||"";
      const o={}; for(const [k,v] of Object.entries(S)){ const j=D[v.n]; if(j && !/[가-힣]/.test(j)) o[k]=j+(G[k]?" "+G[k]:""); } console.log(JSON.stringify(o));'''
    return _sp.run(['node','-e',js],capture_output=True,text=True,check=True).stdout.strip()
AR_JP = _arjp()
R = [
 ('<li><span class="no">${i+1}</span><b class="nm">${esc(x.n)}</b>', '<li><span class="no">${i+1}</span><b class="nm">${shopHref(x)?`<a href="${esc(shopHref(x))}" target="_blank" rel="noopener">${esc(x.n)}</a>`:esc(x.n)}</b>'),
 ('["ramen","washoku","izakaya"].map(m=>{const x=arShops(pa,m,1)[0]; return x?{...x,m}:null;}).filter(Boolean)',
  'Object.keys(MENU).filter(m=>m!==st.menu).map(m=>{const x=arShops(pa,m,1)[0]; return x?{...x,m}:null;}).filter(Boolean).slice(0,3)'),
 ('gpP ? Object.keys(MENU).flatMap(m=>arShops(pa,m,3)', 'gpP ? Object.keys(MENU).filter(m=>m!==st.menu).flatMap(m=>arShops(pa,m,3)'),
 ('<ol class="picks">${picks.map(x=>`<li><span class="pick"><b>${esc(x.n)}</b><em class="pm">${esc(MENU[x.m].ko.split("·")[0])}</em><span class="pd">${esc(x.dish||"")}</span></span></li>`).join("")}</ol>',
  '<ol class="picks">${picks.map(x=>`<li><button type="button" class="pick" data-chip="menu" data-v="${x.m}"><b>${esc(x.n)}</b><em class="pm">${esc(MENU[x.m].ko.split("·")[0])}</em><span class="pd">${esc(x.dish||"")}</span></button></li>`).join("")}</ol>'),
 ('<ol class="picks">${picks.map(x=>`<li><button type="button" class="pick" data-chip="menu" data-v="${x.m}"><b>${esc(x.n)}</b><em class="pm">${esc(MENU[x.m].ko.split("·")[0])}</em><span class="pd">${esc(x.dish||"")}</span></button></li>`).join("")}</ol>',
  '<ol class="picks">${picks.map(x=>`<li><a class="pick" href="${esc(shopHref(x)||"#")}" target="_blank" rel="noopener"><b>${esc(x.n)}</b><em class="pm">${esc(MENU[x.m].ko.split("·")[0])}</em><span class="pd">${esc(x.dish||"")}</span></a></li>`).join("")}</ol>'),
 (':`<dd class="sub"><a href="${esc(arUrl(pa,"all"))}" target="_blank" rel="noopener sponsored">AutoReserve에서 예약하기 ↗</a></dd>`', ':`<dd class="sub">메뉴를 누르면 아래 목록이 그 메뉴로 바뀌어요</dd>`'),
 (':`<dd class="sub">메뉴를 누르면 아래 목록이 그 메뉴로 바뀌어요</dd>`', ':``'),
 ('      const own = A ? SHOPS.filter(it=>it.sub===A.key) : [];\n      const items = (own.length ? own : inArea(SHOPS)).slice(0,3);\n      topicCell = `<div class="bshop"><dt>${esc(where)} 쇼핑 명소</dt>${items.length?pickList(items, x=>x.cat.split("·")[0], x=>x.station||""):`<dd class="sub">등록된 쇼핑 명소가 없어요</dd>`}</div>`;',
  '      const gl = GIFTS.filter(x=>x.city===st.city), inA = x => A && (A.vg||A.tg||[A.key]).includes(x.sub);\n'
  '      const gs = [...gl.filter(inA), ...gl.filter(x=>!inA(x))].slice(0,3);\n'
  '      topicCell = `<div class="bgift"><dt>${esc(where)} 사 갈 만한 선물</dt>${gs.length?`<ol class="picks">${gs.map(x=>`<li><span class="pick"><b>${esc(x.name)}</b><em class="pm">${esc((AREA[x.sub]&&AREA[x.sub].ko.split("·")[0])||CITIES[x.city].ko)}</em><span class="pdx">${esc(x.desc)}</span></span></li>`).join("")}</ol><dd class="sub links"><a href="#gifts">특산물·선물 추천 전체 보기 ↓</a></dd>`:`<dd class="sub">등록된 선물 정보가 없어요</dd>`}</div>`;'),
 ('''      extraCell = `<div class="btax"><dt>면세·쇼핑 안내</dt><dd class="mv">
        <p class="mv-rail"><span>면세</span>11월 1일부터 '환급 방식'으로 바뀌어요. 가게에선 세금 포함 가격으로 사고, 출국 때 공항 세관 확인 후 돌려받아요. 여권을 꼭 챙기세요.</p>
        <p class="mv-walk"><span>기념품</span>${esc(ash?ash[0]:SOUVENIR[st.city]||"")}</p>
        ${ash?`<p class="mv-etc"><span>쇼핑 팁</span>${esc(ash[1])}</p>`:`<p class="mv-etc"><span>영업시간</span>백화점은 보통 오전 10시~오후 8시, 돈키호테 같은 할인점은 밤늦게까지 열어요.</p>`}</dd></div>`;''',
  '''      extraCell = `<div class="btax"><dt>쇼핑 팁</dt><dd class="mv">
        ${ash?`<p class="mv-etc"><span>쇼핑 팁</span>${esc(ash[1])}</p>`:""}
        <p class="mv-walk"><span>영업시간</span>백화점은 보통 오전 10시~오후 8시, 돈키호테 같은 할인점은 밤늦게까지 열어요.</p>
        <p class="mv-rail"><span>결제</span>대부분 카드와 교통카드로 낼 수 있지만, 시장과 노점은 현금이 편해요. 면세 받을 땐 여권을 챙기세요.</p></dd></div>`;'''),
 ('<section class="gifts"><div class="sechead">', '<section class="gifts" id="gifts"><div class="sechead">'),
]
BLK2 = '''/*SHOPHREF_BEGIN*/
const AR_JP = ''' + AR_JP + ''';   // AutoReserve 가게 id → 일본어 이름+지역 (가게 페이지 id가 없는 곳은 구글 지도 검색)
/* 맛집 가게 링크: AutoReserve 가게 페이지(AR_GEO의 가게 id), 구글 지도 기준 가게는 구글 지도 */
const shopHref = x => x.g ? gpMap(null, x.jp) : (((window.AR_GEO||{})[x.id]||[])[2] ? `https://autoreserve.com/${(window.I18N&&window.I18N.ar)||"ko"}/restaurants/${window.AR_GEO[x.id][2]}` : AR_JP[x.id] ? "https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(AR_JP[x.id]) : "");
/*SHOPHREF_END*/
'''
CSS = "/*DDCSS_BEGIN*/\nol.arlist .nm a{color:inherit;text-decoration:none}ol.arlist .nm a:hover{color:var(--shu);text-decoration:underline;text-underline-offset:3px}.brief .picks a.pick{cursor:pointer;text-decoration:none}.brief .picks a.pick:hover b{color:var(--shu);text-decoration:underline;text-underline-offset:3px}\n.brief>.bgift>dt::before{content:\"🎁\"}\n.gifts{scroll-margin-top:150px}@media (max-width:599px){.gifts{scroll-margin-top:76px}}\n/*DDCSS_END*/\n"
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    for a, b in R:
        if b in s: continue
        if s.count(a) == 0: print('  (없음: 이미 다음 규칙으로 바뀌었거나 pre에 없음)', a[:40]); continue
        assert s.count(a) == 1, (f, a[:70], s.count(a)); s = s.replace(a, b)
    s = block(s, '/*SHOPHREF_BEGIN*/', '/*SHOPHREF_END*/', BLK2, 'const ALL = [...SPOTS')
    s = block(s, '/*DDCSS_BEGIN*/', '/*DDCSS_END*/', CSS, '/*BRCSS_BEGIN*/')
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
