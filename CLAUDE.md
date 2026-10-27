# Go Nihon Trip 작업 안내

일본 여행 정보 사이트 (한국어·영어·일본어·스페인어·프랑스어). 배포 주소: https://gonihontrip.com/ (GitHub Pages 사용자 도메인, `sitegen/gen.py`의 ORIGIN·DOMAIN·BASE와 CNAME 파일로 연결)

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
- 번역 누락 확인: `python3 i18n_work/verify2.py en` (ja/es/fr도) → `i18n_work/left_*.json` 이 비어 있어야 해요.
- 제3자 글을 그대로 옮기지 않고, 별점·리뷰 수는 저장하지 않아요. API 키는 넣지 않아요.

## 기타 설정
- Google Analytics 4 측정 ID는 `sitegen/gen.py`의 `GA_ID` (모든 생성 페이지 head에 들어감).
- 공유 미리보기 이미지: `sitegen/og/og-<언어>.png` (`python3 sitegen/og/make_og.py`로 다시 생성), gen.py가 dist로 복사하고 og:image를 넣어요.
- 사이트 소개·문의·개인정보처리방침 페이지(about/contact/privacy)는 `i18n_work/patch_info.py`로 추가했어요. 문의 메일: sdyoung0029@gmail.com. 방침 내용을 바꾸면 시행일도 바꿔 주세요.

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
