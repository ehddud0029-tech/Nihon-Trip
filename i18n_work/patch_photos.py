# 장소 사진을 페이지에 미리 넣기 (검색엔진·이미지 검색·공유 미리보기에 보이게)
# - site/photo_static.json: 장소id -> {src, file, artist, license, commons:true} (위키미디어 공용 사진만)
#   GitHub Actions 사진 작업(photo-job 브랜치의 photos.py)이 위키 문서 대표 사진을 풀어 오고,
#   사진이 없던 상위 장소는 공용에서 직접 고른 파일(photo_fix)을 더해 만들어요.
# - 처음부터 PHOTO에 넣어 두고, 방문자 브라우저의 위키 사진 불러오기(loadPhotos)는 빈 곳만 채워요.
# - 사진 alt에 장소 이름(번역), 장소 JSON-LD에 image → gen.py가 og:image로도 써요.
# html과 backup pre에 같이 적용 (여러 번 돌려도 안전, 데이터 블록은 다시 돌리면 교체)
import json
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
DATA = json.load(open(f'{W}/site/photo_static.json', encoding='utf-8'))
BLOCK = '/*PHSTATIC_BEGIN*/const PHOTO_STATIC = ' + json.dumps(DATA, ensure_ascii=False, separators=(',', ':')) + ';/*PHSTATIC_END*/\n'
R = [
 ('let PHOTO = {};', 'let PHOTO = {...PHOTO_STATIC};'),
 ('PHOTO=c.p; render(); return;', 'PHOTO={...c.p,...PHOTO_STATIC}; render(); return;'),
 ('    PHOTO = p;', '    PHOTO = {...p, ...PHOTO_STATIC};'),
 ('const imgTag = id => PHOTO[id] ? `<img src="${esc(PHOTO[id].src)}" alt=""',
  'const imgTag = id => PHOTO[id] ? `<img src="${esc(PHOTO[id].src)}" alt="${esc((window.__tr||(x=>x))((byId(id)||{}).name||""))}"'),
 ('window.__ld={"@context":"https://schema.org","@type":it.type==="spot"?"TouristAttraction":"Place",name:n,',
  'window.__ld={"@context":"https://schema.org","@type":it.type==="spot"?"TouristAttraction":"Place",name:n,...(PHOTO[it.id]&&PHOTO[it.id].commons?{image:PHOTO[it.id].src}:{}),'),
]
for f in FILES:
    s = open(f, encoding='utf-8').read()
    if '/*PHSTATIC_BEGIN*/' in s:
        i = s.index('/*PHSTATIC_BEGIN*/'); j = s.index('/*PHSTATIC_END*/', i) + len('/*PHSTATIC_END*/\n')
        s = s[:i] + BLOCK + s[j:]
    else:
        a = 'let PHOTO = {};'; assert s.count(a) == 1; s = s.replace(a, BLOCK + a)
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (f, a[:50], s.count(a))
        s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f, len(DATA), 'photos')
