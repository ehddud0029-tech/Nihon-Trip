/*SHOPINFO_BEGIN*/
/* 쇼핑 장소의 영업시간·공식 사이트 (2026년 11월, 각 시설 공식 사이트 기준). h=매장 영업시간, r=식당가, hs=일요일·공휴일, u=공식 사이트, f=층별 안내가 있는 시설 */
const SHOP_INFO = {
 yodobashi_umeda:{tf:1,h:"9:30–22:00",u:"https://www.yodobashi.com/ec/store/0081/",f:1},
 yodobashi_shinjuku:{tf:1,h:"9:30–22:00",u:"https://www.yodobashi.com/ec/store/0011/",f:1},
 iwataya:{tf:1,h:"10:00–20:00",u:"https://www.iwataya-mitsukoshi.mistore.jp/iwataya.html",f:1},
 hakatahankyu:{tf:1,h:"10:00–20:00",u:"https://www.hankyu-dept.co.jp/hakata/",f:1},
 amu_hakata:{tf:1,h:"10:00–20:00",r:"11:00–22:00",u:"https://www.jrhakatacity.com/",f:1},
 s109:{tf:1,h:"10:00–21:00",u:"https://shibuya109.jp/",f:1},
 nambaparks:{tf:1,h:"11:00–21:00",r:"11:00–22:00",u:"https://nambaparks.com/",f:1},
 daimaru_sapporo:{tf:1,h:"10:00–20:00",r:"11:00–22:00",u:"https://www.daimaru.co.jp/sapporo/",f:1},
 kitte:{tf:1,h:"11:00–20:00",r:"11:00–22:00",u:"https://marunouchi.jp-kitte.jp/",f:1},
 umie:{tf:1,h:"10:00–20:00",u:"https://umie.jp/",f:1},
 worldporters:{tf:1,h:"10:30–21:00",r:"11:00–23:00",u:"https://www.yim.co.jp/",f:1},
 itosaisai:{h:"9:00–18:00",u:"https://ja-itoshima.or.jp/itosaisai/"},
 isetan:{tf:1,h:"10:00–20:00",u:"https://www.mistore.jp/store/shinjuku.html",f:1},
 solamachi:{tf:1,r:"11:00–23:00",u:"https://www.tokyo-solamachi.jp/",f:1},
 itoya:{h:"10:00–20:00",hs:"10:00–19:00",u:"https://www.ito-ya.co.jp/ext/store/ginza/ginza/index.html",f:1},
 canal:{tf:1,h:"10:00–21:00",r:"11:00–23:00",u:"https://canalcity.co.jp/",f:1},
 floral:{h:"9:30–17:30",u:"https://floral-village.com/"},
 harukas:{tf:1,h:"10:00–20:00",u:"https://abenoharukas.d-kintetsu.co.jp/",f:1},
 hepfive:{tf:1,h:"11:00–21:00",r:"11:00–22:30",u:"https://www.hepfive.jp/",f:1},
 scramble:{tf:1,h:"10:00–21:00",r:"11:00–23:00",u:"https://www.shibuya-scramble-square.com/",f:1},
 omohills:{tf:1,h:"11:00–20:00",r:"11:00–22:30",u:"https://www.omotesandohills.com/",f:1},
 ginzasix:{tf:1,h:"10:30–20:30",r:"11:00–23:00",u:"https://ginza6.tokyo/",f:1},
 gotemba:{tf:1,h:"10:00–20:00",u:"https://www.premiumoutlets.co.jp/gotemba/",f:1},
 factory:{tf:1,h:"10:00–20:00",r:"11:00–22:00",u:"https://sapporofactory.jp/",f:1},
 orgel:{h:"9:00–18:00",u:"https://www.otaru-orgel.co.jp/"},
 kanemori_shop:{h:"9:30–19:00",u:"https://hakodate-kanemori.com/"},
 pineapple:{h:"10:00–18:00",u:"https://www.nagopine.com/"},
 stellar:{tf:1,u:"https://www.stellarplace.net/",f:1},
 grandfront:{tf:1,u:"https://www.grandfront-osaka.jp/",f:1},
 p_meieki:{tf:1,u:"https://www.jr-takashimaya.co.jp/",f:1},
 marinoa:{tf:1,u:"https://www.marinoacity.com/",f:1},
 p_ekie:{tf:1,u:"https://www.ekie.jp/",f:1},
 tomita_shop:{u:"https://www.farm-tomita.co.jp/"},
 kyotostation:{tf:1}
};
/* 노출이 많은 장소의 추가 정보 (공식 사이트 기준, 2026년 11월). a=주소(일본어), w=가는 길 보충, fl=층별 구성, m=추가 소개 */
const PLACE_PLUS = {
 yodobashi_umeda:{a:"大阪府大阪市北区大深町1-1",w:"JR 오사카역 미도스지 출구에서 걸어서 약 1분이에요."},
 yodobashi_shinjuku:{a:"東京都新宿区西新宿1-11-1",w:"JR 신주쿠역 서쪽 출구에서 걸어서 약 2분이에요."},
 iwataya:{a:"福岡県福岡市中央区天神2-5-35",w:"본관과 신관 두 건물로 나뉘어 있어요."},
 hakatahankyu:{a:"福岡県福岡市博多区博多駅中央街1-1",w:"하카타역 건물 안에 있어요.",fl:[["B1","식품관 '우마치카!'·푸드코트"],["1F","화장품·여성 잡화·해외 부티크"],["2F","남성 브랜드 (면세 카운터)"],["3F","주얼리·액세서리·해외 부티크"],["4F–5F","여성복·가방·구두"],["6F","남성복·남성 잡화·골프웨어"],["7F","식기·조리도구·침구·아동복"],["8F","취미 잡화·스포츠·여행 가방·안경"]]},
 amu_hakata:{a:"福岡県福岡市博多区博多駅中央街1-1",w:"하카타역과 바로 이어져요.",fl:[["B1","카페·먹거리 (아뮤 지하)"],["1F","먹거리·잡화·액세서리"],["2F–5F","패션·잡화"],["6F–7F","패션·인테리어·코스메·키즈"],["8F","서점·취미·잡화"],["9F–10F","식당가 '시티 다이닝 구텐'·영화관 T·JOY 하카타"],["RF","옥상 광장 '쓰바메노모리 히로바'"]]},
 s109:{a:"東京都渋谷区道玄坂2-29-1",m:"지하 2층부터 지상 8층까지 10~20대 여성 패션·코스메·잡화 매장이 모여 있어요. 지하 1층에 면세 카운터가 있어요."},
 nambaparks:{a:"大阪府大阪市浪速区難波中2-10-70",w:"난카이 난바역과 바로 이어지고, 지하철 난바역에서도 가까워요.",fl:[["1F–5F","패션·잡화 (로프트·프랑프랑·타워레코드 등)"],["6F","식당가"],["7F","식당가·면세 카운터·외화 환전기"],["8F","영화관·스모 공연장"],["9F","옥상 잔디 광장"]],m:"건물 바깥쪽으로 층층이 이어진 옥상 정원 '파크스 가든'이 있어요."},
 kitte:{a:"東京都千代田区丸の内2-7-2",w:"JR 도쿄역 마루노우치 남쪽 출구에서 걸어서 약 1분이에요.",m:"옛 도쿄중앙우체국 건물을 살린 상업 시설로, 지하 1층~6층에 일본 각지의 먹거리·잡화 가게와 오래된 식당이 모여 있어요. 6층 옥상 정원 'KITTE 가든'에서 도쿄역 건물이 내려다보여요."},
 kyotostation:{subs:[{"n": "교토 포르타", "w": "JR·지하철 교토역, 역 앞 버스 정류장과 바로 이어진 지하상가·역 건물", "d": "1~2층 '오미야게 가도'에 교토 과자·기념품 가게가 모여 있어요. 지하 1층에 면세 카운터가 있어요.", "h": [["1~2층 기념품 거리", "7:30–22:00"], ["지하 1층 상점", "11:00–20:30"], ["11층 식당가", "11:00–22:00"]], "u": "https://www.porta.co.jp/"}, {"n": "아스티 교토", "w": "하치조 출구 쪽 신칸센 개찰구 주변", "d": "1층 개찰구 밖 'ASTY ROAD'에는 기념품·드럭스토어, 2층 신칸센 개찰구 안 'ASTY SQUARE'에는 역 도시락과 교토 기념품 가게가 있어요. 개찰구 안은 승차권이나 입장권이 있어야 들어가요.", "h": [["대부분의 가게", "9:00–21:00 무렵"]], "u": "https://www.asty-kyoto.co.jp/"}, {"n": "더 큐브", "w": "교토역 빌딩 바로 아래 지하", "d": "교토역 빌딩 전문점가. 교토 과자·차 같은 기념품과 패션, 먹거리 가게가 있어요.", "h": [], "u": "https://www.thecube.co.jp/"}, {"n": "JR 교토 이세탄", "w": "교토역 빌딩 안", "d": "역 빌딩 안의 백화점. 지하 식품관에서 교토 과자를 사기 좋고, 미술관 '에키' KYOTO도 있어요.", "h": [], "u": "https://kyoto.wjr-isetan.co.jp/"}, {"n": "교토 타워 산도", "w": "교토역 가라스마 중앙 출구 앞 교토 타워 건물", "d": "지하 1층 푸드홀에 17곳, 1층 마켓에 야쓰하시·화과자·차 가게 17곳이 있어요. 2층에서는 화과자 만들기·기모노 대여 같은 체험을 할 수 있어요.", "h": [["지하 1층 푸드홀", "11:00–23:00"], ["1층 마켓", "10:00–21:00"], ["2층 체험", "10:00–19:00"]], "u": "https://www.kyoto-tower-sando.jp/"}, {"n": "교토 요도바시", "w": "교토역 북쪽, 가라스마 거리", "d": "지하 1층~3층은 가전·카메라 매장 요도바시카메라, 4~5층은 패션(유니클로 등), 6층은 식당가예요.", "h": [["가전 (지하 1층~3층)", "9:30–22:00"], ["6층 식당가", "11:00–23:00"]], "u": "https://www.yodobashi-kyoto.com/"}]},
 nakamise:{m:"길이 약 250m에 가게 87곳이 늘어서 있어요. 에도 시대에 시작된 상점가로, 지금 같은 가게 건물은 1885년에 처음 지어졌어요."}
};
const TAXFREE = ["2026년 11월 1일부터 일본 면세는 환급 방식으로 바뀌었어요. 매장에서는 소비세를 포함한 값으로 계산해요.",
 "면세 매장 한 곳에서 5,000엔(세금 제외) 이상 사면 대상이에요. 계산할 때 여권을 보여 주세요.",
 "산 날부터 90일 안에 출국하면서 공항·항구 세관에서 물건을 가지고 나간다는 확인을 받아야 해요.",
 "확인이 끝나면 산 가게를 통해 소비세만큼 돌려받아요(신용카드 등). 돌려받는 방법과 수수료는 가게마다 달라요.",
 "나리타·하네다·간사이·주부·후쿠오카·신치토세·나하 공항에서는 Visit Japan Web으로 세관 확인을 온라인으로 할 수도 있어요."];
function shopPlus(it){
  if(!it||it.type!=="shop") return "";
  const s=SHOP_INFO[it.id]||{}, p=PLACE_PLUS[it.id]||{};
  if(!s.h&&!s.tf&&!p.a&&!p.m&&!p.fl&&!p.subs) return "";
  const qa=(q,x)=>`<div class="faqi" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><dt itemprop="name">${q}</dt><dd itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><div itemprop="text">${x}</div></dd></div>`;
  const faq=[];
  if(s.h) faq.push(qa("영업시간은 어떻게 되나요?", `<span>영업 시간</span> ${esc(s.h)}${s.hs?` · <span>일요일·공휴일</span> ${esc(s.hs)}`:""}${s.r?` · <span>식당가</span> ${esc(s.r)}`:""} · <span>매장마다 다를 수 있으니 방문 전에 공식 사이트에서 확인하세요.</span>`));
  if(s.tf) faq.push(qa("면세가 되나요?", `<span>면세 매장에서 5,000엔(세금 제외) 이상 사면 대상이에요.</span> <span>2026년 11월부터는 먼저 세금을 포함해 계산하고, 출국할 때 세관 확인을 받으면 돌려받아요.</span>`));
  if(it.station||p.a) faq.push(qa("어떻게 가나요?", `${it.station?`<span>가는 길</span>: <span>${esc(it.station)}</span> · `:""}${p.w?` <span>${esc(p.w)}</span>`:""}${p.a?` <span class="notranslate" lang="ja">${esc(p.a)}</span>`:""}`));
  return `<div class="pplus">
   ${p.m?`<p class="pmore">${esc(p.m)}</p>`:""}
   ${p.fl?`<div class="gblk pfloor"><h4>층별 구성</h4><dl>${p.fl.map(([f,t])=>`<dt>${esc(f)}</dt><dd>${esc(t)}</dd>`).join("")}</dl></div>`:""}
   ${p.subs?`<section class="psubs"><h3 class="sgh"><span>교토역 쇼핑 매장별 안내</span></h3><div class="psgrid">${p.subs.map(x=>`<article class="gblk psub"><h4>${esc(x.n)}</h4><p class="psw">${esc(x.w)}</p><p>${esc(x.d)}</p>${x.h.length?`<dl>${x.h.map(([a,b])=>`<dt>${esc(a)}</dt><dd>${esc(b)}</dd>`).join("")}</dl>`:""}<a class="more" href="${x.u}" target="_blank" rel="noopener">공식 사이트 ↗</a></article>`).join("")}</div></section>`:""}
   ${s.tf?`<div class="gblk ptax"><h4>면세 쇼핑 (2026년 11월부터 바뀐 방식)</h4><ul class="gul">${TAXFREE.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>`:""}
   ${faq.length?`<section class="gblk faq" itemscope itemtype="https://schema.org/FAQPage"><h4>자주 묻는 질문</h4><dl>${faq.join("")}</dl></section>`:""}
  </div>`;
}
const shopInfo = it => (it && it.type==="shop" && SHOP_INFO[it.id]) || null;
function shopFacts(it, facts){ const pa=it&&it.type==="shop"&&PLACE_PLUS[it.id]; if(pa&&pa.a) facts.push(["주소", pa.a]); const s=shopInfo(it); if(!s) return;
  if(s.h) facts.push(["영업 시간", s.h]); if(s.hs) facts.push(["일요일·공휴일", s.hs]); if(s.r) facts.push(["식당가", s.r]); }
function shopNote(it){ const s=shopInfo(it); return s&&(s.h||s.r) ? `<p class="sisrc">2026년 11월 기준 · 매장마다 영업시간이 다를 수 있으니 방문 전에 공식 사이트에서 확인하세요.</p>` : ""; }
function shopBtn(it){ const s=shopInfo(it); return s&&s.u ? `<a class="btn" href="${s.u}" target="_blank" rel="noopener">${s.f?"공식 사이트·층별 안내 ↗":"공식 사이트 ↗"}</a>` : ""; }
/*SHOPINFO_END*/
