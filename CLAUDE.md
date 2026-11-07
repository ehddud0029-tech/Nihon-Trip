# Go Nihon Trip 작업 안내

일본 여행 정보 사이트 (한국어·영어·일본어·중국어 간체/번체·태국어·스페인어·프랑스어). 배포 주소: https://gonihontrip.com/ (GitHub Pages 사용자 도메인, `sitegen/gen.py`의 ORIGIN·DOMAIN·BASE와 CNAME 파일로 연결)

## 브랜치
- `main`: GitHub Pages로 배포되는 완성된 사이트 (생성 결과물만 있음, 직접 고치지 않음)
- `source`: 원본과 작업 도구 전부 (이 브랜치를 고쳐요)

## 폴더 (작업 공간 /home/claude 기준)
- `tabishiori.html` — 사이트 원본 한 파일 (HTML·CSS·JS). 화면·데이터 대부분이 여기 있어요.
- `site/` — areas.js(지역 목록), geo.js(지도 좌표), autoreserve.js(맛집 순위), google_picks.js, i18n/(언어별 사전, 생성물), README.md
- `sitegen/gen.py` — tabishiori.html을 언어×지역×주제 정적 페이지로 미리 그려 `sitegen/dist`에 만듦 (Playwright 필요)
- `sitegen/*_data.js, *_view.js` — 여행 준비(guide)·추천 일정(itin)·입장료(spot_info) 데이터와 화면 코드 원본
- `i18n_work/` — 번역 원본(`tr_*.tsv`: 한국어/영어/일본어/스페인어/프랑스어 5칸), `build.py emit`(사전 생성), `verify2.py`(번역 누락 검사), 지역 데이터(`region_*.py`)와 주입 스크립트(`region_inject.py`)

## 주의
- `region_inject.py`는 `i18n_work/backup/tabishiori.pre.html`(새 지역 넣기 전 원본)에서 tabishiori.html을 **다시 만들어요**. tabishiori.html을 직접 고친 뒤 이 스크립트를 돌리면 고친 내용이 사라지니, 같은 수정을 backup의 pre 파일에도 적용하세요 (예: `i18n_work/patch_cityarrows.py`처럼 두 파일에 같은 패치).
- 화면 문구는 한국어로 쓰고, 번역은 DOM 텍스트 일치 방식이에요. 새 문구를 넣으면 `tr_*.tsv`에 5개 언어 줄을 추가하고 `python3 i18n_work/build.py emit /home/claude/site/i18n` → `cp site/i18n/*.js /home/claude/i18n/`.
- 번역 누락 확인: `python3 i18n_work/verify2.py en` (ja/es/fr/zh/tw도) → `i18n_work/left_*.json` 이 비어 있어야 해요.
- 제3자 글을 그대로 옮기지 않고, 별점·리뷰 수는 저장하지 않아요. API 키는 넣지 않아요.

## 중국어 (간체 zh · 번체 tw)
- 주소는 `/zh/`(간체)·`/tw/`(번체), html lang과 hreflang은 `zh-Hans`·`zh-Hant`.
- 간체 번역은 `i18n_work/zh_*.tsv`(한국어 \t 간체)와 `zhtpl.tsv`(문장 틀). 번체는 `build.py`가 `s2tw.py`(OpenCC 사전, `i18n_work/opencc/`)로 자동 변환해요. 번체만 고칠 땐 `tw_fix.tsv`(한국어 \t 번체)를 만들면 덮어써요.
- 가게 이름(arnames)은 중국어에서도 일본어 원래 이름을 써요.
- 새 문구를 넣을 땐 `tr_*.tsv` 5칸에 더해 `zh_*.tsv`에도 한 줄 추가하세요. 빠진 문구는 `python3 i18n_work/zh_inventory.py`로 `zh_src/`에 모아 볼 수 있어요.
- 다국어 객체(입장료 안내 등)는 중국어일 때 사전에서 한국어 문장으로 찾아요(`t()` 함수).
- 화면 코드의 중국어 처리는 `i18n_work/patch_zh.py` (html과 backup pre 파일에 같이 적용).

## 태국어 (th)
- 주소 `/th/`, html lang `th`, og:locale `th_TH`. 번역은 `i18n_work/th_*.tsv`(한국어 \t 태국어)와 `thtpl.tsv`(문장 틀). 가게·장소 이름 기본값은 영어(names_en·arnames), th_*.tsv가 덮어써요.
- 새 문구를 넣을 땐 `tr_*.tsv`·`zh_*.tsv`에 더해 `th_*.tsv`에도 한 줄 추가. 빠진 문구는 `python3 i18n_work/th_inventory.py 300` → `th_src/`에 모아 번역 → `th_out/NN.txt`(번호 \t 태국어) → `python3 i18n_work/th_merge.py`.
- 화면 코드의 태국어 처리(엔 표기·날짜·메타 제목 등)는 `i18n_work/patch_th.py` (html, backup pre, sitegen 화면 코드, gen.py에 같이 적용). region_inject.py가 일정 제목(IM) 태국어도 넣어요.
- 번역은 원어민 검수 전이에요.

## 기타 설정
- Google Analytics 4 측정 ID는 `sitegen/gen.py`의 `GA_ID` (모든 생성 페이지 head에 들어감).
- 공유 미리보기 이미지: `sitegen/og/og-<언어>.png` (`python3 sitegen/og/make_og.py`로 다시 생성), gen.py가 dist로 복사하고 og:image를 넣어요.
- 사이트 소개·문의·개인정보처리방침 페이지(about/contact/privacy)는 `i18n_work/patch_info.py`로 추가했어요. 문의 메일: sdyoung0029@gmail.com. 방침 내용을 바꾸면 시행일도 바꿔 주세요.

- 장소 페이지 검색 제목·설명(`pageMeta()`): 관광지는 동네(it.area)와 입장료·운영 시간·가는 길, 쇼핑은 가는 길과 추천 쇼핑 목록을 넣어요. `i18n_work/patch_placemeta.py` (html과 backup pre 파일에 같이 적용).
- 후지산·가와구치코(도쿄 아래)와 교토 5개 지역 나누기: `i18n_work/region_fuji_kyoto.py` (region_inject.py가 읽음). 새 교토 지역(kyotoeki·arashiyama·nanzenji·uji)과 fuji는 AutoReserve 목록 대신 구글 지도 기준 추천 가게(`i18n_work/gp_add.py`, AR_SLUG 값이 `gp/…`)를 보여줘요. 가게 이름은 arnames_5.tsv, 메뉴·특징 번역은 tr_35·zh_35 (region_inject.py가 만듦).

- 월별 날씨·옷차림 페이지(`weather/`, `weather/<월>/`, `<도시>/weather/`, `<도시>/weather/<월>/`): 화면 코드와 기상청 평년값(1991~2020) 데이터는 `sitegen/weather_view.js`, 붙이는 스크립트는 `i18n_work/patch_weather.py` (html과 backup pre에 같이 적용, 다시 돌리면 블록만 교체). 옷차림·준비물 문장은 기온·강수량 규칙으로 골라요. 번역은 tr_37·zh_37·th_37, 문장 틀은 tpl.tsv 맨 앞 5줄.

- 공항에서 시내 가는 법 페이지(`airport/`, `airport/<공항>/`, `airport/<공항>/<지역>/`): 경로는 사이트의 TO_AREA를 그대로 쓰고, 공항 목록(APS)과 화면은 `sitegen/airport_view.js`, 붙이는 스크립트는 `i18n_work/patch_airport.py` (html과 backup pre에 같이 적용). 교통 화면에도 공항 링크가 붙어요. 번역은 tr_38·zh_38·th_38. 사이트 TO_AREA에 없는 다른 방법은 airport_view.js의 AP_EXTRA(번역 tr_39·zh_40·th_40), 요금은 고정값 대신 구글 지도 대중교통 길찾기 링크(APJ 공항 일본어 이름)로 보여줘요.
- 추가 추천 일정 10개는 `i18n_work/itin_more.py` (7개 언어 문구를 한곳에), `itin_emit.py`가 합쳐서 itin_data.js·tr_27과 zh_39·th_39를 만들어요. 그다음 html·pre의 `const ITIN =` 줄을 itin_data.js로 바꿔요 (region_inject.py도 같은 일을 해요).

- 모바일 하단 탭바 색(--bar)·선택 표시·날씨 탭, 모든 언어에서 가로 스크롤(칸 최소 58px, 지금 탭이 화면 안으로): `i18n_work/patch_tabbar.py` (html과 backup pre에 같이 적용).

- 도쿄 영상 참고 보완: 도청 전망실 시간·휴무·프로젝션 매핑, 센소지 팁(아사쿠사 문화관광센터 전망 테라스)은 `i18n_work/patch_tokyo_video.py`, 도쿄돔 시티(s_tokyodome)는 region_fuji_kyoto.py의 POPULAR. 번역 tr_40·zh_41·th_41.
- **region_inject.py를 돌린 뒤에는** `patch_th.py → patch_weather.py → patch_airport.py → patch_tabbar.py → patch_tokyo_video.py`를 차례로 다시 돌려 주세요 (region_inject가 DESC 등 일부 줄을 다시 써요. 각 패치는 여러 번 돌려도 안전해요).

- 사이트 아이콘 파일(favicon.ico·icon-*.png, 네이버 검색 결과 아이콘용)은 `sitegen/icons/` (`make_icons.py`로 다시 생성), gen.py가 dist 맨 위로 복사해요. 네이버 서치어드바이저용 RSS(`rss.xml`, 한국어 일정·날씨·공항·여행 준비·축제 달력 페이지)는 gen.py의 `write_rss()`가 만들어요.

- AI·검색 인용용: 날씨(도시·월)·공항 경로 페이지의 "자주 묻는 질문"(FAQPage 마이크로데이터)과 이동 경로(BreadcrumbList)는 weather_view.js·airport_view.js, 추천 일정 상세의 TouristTrip 마이크로데이터는 `i18n_work/patch_aio.py`. 번역 tr_41·zh_42·th_42, 문장 틀은 tpl.tsv 맨 앞. gen.py가 `llms.txt`(AI용 사이트 안내)와 IndexNow 키 파일(`<INDEXNOW_KEY>.txt`), `.github/workflows/indexnow.yml`(main에 올라가면 GitHub Pages에 새 버전이 뜰 때까지 `build.txt`로 기다린 뒤, 버전 번호·현재 시각 줄만 바뀐 페이지는 빼고 실제로 바뀐 페이지만 IndexNow로 알림. 전체를 한 번 다시 보내려면 `INDEXNOW_FULL=1 python3 deploy.py ...`)을 만들어요. region_inject 뒤에는 patch_aio.py도 다시 돌려 주세요.

- 숙소 페이지(`stay/`, `<도시>/stay/`, 도시 8곳: 도쿄·오사카·후쿠오카·홋카이도·오키나와·나고야·히로시마·시코쿠): 화면·추천 숙소(HOTELS, 마이리얼트립 제휴 링크)·나고야 동네 데이터는 `sitegen/stay_view.js`, 붙이는 스크립트는 `i18n_work/patch_stay.py`. 동네 비교 데이터는 GUIDE stay 섹션(guide_data.js)에 그대로 두고 숙소 페이지가 읽어요. 숙소 전체 페이지(`stay/`)에 지역별 동네 비교가 모두 보이고(도시별 섹션 `#st-<도시>`, 위 지역 버튼은 같은 페이지 안으로 이동, 모바일에선 "이런 분께"만 보이고 "장단점 펼쳐 보기"로 펼침, 한국어·영어는 추천 숙소 카드+예약 버튼, 자세히 보기 → 도시 페이지), 여행 준비에는 숙소 탭이 없어요(GKEYS·탭에서 뺌). 예전 주소 `guide/stay/`는 gen.py `MOVED`/`write_moved()`가 만든 안내 페이지로 `stay/`에 보내요. 숙소 페이지는 RSS·llms.txt에도 들어가요. 제휴 링크와 추천 숙소는 **한국어·영어 페이지에만** 보이고(사용자 결정), 아래에 제휴 수수료 안내를 붙여요. 번역 tr_42·zh_43·th_43 (호텔 문구는 영어만). PC 상단 메뉴와 모바일 하단 탭바(11칸, 날씨와 준비 사이)에 "숙소"가 들어가요. region_inject 뒤에는 patch_stay.py도 다시 돌려 주세요.

- 검색 클릭률 개선(2026-11, 서치콘솔 분석): 장소 페이지 검색 설명은 소개 문장 먼저, 입장료·운영·가는 길·추천 쇼핑은 뒤에(`pageMeta()`). 쇼핑 장소 33곳의 영업시간·식당가 시간·공식 사이트(층별 안내) 데이터는 `sitegen/shop_info.js`(SHOP_INFO, 2026년 11월 공식 사이트 기준), 붙이는 스크립트 `i18n_work/patch_shopinfo.py`(html·pre, 여러 번 돌려도 안전). 영업시간이 있으면 제목이 '영업시간·추천 쇼핑·가는 길'(PTH)로 바뀌고 JSON-LD에 url·openingHours가 들어가요. 번역 tr_43·zh_44·th_44. 영어·스페인어·프랑스어 사전은 `build.py emit`이 붙여 쓴 가운뎃점(A·B·C)을 'A, B & C'로 바꿔요(amp). region_inject 뒤에는 patch_shopinfo.py도 다시 돌려 주세요.

- 상위 페이지 보강(2026-11): `sitegen/shop_info.js`의 PLACE_PLUS(주소·가는 길 보충·층별 구성·추가 소개, 교토역은 매장별 안내 subs)와 TAXFREE(2026년 11월 1일 시작한 환급 방식 면세 안내), 쇼핑 장소 '자주 묻는 질문'(FAQPage). SHOP_INFO의 tf=면세 안내를 보여줄 큰 시설. 번역 tr_43·zh_44·th_44.
- 맛집 목록의 똑같이 반복되는 틀 문장 특징(feat)은 `i18n_work/ar_dedupe.py`가 비워요(region_inject 뒤에 다시 돌려 주세요).
- `i18n_work/patch_navfix.py`: 메뉴의 '추천 일정' 링크는 항상 일정 목록, '여행 준비'는 첫 섹션(전에는 정적 생성 때 남은 상태 때문에 오키나와 일정으로 가 있었어요). 추천 일정의 장소는 장소 페이지 링크(<a class="istop">), 장소 페이지에는 '이 장소가 들어간 추천 일정'(placeItins). html·pre·itin_view.js에 같이 적용, region_inject 뒤에 다시 돌려 주세요. 메뉴(상단·하단 탭)를 누르면 어느 메뉴든 항상 첫 페이지(전체)로 가요(도시·동네·날씨 월·공항 선택을 넘기지 않음, 같은 파일의 MENU_RESET).

- 사진을 페이지에 미리 넣기(2026-11): 작업 공간·페이지 생성은 위키 사이트에 못 붙어서, 사진 주소·저작자·라이선스는 GitHub의 `photo-job` 브랜치(photos.py + titles.json·search.json, push하면 Actions가 돌고 photo_cache.json·photo_candidates.json을 커밋)로 받아요. 결과 중 위키미디어 공용 사진만 `site/photo_static.json`에 모으고(사진 없던 곳은 후보 중 직접 고른 파일), `i18n_work/patch_photos.py`가 html·pre에 PHOTO_STATIC으로 넣어요(사진 alt=장소 이름, 장소 JSON-LD image → gen.py가 og:image로 사용). gen.py·compare.py는 위키 이미지 요청에 1px 이미지로 답해서 img 태그가 지워지지 않게 해요(비교 이미지에서는 사진 자리가 비어 보여요). region_inject 뒤에는 patch_photos.py도 다시 돌려 주세요.

- 술 여행 페이지(2026-11, `drink/`, `<도시>/drink/`, 도시 8곳): 일본 술 종류·사케 라벨 읽는 법·주문 말·견학 팁·가지고 올 때 규칙(한국 세관 문구는 한국어에서만, 다른 언어는 "나라마다 다름"), 지역별 견학·시음 장소 23곳(DRINKS, 2026년 11월 공식 사이트 기준, 별점 없음). 화면·데이터는 `sitegen/drink_view.js`, 붙이는 스크립트 `i18n_work/patch_drink.py`(html·pre, 메뉴·하단 탭 "술", 메타 제목·설명 8개 언어). 번역 tr_44·zh_45·th_45(`i18n_work/drink_tr.py`로 생성), 문장 틀 tpl.tsv 맨 앞 3줄. RSS·llms.txt·verify2에도 들어가요. 아사히 하카타·나고야 공장은 견학 종료라 뺐어요. 도시별 '사 가면 좋은 술'(DRINK_BUY: 종류·이름·일본어 이름·설명·살 수 있는 곳)과 '술 살 때 팁'(DRINK_SHOP), 도시 페이지 FAQ '{x}에서 사 갈 만한 술은 무엇인가요?'도 drink_view.js에 있어요(번역 tr_45·zh_46·th_46, `i18n_work/drink_tr2.py`). 카드마다 가격대(p, 2026년 11월 일본 매장 기준 대략)·맛 한 줄(t)·사진(DRINK_PHOTO, `site/drink_photos.json`에서 넣음: 위키미디어 공용 자유 라이선스 사진만, 카드에 저작자·라이선스 표시. 후보는 photo-job 브랜치의 drinks.py+drink_search.json → drink_candidates.json, 직접 보고 고름. 사진 없는 술: 시게마스·잔파·긴샤치·초야 → 종류별 술병 그림 DRINK_ART(SVG)를 대신 보여 줌). 카드마다 '구글 지도에서 파는 곳 찾기'(일본어 이름+도시 일본어 이름 검색), 매장 탭은 매장 종류별 지도 검색(DRINK_STORE_Q)과 추천 술별 '지도' 링크(번역 tr_50·zh_51·th_51, 문장 틀 tpl.tsv 맨 앞). 번역 tr_46·zh_47·th_47(`i18n_work/drink_tr3.py`). 도시 술 페이지는 탭 4개로 나눠요(st.dtab, DRINK_TABS): `<도시>/drink/`(견학·시음), `/buy/`(사 가면 좋은 술), `/tips/`(술 살 때 팁·라벨·가지고 올 때), `/shops/`(매장 종류 DRINK_STORES + 추천 술별 구매처 + 직매장 있는 양조장). 탭별 검색 제목은 patch_drink.py의 TABM, gen.py 경로·verify2도 탭까지 돌아요. 번역 tr_47·zh_48·th_48. region_inject 뒤에는 patch_drink.py도 다시 돌려 주세요.

- 여행 준비 > 통신 > eSIM 구매 링크(마이리얼트립 제휴, https://myrealt.rip/10FBq6a): `i18n_work/patch_esim.py`(guide_data.js·html·pre·guide_view.js). 비교(compare) 블록의 구매 링크는 한국어·영어에서만 보이고 아래 제휴 수수료 안내가 붙어요. region_inject 뒤에는 patch_esim.py도 다시 돌려 주세요.
- patch_drink.py는 R2(이미 붙은 줄을 탭용으로 고치는 규칙)가 있어서, R의 같은 규칙이 다시 끼어들지 않게 막아 두었어요(중복 선언으로 페이지 생성이 멈춘 적 있음). 패치 후 `node --check`로 app.js 문법을 확인하면 안전해요.

- 페이지 안 탭(하위 페이지, 2026-11): `i18n_work/patch_tabs.py`(공통: st.sub, subTabs(), subOk()/subFromSeg()로 주소 끝 탭 처리, data-subtab 클릭, 메뉴·다른 화면 링크는 첫 탭, 탭별 검색 제목 subMeta). 화면은 각 view 파일이 st.sub로 그려요.
  - 숙소: `stay/`(묵기 좋은 동네) · `stay/hotels/`(추천 숙소, 한국어·영어만) · `stay/booking/`(예약 방법), 도시도 같은 3탭(`<도시>/stay/hotels/`…).
  - 술 전체: `drink/`(지역별 견학·시음) · `drink/types/` · `drink/visit/` · `drink/carry/`. (도시 술 페이지는 따로 st.dtab의 buy/tips/shops)
  - 날씨 도시: `<도시>/weather/`(월별 기온·강수) · `/outfit/`(월별 옷차림) · `/faq/`(가장 더운·추운·비 많은 달, 여행하기 좋은 달). 월 페이지는 그대로.
  - 공항: `airport/<공항>/`(시내 가는 법) · `/all/`(모든 방법 비교) · `/faq/`(목적지별 걸리는 시간·교통카드).
  - gen.py 경로·verify2도 탭까지 돌아요. 번역 tr_48·zh_49·th_49, 문장 틀 tpl.tsv 맨 앞 4줄. region_inject 뒤에는 patch_tabs.py도(맨 마지막에) 다시 돌려 주세요. patch_navfix의 MENU_RESET에 sub:"" 포함.

- 교통 화면 지역 묶기(2026-11): 이동 방법이 거의 같은 하위 지역은 교통 화면에서만 하나로 보여요. 묶음은 `site/tgroups.json`(도쿄 시내·오사카 시내·교토·후쿠오카 시내·삿포로·나하, 첫 지역이 대표 주소), 스크립트 `i18n_work/patch_tgroup.py`(지역 버튼 묶기, 공항 직행편·시내 이동 합치기(종류별 2줄, 최대 6줄), 묶음 안 다른 지역은 대표로). gen.py는 묶인 지역의 `<도시>/<지역>/transport/`를 만들지 않고 MOVED로 대표 주소에 보내요. 번역 tr_49·zh_50·th_50. region_inject 뒤에는 patch_tgroup.py도 다시 돌려 주세요.

- 교통 페이지 탭(2026-11): 한눈에 보기 / 이동별 걸리는 시간(`times/`) / 공항에서 시내 가는 법(`airport/`, 공항별 목적지 가장 빠른 길) / 교통카드 안내(`ic/`). 주소는 `transport/…`, `<도시>/<지역>/transport/…`. `i18n_work/patch_ttabs.py`가 원래 V.transport 결과에서 탭에 맞는 부분만 골라 보여 주고(원래 코드는 그대로), 맨 위 요약 칸은 '한눈에 보기'에서만(body.tsub). patch_tabs.py의 subOk·subFromSeg·subMeta에 교통 탭을 더하므로 **patch_tabs.py 다음에** 돌려 주세요. 탭별 검색 제목 TTABM, gen.py·verify2도 탭까지. 번역 tr_50·zh_51·th_51.

- 페이지 맨 위 요약 칸(2026-11): 날씨·시내 이동을 빼고 주제 내용만. 관광지 = 추천 관광지 TOP 3(설명 2줄 .pdx, 분류 표시와 지역명 사이 세로 구분선) · 추천 여행 경로, 맛집·축제·쇼핑·나의 여행 = 주제 칸 두 개, 교통 = 공항 가는 법·교통카드·시내 이동(날씨만 뺌). 도시를 고른 화면에선 날씨 출처 줄(#wxnote)도 숨김(body.nowx). `i18n_work/patch_brief.py` (**patch_ttabs.py 다음에** 돌리기).

## 수정 전·후 비교 (사용자 요청: 사이트를 고치면 항상 보여주기)
- 날씨 값은 비교용 예시로 채워요(실제 예보 아님). 화면이 바뀌는 수정을 하면 배포 전에 `python3 sitegen/compare.py <이름> <언어:주소> ... [--mobile] [--ref main]`로 비교 이미지를 만들어 사용자에게 보내요 (왼쪽 수정 전 = 배포된 main, 오른쪽 수정 후 = 작업 공간 원본). 결과는 `sitegen/compare_out/<이름>_<번호>.png`.
- 바뀐 페이지의 대표 주소 1~3개를 고르고, 모바일 화면이 바뀌면 `--mobile`도 같이 만들어요.

## 배포
```
python3 /home/claude/deploy.py "변경 내용" --trailer "Co-Authored-By: ..."
```
원본을 `source` 브랜치에 백업하고, 페이지를 생성해 `main`에 올려요.

## 새 작업 공간에서 되살리기
```
git clone -b source https://github.com/ehddud0029-tech/Nihon-Trip.git /home/claude/nihon-src
python3 /home/claude/nihon-src/restore.py
```
(내 컴퓨터에서 Claude Code로 작업할 때는 스크립트 안의 `/home/claude` 경로를 작업 폴더로 바꿔야 해요.)
