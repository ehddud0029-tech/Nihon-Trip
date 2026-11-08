# 여행 추천(첫 화면) '지역 고르기': 고른 주제에 맞게 버튼을 바꿔요 (2026-11 사용자 요청)
# - 축제: 축제 화면은 도시 단위라 도시마다 버튼 하나 (축제 수 표시)
# - 교통: 교통 화면처럼 묶인 지역은 하나로 (site/tgroups.json, 예: 도쿄 시내)
# html·backup pre에 같이 적용, 여러 번 돌려도 안전. region_inject 뒤에 다시 돌려 주세요 (patch_tgroup.py 다음).
W = '/home/claude'
A = '    <div class="areas">${areasOf(k).map(a=>{const n=cnt[to]?cnt[to](a.key):0; return `<button class="area" type="button" data-goarea="${a.key}" data-region="${k}">${a.ko}${n?` <span class="acount">${n}</span>`:""}</button>`;}).join("")}</div></div>`).join("");'
B = '    <div class="areas">${homeAreas(k,to).map(a=>{const n=to==="festivals"?FESTS.filter(f=>f.city===k).length:cnt[to]?cnt[to](a.key):0; return `<button class="area" type="button" data-goarea="${a.key}" data-region="${k}">${a.ko}${n?` <span class="acount">${n}</span>`:""}</button>`;}).join("")}</div></div>`).join("");'
F = ('const PAGE_LABEL = {spots:"관광지",festivals:"축제",food:"맛집",transport:"교통",shopping:"쇼핑"};\n',
     'const PAGE_LABEL = {spots:"관광지",festivals:"축제",food:"맛집",transport:"교통",shopping:"쇼핑"};\n'
     'function homeAreas(k,to){ const as=areasOf(k); if(!as.length) return as;\n'
     '  if(to==="festivals") return [{key:as[0].key, ko:CITIES[k].ko}];\n'
     '  if(to==="transport" && typeof tgOf==="function") return as.filter(a=>{const g=tgOf(a.key); return !g||g.rep===a.key;}).map(a=>{const g=tgOf(a.key); return g?{key:a.key, ko:g.name}:a;});\n'
     '  return as; }\n')
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    if B not in s: assert s.count(A) == 1, f; s = s.replace(A, B)
    if 'function homeAreas(' not in s: assert s.count(F[0]) == 1, f; s = s.replace(F[0], F[1])
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
