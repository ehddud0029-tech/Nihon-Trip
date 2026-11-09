# 축제·맛집 화면 지역 묶기 (2026-11 사용자 요청, 예전 '축제는 도시 단위' 패치를 바꿈)
# - 축제: 도시 전체(<도시>/festivals/) + 지역 묶음(<도시>/<대표 지역>/festivals/, 예: 도쿄 시내·하코네·후지산). 위에 '전체'+묶음 버튼.
# - 맛집: 교토 5개 지역 → '교토' 하나(기온 AutoReserve 목록 아래에 교토역·아라시야마·난젠지·우지 구글 지도 인기 가게),
#         같은 AutoReserve 목록을 쓰던 우메다·덴마, 하카타·나카스, 국제거리·나하도 하나로.
# 묶음 데이터는 VGROUPS(아래 BLK). 묶음 안 다른 지역 주소는 gen.py MOVED로 대표 주소에 보내요.
# html·backup pre·gen.py·verify2에 같이 적용, 여러 번 돌려도 안전. patch_tgroup.py·patch_brief.py 다음에, region_inject 뒤에 다시 돌려 주세요.
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
HTML = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
FEST = {
 "tokyo":   [["도쿄 시내", ["shinjuku","shibuya","ginza","asakusa","tokyoeki"]], ["요코하마·가마쿠라", ["kamakura","yokohama"]], ["하코네·후지산", ["fuji","hakone"]]],
 "osaka":   [["오사카 시내", ["dotonbori","umeda","shinsekai","tenma"]], ["교토", ["kyoto","kyotoeki","arashiyama","nanzenji","uji"]], ["나라", ["nara"]], ["고베", ["kobe"]]],
 "fukuoka": [["후쿠오카 시내", ["hakata","tenjin","nakasu"]], ["다자이후·이토시마", ["dazaifu","itoshima"]], ["유후인·벳푸", ["yufuin","beppu"]]],
 "hokkaido":[["삿포로", ["susukino","sapporoeki"]], ["오타루", ["otaru"]], ["하코다테", ["hakodate"]], ["아사히카와·후라노", ["asahikawa","furano"]]],
 "okinawa": [["나하", ["kokusai","naha"]], ["중부·북부", ["chubu","hokubu"]], ["이시가키·미야코", ["ishigaki","miyako"]]],
 "nagoya":  [["나고야", ["meieki"]], ["이누야마", ["inuyama"]], ["다카야마·시라카와고", ["takayama","shirakawago"]]],
 "hiroshima":[["히로시마 시내", ["hirocity"]], ["미야지마", ["miyajima"]], ["오노미치·구라시키", ["onomichi","kurashiki"]]],
 "shikoku": [["마쓰야마", ["matsuyama"]], ["다카마쓰·나오시마", ["takamatsu","naoshima"]], ["고토히라", ["kotohira"]]],
}
FOOD = {
 "osaka":   [["교토", ["kyoto","kyotoeki","arashiyama","nanzenji","uji"]], ["우메다·덴마", ["umeda","tenma"]]],
 "fukuoka": [["하카타·나카스", ["hakata","nakasu"]]],
 "okinawa": [["국제거리·나하", ["kokusai","naha"]]],
}
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
BLK = ("/*VGROUP_BEGIN*/\n"
 f"const VGROUPS = {{festivals:{J(FEST)}, food:{J(FOOD)}}};\n"
 "FESTS.forEach(f=>{ if(!f.sub && VGROUPS.festivals[f.city]) f.sub = VGROUPS.festivals[f.city][0][1][0]; });   // 단지리(기시와다) 등 지역 없는 축제는 도시 첫 묶음\n"
 "const vgOf = (k, v=st.view) => { const G=VGROUPS[v]; if(!G) return null; for(const c in G) for(const [n,m] of G[c]) if(m.includes(k)) return {name:m.length>1?n:((AREA[m[0]]&&AREA[m[0]].ko)||n), members:m, rep:m[0]}; return null; };\n"
 "const vgRep = (k, v) => { const g=vgOf(k,v); return g?g.rep:k; };\n"
 "const vgSame = (a, b) => { const g=vgOf(b); return !!g && g.members.includes(a); };\n"
 "function vgAreas(c, v){ return areasOf(c).filter(a=>vgRep(a.key,v)===a.key).map(a=>{ const g=vgOf(a.key,v); return g?{...a, ko:g.name, vg:g.members}:a; }); }\n"
 "const vgFestN = (c, k) => { const g=vgOf(k,\"festivals\"); return FESTS.filter(f=>f.city===c&&(g?g.members.includes(f.sub):f.sub===k)).length; };\n"
 "function vgFood(k, m){ const g=vgOf(k,\"food\"); if(!g) return arBlock(k,m); const seen=new Set();\n"
 "  return g.members.map((x,i)=>{ const sl=(window.AR_SLUG||{})[x]; if(!sl||seen.has(sl)) return \"\"; seen.add(sl); if(i>0&&!arShops(x,m).length) return \"\"; return arBlock(x,m); }).join(\"\"); }\n"
 "/*VGROUP_END*/\n")
OLD_A = '  if(s.view==="festivals" && areasOf(s.city)[0]) return `${s.city}/${areasOf(s.city)[0].key}/festivals/`;\n'
NEW_A = ('  if(s.view==="festivals") return AREA[s.area] ? `${s.city}/${vgRep(s.area,"festivals")}/festivals/` : `${s.city}/festivals/`;\n'
         '  if(s.view==="food" && AREA[s.area]) return `${s.city}/${vgRep(s.area,"food")}/food/`;\n')
AREAS_OLD = '  if(c) $("#areas").innerHTML = areasOf(st.city).filter(a=>!tgOn()||tgRep(a.key)===a.key).map(a=>{ const g=tgOn()&&tgOf(a.key); return `<button class="area" type="button" data-area="${a.key}" aria-pressed="${st.area===a.key}">${g?g.name:a.ko}</button>`; }).join("");'
AREAS_NEW = ('  if(c) $("#areas").innerHTML = (st.view==="festivals"?`<button class="area" type="button" data-area="all" aria-pressed="${st.area==="all"}">전체</button>`:"")'
             ' + areasOf(st.city).filter(a=>(!tgOn()||tgRep(a.key)===a.key)&&vgRep(a.key)===a.key&&(st.view!=="festivals"||vgFestN(st.city,a.key))).map(a=>{ const g=tgOn()&&tgOf(a.key), v=vgOf(a.key); return `<button class="area" type="button" data-area="${a.key}" aria-pressed="${st.area===a.key}">${g?g.name:v?v.name:a.ko}</button>`; }).join("");')
R = [  # (바꿀 문자열들, 새 문자열)
 (['const cityName = () => curArea() ? (curArea().ko.startsWith(CITIES[st.city].ko) ? curArea().ko : `${CITIES[st.city].ko} ${curArea().ko}`)', 'const cityName = () => curArea() && st.view!=="festivals" ? `${CITIES[st.city].ko} ${curArea().ko}`', 'const cityName = () => curArea() ? `${CITIES[st.city].ko} ${curArea().ko}`'],
  'const cityName = () => curArea() ? (st.view==="festivals" && curArea().vg && curArea().ko.startsWith(CITIES[st.city].ko+" ") ? curArea().ko : `${CITIES[st.city].ko} ${curArea().ko}`)'),   # '도쿄 도쿄 시내' 방지
 (['  const c = CITIES[st.city], A = st.view==="festivals" ? null : curArea();\n  $("#areas").hidden = !c || st.view==="festivals";\n', '  const c = CITIES[st.city], A = curArea();\n  $("#areas").hidden = !c;\n', '  const c = CITIES[st.city], apT = st.view==="transport" && st.sub==="airport", A = apT ? null : curArea();\n  $("#areas").hidden = !c || apT;\n'],
  '  const c = CITIES[st.city], apT = st.view==="transport" && ["times","airport","ic"].includes(st.sub), A = apT ? null : curArea();\n  $("#areas").hidden = !c || apT;\n'),   # 교통 탭(걸리는 시간·공항·교통카드)은 도시 단위   # 교통 '공항에서 시내 가는 법' 탭은 도시 단위
 (['  if(VGROUPS[st.view] && AREA[st.area]){ const r=vgRep(st.area); if(r!==st.area) st.area=r; }\n'],
  '  if(VGROUPS[st.view] && AREA[st.area]){ const r=vgRep(st.area); if(r!==st.area) st.area=r; }\n  if(st.view==="transport" && ["times","airport","ic"].includes(st.sub) && areasOf(st.city)[0]) st.area = areasOf(st.city)[0].key;\n'),
 (['  if(st.view==="transport" && st.sub==="airport" && areasOf(st.city)[0]) st.area'], '  if(st.view==="transport" && ["times","airport","ic"].includes(st.sub) && areasOf(st.city)[0]) st.area'),
 (['const a=st.city==="all"?T("일본"):A?T(A.ko):T(CITIES[st.city].ko);'], 'const a=st.city==="all"?T("일본"):(A&&!["times","airport","ic"].includes(st.sub))?T(A.ko):T(CITIES[st.city].ko);'),
 (['const a=st.city==="all"?T("일본"):(A&&st.sub!=="airport")?T(A.ko)'], 'const a=st.city==="all"?T("일본"):(A&&!["times","airport","ic"].includes(st.sub))?T(A.ko)'),
 ([AREAS_OLD], AREAS_NEW),
 ([OLD_A, '  return `${s.city}/${s.area}/${s.view}/`;\n}'], None),   # 특별 처리 (아래)
 (['const inSub = it => st.area==="all" || it.sub===st.area;'], 'const inSub = it => st.area==="all" || it.sub===st.area || vgSame(it.sub, st.area);'),
 (['function tgArea(A){ if(!A||!tgOn()) return A;'], 'function tgArea(A){ if(A){ const v=vgOf(A.key); if(v) return {...A, ko:v.name, vg:v.members}; } if(!A||!tgOn()) return A;'),
 (['  if(st.view==="transport" && st.area!=="all"){ const r=tgRep(st.area); if(r!==st.area) st.area=r; }\n'],
  '  if(st.view==="transport" && st.area!=="all"){ const r=tgRep(st.area); if(r!==st.area) st.area=r; }\n  if(VGROUPS[st.view] && AREA[st.area]){ const r=vgRep(st.area); if(r!==st.area) st.area=r; }\n'),
 (['      const inC = FESTS.filter(f=>f.city===st.city);\n      let items'], '      const inC = FESTS.filter(f=>f.city===st.city&&inSub(f));\n      let items'),
 (['      const inC = FESTS.filter(f=>f.city===st.city);\n      const cnt'], '      const inC = FESTS.filter(f=>f.city===st.city&&inSub(f));\n      const cnt'),
 (['<div class="bfest"><dt>${esc(c.ko)} ${label} 축제</dt>'], '<div class="bfest"><dt>${esc(A?A.ko:c.ko)} ${label} 축제</dt>'),
 (['<div class="bcal"><dt>${esc(c.ko)} 축제 달력</dt>'], '<div class="bcal"><dt>${esc(A?A.ko:c.ko)} 축제 달력</dt>'),
 (['  const inC = FESTS.filter(inCity);\n'], '  const inC = FESTS.filter(it=>inCity(it)&&inSub(it));\n'),
 (['    body = arBlock(st.area, st.menu);\n'], '    body = vgFood(st.area, st.menu);\n'),
 (['    body = areasOf(st.city).map(A=>{\n'], '    body = vgAreas(st.city,"food").map(A=>{\n'),
 (['`${c}/${areasOf(c)[0].key}/festivals/`'], '`${c}/festivals/`'),
 (['if(c!=="all") st.area=areasOf(c)[0].key; st.view="festivals"'], 'st.area="all"; st.view="festivals"'),
 (['  if(st.city!=="all" && (st.area==="all" || !areasOf(st.city).some(a=>a.key===st.area))) st.area'], '  if(st.city!=="all" && ((st.area==="all" && st.view!=="festivals") || (st.area!=="all" && !areasOf(st.city).some(a=>a.key===st.area)))) st.area'),
 (['  <div class="areas">${areasOf(k).map(a=>{const n=count?count(a.key):null;'], '  <div class="areas">${vgAreas(k,st.view).map(a=>{const n=count?count(a.key):null;'),   # 전체 화면 지역 고르기도 묶음대로
 (['  if(CITIES[seg[0]]){ st.city=seg[0]; st.area=seg[1]||"all";'],
  '  if(CITIES[seg[0]]&&seg[1]==="festivals"){ st.city=seg[0]; st.area="all"; st.view="festivals"; return; }\n  if(CITIES[seg[0]]){ st.city=seg[0]; st.area=seg[1]||"all";'),
]
def rep(s, f):
    for olds, new in R:
        if new is None:   # pathOf
            if NEW_A in s: continue
            if OLD_A in s: s = s.replace(OLD_A, NEW_A); continue
            a = olds[1]; assert s.count(a) == 1, (f, 'pathOf'); s = s.replace(a, NEW_A + a); continue
        if new in s: continue
        for a in olds:
            if s.count(a) == 1: s = s.replace(a, new); break
        else: raise AssertionError((f, olds[0][:70]))
    return s
for f in HTML:
    s = open(f, encoding='utf-8').read()
    s = block(s, '/*VGROUP_BEGIN*/', '/*VGROUP_END*/', BLK, 'const ALL = [...SPOTS')
    s = rep(s, f); open(f, 'w', encoding='utf-8').write(s); print('patched', f)
G = f'{W}/sitegen/gen.py'; s = open(G, encoding='utf-8').read()
new = '&&(!["festivals","food"].includes(v)||vgRep(a.key,v)===a.key)){ r.push(`${c}/${a.key}/${v}/`);'
if new not in s:
    for a in ['&&(v!=="festivals"||a.key===areasOf(c)[0].key)){ r.push(`${c}/${a.key}/${v}/`);', '){ r.push(`${c}/${a.key}/${v}/`);']:
        if s.count(a) == 1: s = s.replace(a, new); break
    else: raise AssertionError('gen routes')
a = '              return r; }\'\'\')\n'
add = "              for(const c of Object.keys(CITIES)) r.push(`${c}/festivals/`);   // 축제 도시 전체 (patch_festcity.py)\n"
if add not in s: assert s.count(a) == 1; s = s.replace(a, add + a)
import re
s = re.sub(r"            if not any\(k\.endswith\('/festivals/'\) for k in MOVED\).*\n", '', s)
mv = ("            MOVED.update(dict(pg.evaluate('''()=>Object.keys(CITIES).flatMap(c=>areasOf(c).flatMap(a=>[\"festivals\",\"food\"].filter(v=>vgRep(a.key,v)!==a.key).map(v=>[`${c}/${a.key}/${v}/`,`${c}/${vgRep(a.key,v)}/${v}/`])))''')))   # 축제·맛집 지역 묶음 (i18n_work/patch_festcity.py)\n")
if mv not in s: s = s.replace(add + a, add + a + mv)
assert mv in s
a = 'for(const t of ["times","airport","ic"]) r.push(`${c}/${a.key}/transport/${t}/`);'
b0 = 'for(const t of ["times","airport","ic"]) if(t!=="airport"||a.key===areasOf(c)[0].key) r.push(`${c}/${a.key}/transport/${t}/`);'
b = 'if(a.key===areasOf(c)[0].key) for(const t of ["times","airport","ic"]) r.push(`${c}/${a.key}/transport/${t}/`);'
s = s.replace(b0, b)
if b not in s: assert s.count(a) == 1, 'gen airport'; s = s.replace(a, b)
mv1 = ("            MOVED.update(dict(pg.evaluate('''()=>Object.keys(CITIES).flatMap(c=>areasOf(c).slice(1).filter(a=>tgRep(a.key)===a.key).map(a=>[`${c}/${a.key}/transport/airport/`,`${c}/${areasOf(c)[0].key}/transport/airport/`]))''')))   # 교통 공항 탭은 도시 단위\n")
mv2 = ("            MOVED.update(dict(pg.evaluate('''()=>Object.keys(CITIES).flatMap(c=>areasOf(c).slice(1).filter(a=>tgRep(a.key)===a.key).flatMap(a=>[\"times\",\"airport\",\"ic\"].map(t=>[`${c}/${a.key}/transport/${t}/`,`${c}/${areasOf(c)[0].key}/transport/${t}/`])))''')))   # 교통 탭(걸리는 시간·공항·교통카드)은 도시 단위\n")
s = s.replace(mv1, mv2)
if mv2 not in s: assert mv in s; s = s.replace(mv, mv + mv2)
open(G, 'w', encoding='utf-8').write(s); print('gen ok')
V = f'{W}/i18n_work/verify2.py'; s = open(V, encoding='utf-8').read()
a = 'const areas=c==="all"?[{key:"all"}]:areasOf(c);'
b = 'const areas=c==="all"?[{key:"all"}]:[...(["festivals","food"].includes(v)?[{key:"all"}]:[]),...areasOf(c)];'
if b not in s: assert s.count(a) == 1; s = s.replace(a, b)
open(V, 'w', encoding='utf-8').write(s); print('verify2 ok')
