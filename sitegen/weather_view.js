/*WX_BEGIN*/
/* 월별 날씨·옷차림 (기상청 평년값 1991~2020: 일 최고·최저기온 평균 ℃, 강수량 mm)
   관측 지점: 도쿄·오사카·나고야·히로시마·후쿠오카 / 홋카이도=삿포로, 오키나와=나하, 시코쿠=다카마쓰 */
const WXN = {
 tokyo:{hi:[9.8,10.9,14.2,19.4,23.6,26.1,29.9,31.3,27.5,22.0,16.7,12.0],lo:[1.2,2.1,5.0,9.8,14.6,18.5,22.4,23.5,20.3,14.8,8.8,3.8],pr:[60,57,116,134,140,168,156,155,225,235,96,58]},
 osaka:{hi:[9.7,10.5,14.2,19.9,24.9,28.0,31.8,33.7,29.5,23.7,17.8,12.3],lo:[3.0,3.2,6.0,10.9,16.0,20.3,24.6,25.8,21.9,16.0,10.2,5.3],pr:[47,61,103,102,137,185,174,113,153,136,73,56]},
 nagoya:{hi:[9.3,10.5,14.5,20.1,24.6,27.6,31.4,33.2,29.1,23.3,17.3,11.7],lo:[1.1,1.4,4.6,9.7,14.9,19.4,23.5,24.7,21.0,14.8,8.6,3.4],pr:[51,65,116,128,150,187,211,140,232,165,79,57]},
 hiroshima:{hi:[9.9,10.9,14.5,19.8,24.4,27.2,30.9,32.8,29.1,23.7,17.7,12.1],lo:[2.0,2.4,5.1,10.1,15.1,19.8,24.1,25.1,21.1,14.9,8.9,4.0],pr:[46,64,118,141,170,227,280,131,163,109,69,54]},
 shikoku:{hi:[9.7,10.5,14.1,19.8,24.8,27.5,31.7,33.0,28.8,23.2,17.5,12.1],lo:[2.1,2.2,5.0,9.9,15.1,19.8,24.1,25.1,21.2,15.1,9.1,4.3],pr:[39,46,81,75,101,153,160,106,167,120,55,47]},
 fukuoka:{hi:[10.2,11.6,15.0,19.9,24.4,27.2,31.2,32.5,28.6,23.7,18.2,12.6],lo:[3.9,4.4,7.2,11.5,16.1,20.3,24.6,25.4,21.6,16.0,10.6,5.8],pr:[74,70,104,118,134,250,299,210,175,95,91,68]},
 hokkaido:{hi:[-0.4,0.4,4.5,11.7,17.9,21.8,25.4,26.4,22.8,16.4,8.7,2.0],lo:[-6.4,-6.2,-2.4,3.4,9.0,13.4,17.9,19.1,14.8,8.0,1.6,-4.0],pr:[108,92,78,55,56,60,91,127,142,110,114,115]},
 okinawa:{hi:[19.8,20.2,21.9,24.3,27.0,29.8,31.9,31.8,30.6,28.1,25.0,21.5],lo:[14.9,15.1,16.7,19.1,22.1,25.2,27.0,26.8,25.8,23.5,20.4,16.8],pr:[102,115,143,161,245,284,188,240,275,179,119,110]}
};
const WX_ORDER = ["tokyo","osaka","nagoya","hiroshima","shikoku","fukuoka","hokkaido","okinawa"];
const WX_RAINY = {okinawa:[5,6],hokkaido:[]}, WX_TYPH = {okinawa:[7,8,9,10],hokkaido:[]};
const WX_OUT = [[30,"반팔·반바지처럼 얇고 통풍이 잘 되는 옷"],[26,"반팔 티셔츠에 얇은 셔츠나 카디건"],[22,"반팔이나 얇은 긴팔, 저녁엔 가벼운 겉옷"],[18,"긴팔 셔츠나 얇은 니트에 카디건·얇은 재킷"],
  [14,"니트에 재킷이나 트렌치코트"],[10,"코트와 니트, 쌀쌀한 날엔 경량 패딩"],[5,"두꺼운 코트나 패딩에 목도리"],[-99,"두꺼운 패딩과 모자·장갑·목도리, 기모 내의"]];
const WX_FEEL = [[30,"무더운 한여름이에요."],[26,"덥고 습한 날씨예요."],[20,"따뜻해서 다니기 좋은 날씨예요."],[14,"선선한 날씨예요."],[5,"쌀쌀한 겨울 날씨예요."],[-99,"한겨울 추위예요."]];
function wxData(c,m){ const d=WXN[c], i=m-1; return {hi:Math.round(d.hi[i])||0, lo:Math.round(d.lo[i])||0, pr:d.pr[i], hum:(HUM[c]||[])[i]}; }
const wxR = v => Math.round(v);
function wxOutfit(c,m){ const h=wxData(c,m).hi; return WX_OUT.find(x=>h>=x[0])[1]; }
function wxFeel(c,m){ const h=wxData(c,m).hi; return WX_FEEL.find(x=>h>=x[0])[1]; }
function wxExtras(c,m){
  const {hi,lo,pr,hum} = wxData(c,m), out=[];
  const rainy = (WX_RAINY[c]||[6,7]).includes(m), typh = (WX_TYPH[c]||[8,9]).includes(m);
  if(hi-lo>=7 && hi>=12 && hi<28) out.push("아침저녁과 낮의 기온 차가 커요. 벗고 입기 쉬운 겉옷을 챙기세요.");
  if(hi<=5) out.push("눈길이 미끄러워요. 미끄럼 방지 신발이나 방한 부츠를 준비하세요.");
  if(hi<=9) out.push("핫팩이 있으면 야외 관광이 훨씬 편해요.");
  if(hi>9 && hi<18) out.push("해가 지면 쌀쌀해요. 얇은 머플러나 스카프가 있으면 좋아요.");
  if(rainy) out.push("장마철이에요. 접이식 우산과 젖어도 괜찮은 신발을 챙기세요.");
  else if(pr>=150) out.push("비 오는 날이 많은 달이에요. 접이식 우산을 챙기세요.");
  if(typh) out.push("태풍 시즌이에요. 일정에 여유를 두고 출발 전 예보를 확인하세요.");
  if(hi>=30) out.push("무더워요. 모자나 양산, 손 선풍기, 물을 챙기고 한낮엔 실내 일정을 넣으세요.");
  if(hi>=27) out.push("실내 냉방이 강하니 얇은 겉옷 하나를 들고 다니세요.");
  if(hum>=75 && hi>=26) out.push("습도가 높아요. 땀이 잘 마르는 옷이 편해요.");
  if(c==="okinawa" ? hi>=24 : (hi>=24 && m>=5 && m<=8)) out.push("햇볕이 강해요. 선크림과 선글라스를 챙기세요.");
  if(hi<=13 && hum && hum<=60) out.push("공기가 건조해요. 립밤과 보습제가 있으면 좋아요.");
  if(hi>=18 && hi<26 && !rainy && pr<150) out.push("걷기 좋은 날씨예요. 편한 운동화면 충분해요.");
  return out;
}
const wxHref = (c,m) => ROUTED ? window.NT_BASE + LPRE + (c==="all" ? (m?`weather/${m}/`:"weather/") : (m?`${c}/weather/${m}/`:`${c}/weather/`)) : "#weather";
const wxA = (c,m,inner,cls) => `<a${cls?` class="${cls}"`:""} href="${wxHref(c,m)}" data-wxc="${c}" data-wxm="${m||0}">${inner}</a>`;
function wxChart(c,m){
  const d=WXN[c], W=600, H=190, top=18, bot=44, lo=Math.min(...d.lo, 0), hi=Math.max(...d.hi, 30), y=v=>top+(1-(v-lo)/(hi-lo))*(H-top-bot), cw=W/12;
  const pt = a => a.map((v,i)=>`${(i*cw+cw/2).toFixed(1)},${y(v).toFixed(1)}`).join(" ");
  return `<svg class="wxchart" viewBox="0 0 ${W} ${H}" role="img" aria-hidden="true">
    ${m?`<rect x="${(m-1)*cw+2}" y="4" width="${cw-4}" height="${H-8}" rx="8" fill="var(--shu)" opacity=".09"/>`:""}
    <line x1="0" x2="${W}" y1="${y(0)}" y2="${y(0)}" stroke="var(--line)" stroke-dasharray="3 4"/>
    <polyline points="${pt(d.hi)}" fill="none" stroke="var(--shu)" stroke-width="2.5" stroke-linejoin="round"/>
    <polyline points="${pt(d.lo)}" fill="none" stroke="var(--ai)" stroke-width="2.5" stroke-linejoin="round"/>
    ${d.hi.map((v,i)=>`<circle cx="${i*cw+cw/2}" cy="${y(v)}" r="${i===m-1?4.5:3}" fill="var(--shu)"/><text x="${i*cw+cw/2}" y="${y(v)-8}" text-anchor="middle" class="th">${wxR(v)}°</text>`).join("")}
    ${d.lo.map((v,i)=>`<circle cx="${i*cw+cw/2}" cy="${y(v)}" r="${i===m-1?4.5:3}" fill="var(--ai)"/><text x="${i*cw+cw/2}" y="${y(v)+16}" text-anchor="middle" class="tl">${wxR(v)}°</text>`).join("")}
    ${d.hi.map((v,i)=>`<text x="${i*cw+cw/2}" y="${H-6}" text-anchor="middle" class="tm">${i+1}</text>`).join("")}
  </svg>`;
}
const wxStat = (lbl,val,cls) => `<div class="wxst${cls?" "+cls:""}"><span>${lbl}</span><b>${val}</b></div>`;
function wxMonths(c,m){ return `<div class="wxmon">${Array.from({length:12},(_,i)=>i+1).map(k=>wxA(c,k,`${k}월`,k===m?"on":"")).join("")}</div>`; }
function wxCities(c,m){ return `<div class="wxmon wxcit">${WX_ORDER.map(k=>wxA(k,m,esc(CITIES[k].ko),k===c?"on":"")).join("")}</div>`; }
function wxFestLink(c,m){ return c==="all"
  ? `<a class="btn ghost" href="${ROUTED?window.NT_BASE+LPRE+`festivals/${m}/`:"#festivals"}" data-wxfest="all" data-m="${m}">${m}월 축제 보기<i> →</i></a>`
  : `<a class="btn ghost" href="${ROUTED?window.NT_BASE+LPRE+`${c}/${areasOf(c)[0].key}/festivals/`:"#festivals"}" data-wxfest="${c}" data-m="${m}">${m}월 축제 보기<i> →</i></a>`; }
const WX_SRC = `<p class="sisrc">기상청 평년값(1991~2020년) 기준이에요. 그해 날씨에 따라 다를 수 있어요.</p><p class="sisrc">홋카이도는 삿포로, 오키나와는 나하, 시코쿠는 다카마쓰 관측값이에요.</p>`;
function wxMemo(m){ const mm=(typeof MONTH_MOOD!=="undefined"&&MONTH_MOOD[m-1])||[]; return mm.length?`<div class="gblk"><h4>${m}월 여행 메모</h4><dl class="wxmemo">${mm.map(r=>`<dt>${esc(r[0])}</dt><dd>${esc(r[1])}</dd>`).join("")}</dl></div>`:""; }
V.weather = function(){
  const c = WXN[st.city] ? st.city : "all", m = st.wm>=1&&st.wm<=12 ? st.wm : 0;
  const crumb = `<nav class="wxcrumb">${wxA("all",0,"일본 월별 날씨와 옷차림")}${c!=="all"?` <i>›</i> ${wxA(c,0,esc(CITIES[c].ko))}`:""}</nav>`;
  if(c==="all" && !m){
    return `<div class="wx">
     <div class="ghead"><h2>일본 월별 날씨와 옷차림</h2><p>도시와 달을 고르면 평균 기온, 강수량, 추천 옷차림을 볼 수 있어요.</p></div>
     <div class="gblk"><h4>도시를 고르세요</h4>${wxCities("",0)}</div>
     <div class="gblk"><h4>달을 고르세요</h4>${wxMonths("all",0)}</div>
     <div class="gblk"><h4>평균 최고·최저 기온 (°C)</h4><div class="wxtblw"><table class="wxtbl"><thead><tr><th></th>${Array.from({length:12},(_,i)=>`<th>${wxA("all",i+1,`${i+1}월`)}</th>`).join("")}</tr></thead>
      <tbody>${WX_ORDER.map(k=>`<tr><th>${wxA(k,0,esc(CITIES[k].ko))}</th>${WXN[k].hi.map((v,i)=>`<td>${wxA(k,i+1,`<b>${wxR(v)}°</b><small>${wxR(WXN[k].lo[i])}°</small>`)}</td>`).join("")}</tr>`).join("")}</tbody></table></div></div>
     ${WX_SRC}
    </div>`;
  }
  if(c==="all"){
    return `<div class="wx">${crumb}
     <div class="ghead"><h2>일본 ${m}월 날씨와 옷차림</h2><p>도시별 평균 기온과 강수량, 추천 옷차림을 비교해 보세요.</p></div>
     ${wxMonths("all",m)}
     <h3 class="sgh"><span>도시별 ${m}월 날씨</span></h3>
     <div class="wxgrid">${WX_ORDER.map(k=>{ const d=wxData(k,m); return `<article class="wxcard"><h3>${esc(CITIES[k].ko)}</h3>
       <div class="wxsts">${wxStat("평균 최고",`${wxR(d.hi)}°`,"hi")}${wxStat("평균 최저",`${wxR(d.lo)}°`,"lo")}${wxStat("강수량",`${d.pr}mm`)}</div>
       <p class="wxfeel">${esc(wxFeel(k,m))}</p><p class="wxo"><span>추천 옷차림</span> ${esc(wxOutfit(k,m))}</p>
       ${wxA(k,m,`자세히 보기<i> →</i>`,"more")}</article>`; }).join("")}</div>
     ${wxMemo(m)}
     <div class="wxlinks">${wxFestLink("all",m)}</div>
     ${WX_SRC}
    </div>`;
  }
  if(!m){
    return `<div class="wx">${crumb}
     <div class="ghead"><h2>${esc(CITIES[c].ko)} 월별 날씨와 옷차림</h2><p>달을 누르면 그달의 옷차림과 챙기면 좋은 것을 볼 수 있어요.</p></div>
     <div class="gblk"><h4>월별 평균 기온</h4>${wxChart(c,0)}<p class="wxleg"><span class="hi">평균 최고</span><span class="lo">평균 최저</span></p></div>
     <div class="wxtblw"><table class="wxtbl wxrows"><thead><tr><th></th><th>평균 최고</th><th>평균 최저</th><th>강수량</th><th>추천 옷차림</th></tr></thead>
      <tbody>${Array.from({length:12},(_,i)=>{ const d=wxData(c,i+1); return `<tr><th>${wxA(c,i+1,`${i+1}월`)}</th><td>${wxR(d.hi)}°</td><td>${wxR(d.lo)}°</td><td>${d.pr}mm</td><td class="o">${esc(wxOutfit(c,i+1))}</td></tr>`; }).join("")}</tbody></table></div>
     ${wxCities(c,0)}
     ${WX_SRC}
    </div>`;
  }
  const d = wxData(c,m), ex = wxExtras(c,m);
  return `<div class="wx">${crumb}
   <div class="ghead"><h2>${esc(CITIES[c].ko)} ${m}월 날씨와 옷차림</h2><p>${esc(wxFeel(c,m))}</p></div>
   <div class="wxsts big">${wxStat("평균 최고",`${wxR(d.hi)}°`,"hi")}${wxStat("평균 최저",`${wxR(d.lo)}°`,"lo")}${wxStat("강수량",`${d.pr}mm`)}${d.hum?wxStat("습도",`${d.hum}%`):""}</div>
   <div class="wxtwo">
    <div class="gblk"><h4>추천 옷차림</h4><p class="wxout">${esc(wxOutfit(c,m))}</p>
     ${ex.length?`<h4>챙기면 좋은 것</h4><ul class="gul">${ex.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>`:""}</div>
    <div class="gblk"><h4>월별 평균 기온</h4>${wxChart(c,m)}<p class="wxleg"><span class="hi">평균 최고</span><span class="lo">평균 최저</span></p></div>
   </div>
   <h3 class="sgh"><span>다른 달 보기</span></h3>${wxMonths(c,m)}
   <h3 class="sgh"><span>다른 도시 보기</span></h3>${wxCities(c,m)}
   ${wxMemo(m)}
   <div class="wxlinks">${wxFestLink(c,m)}${wxA("all",m,`일본 ${m}월 날씨와 옷차림<i> →</i>`,"btn ghost")}</div>
   ${WX_SRC}
  </div>`;
};
/*WX_END*/
