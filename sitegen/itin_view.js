/* 추천 일정 */
const IKEYS = ITIN.map(c=>c.key);
const ilang = () => (window.I18N&&window.I18N.lang)||"ko";
function nightsLabel(n){
  const l=ilang();
  if(n===0) return "당일치기";
  return l==="ko"?`${n}박 ${n+1}일`:l==="ja"?`${n}泊${n+1}日`:l==="en"?`${n} night${n>1?"s":""} · ${n+1} days`:l==="es"?`${n} noche${n>1?"s":""} · ${n+1} días`:`${n} nuit${n>1?"s":""} · ${n+1} jours`;
}
function dayLabel(i){ const l=ilang(); return l==="ko"?`${i}일차`:l==="ja"?`${i}日目`:l==="en"?`Day ${i}`:l==="es"?`Día ${i}`:`Jour ${i}`; }
function stopsLabel(n){ const l=ilang(); return l==="ko"?`${n}곳`:l==="ja"?`${n}か所`:l==="en"?`${n} stops`:l==="es"?`${n} paradas`:`${n} étapes`; }
const itinHref = k => ROUTED ? window.NT_BASE + LPRE + (k?`itinerary/${k}/`:"itinerary/") : "#itin";
const ICITY_ORDER = ["tokyo","osaka","fukuoka","hokkaido","okinawa","nagoya","hiroshima","shikoku"];
function itinCard(c){
  const stops = c.plan.reduce((a,d)=>a+d.s.length,0);
  return `<a class="icard" href="${itinHref(c.key)}" data-itin="${c.key}">
    <div class="ich"><span class="inb${c.n===0?" day":""}">${esc(nightsLabel(c.n))}</span><span class="ist">${esc(stopsLabel(stops))}</span></div>
    <h3>${esc(c.title)}</h3><p>${esc(c.sum)}</p>
    <ol class="iflow">${c.plan.map(d=>`<li>${esc(d.t)}</li>`).join("")}</ol>
    <span class="igo">일정 보기<i> →</i></span></a>`;
}
function itinStop(id){
  const it = byId(id); if(!it) return "";
  const si = SIV.rows(id), fee = si && si.rows.find(r=>r[0]==="fee");
  return `<li><button type="button" class="istop" data-open="${id}" style="--c:var(${colorOf(it)})">${mapThumb({id,cat:"spot"})}<span class="isn"><b>${esc(it.name)}</b><small>${esc((it.sub&&AREA[it.sub]?.ko)||CITIES[it.city].ko)}${fee?` · <span class="ifee">${esc(fee[1][0])}</span>`:""}</small></span><span class="iar">›</span></button></li>`;
}
V.itin = function(){
  const c = ITIN.find(x=>x.key===st.itin);
  if(!c){
    return `<div class="itin">
     <div class="ghead"><h2>추천 일정</h2><p>사이트에 소개된 장소들로 짠 일정이에요. 장소를 누르면 입장료와 가는 길을 볼 수 있어요.</p></div>
     ${ICITY_ORDER.map(k=>{ const g=ITIN.filter(x=>x.city===k); return g.length?`<section class="igrp"><h3 class="sgh"><span>${esc(CITIES[k].ko)}</span><small>${esc(CITIES[k].jp)}</small></h3><div class="igrid">${g.map(itinCard).join("")}</div></section>`:""; }).join("")}
    </div>`;
  }
  const others = ITIN.filter(x=>x.city===c.city && x.key!==c.key);
  return `<div class="itin">
   <a class="iback" href="${itinHref("")}" data-itin=""><i>← </i>전체 일정</a>
   <div class="ghead"><div class="ich"><span class="inb${c.n===0?" day":""}">${esc(nightsLabel(c.n))}</span><span class="ist">${esc(CITIES[c.city].ko)}</span></div><h2>${esc(c.title)}</h2><p>${esc(c.sum)}</p></div>
   <ol class="idays">${c.plan.map((d,i)=>`<li class="iday"><div class="idh"><span class="idn">${esc(dayLabel(i+1))}</span><h3>${esc(d.t)}</h3></div><ol class="istops">${d.s.map(itinStop).join("")}</ol></li>`).join("")}</ol>
   ${c.tips.length?`<div class="gblk"><h4><span class="gbi">${gsvg("list")}</span>일정 팁</h4><ul class="gul">${c.tips.map(t=>`<li>${esc(t)}</li>`).join("")}</ul></div>`:""}
   <p class="sisrc">2026년 10월 기준 · 요금과 시간은 바뀔 수 있으니 방문 전에 공식 사이트에서 확인하세요.</p>
   ${others.length?`<div class="gmore"><h4>다른 일정</h4><div>${others.map(o=>`<a href="${itinHref(o.key)}" data-itin="${o.key}"><span>${esc(o.title)}</span> →</a>`).join("")}</div></div>`:""}
  </div>`;
};
