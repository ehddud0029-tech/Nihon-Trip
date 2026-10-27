"""장소별 개별 페이지 (/place/<id>/): tabishiori.html 과 backup/tabishiori.pre.html 에 같은 패치를 적용해요."""
import sys

CSS_A = '.drawer p{margin:0}'
CSS_B = CSS_A + '''
body.is-place .hero{display:none}
a.card,a.fest{color:inherit;text-decoration:none}
.place{padding:22px 0 40px}
.crumb{font-size:13px;color:var(--ink-2);display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:14px}
.crumb a{color:inherit}
.crumb i{font-style:normal;opacity:.5}
.pl-grid{display:grid;gap:22px}
@media (min-width:860px){.pl-grid{grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);align-items:start}}
.place .plate{aspect-ratio:3/2;width:100%;border-radius:var(--r);overflow:hidden}
.place .plate img{object-fit:contain}
.place .plate img.bg{object-fit:cover;filter:blur(20px) brightness(.8);transform:scale(1.2)}
.place .plate .k{font-size:110px}
.pl-main{display:flex;flex-direction:column;gap:12px}
.pl-main h1{margin:0;font-family:var(--f-display);font-size:clamp(26px,3.4vw,34px);line-height:1.25}
.pl-main .jpn{font-family:var(--f-kanji);color:var(--ink-2);margin-top:-6px}
.pl-main p{margin:0;line-height:1.65}
.pl-more{margin-top:34px}
.pl-more h2{font-family:var(--f-display);font-size:20px;margin:0 0 12px}
.pl-all{margin-top:18px}
.pl-all i,.actions i{font-style:normal}'''

R = []  # (old, new, count)
R.append((CSS_A, CSS_B, 1))
R.append(('const VIEWS = ["home","spots","festivals","food","transport","shopping","map","saved","guide","itin"];',
          'const VIEWS = ["home","spots","festivals","food","transport","shopping","map","saved","guide","itin","place"];', 1))
# 카드·축제 목록: 크롤링되는 링크로 (누르면 지금처럼 상세 창)
R.append(('''  return `<button class="card" type="button" data-open="${it.id}" style="--c:var(${colorOf(it)})">''',
          '''  const tg = PLACE_TYPES.includes(it.type) ? ["a",` href="${placeHref(it.id)}"`] : ["button",' type="button"'];
  return `<${tg[0]} class="card"${tg[1]} data-open="${it.id}" style="--c:var(${colorOf(it)})">''', 1))
R.append(('''    <div class="meta"><span>${extra}</span>${isSaved?'<span class="saved-mark">저장됨</span>':''}</div></div></button>`;''',
          '''    <div class="meta"><span>${extra}</span>${isSaved?'<span class="saved-mark">저장됨</span>':''}</div></div></${tg[0]}>`;''', 1))
R.append(('<button class="fest" type="button" data-open="${x.id}" style="--c:var(--yamabuki)">', '<a class="fest" href="${placeHref(x.id)}" data-open="${x.id}" style="--c:var(--yamabuki)">', 1))
R.append(('<p>${esc(x.desc)}</p></span></button>`).join("")}</div>`', '<p>${esc(x.desc)}</p></span></a>`).join("")}</div>`', 1))
R.append(('<button class="fest" type="button" data-open="${f.id}" style="--c:var(--yamabuki)">', '<a class="fest" href="${placeHref(f.id)}" data-open="${f.id}" style="--c:var(--yamabuki)">', 1))
R.append(('''<span class="saved-mark" style="font-size:12px">저장됨</span>':''}</span></button>`).join("")}</div>`''',
          '''<span class="saved-mark" style="font-size:12px">저장됨</span>':''}</span></a>`).join("")}</div>`''', 1))
# 주소
R.append(('''  if(s.view==="saved") return "saved/";''', '''  if(s.view==="saved") return "saved/";
  if(s.view==="place") return `place/${placeSlug(s.place||"")}/`;''', 1))
R.append(('''  if(seg[0]==="saved"){ st.view="saved"; return; }''', '''  if(seg[0]==="saved"){ st.view="saved"; return; }
  if(seg[0]==="place"){ const id=placeIdOf(seg[1]||""); if(id){ st.view="place"; st.place=id; } return; }''', 1))
# 제목·설명·구조화 데이터
R.append(('''  const L = (window.I18N&&window.I18N.lang)||"ko", M = PMETA[L]||PMETA.ko, T = window.__tr||(x=>x);
  if(st.view==="home")''', '''  const L = (window.I18N&&window.I18N.lang)||"ko", M = PMETA[L]||PMETA.ko, T = window.__tr||(x=>x);
  window.__ld = null;
  if(st.view==="place"){ const it=byId(st.place); if(it){
    const PT={ko:{spot:"{n} – 입장료·운영 시간·가는 길 ({a})",fest:"{n} – 일정·장소·즐기는 팁 ({a})",shop:"{n} – 쇼핑 정보·추천 쇼핑 목록 ({a})",food:"{n} – {a} 향토음식과 먹는 곳"},
      en:{spot:"{n} – Admission, Hours & Access ({a})",fest:"{n} – Dates, Venue & Tips ({a})",shop:"{n} – Shopping Guide & What to Buy ({a})",food:"{n} – Local Dish in {a} & Where to Try It"},
      ja:{spot:"{n} – 入場料・営業時間・アクセス（{a}）",fest:"{n} – 日程・会場・楽しみ方（{a}）",shop:"{n} – ショッピング情報・おすすめの買い物（{a}）",food:"{n} – {a}の郷土料理と食べられる場所"},
      es:{spot:"{n} – Precio, horario y cómo llegar ({a})",fest:"{n} – Fechas, lugar y consejos ({a})",shop:"{n} – Guía de compras y qué comprar ({a})",food:"{n} – Plato local de {a} y dónde probarlo"},
      fr:{spot:"{n} – Tarifs, horaires et accès ({a})",fest:"{n} – Dates, lieu et conseils ({a})",shop:"{n} – Guide shopping et quoi acheter ({a})",food:"{n} – Spécialité de {a} et où la goûter"}};
    const a=T((it.sub&&AREA[it.sub]?.ko.split("·")[0])||CITIES[it.city].ko), n=T(it.name);
    let desc=[T(it.desc),T(it.tip||"")].filter(Boolean).join(" "); if(desc.length>160) desc=desc.slice(0,157)+"…";
    const g=(window.GEO||{})[it.id];
    window.__ld={"@context":"https://schema.org","@type":it.type==="spot"?"TouristAttraction":"Place",name:n,alternateName:it.jp,description:T(it.desc),
      ...(g?{geo:{"@type":"GeoCoordinates",latitude:g[0],longitude:g[1]}}:{}),address:{"@type":"PostalAddress",addressCountry:"JP",addressRegion:T(CITIES[it.city].ko)}};
    return {title:(PT[L]||PT.ko)[it.type].replace("{n}",n).replace("{a}",a)+" | Nihon Trip", desc};
  } }
  if(st.view==="home")''', 1))
# 그리기
R.append(('''  document.body.classList.toggle("is-itin", st.view==="itin");''', '''  document.body.classList.toggle("is-itin", st.view==="itin");
  document.body.classList.toggle("is-place", st.view==="place");
  if(st.view==="place"){ const it=byId(st.place); if(!it || !PLACE_TYPES.includes(it.type)) st.view="home"; else { st.city=it.city; st.area=it.sub&&AREA[it.sub]?it.sub:"all"; } }''', 1))
# 상세 창을 조각으로 나눠 장소 페이지와 같이 써요
R.append(('''let SINFO=null;
function openItem(id){''', '''let SINFO=null;
const PLACE_TYPES = ["spot","fest","shop","food"];
const placeSlug = id => String(id).replace(/_/g,"-");
let PLACE_IDX = null;
function placeIdOf(slug){ if(!PLACE_IDX){ PLACE_IDX={}; ALL.forEach(x=>{ if(PLACE_TYPES.includes(x.type)) PLACE_IDX[placeSlug(x.id)]=x.id; }); } return PLACE_IDX[slug]; }
const placeHref = id => ROUTED ? window.NT_BASE + LPRE + `place/${placeSlug(id)}/` : "#";
const TYPE_VIEW = {spot:"spots",fest:"festivals",shop:"shopping",food:"food"};
const plateHTML = it => `<div class="plate" style="--c:var(${colorOf(it)})"><span class="tag">${esc(tagOf(it))}</span><span class="k">${itemIcon(it)}</span>${PHOTO[it.id]?`<img class="bg" src="${esc(PHOTO[it.id].src)}" alt="" aria-hidden="true" decoding="async" referrerpolicy="no-referrer">`:""}${imgTag(it.id)}</div>`;
function detailHTML(it, htag, inDrawer){
  const c = CITIES[it.city], isSaved = saved.includes(it.id);
  const facts = [["지역",`${c.ko}${it.sub&&AREA[it.sub]?" · "+AREA[it.sub].ko:""}`]];
  if(it.dish) facts.push(["대표 메뉴",it.dish]);
  if(it.when) facts.push(["시기",it.when]);
  if(it.area) facts.push(["위치",it.area]);
  if(it.station) facts.push(["가는 길",it.station]);
  if(it.price) facts.push(["가격대","¥".repeat(it.price)+" (3단계 중 "+it.price+")"]);
  const mq = encodeURIComponent(`${it.jp} ${it.sub?placeQ(it):c.jp}`);
  const si = it.type==="spot" ? SIV.rows(it.id) : null;
  return `<${htag}>${esc(it.name)}</${htag}><div class="jpn">${esc(it.jp)}</div><p>${esc(it.desc)}</p>
   <dl class="facts">${facts.map(([a,b])=>`<dt>${a}</dt><dd>${esc(b)}</dd>`).join("")}${si?si.rows.map(([k,v])=>`<dt>${{fee:"입장료",hours:"운영 시간",closed:"휴무",status:"현재 상태"}[k]}</dt><dd class="si${k==="status"?" warn":""}">${v.map(x=>`<span>${esc(x)}</span>`).join("")}</dd>`).join(""):""}</dl>
   ${si?`${si.note?`<p class="sinote">${esc(si.note)}</p>`:""}<p class="sisrc">2026년 10월 기준 · 요금과 시간은 바뀔 수 있으니 방문 전에 공식 사이트에서 확인하세요.</p>`:""}
   ${SHOP_PICKS[it.id]&&it.type==="shop"?`<div class="picks2"><b>추천 쇼핑 목록</b><ul>${SHOP_PICKS[it.id].map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>`:""}
   ${it.tip?`<div class="tip"><b>여행 팁</b> · ${esc(it.tip)}</div>`:""}
   ${it.type==="rest"?`<p class="credit">별점과 리뷰는 아래 링크에서 확인하세요. 영업시간·휴무일도 방문 전에 확인하는 게 좋아요.</p>`:""}
   <div class="actions"><button class="btn${isSaved?"":" primary"}" type="button" data-psave="${it.id}">${isSaved?"나의 여행에서 빼기":"나의 여행에 저장"}</button>
   <a class="btn" href="https://www.google.com/maps/search/?api=1&query=${mq}" target="_blank" rel="noopener">${it.type==="rest"?"Google 지도 평점 ↗":"지도에서 보기 ↗"}</a>
   ${inDrawer&&ROUTED&&PLACE_TYPES.includes(it.type)?`<a class="btn" href="${placeHref(it.id)}">장소 페이지<i> →</i></a>`:""}
</div>
   ${it.type!=="rest"&&PHOTO[it.id]?`<div class="credit">사진:${esc(PHOTO[it.id].artist||"저작자 정보는 원본 참고")}${PHOTO[it.id].license?" · "+esc(PHOTO[it.id].license):""} · <a href="${PHOTO[it.id].lang==="ja"&&!PHOTO[it.id].commons?"https://ja.wikipedia.org/wiki/File:":"https://commons.wikimedia.org/wiki/File:"}${encodeURIComponent(PHOTO[it.id].file.replace(/ /g,"_"))}" target="_blank" rel="noopener">사진 원본 ↗</a></div>`:""}`;
}
V.place = function(){
  const it = byId(st.place); if(!it) return "";
  const c = CITIES[it.city], A = it.sub&&AREA[it.sub], view = TYPE_VIEW[it.type];
  const pool = ALL.filter(x=>x.id!==it.id && PLACE_TYPES.includes(x.type) && x.city===it.city);
  const hv = v => ROUTED ? ` href="${window.NT_BASE + LPRE + pathOf({...st, view:v, city:v==="home"?"all":st.city})}"` : ` href="#"`;
  const near = [...new Set([...pool.filter(x=>x.sub===it.sub && x.type===it.type), ...pool.filter(x=>x.sub===it.sub && x.type!==it.type), ...pool.filter(x=>x.type===it.type)])].slice(0,8);
  return `<article class="place">
   <nav class="crumb" aria-label="breadcrumb"><a${hv("home")} data-view="home">Nihon Trip</a><i>›</i><a${hv(view)} data-view="${view}"><span>${esc(c.ko)}</span>${A?`<i>·</i><span>${esc(A.ko)}</span>`:""}</a><i>›</i><a${hv(view)} data-view="${view}">${esc(PAGE_LABEL[view])}</a></nav>
   <div class="pl-grid">${plateHTML(it)}<div class="pl-main">${detailHTML(it,"h1")}</div></div>
   ${near.length?`<section class="pl-more"><h2>같은 지역의 다른 곳</h2><div class="grid">${near.map(card).join("")}</div></section>`:""}
   <div class="pl-all"><a class="btn"${hv(view)} data-view="${view}">목록 전체 보기<i> →</i></a></div>
  </article>`;
};
function openItem(id){''', 1))
# 상세 창 본문을 조각 함수로
DRAWER_OLD_START = '''  const it = byId(id); if(!it) return;
  lastFocus=document.activeElement;
  const c = CITIES[it.city], isSaved = saved.includes(it.id);'''
DRAWER_END = '''  $("#drawer").hidden=false; $("#scrim").hidden=false;
  $("#closeD").focus();
  $("#closeD").onclick=closeItem;
  $("#toggleSave").onclick=()=>{ saved = saved.includes(it.id)? saved.filter(x=>x!==it.id) : [...saved,it.id]; persist(); render(); openItem(it.id); };
}'''
DRAWER_NEW = '''  const it = byId(id); if(!it) return;
  lastFocus=document.activeElement;
  $("#drawer").innerHTML = `<button class="close" type="button" id="closeD" aria-label="닫기">×</button>
   ${it.type==="rest" ? restGallery(it) : plateHTML(it)}
   <div class="in">${detailHTML(it,"h2",true)}</div>`;
  $("#drawer").hidden=false; $("#scrim").hidden=false;
  $("#closeD").focus();
  $("#closeD").onclick=closeItem;
}'''
# 클릭: 링크 카드는 새 탭 열기(Ctrl·Cmd 클릭)를 살리고, 저장 버튼은 위임 처리
R.append(('''  const o = e.target.closest("[data-open]"); if(o){ openItem(o.dataset.open); return; }''',
          '''  const ps = e.target.closest("[data-psave]"); if(ps){ const id=ps.dataset.psave; saved = saved.includes(id)? saved.filter(x=>x!==id) : [...saved,id]; persist(); const dOpen=!$("#drawer").hidden; render(); if(dOpen) openItem(id); return; }
  const o = e.target.closest("[data-open]"); if(o){ if(o.tagName==="A" && (e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)) return; e.preventDefault(); openItem(o.dataset.open); return; }''', 1))

def apply(p):
    s = open(p, encoding='utf-8').read()
    if 'V.place = function' in s:
        print('already', p); return
    for a, b, n in R:
        assert s.count(a) == n, (p, a[:70], s.count(a)); s = s.replace(a, b)
    i = s.index(DRAWER_OLD_START); j = s.index(DRAWER_END, i) + len(DRAWER_END)
    s = s[:i] + DRAWER_NEW + s[j:]
    open(p, 'w', encoding='utf-8').write(s); print('patched', p)

for p in sys.argv[1:]:
    apply(p)
