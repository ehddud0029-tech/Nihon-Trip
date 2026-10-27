import json,sys
from playwright.sync_api import sync_playwright
LANG=sys.argv[1]; OUT=f"/home/claude/i18n_work/left_{LANG}.json"
import os
JS=r"""
async ()=>{
const S=new Set(); const H=/[가-힣]/;
function grab(){
  const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  let n; while(n=w.nextNode()){ const p=n.parentElement; if(!p||p.closest('script,style,.notranslate')) continue; const v=n.nodeValue.trim(); if(H.test(v)) S.add(v); }
  document.querySelectorAll('[placeholder],[aria-label],[title],[alt]').forEach(e=>{ if(e.closest('.notranslate')) return; for(const a of ['placeholder','aria-label','title','alt']){ const v=e.getAttribute(a); if(v&&H.test(v)) S.add(v.trim()); } });
  if(H.test(document.title)) S.add(document.title);
}
const tick=()=>new Promise(r=>setTimeout(r,0));
const R=async()=>{ render(); await tick(); grab(); };
const views=["home","spots","festivals","food","transport","shopping","saved"];
// fake photos for credits
ALL.forEach(x=>{ PHOTO[x.id]={src:"data:,",file:"a.jpg",artist:"",license:"",lang:"en"}; });
GIFTS.forEach(x=>{ PHOTO[x.id]={src:"data:,",file:"a.jpg",artist:"",license:""}; });
for(const pass of [0,1]){
 for(let m=1;m<=12;m++){ st.hm=m; st.view="home"; st.city="all"; st.area="all"; for(const h of Object.keys(PAGE_LABEL)){ st.homeTo=h; await R(); } 
   for(let i=0;i<(MONTH_PICKS[m-1]||[]).length;i++){ st.view="home"; st.hm=m; render(); const b=document.querySelector(`[data-rec="${i}"]`); if(b){ b.click(); await tick(); grab(); } } }
 st.hm=null;
 for(const v of views){ for(const c of ["all",...Object.keys(CITIES)]){ const areas=c==="all"?[{key:"all"}]:areasOf(c);
   for(const a of areas){ st.view=v; st.city=c; st.area=a.key; st.more=false; st.focus=null;
     if(v==="festivals"){ for(let m=1;m<=12;m++){ st.month=m; await R(); } }
     else if(v==="food"){ for(const mk of Object.keys(MENU)){ st.menu=mk; await R(); } }
     else if(v==="spots"){ for(const sc of ["all",...Object.keys(SPOT_CAT)]){ st.spotCat=sc; st.more=false; await R(); st.more=true; await R(); } st.spotCat="all"; }
     else await R();
     for(const t of ["t","p","w","h"]){ st.wxTab=t; renderCities(); await tick(); grab(); }
   } } }
 // saved with items
 saved=ALL.slice(0,40).map(x=>x.id); st.view="saved"; st.city="all"; await R(); saved=[];
 // drawer for each item
 for(const x of ALL){ openItem(x.id); await tick(); grab(); saved=[x.id]; openItem(x.id); await tick(); grab(); saved=[]; }
 closeItem();
 st.view="itin"; st.itin=null; await R(); for(const k of IKEYS){ st.itin=k; await R(); } st.itin=null;
 for(const g of GKEYS){ st.view="guide"; st.gsec=g; await R(); }
 st.view="map"; st.city="all"; await R(); for(const c of Object.keys(CITIES)){ st.city=c; await R(); }
 // language menu
 document.querySelector('#langBtn').click(); await tick(); grab(); document.body.click();
 if(pass===0){ WX=window.__FAKEWX; }
}
return [...S];
}
"""
def fake():
    import json
    hours=[f"2026-10-25T{h:02d}:00" for h in range(24)]
    days=[f"2026-10-{d}" for d in range(25,32)]
    hrs=[]; 
    for d in days: hrs+= [f"{d}T{h:02d}:00" for h in range(24)]
    one={"current":{"time":"2026-10-25T10:00","temperature_2m":18.4,"apparent_temperature":17,"weather_code":2,"relative_humidity_2m":63},
     "hourly":{"time":hrs,"temperature_2m":[18]*168,"weather_code":[0,1,2,3,45,51,61,71,80,85,95,2]*14,"precipitation_probability":[10]*168,"wind_speed_10m":[3]*168,"relative_humidity_2m":[60]*168},
     "daily":{"time":days,"weather_code":[0,2,3,61,71,95,45],"temperature_2m_max":[21]*7,"temperature_2m_min":[13]*7,"precipitation_probability_max":[10]*7}}
    return one
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1300,"height":900})
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(f"file:///home/claude/tabishiori.html?lang={LANG}"); pg.wait_for_timeout(800)
    one=fake(); keys=pg.evaluate("Object.keys(CITIES)")
    pg.evaluate("w=>{window.__FAKEWX=w}", {k:one for k in keys})
    res=pg.evaluate(JS)
    print(LANG,len(res), errs[:5]); print(pg.evaluate("document.documentElement.lang+' '+!!window.I18N+' '+document.title"))
    json.dump(sorted(res),open(OUT,"w",encoding="utf-8"),ensure_ascii=False,indent=0)
    b.close()
