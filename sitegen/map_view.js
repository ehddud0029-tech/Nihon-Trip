/* 지도 페이지: 관광지·축제·맛집(AutoReserve 지역별 TOP 10)·쇼핑을 일본 지도에 표시
   좌표는 geo.js (GEO: 항목 id → [위도, 경도], AR_GEO: AutoReserve 가게 번호 → [위도, 경도, 가게 ID])
   지도: MapLibre GL + OpenFreeMap(무료, API 키 없음). 지도 글자는 고른 언어로 보여요 */
const MCAT = {spot:["관광지","--ai"],fest:["축제","--yamabuki"],rest:["맛집","--shu"],shop:["쇼핑","--matsu"]};
const mst = {cats:{spot:true,fest:true,rest:true,shop:true}, m:0, q:"", area:"all", sel:null};
let MAP=null, MAPREADY=false, MITEMS=null, mlistTimer=0, MPOP=null;
function mapItems(){
  if(MITEMS) return MITEMS;
  const G = window.GEO||{}, AG = window.AR_GEO||{}, out=[];
  ALL.forEach(x=>{ if(!MCAT[x.type]||!G[x.id]) return; out.push({id:x.id,cat:x.type,name:x.name,jp:x.jp,city:x.city,sub:x.sub||null,
    sub2: x.type==="fest" ? `${x.when} · ${placeOf(x)}` : (x.area||x.station||""), month:x.month||0, ll:G[x.id]}); });
  const slugArea = {}; Object.entries(window.AR_SLUG||{}).forEach(([a,sl])=>{ if(!slugArea[sl]) slugArea[sl]=a; });
  const seen = new Set();
  Object.entries(window.AR_LISTS||{}).forEach(([sl,l])=>(l.all||[]).forEach(i=>{
    const g = AG[i], r = (window.AR_SHOPS||{})[i]; if(!g||!r||seen.has(i)) return; seen.add(i);
    const ak = slugArea[sl], A = AREA[ak];
    out.push({id:"ar:"+i,cat:"rest",name:r.n,jp:"",city:A?.region||"",sub:ak||null,sub2:[r.dish,r.feat].filter(Boolean).join(" · "),b:r.b||"",ar:g[2],ll:[g[0],g[1]]});
  }));
  return MITEMS=out;
}
function mapFiltered(){
  const T = window.__tr||(x=>x), q = mst.q.trim().toLowerCase();
  return mapItems().filter(x=>mst.cats[x.cat] && (x.cat!=="fest"||!mst.m||x.month===mst.m)
    && (mst.area==="all" || (mst.area.startsWith("c:") ? x.city===mst.area.slice(2) : x.sub===mst.area))
    && (!q || (x.name+" "+x.jp+" "+T(x.name)+" "+x.sub2+" "+T(x.sub2)).toLowerCase().includes(q)));
}
V.map = () => {
  const n = mapItems(), cnt = c => n.filter(x=>x.cat===c).length;
  const regions = Object.entries(CITIES).map(([k,c])=>`<optgroup label="${esc(c.ko)}"><option value="c:${k}">${esc(c.ko)}</option>${areasOf(k).map(a=>`<option value="${a.key}">${esc(a.ko)}</option>`).join("")}</optgroup>`).join("");
  return `<div class="mapwrap" id="mapwrap">
   <div class="mphead"><div class="eyebrow">日本旅行 · 지도</div><h1>지도에서 찾기</h1>
    <p>관광지·축제·맛집·쇼핑 장소를 일본 지도에서 한눈에 보세요. 핀을 누르면 자세한 정보가 열려요.</p>
    <div class="mcats">${Object.entries(MCAT).map(([k,[l,c]])=>`<button type="button" class="mcat" data-mcat="${k}" aria-pressed="${mst.cats[k]}" style="--c:var(${c})"><i></i>${l} <b>${cnt(k)}</b></button>`).join("")}</div>
    <div class="mmonths" id="mmonths"${mst.cats.fest?"":" hidden"}><button type="button" data-mm="0" aria-pressed="${!mst.m}">축제 전체</button>${Array.from({length:12},(_,i)=>`<button type="button" data-mm="${i+1}" aria-pressed="${mst.m===i+1}">${i+1}월</button>`).join("")}</div>
    <div class="mtools"><select id="marea" aria-label="지역 선택"><option value="all">일본 전체</option>${regions}</select><input id="mq" type="search" placeholder="이름으로 찾기" aria-label="검색" value="${esc(mst.q)}"></div>
   </div>
   <div class="mapbox"><div id="mapc"></div><div class="mapmsg" id="mapmsg">지도를 불러오는 중이에요</div>
    <div class="mapnote">위치는 위키백과·국토지리원·AutoReserve 자료 기준이라 실제 입구와 조금 다를 수 있어요.</div></div>
   <div class="mlistwrap"><div class="mlhead"><span>지도에 보이는 곳</span><b id="mln">0</b></div><div class="mlist" id="mlist"></div></div>
  </div>`;
};
function mapListRender(){
  const el = $("#mlist"); if(!el) return;
  let items = mapFiltered();
  if(MAP && MAPREADY){ const b = MAP.getBounds(); items = items.filter(x=>b.contains([x.ll[1],x.ll[0]])); }
  $("#mln").textContent = items.length;
  const shown = items.slice(0,150);
  el.innerHTML = shown.length ? shown.map(x=>`<button type="button" class="mitem${mst.sel===x.id?" on":""}" data-mid="${x.id}" style="--c:var(${MCAT[x.cat][1]})"><i class="dot"></i><div><small>${MCAT[x.cat][0]}${x.sub&&AREA[x.sub]?" · "+esc(AREA[x.sub].ko):""}</small><b>${esc(x.name)}</b>${x.sub2?`<span>${esc(x.sub2)}</span>`:""}</div></button>`).join("")
    : `<div class="empty">이 범위에는 표시할 곳이 없어요. 지도를 옮기거나 축소해 보세요.</div>`;
}
function mapGeoJSON(){
  return {type:"FeatureCollection",features:mapFiltered().map(x=>({type:"Feature",properties:{id:x.id,cat:x.cat},geometry:{type:"Point",coordinates:[x.ll[1],x.ll[0]]}}))};
}
function mapRefresh(fit){
  mapListRender();
  if(!(MAP&&MAPREADY)) return;
  MAP.getSource("pts")?.setData(mapGeoJSON());
  if(fit) mapFit();
}
function mapFit(){
  const items = mapFiltered(); if(!MAP||!items.length) return;
  if(mst.area==="all" && !mst.q){ MAP.fitBounds([[122.5,24],[146,45.6]],{padding:30,duration:600}); return; }
  let w=180,s=90,e=-180,n=-90; items.forEach(x=>{ w=Math.min(w,x.ll[1]); e=Math.max(e,x.ll[1]); s=Math.min(s,x.ll[0]); n=Math.max(n,x.ll[0]); });
  if(e-w<0.02&&n-s<0.02){ MAP.flyTo({center:[(w+e)/2,(s+n)/2],zoom:15}); return; }
  MAP.fitBounds([[w,s],[e,n]],{padding:60,maxZoom:15,duration:600});
}
function mapPopupHTML(x){
  const c = MCAT[x.cat], L = (window.I18N&&window.I18N.ar)||"ko";
  const gm = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(x.ll[0]+","+x.ll[1])}`;
  const acts = x.cat==="rest"
    ? `<a class="pri" href="https://autoreserve.com/${L}/restaurants/${esc(x.ar)}" target="_blank" rel="noopener">AutoReserve에서 보기 ↗</a><a href="${gm}" target="_blank" rel="noopener">구글 지도 ↗</a>`
    : `<button type="button" class="pri" data-open="${x.id}">자세히 보기</button><a href="${gm}" target="_blank" rel="noopener">구글 지도 ↗</a>`;
  return `<div class="mpop" style="--c:var(${c[1]})"><small>${c[0]}</small><b>${esc(x.name)}</b>${x.jp?`<div class="jp">${esc(x.jp)}</div>`:""}<p>${esc(x.sub2||"")}${x.b?` · ${esc(x.b)}`:""}</p><div class="acts">${acts}</div></div>`;
}
function mapOpen(id, fly){
  const x = mapItems().find(y=>y.id===id); if(!x||!MAP||!MAPREADY) return;
  mst.sel = id;
  if(fly) MAP.flyTo({center:[x.ll[1],x.ll[0]],zoom:Math.max(MAP.getZoom(),14)});
  MPOP?.remove();
  MPOP = new maplibregl.Popup({offset:12,maxWidth:"280px"}).setLngLat([x.ll[1],x.ll[0]]).setHTML(mapPopupHTML(x)).addTo(MAP);
  document.querySelectorAll(".mitem.on").forEach(e=>e.classList.remove("on"));
  document.querySelector(`.mitem[data-mid="${CSS.escape(id)}"]`)?.classList.add("on");
}
function loadMapLib(){
  if(window.maplibregl) return Promise.resolve();
  return new Promise((ok,no)=>{
    const l=document.createElement("link"); l.rel="stylesheet"; l.href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css"; document.head.appendChild(l);
    const s=document.createElement("script"); s.src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"; s.onload=ok; s.onerror=no; document.head.appendChild(s);
  });
}
function mapFail(){ const m=$("#mapmsg"); if(m){ m.hidden=false; m.textContent="지도를 불러오지 못했어요. 인터넷 연결을 확인해 주세요."; } }
function mapMount(){
  const wrap = $("#mapwrap"); if(!wrap) return;
  if(innerWidth>820){ const top = document.querySelector("header.top").getBoundingClientRect().bottom + scrollY; wrap.style.height = Math.max(520, innerHeight - top)+"px"; }
  $("#marea").value = mst.area;
  mapListRender();
  MAPREADY=false;
  loadMapLib().then(()=>{
    if(!document.getElementById("mapc")) return;
    const lang = (window.I18N&&window.I18N.lang)||"ko";
    MAP = new maplibregl.Map({container:"mapc",style:"https://tiles.openfreemap.org/styles/positron",bounds:[[122.5,24],[146,45.6]],fitBoundsOptions:{padding:30},attributionControl:{compact:true},cooperativeGestures:innerWidth<=820});
    MAP.addControl(new maplibregl.NavigationControl({showCompass:false}),"bottom-right");
    MAP.on("load",()=>{
      $("#mapmsg").hidden = true;
      // 지도 글자를 고른 언어로 (없으면 영어, 그다음 현지 이름). 일본어는 현지 이름 그대로
      const nm = lang==="ja" ? ["get","name"] : ["coalesce",["get","name:"+lang],["get","name:en"],["get","name_en"],["get","name"]];
      MAP.getStyle().layers.forEach(l=>{ if(l.type==="symbol" && l.layout && l.layout["text-field"]) try{ MAP.setLayoutProperty(l.id,"text-field",nm); }catch(_){} });
      MAP.addSource("pts",{type:"geojson",data:mapGeoJSON(),cluster:true,clusterRadius:46,clusterMaxZoom:13});
      MAP.addLayer({id:"cl",type:"circle",source:"pts",filter:["has","point_count"],paint:{"circle-color":"#C4452C","circle-opacity":.92,"circle-stroke-color":"#fff","circle-stroke-width":3,
        "circle-radius":["step",["get","point_count"],16,10,20,50,25,150,30]}});
      MAP.addLayer({id:"cln",type:"symbol",source:"pts",filter:["has","point_count"],layout:{"text-field":["get","point_count_abbreviated"],"text-font":["Noto Sans Bold"],"text-size":13,"text-allow-overlap":true},paint:{"text-color":"#fff"}});
      MAP.addLayer({id:"pt",type:"circle",source:"pts",filter:["!",["has","point_count"]],paint:{"circle-radius":7,"circle-stroke-color":"#fff","circle-stroke-width":2,
        "circle-color":["match",["get","cat"],"spot","#23395B","fest","#B8860B","rest","#C4452C","shop","#3E6B48","#555"]}});
      MAP.on("click","cl",e=>{ const f=e.features[0]; MAP.getSource("pts").getClusterExpansionZoom(f.properties.cluster_id).then(z=>MAP.easeTo({center:f.geometry.coordinates,zoom:z})); });
      MAP.on("click","pt",e=>mapOpen(e.features[0].properties.id,false));
      ["cl","pt"].forEach(l=>{ MAP.on("mouseenter",l,()=>MAP.getCanvas().style.cursor="pointer"); MAP.on("mouseleave",l,()=>MAP.getCanvas().style.cursor=""); });
      MAP.on("moveend",()=>{ clearTimeout(mlistTimer); mlistTimer=setTimeout(mapListRender,120); });
      MAPREADY = true;
      if(mst.area!=="all"||mst.q) mapFit(); else mapListRender();
    });
    MAP.on("error",()=>{ if(!MAPREADY) mapFail(); });
  }).catch(mapFail);
}
document.addEventListener("click",e=>{
  const c = e.target.closest("[data-mcat]");
  if(c){ const k=c.dataset.mcat; mst.cats[k]=!mst.cats[k]; c.setAttribute("aria-pressed",String(mst.cats[k])); if(k==="fest") $("#mmonths").hidden=!mst.cats.fest; mapRefresh(false); return; }
  const mm = e.target.closest("[data-mm]");
  if(mm){ mst.m=+mm.dataset.mm; document.querySelectorAll("[data-mm]").forEach(b=>b.setAttribute("aria-pressed",String(+b.dataset.mm===mst.m))); mapRefresh(false); return; }
  const it = e.target.closest("[data-mid]");
  if(it){ mapOpen(it.dataset.mid,true); if(innerWidth<=820) $("#mapwrap .mapbox").scrollIntoView({behavior:"smooth",block:"start"}); }
});
document.addEventListener("change",e=>{ if(e.target.id==="marea"){ mst.area=e.target.value; mapRefresh(true); } });
document.addEventListener("input",e=>{ if(e.target.id==="mq"){ mst.q=e.target.value; clearTimeout(mlistTimer); mlistTimer=setTimeout(()=>mapRefresh(true),250); } });
