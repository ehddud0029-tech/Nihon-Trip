/*STAY_BEGIN*/
/* 숙소: stay/ (전체·예약 방법), <도시>/stay/ (묵기 좋은 동네 + 추천 숙소). 동네 비교는 여행 준비 > 숙소(GUIDE)의 내용을 그대로 써요.
   추천 숙소 링크는 마이리얼트립 제휴 링크라 한국어·영어 페이지에만 보여요. */
const STAY_CITIES = ["tokyo","osaka","fukuoka","hokkaido","okinawa","nagoya"];
const STAY_GUIDE_IDX = {tokyo:1, osaka:2, fukuoka:3, hokkaido:4, okinawa:5};   // GUIDE 숙소 섹션의 compare 블록 순서
const STAY_EXTRA = {
 nagoya:{sub:"짧게 머문다면 나고야역, 쇼핑과 밤 시간을 즐기려면 사카에가 좋아요.", opts:[
  {name:"나고야역", pros:"공항 열차와 신칸센이 바로 닿고, 이누야마·다카야마로 가는 열차도 여기서 출발해요.", cons:"저녁 분위기는 사카에보다 조용한 편이에요.", for:"근교로 자주 이동하는 분, 일정이 짧은 분"},
  {name:"사카에", pros:"백화점·맛집·오아시스21이 모인 번화가라 밤까지 즐길 거리가 많아요.", cons:"신칸센을 타려면 지하철로 나고야역까지 가야 해요(약 5분).", for:"쇼핑과 맛집을 즐기는 분"}]}
};
const HOTELS = [
 {city:"osaka", area:"난바", ko:"APA호텔&리조트 오사카 난바 역앞 타워", ja:"アパホテル&リゾート〈大阪難波駅前タワー〉", url:"https://myrealt.rip/101a94d",
  st:"난바역 앞", pts:["객실 2,000실이 넘는 대형 타워 호텔","노천탕·사우나가 있는 대욕장 (투숙객 무료)","40층 수영장 (여름 시즌)"]},
 {city:"osaka", area:"교토역 주변", ko:"교토 우메코지 카덴쇼", ja:"京都 梅小路 花伝抄", url:"https://myrealt.rip/101bF2d",
  st:"JR 우메코지교토니시역 도보 약 1분 (교토역에서 한 정거장)", pts:["천연 온천 대욕장","무료 전세탕 5곳 (예약 없이 빈 곳 이용)","교토 철도박물관이 바로 옆"]},
 {city:"tokyo", area:"신주쿠", ko:"신주쿠 워싱턴 호텔 본관", ja:"新宿ワシントンホテル本館", url:"https://myrealt.rip/101aG3e",
  st:"JR 신주쿠역 남쪽 출구 도보 약 8분 (지하도 연결)", pts:["공항 리무진버스가 호텔에 바로 서요","도쿄도청 전망실까지 걸어갈 수 있어요","건물 안에 편의점·식당"]},
 {city:"fukuoka", area:"텐진", ko:"컴포트 인 후쿠오카 텐진", ja:"コンフォートイン福岡天神", url:"https://myrealt.rip/101aC05",
  st:"덴진미나미역 도보 약 1분 · 덴진역 도보 약 5분", pts:["나카스 야타이 거리까지 걸어서 약 7분","1층 코메다 커피에서 조식","24시간 코인 세탁 (세제 무료)"]},
 {city:"fukuoka", area:"유후인", ko:"유후인 바이엔 가든 리조트", ja:"由布院 梅園 GARDEN RESORT", url:"https://myrealt.rip/101bJ18",
  st:"JR 유후인역에서 택시 약 5분", pts:["유후다케가 보이는 노천 대욕장","노천탕이 딸린 별채 객실","경사·계단이 많아 걷기 불편하면 확인하세요"]},
 {city:"hokkaido", area:"삿포로역", ko:"삿포로 호텔 바이 그랑벨", ja:"札幌ホテル by グランベル", url:"https://myrealt.rip/101aUe8",
  st:"JR 삿포로역 북쪽 출구 도보 약 7분", pts:["25층 천연 온천 대욕장·사우나 (투숙객 무료)","1층 24시간 편의점","삿포로역에서 신치토세공항까지 열차로 약 37분"]},
 {city:"okinawa", area:"차탄", ko:"레쿠 오키나와 차탄 스파&리조트", ja:"レクー沖縄北谷スパ&リゾート", url:"https://myrealt.rip/101bB24",
  st:"아메리칸 빌리지 안 · 나하공항에서 차로 약 40분", pts:["천연 온천 대욕장 (투숙객 무료)","옥상 인피니티 풀 (시즌·유료)","선셋 비치까지 걸어서 몇 분"]},
 {city:"nagoya", area:"사카에", ko:"컴포트 인 나고야 사카에", ja:"コンフォートイン名古屋栄", url:"https://myrealt.rip/101bG56",
  st:"사카에역 2번 출구 도보 약 1분", pts:["주부공항에서 리무진버스로 약 55분 (사카에 오아시스21)","나고야 명물 요리가 나오는 조식 (조식 포함 요금)","전 객실 금연"]}
];
const stayShowHotels = () => { const l=(window.I18N&&window.I18N.lang)||"ko"; return l==="ko"||l==="en"; };
function stayAreas(c){
  if(STAY_EXTRA[c]) return STAY_EXTRA[c];
  const sec = (GUIDE.secs||[]).find(x=>x.key==="stay"); const b = sec && sec.blocks[STAY_GUIDE_IDX[c]];
  return b ? {sub:b.sub, opts:b.opts} : {sub:"", opts:[]};
}
const stayHref = c => ROUTED ? window.NT_BASE + LPRE + (c && c!=="all" ? `${c}/stay/` : "stay/") : "#stay";
const stayA = (c,inner,cls) => `<a${cls?` class="${cls}"`:""} href="${stayHref(c)}" data-stayc="${c||"all"}">${inner}</a>`;
function hotelCard(h){
  return `<article class="hcard"><div class="htop"><span class="harea">${esc(h.area)}</span></div>
   <h3>${esc(h.ko)}</h3><p class="hja notranslate" lang="ja">${esc(h.ja)}</p>
   <p class="hst">${esc(h.st)}</p><ul class="gul">${h.pts.map(p=>`<li>${esc(p)}</li>`).join("")}</ul>
   <a class="btn hbtn" href="${h.url}" target="_blank" rel="sponsored noopener">마이리얼트립에서 예약하기 ↗</a></article>`;
}
const STAY_AD = `<p class="sisrc">이 링크로 예약하면 Go Nihon Trip이 제휴 수수료를 받을 수 있어요. 숙박 요금은 같아요.</p>`;
function stayChips(cur){ return `<div class="wxmon">${STAY_CITIES.map(k=>stayA(k,esc(CITIES[k].ko),k===cur?"on":"")).join("")}</div>`; }
const STAY_SITES = ["아고다: 아시아 숙소가 많고 한국어로 예약할 수 있어요.","부킹닷컴: 무료 취소 요금이 많아 일정이 바뀔 수 있을 때 좋아요.",
 "라쿠텐 트래블·자란: 일본 예약 사이트라 료칸·온천 숙소가 많고 할인 쿠폰이 자주 나와요.","호텔 공식 사이트: 회원 요금이나 조식 같은 특전이 있는지 비교해 보세요."];
const STAY_CHECK = ["무료 취소 기한: 일본 시간 기준인지, 며칠 전까지인지 확인하세요.","표시된 금액이 1인 요금인지 1실 요금인지 확인하세요. 일본 사이트는 1인 요금으로 보여 주는 경우가 많아요.",
 "숙박세: 도쿄·오사카·교토·후쿠오카·삿포로 등은 1인 1박마다 숙박세가 붙고, 현장에서 따로 내는 경우도 있어요.","체크인은 보통 15시, 체크아웃은 10~11시예요. 일찍 도착하면 프런트에 짐을 맡길 수 있는지 확인하세요.",
 "침대 크기: '세미더블'은 1인용에 가까운 크기라 둘이 쓰기엔 좁아요."];
const STAY_TYPES = ["비즈니스호텔: 방은 작지만 역 가깝고 깔끔해요. 짧은 일정에 가장 무난해요.","료칸: 다다미방과 온천, 저녁·아침 2식이 포함된 경우가 많아요. 저녁 시간에 맞춰 도착하세요.",
 "캡슐호텔: 가장 저렴하지만 짐 둘 곳이 작고 남녀 층이 나뉘어요.","민박(민파쿠): 가족 여행에 넓은 방이 좋지만, 허가 번호가 있는 숙소인지 확인하세요."];
const stayList = (h,items) => `<div class="gblk"><h4>${h}</h4><ul class="gul">${items.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>`;
V.stay = function(){
  const c = STAY_CITIES.includes(st.city) ? st.city : "";
  const show = stayShowHotels();
  const bc=(i,h)=>`<span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">${h.replace("<a ",'<a itemprop="item" ').replace(/>([^<]*)<\/a>$/,'><span itemprop="name">$1</span></a>')}<meta itemprop="position" content="${i}"></span>`;
  if(!c){
    const sec = (GUIDE.secs||[]).find(x=>x.key==="stay");
    return `<div class="wx">
     <div class="ghead"><h2>일본 숙소 추천과 예약 방법</h2><p>${esc(sec?sec.lead:"")}</p></div>
     <div class="wxgrid">${STAY_CITIES.map(k=>{ const a=stayAreas(k), hs=HOTELS.filter(h=>h.city===k);
       return `<article class="wxcard"><h3>${esc(CITIES[k].ko)}</h3><p class="wxfeel">${a.opts.map(o=>esc(o.name)).join(" · ")}</p>
        ${show&&hs.length?`<p class="wxo"><span>추천 숙소</span> ${hs.map(h=>esc(h.ko)).join(" · ")}</p>`:""}
        ${stayA(k,`자세히 보기<i> →</i>`,"more")}</article>`; }).join("")}</div>
     ${sec?stayList(esc(sec.blocks[0].h), sec.blocks[0].items):""}
     <section id="booking">${stayList("예약 사이트 고르기", STAY_SITES)}</section>
     ${stayList("예약할 때 꼭 확인할 것", STAY_CHECK)}
     ${stayList("숙소 종류", STAY_TYPES)}
     <p class="sisrc">숙소 정보와 요금은 바뀔 수 있어요. 예약 전에 숙소 페이지에서 다시 확인하세요.</p>
    </div>`;
  }
  const a = stayAreas(c), hs = HOTELS.filter(h=>h.city===c), n = esc(CITIES[c].ko);
  const qa=(q,x)=>`<div class="faqi" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><dt itemprop="name">${q}</dt><dd itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><div itemprop="text">${x}</div></dd></div>`;
  return `<div class="wx">
   <nav class="wxcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">${bc(1,stayA("all","일본 숙소 추천과 예약 방법"))}</nav>
   <div class="ghead"><h2>${n} 숙소 추천</h2><p>${esc(a.sub)}</p></div>
   ${stayChips(c)}
   <h3 class="sgh"><span>묵기 좋은 동네</span></h3>
   <div class="stgrid">${a.opts.map(o=>`<article class="gblk starea"><h4>${esc(o.name)}</h4>
     <dl><dt>장점</dt><dd>${esc(o.pros)}</dd><dt>단점</dt><dd>${esc(o.cons)}</dd><dt>이런 분께</dt><dd>${esc(o.for)}</dd></dl></article>`).join("")}</div>
   ${show&&hs.length?`<h3 class="sgh"><span>추천 숙소</span></h3><div class="hgrid">${hs.map(hotelCard).join("")}</div>${STAY_AD}`:""}
   <section class="gblk faq" itemscope itemtype="https://schema.org/FAQPage"><h4>자주 묻는 질문</h4><dl>
    ${qa(`${n}에서는 어느 동네에 묵는 게 좋나요?`, a.opts.map(o=>`<span><b>${esc(o.name)}</b>: <span>${esc(o.for)}</span></span>`).join(" / "))}
    ${qa(`숙소 예약할 때 무엇을 확인해야 하나요?`, STAY_CHECK.slice(0,3).map(x=>`<span>${esc(x)}</span>`).join(" "))}
   </dl></section>
   ${typeof apLinks==="function"?apLinks([c]):""}
   <div class="wxlinks">${stayA("all",`예약 사이트 고르는 법<i> →</i>`,"btn ghost")}</div>
  </div>`;
};
/*STAY_END*/
