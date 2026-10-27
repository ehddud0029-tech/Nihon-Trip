/* 여행 준비 (입국·돈·통신·에티켓) */
const GKEYS = GUIDE.secs.map(s=>s.key);
const GICON = {
  passport:'<rect x="5" y="3" width="14" height="18" rx="2"/><circle cx="12" cy="10" r="3"/><path d="M9 16h6"/>',
  yen:'<circle cx="12" cy="12" r="9"/><path d="M8.5 7.5 12 12l3.5-4.5M12 12v5M9 13h6M9 15.5h6"/>',
  signal:'<path d="M4 20v-3M9 20v-6M14 20v-9M19 20V5"/>',
  bow:'<circle cx="12" cy="5" r="2"/><path d="M12 7.5c-2.5 0-4 1.6-4.5 4L6 20M12 7.5c2.5 0 4 1.6 4.5 4L18 20M9 13.5h6"/>',
  onsen:'<path d="M3 15c0 3 4 5 9 5s9-2 9-5"/><path d="M3 15h18M8 11c-1-1.2 1-2.3 0-3.5M12 11c-1-1.2 1-2.3 0-3.5M16 11c-1-1.2 1-2.3 0-3.5"/>',
  torii:'<path d="M3 6.5c3 .8 15 .8 18 0M5 6.8 4.6 9M19 6.8l.4 2.2M3.5 9.5h17M7 9.5V21M17 9.5V21M11 9.5v3h2v-3"/>',
  trash:'<path d="M4 7h16M9 7V4.5h6V7M6 7l1 13h10l1-13M10 11v5M14 11v5"/>',
  train:'<rect x="6" y="3.5" width="12" height="13" rx="3"/><path d="M6 10h12M9.5 13.5h.01M14.5 13.5h.01M9 16.5 7 20.5M15 16.5l2 4"/>',
  bowl:'<path d="M3.5 12h17c0 4.4-3.6 8-8 8h-1c-4.4 0-8-3.6-8-8z"/><path d="M8 20.5h8M14 3 9.5 11M19 4l-6.5 7.5"/>',
  warn:'<path d="M12 3 2.5 20h19z"/><path d="M12 10v4.5M12 17.5h.01"/>',
  steps:'<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6h1M4 12h1M4 18h1"/>',
  list:'<path d="M5 12.5 9.5 17 19 7"/>',
  card:'<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 14.5h4"/>',
  ratio:'<path d="M4 20V10M10 20V4M16 20v-7M21 20H3"/>',
  compare:'<rect x="3" y="4" width="7" height="16" rx="1.5"/><rect x="14" y="4" width="7" height="16" rx="1.5"/>'
};
const gsvg = k => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${GICON[k]||GICON.list}</svg>`;
const gsecHref = k => ROUTED ? window.NT_BASE + LPRE + `guide/${k}/` : "#guide";
function gBlock(b){
  const h = `<h4><span class="gbi">${gsvg(b.icon||(b.type==="warn"?"warn":b.type==="steps"?"steps":b.type))}</span>${esc(b.h)}</h4>${b.sub?`<p class="gsub">${esc(b.sub)}</p>`:""}`;
  if(b.type==="steps") return `<div class="gblk">${h}<ol class="gsteps">${b.items.map(t=>`<li>${esc(t)}</li>`).join("")}</ol>${(b.tips||[]).map(t=>`<p class="gtip">${esc(t)}</p>`).join("")}</div>`;
  if(b.type==="ratio") return `<div class="gblk">${h}<div class="gratio">${b.bars.map(([l,v])=>`<div class="grow"><span class="gl">${esc(l)}</span><div class="gbar"><span class="gcard" style="width:${v}%"><b>${esc(b.cardL)}</b> <i>${v}%</i></span><span class="gcash" style="width:${100-v}%"><b>${esc(b.cashL)}</b> <i>${100-v}%</i></span></div></div>`).join("")}</div><ul class="gul">${b.items.map(t=>`<li>${esc(t)}</li>`).join("")}</ul></div>`;
  if(b.type==="cards") return `<div class="gblk">${h}<div class="gcards">${b.cards.map(c=>`<article class="gc"><b>${esc(c.name)}</b><div class="gtags">${c.tags.map(t=>`<span>${esc(t)}</span>`).join("")}</div><p>${esc(c.desc)}</p></article>`).join("")}</div>${b.foot?`<p class="gfoot">${esc(b.foot)}</p>`:""}</div>`;
  if(b.type==="compare") return `<div class="gblk">${h}<div class="gopts">${b.opts.map(o=>`<article class="go go-${o.key}"><h5>${esc(o.name)}</h5><dl><dt>${esc(b.pros)}</dt><dd>${esc(o.pros)}</dd><dt>${esc(b.cons)}</dt><dd>${esc(o.cons)}</dd><dt>${esc(b.for)}</dt><dd>${esc(o.for)}</dd></dl>${o.link?`<a class="gbuy" href="${esc(o.link)}" target="_blank" rel="noopener sponsored">${esc(b.buy)} ↗</a>`:""}</article>`).join("")}</div></div>`;
  return `<div class="gblk${b.type==="warn"?" warn":""}">${h}<ul class="gul">${b.items.map(t=>`<li>${esc(t)}</li>`).join("")}</ul>${b.foot?`<p class="gfoot">${esc(b.foot)}</p>`:""}</div>`;
}
V.guide = function(){
  const isKo = !((window.I18N&&window.I18N.lang)||"").length || window.I18N.lang==="ko";
  const sec = GUIDE.secs.find(s=>s.key===st.gsec) || GUIDE.secs[0];
  const blocks = sec.blocks.filter(b=>!b.only || (b.only==="ko")===isKo);
  const tabs = GUIDE.secs.map(s=>`<a class="gtab" href="${gsecHref(s.key)}" data-gsec="${s.key}"${s.key===sec.key?' aria-current="page"':""}>${gsvg(s.icon)}<span>${esc(s.name)}</span></a>`).join("");
  return `<div class="guide">
   <div class="ghead"><h2>${esc(GUIDE.page.title)}</h2><p>${esc(GUIDE.page.lead)}</p></div>
   <nav class="gtabs" aria-label="${esc(GUIDE.page.title)}">${tabs}</nav>
   <section class="gsec"><div class="gsech"><span class="gsi">${gsvg(sec.icon)}</span><div><h3>${esc(sec.name)}</h3><p>${esc(sec.lead)}</p></div></div>
    ${blocks.map(gBlock).join("")}
    <p class="gupd">${esc(GUIDE.page.upd)}</p></section>
   <div class="gmore"><h4>다른 준비 정보</h4><div>${GUIDE.secs.filter(s=>s.key!==sec.key).map(s=>`<a href="${gsecHref(s.key)}" data-gsec="${s.key}">${gsvg(s.icon)}<span>${esc(s.name)}</span> →</a>`).join("")}</div></div>
  </div>`;
};
