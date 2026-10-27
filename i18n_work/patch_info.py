# 사이트 소개(about)·문의(contact)·개인정보처리방침(privacy) 페이지와 푸터 링크 추가
# tabishiori.html 과 backup/tabishiori.pre.html 두 곳에 같은 패치를 적용해요.
import sys
EMAIL = "sdyoung0029@gmail.com"
FILES = ["/home/claude/tabishiori.html", "/home/claude/i18n_work/backup/tabishiori.pre.html"]

CSS = """.info{max-width:760px;padding:26px 0 48px}
.info h1{font-family:var(--f-display);font-size:28px;margin:0 0 14px}
.info h2{font-size:17px;margin:28px 0 8px}
.info p,.info li{line-height:1.75;color:var(--ink);margin:0 0 10px}
.info ul{padding-left:20px;margin:0 0 10px}
.info .muted{color:var(--ink-2);font-size:13.5px}
.info .mail{display:inline-block;margin:6px 0 14px;padding:12px 18px;border:1px solid var(--line);border-radius:var(--r);background:var(--surface);font-weight:700;color:var(--ai)}
footer .flinks{margin-top:8px}
footer .flinks a{color:var(--ink-2)}
body.is-info .hero{display:none}
"""

JS = r"""V.about = function(){ return `<article class="info">
  <h1>사이트 소개</h1>
  <p>Go Nihon Trip은 일본을 여행하는 사람이 지역별로 필요한 정보를 한곳에서 찾을 수 있도록 만든 여행 정보 사이트예요.</p>
  <p>도쿄·오사카·후쿠오카·홋카이도·오키나와·나고야·히로시마·시코쿠의 관광지, 축제, 맛집, 쇼핑, 교통 정보와 추천 일정, 여행 준비 안내를 한국어·영어·일본어·스페인어·프랑스어로 제공해요.</p>
  <h2>정보 출처</h2>
  <ul>
   <li>날씨: Open-Meteo 예보를 실시간으로 불러와요.</li>
   <li>사진: Wikimedia Commons와 위키백과의 자유 라이선스 사진을 써요. 각 사진의 저작자와 라이선스는 상세 화면에 표시해요.</li>
   <li>지도: OpenFreeMap과 OpenStreetMap 기여자의 지도 데이터를 써요.</li>
   <li>맛집 추천: AutoReserve에 공개된 지역별 순위를 참고했어요. 가게 이름을 누르면 AutoReserve 페이지로 연결돼요.</li>
   <li>입장료·운영 시간: 각 시설의 공식 안내를 바탕으로 직접 정리했어요.</li>
  </ul>
  <p class="muted">입장료, 운영 시간, 교통 정보는 바뀔 수 있어요. 여행 전에 공식 사이트에서 다시 확인하세요.</p>
  <h2>문의</h2>
  <p>잘못된 정보를 발견하셨거나 추가했으면 하는 장소가 있다면 알려 주세요.</p>
  <p><a class="btn"${infoHref("contact")} data-view="contact">문의하기<i> →</i></a></p>
 </article>`; };
V.contact = function(){ return `<article class="info">
  <h1>문의하기</h1>
  <p>잘못된 정보, 추가했으면 하는 장소, 제휴 문의는 아래 메일로 보내 주세요.</p>
  <a class="mail" href="mailto:__EMAIL__">__EMAIL__</a>
  <p>장소 정보 수정을 요청하실 때는 해당 페이지 주소를 함께 적어 주시면 빨리 확인할 수 있어요.</p>
  <p>메일을 확인하는 대로 답장드릴게요.</p>
 </article>`; };
V.privacy = function(){ return `<article class="info">
  <h1>개인정보처리방침</h1>
  <p class="muted">시행일: 2026년 10월 27일</p>
  <h2>수집하는 정보</h2>
  <p>Go Nihon Trip은 회원 가입이 없고, 이름이나 연락처 같은 개인정보를 직접 수집하지 않아요.</p>
  <h2>방문 통계 (Google Analytics)</h2>
  <p>사이트를 개선하기 위해 Google Analytics 4를 사용해요. Google Analytics는 쿠키를 이용해 방문한 페이지, 머문 시간, 대략적인 지역, 기기와 브라우저 종류 같은 정보를 개인을 알아볼 수 없는 형태로 수집해요.</p>
  <p>브라우저 설정에서 쿠키를 차단하거나 Google 애널리틱스 차단 부가기능을 설치하면 수집을 거부할 수 있어요.</p>
  <p><a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google 애널리틱스 차단 부가기능 ↗</a> · <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google 개인정보처리방침 ↗</a></p>
  <h2>브라우저에 저장되는 정보</h2>
  <p>저장한 장소 목록, 언어 설정, 사진 정보 캐시는 사용하는 브라우저에만 저장되고 서버로 전송되지 않아요. 브라우저의 사이트 데이터를 지우면 함께 삭제돼요.</p>
  <h2>외부 서비스</h2>
  <p>날씨(Open-Meteo), 지도(OpenFreeMap), 사진(위키미디어), 글꼴(Google Fonts)을 불러올 때 브라우저가 각 서비스에 직접 접속해요. AutoReserve, Google 지도, 시설 공식 사이트 등 외부 링크로 이동하면 해당 사이트의 개인정보처리방침이 적용돼요.</p>
  <h2>문의 메일</h2>
  <p>문의 메일로 받은 이메일 주소와 내용은 답장하는 데만 사용하고, 다른 목적으로 쓰거나 다른 곳에 제공하지 않아요.</p>
  <h2>방침의 변경</h2>
  <p>이 방침이 바뀌면 이 페이지에 시행일과 함께 알려 드려요.</p>
  <p>개인정보 관련 문의: <a href="mailto:__EMAIL__">__EMAIL__</a></p>
 </article>`; };
function infoHref(v){ return ROUTED ? ` href="${window.NT_BASE + LPRE + v + "/"}"` : ` href="#${v}"`; }
""".replace("__EMAIL__", EMAIL)

INFO_T = """ const IT={ko:{about:"사이트 소개",contact:"문의하기",privacy:"개인정보처리방침",d:"Go Nihon Trip 사이트 소개, 정보 출처, 문의 방법과 개인정보처리방침."},
   en:{about:"About",contact:"Contact",privacy:"Privacy Policy",d:"About Go Nihon Trip, where our information comes from, how to contact us, and our privacy policy."},
   ja:{about:"サイトについて",contact:"お問い合わせ",privacy:"プライバシーポリシー",d:"Go Nihon Tripについて、情報の出典、お問い合わせ方法、プライバシーポリシー。"},
   es:{about:"Acerca de",contact:"Contacto",privacy:"Política de privacidad",d:"Acerca de Go Nihon Trip, de dónde viene la información, cómo contactarnos y nuestra política de privacidad."},
   fr:{about:"À propos",contact:"Contact",privacy:"Politique de confidentialité",d:"À propos de Go Nihon Trip, sources des informations, comment nous contacter et politique de confidentialité."}}[(window.I18N&&window.I18N.lang)||"ko"];
  if(INFO_VIEWS.includes(st.view)) return {title:IT[st.view]+" | Go Nihon Trip", desc:IT.d};
"""

FOOT_OLD = "공식 사이트에서 다시 확인하세요.</div></footer>"
FOOT_NEW = ('공식 사이트에서 다시 확인하세요.<div class="flinks"><a href="#about" data-view="about">사이트 소개</a> · '
            '<a href="#contact" data-view="contact">문의하기</a> · <a href="#privacy" data-view="privacy">개인정보처리방침</a></div></div></footer>')

def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a))
    return s.replace(a, b)

for f in FILES:
    s = open(f, encoding="utf-8").read()
    if "INFO_VIEWS" in s:
        print("skip", f); continue
    s = rep(s, "footer{border-top:1px solid var(--line);", CSS + "footer{border-top:1px solid var(--line);")
    s = rep(s, '"guide","itin","place"];', '"guide","itin","place","about","contact","privacy"];\nconst INFO_VIEWS = ["about","contact","privacy"];')
    s = rep(s, "function pathOf(s){\n  if(s.view===\"home\") return \"\";",
            "function pathOf(s){\n  if(s.view===\"home\") return \"\";\n  if(INFO_VIEWS.includes(s.view)) return s.view+\"/\";")
    s = rep(s, '!["home","saved","map","guide","itin"].includes(seg[2])', '!["home","saved","map","guide","itin","place","about","contact","privacy"].includes(seg[2])')
    s = rep(s, '  if(st.view==="home") return {title:T("Go Nihon Trip · 일본 여행 가이드"), desc:null};',
            INFO_T + '  if(st.view==="home") return {title:T("Go Nihon Trip · 일본 여행 가이드"), desc:null};')
    s = rep(s, '  document.body.classList.toggle("is-place", st.view==="place");\n',
            '  document.body.classList.toggle("is-place", st.view==="place");\n  document.body.classList.toggle("is-info", INFO_VIEWS.includes(st.view));\n')
    s = rep(s, '  if(st.view==="home"){ st.city="all"; }\n  if(st.city==="all") st.area="all";',
            '  if(st.view==="home" || INFO_VIEWS.includes(st.view)){ st.city="all"; }\n  if(st.city==="all") st.area="all";')
    s = rep(s, '  if(view==="home"){ st.city="all"; st.area="all"; st.focus=null; }',
            '  if(view==="home" || INFO_VIEWS.includes(view)){ st.city="all"; st.area="all"; st.focus=null; }')
    s = rep(s, "V.place = function(){", JS + "V.place = function(){")
    s = rep(s, FOOT_OLD, FOOT_NEW)
    open(f, "w", encoding="utf-8").write(s)
    print("patched", f)
