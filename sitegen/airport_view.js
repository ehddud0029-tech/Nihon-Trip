/*AP_BEGIN*/
/* 공항에서 시내 가는 법: airport/, airport/<공항>/, airport/<공항>/<지역>/  (경로 데이터는 TO_AREA를 그대로 써요) */
const APS = {
 narita:["나리타공항"], haneda:["하네다공항"], kansai:["간사이공항"], fukuoka:["후쿠오카공항","공항 국제선","공항 국내선"],
 oita:["오이타공항"], newchitose:["신치토세공항"], hakodate:["하코다테공항"], asahikawa:["아사히카와공항"],
 naha:["나하공항"], ishigaki:["이시가키공항"], miyako:["미야코공항"], chubu:["주부국제공항"],
 hiroshima:["히로시마공항"], okayama:["오카야마공항"], matsuyama:["마쓰야마공항"], takamatsu:["다카마쓰공항"]
};
const apName = a => APS[a][0];
const apSum = s => s.reduce((t,r)=>t+r.min,0) + (s.length>1?10:0);
function apOpts(a,k){
  const v=TO_AREA[k]||{}, ks=APS[a], o=[];
  (v.direct||[]).filter(r=>ks.includes(r.from)).forEach(r=>o.push([r]));
  if(v.steps && ks.includes(v.steps[0].from)) o.push(v.steps);
  return o.sort((x,y)=>apSum(x)-apSum(y));
}
function apDests(a){ return Object.keys(TO_AREA).filter(k=>AREA[k]&&apOpts(a,k).length).sort((x,y)=>apSum(apOpts(a,x)[0])-apSum(apOpts(a,y)[0])); }
function apRegion(a){ const k=apDests(a)[0]; return k?AREA[k].region:"tokyo"; }
const AP_ORDER = ["tokyo","osaka","nagoya","hiroshima","shikoku","fukuoka","hokkaido","okinawa"];
const apHref = (a,k) => ROUTED ? window.NT_BASE + LPRE + "airport/" + (a?a+"/"+(k?k+"/":""):"") : "#airport";
const apA = (a,k,inner,cls) => `<a${cls?` class="${cls}"`:""} href="${apHref(a,k)}" data-apa="${a||""}" data-apk="${k||""}">${inner}</a>`;
const apMin = m => m>=60 ? `약 ${Math.floor(m/60)}시간${m%60?` ${m%60}분`:""}` : `약 ${m}분`;
function apSteps(s){
  return `<ol class="apsteps">${s.map((r,i)=>`<li><span class="rt">${s.length>1?`<span class="step">${i+1}</span>`:""}<span class="mode m-${r.mode}">${r.mode}</span> ${r.from} → ${r.to} <b class="min">약 ${r.min}분</b></span><small>${r.line}</small></li>`).join("")}</ol>
   <p class="apnote">${s.length>1?`${esc(s[0].to)}에서 갈아타요 · 총 약 ${apSum(s)}분`:"갈아타지 않고 바로 가요"}</p>`;
}
function apIC(r){
  const c=CITIES[r]; if(!c) return "";
  return `<div class="gblk"><h4>교통카드</h4><p class="apic"><b>${esc(c.ic)}</b></p><p>공항에서 교통카드를 사 두면 시내 전철·버스·편의점에서 바로 쓸 수 있어요.</p>
   ${ICBUY[r]?`<p><span class="aplbl">교통카드 사는 곳</span> ${esc(ICBUY[r])}</p>`:""}</div>`;
}
const AP_NOTE = `<p class="sisrc">걸리는 시간은 대략적인 값이에요. 시간표와 요금은 출발 전에 공식 사이트에서 확인하세요.</p>`;
function apChips(list,cur){ return `<div class="wxmon">${list.map(a=>apA(a,"",esc(apName(a)),a===cur?"on":"")).join("")}</div>`; }
V.airport = function(){
  const a = APS[st.ap] ? st.ap : "", k = a && st.apk && apOpts(a,st.apk).length ? st.apk : "";
  const crumb = `<nav class="wxcrumb">${apA("","","일본 공항에서 시내 가는 법")}${a&&k?` <i>›</i> ${apA(a,"",esc(apName(a)))}`:""}</nav>`;
  if(!a){
    return `<div class="wx">
     <div class="ghead"><h2>일본 공항에서 시내 가는 법</h2><p>공항을 고르면 시내와 관광지까지 가는 기차·버스와 걸리는 시간을 볼 수 있어요.</p></div>
     ${AP_ORDER.map(r=>{ const l=Object.keys(APS).filter(x=>apRegion(x)===r); return l.length?`<section><h3 class="sgh"><span>${esc(CITIES[r].ko)}</span><small>${esc(CITIES[r].jp)}</small></h3>
       <div class="apgrid">${l.map(x=>{ const d=apDests(x); return apA(x,"",`<b>${esc(apName(x))}</b><span>${d.slice(0,3).map(k=>esc(AREA[k].ko)).join(" · ")}</span><small>${d.length}곳</small>`,"apcard"); }).join("")}</div></section>`:""; }).join("")}
     ${AP_NOTE}
    </div>`;
  }
  const r = apRegion(a), dests = apDests(a), same = Object.keys(APS).filter(x=>x!==a&&apRegion(x)===r);
  if(!k){
    return `<div class="wx">${crumb}
     <div class="ghead"><h2>${esc(apName(a))}에서 시내 가는 법</h2><p>가고 싶은 곳을 누르면 자세한 가는 법을 볼 수 있어요.</p></div>
     <div class="wxgrid">${dests.map(k2=>{ const o=apOpts(a,k2)[0]; return `<article class="wxcard"><h3>${esc(AREA[k2].ko)}</h3>
       <p class="aprt"><span class="mode m-${o[0].mode}">${o[0].mode}</span> ${o.map(x=>`<span>${x.line}</span>`).join(" → ")}</p><p class="aptm">${apMin(apSum(o))}</p>
       ${apA(a,k2,`자세히 보기<i> →</i>`,"more")}</article>`; }).join("")}</div>
     ${apIC(r)}
     ${same.length?`<h3 class="sgh"><span>다른 공항 보기</span></h3>${apChips(same,"")}`:""}
     ${AP_NOTE}
    </div>`;
  }
  const opts = apOpts(a,k), A = AREA[k];
  const others = Object.keys(APS).filter(x=>x!==a && apOpts(x,k).length);
  const sights = ALL.filter(x=>x.type==="spot" && x.sub===k).slice(0,6);
  return `<div class="wx">${crumb}
   <div class="ghead"><h2>${esc(apName(a))}에서 ${esc(A.ko)} 가는 법</h2><p>가장 빠른 방법은 ${apMin(apSum(opts[0]))} 걸려요.</p></div>
   <div class="apopts">${opts.map((o,i)=>`<div class="gblk apopt">${i===0&&opts.length>1?`<span class="apbest">가장 빨라요</span>`:""}${apSteps(o)}</div>`).join("")}</div>
   ${apIC(r)}
   ${sights.length?`<div class="gblk"><h4>도착해서 가 볼 곳</h4><div class="aplinks">${sights.map(x=>`<a href="${placeHref(x.id)}" data-open="${x.id}">${esc(x.name)}</a>`).join("")}</div></div>`:""}
   ${others.length?`<h3 class="sgh"><span>다른 공항에서 가기</span></h3><div class="wxmon">${others.map(x=>apA(x,k,esc(apName(x)))).join("")}</div>`:""}
   <h3 class="sgh"><span>같은 공항에서 갈 수 있는 곳</span></h3>
   <div class="wxmon">${dests.filter(x=>x!==k).map(x=>apA(a,x,esc(AREA[x].ko))).join("")}</div>
   <div class="wxlinks"><a class="btn ghost" href="${ROUTED?window.NT_BASE+LPRE+`${A.region}/${k}/spots/`:"#spots"}" data-apspots="${k}">${esc(A.ko)} 관광지 보기<i> →</i></a></div>
   ${AP_NOTE}
  </div>`;
};
function apLinks(keys){
  const l = Object.keys(APS).filter(a=>keys.includes(apRegion(a)));
  return l.length ? `<section class="apsec"><div class="sechead"><div><h2>공항에서 시내 가는 법</h2><p>공항을 누르면 지역별로 가는 방법과 걸리는 시간을 볼 수 있어요.</p></div></div>${apChips(l,"")}</section>` : "";
}
/*AP_END*/
