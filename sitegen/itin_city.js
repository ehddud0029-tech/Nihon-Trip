/*ICITY_BEGIN*/
/* 도시별 추천 일정 페이지 (itinerary/<도시>/) — 소개·며칠·처음이라면·숙소·시기 (Go Nihon Trip이 직접 쓴 안내, 2026-11) */
const ICITY_INFO = {
 tokyo:{intro:"도쿄는 볼거리가 동네마다 흩어져 있어서 하루에 한두 지역씩 묶어 도는 게 좋아요. 시내만 보면 2박 3일, 하코네·가마쿠라·후지산을 더하면 4박 5일이 알맞아요.",
  days:"처음이라면 3박 4일이 넉넉해요. 2박 3일이면 아사쿠사·시부야·신주쿠 같은 핵심 지역 위주로 보고, 4박 5일 이상이면 근교를 하루 더할 수 있어요.",
  first:"tokyo-3n4d", why:"옛 도쿄와 최신 도쿄를 고르게 볼 수 있어 첫 도쿄 여행에 가장 무난해요.",
  base:"JR 야마노테선과 공항 버스가 편한 신주쿠·시부야, 또는 도쿄역·긴자 주변에 묵으면 어느 일정이든 이동이 쉬워요.",
  season:"벚꽃이 피는 3월 말~4월 초와 단풍이 드는 11월 말~12월 초가 걷기 좋아요. 7~8월은 덥고 습해요."},
 osaka:{intro:"오사카는 교토·나라·고베와 전철로 30분~1시간 거리라, 오사카에 묵으며 근교를 하루씩 다녀오는 일정이 많아요.",
  days:"오사카 시내만이면 2박 3일, 교토를 더하면 3박 4일, 나라까지 넣으면 4박 5일이 알맞아요.",
  first:"osaka-kyoto-3n4d", why:"오사카 먹거리와 교토 대표 명소를 함께 볼 수 있는 가장 인기 있는 조합이에요.",
  base:"교토·나라를 오가려면 우메다(오사카역)나 난바에 묵는 게 편해요. 교토를 오래 본다면 교토역 주변도 좋아요.",
  season:"교토 벚꽃(4월 초)과 단풍(11월 중순~12월 초)이 가장 붐비는 성수기예요. 이때는 숙소를 일찍 잡아 두세요."},
 fukuoka:{intro:"후쿠오카는 공항에서 하카타역까지 지하철로 5분이라 짧은 일정에도 알차게 볼 수 있어요. 유후인·벳푸 온천을 더하면 규슈 여행이 돼요.",
  days:"시내와 다자이후만 보면 1박 2일~2박 3일, 유후인·벳푸까지 가면 3박 4일이 알맞아요.",
  first:"fukuoka-2n3d", why:"하카타·텐진 시내와 다자이후, 야타이까지 무리 없이 다 넣을 수 있어요.",
  base:"하카타역 주변은 공항·기차 이동이 편하고, 텐진·나카스는 쇼핑과 야타이가 가까워요.",
  season:"봄과 가을이 걷기 좋아요. 6~7월 장마와 8~9월 태풍 소식은 미리 확인하세요."},
 hokkaido:{intro:"홋카이도는 도시 사이가 멀어서 한 번에 한두 지역을 고르는 게 좋아요. 삿포로·오타루가 기본이고, 하코다테나 비에이·후라노는 따로 묶어요.",
  days:"삿포로·오타루는 2박 3일~3박 4일, 비에이·후라노나 하코다테를 더하면 하루나 이틀씩 늘려 주세요.",
  first:"sapporo-3n4d", why:"삿포로 시내, 운하 도시 오타루, 야경까지 홋카이도 첫 여행에 필요한 곳을 다 담았어요.",
  base:"삿포로역이나 오도리·스스키노 주변에 묵으면 오타루·공항 가는 JR과 지하철이 모두 편해요.",
  season:"2월 눈축제와 7월 라벤더철이 가장 인기예요. 겨울에는 미끄럽지 않은 신발을 챙기세요."},
 okinawa:{intro:"오키나와 본섬은 버스만으로 다니기 어려워 렌터카 일정이 기본이에요. 이시가키·미야코 같은 섬은 비행기로 따로 가요.",
  days:"본섬은 2박 3일~3박 4일, 이시가키나 미야코를 더하면 섬마다 2박 이상 잡는 게 좋아요.",
  first:"okinawa-3n4d", why:"나하, 북부 수족관, 남부 성지까지 본섬을 한 바퀴 고르게 볼 수 있어요.",
  base:"첫날과 마지막 날은 공항이 가까운 나하에, 중간에는 북부나 중부 해변 쪽 숙소로 옮기면 운전이 줄어요.",
  season:"바다는 4~10월이 좋아요. 6월 장마와 7~9월 태풍은 미리 확인하세요. 겨울은 따뜻하지만 물놀이엔 쌀쌀해요."},
 nagoya:{intro:"나고야는 일본 한가운데에 있어서 시내 관광과 함께 이누야마, 다카야마·시라카와고 같은 산속 마을로 다녀오기 좋아요.",
  days:"나고야 시내와 이누야마는 2박 3일, 다카야마·시라카와고를 더하면 3박 4일 이상이 알맞아요.",
  first:"nagoya-2n3d", why:"나고야성과 박물관, 국보 이누야마성까지 무리 없이 볼 수 있어요.",
  base:"나고야역 주변에 묵으면 공항 열차와 다카야마행 특급 히다가 모두 같은 역에서 출발해 편해요.",
  season:"시라카와고는 1~2월 눈 덮인 풍경이 유명해요. 겨울 산길 버스와 라이트업 행사는 미리 예약하세요."},
 hiroshima:{intro:"히로시마는 평화기념공원과 미야지마를 1박 2일에 볼 수 있고, 오노미치·구라시키를 이어 세토우치 여행으로 넓힐 수 있어요.",
  days:"히로시마와 미야지마만이면 1박 2일, 오노미치·구라시키까지 가면 3박 4일이 알맞아요.",
  first:"hiroshima-miyajima-1n2d", why:"평화기념공원과 바다 위 도리이, 꼭 봐야 할 두 곳을 이틀에 나눠 봐요.",
  base:"히로시마역 주변은 신칸센과 미야지마행 JR이 편하고, 미야지마 안에서 하룻밤 묵으면 저녁 도리이를 조용히 볼 수 있어요.",
  season:"미야지마 도리이는 썰물 때 걸어서 가까이 갈 수 있어요. 방문 전에 물때를 확인하세요."},
 shikoku:{intro:"시코쿠는 도시끼리 거리가 있어서 마쓰야마나 다카마쓰 중 한 곳을 정해 묵는 일정이 편해요.",
  days:"마쓰야마·도고온천은 1박 2일, 다카마쓰와 나오시마·고토히라는 2박 3일이 알맞아요.",
  first:"takamatsu-naoshima-2n3d", why:"정원, 예술 섬, 곤피라궁까지 시코쿠다운 곳을 하루씩 볼 수 있어요.",
  base:"다카마쓰는 항구 근처에 묵으면 나오시마행 페리가 가깝고, 마쓰야마는 도고온천 주변 료칸이 인기예요.",
  season:"나오시마 미술관은 월요일에 쉬는 곳이 많아요. 페리 시간과 휴관일을 함께 확인하세요."}
};
function itinCityMeta(k){
  const L=(window.I18N&&window.I18N.lang)||"ko", T=window.__tr||(x=>x), cn=T(CITIES[k].ko), ns=ITIN.filter(x=>x.city===k).map(x=>x.n);
  const cnt=ns.length, lo=Math.min(...ns), hi=Math.max(...ns), D=hi+1, d1=lo+1, day=lo===0;
  const nl=n=>n===0?T("당일치기"):nightsLabel(n), r=lo===hi?nl(hi):`${nl(lo)}~${nl(hi)}`;
  const t={ko:`${cn} 여행 추천 일정 ${cnt}개 – ${r} 코스`,
    ja:`${cn}旅行のモデルコース${cnt}選 – ${day?"日帰り":`${lo}泊${lo+1}日`}〜${hi}泊${D}日`,
    zh:`${cn}旅行推荐行程${cnt}条 – ${day?"一日游":`${lo}晚${lo+1}天`}到${hi}晚${D}天`,
    tw:`${cn}旅行推薦行程${cnt}條 – ${day?"一日遊":`${lo}晚${lo+1}天`}到${hi}晚${D}天`,
    en:`${cnt} ${cn} Itineraries – ${day?`Day Trips to ${D}-Day Plans`:`${d1}- to ${D}-Day Plans`}`,
    es:`${cnt} itinerarios por ${cn} – ${d1===D?`${D} días`:`de ${d1} a ${D} días`}`,
    fr:`${cnt} itinéraires à ${cn} – ${d1===D?`${D} jours`:`de ${d1} à ${D} jours`}`,
    th:`แผนเที่ยว${cn}แนะนำ ${cnt} แผน – ${day?"ไปกลับวันเดียว":`${d1} วัน`}ถึง ${D} วัน`}[L]||`${cn} – ${r}`;
  return {title:t+" | Go Nihon Trip", desc:T((ICITY_INFO[k]||{}).intro||"")};
}
function itinCityPage(k){
  const I = ICITY_INFO[k] || {}, g = ITIN.filter(x=>x.city===k).sort((a,b)=>a.n-b.n), n = esc(CITIES[k].ko), f = ITIN.find(x=>x.key===I.first);
  const qa=(q,a)=>`<div class="faqi" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><dt itemprop="name">${q}</dt><dd itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><div itemprop="text">${a}</div></dd></div>`;
  return `<div class="itin icity">
   <a class="iback" href="${itinHref("")}" data-itin=""><i>← </i>전체 일정</a>
   <div class="ghead"><h2>${n} 추천 일정</h2>${I.intro?`<p>${esc(I.intro)}</p>`:""}</div>
   <nav class="wxmon ijump">${ICITY_ORDER.filter(c=>ITIN.some(x=>x.city===c)).map(c=>`<a href="${itinHref(c)}" data-itin="${c}"${c===k?' class="on" aria-current="page"':""}>${esc(CITIES[c].ko)}</a>`).join("")}</nav>
   ${f?`<section class="ifirst"><h3 class="sgh"><span>처음이라면 이 일정</span></h3><p class="ifr">${esc(I.why)}</p><div class="igrid">${itinCard(f)}</div></section>`:""}
   <section class="iall"><h3 class="sgh"><span>모든 일정</span></h3><div class="igrid">${g.map(itinCard).join("")}</div></section>
   ${I.days?`<section class="gblk faq" itemscope itemtype="https://schema.org/FAQPage"><h4>자주 묻는 질문</h4><dl>
    ${qa(`${n} 여행은 며칠이 적당한가요?`, esc(I.days))}
    ${f?qa(`${n}에 처음 가면 어떤 일정이 좋나요?`, `<a href="${itinHref(f.key)}" data-itin="${f.key}">${esc(f.title)}</a> <span>${esc(I.why)}</span>`):""}
    ${qa(`${n} 여행 때 어디에 묵으면 좋나요?`, esc(I.base))}
    ${qa(`${n} 여행은 언제 가면 좋나요?`, esc(I.season))}
   </dl></section>`:""}
   <div class="wxlinks ttlinks">${typeof stayA==="function"?stayA(k,`묵기 좋은 동네<i> →</i>`,"btn ghost"):""}${typeof wxA==="function"?wxA(k,0,`월별 기온·강수<i> →</i>`,"btn ghost"):""}</div>
  </div>`;
}
/*ICITY_END*/
