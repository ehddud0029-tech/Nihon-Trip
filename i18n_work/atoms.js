// run inside harness: collect all Hangul strings from data globals
{const H=/[가-힣]/; const A=new Set();
 const walk=(v,d)=>{ if(d>8||v==null) return; if(typeof v==="string"){ if(H.test(v)) A.add(v.trim()); return; } if(typeof v==="function") return; if(Array.isArray(v)) v.forEach(x=>walk(x,d+1)); else if(typeof v==="object") Object.values(v).forEach(x=>walk(x,d+1)); };
 const roots={SPOTS,FESTS,SHOPS,FOODS,GIFTS,AREA_GUIDE,IC_CARDS,LOCAL_EATS,SOUVENIR,MONTH_MOOD,MONTH_PICKS,MONTH_ONLY,MONTH_NOTES,SEASON,THEME_INTRO,TRANSPORT,AREA_ROUTE,TO_AREA,AIRPORT,CITIES,AREA,MENU,SPOT_CAT,FOOD_CAT,DOW,SPOTS_MORE,PAGE_LABEL,MOVE_LABEL,ICBUY,ICMAP,WXTABS,AR:window.AR_SHOPS,GP:window.GOOGLE_PICKS,HUM};
 for(const [k,v] of Object.entries(roots)) walk(v,0);
 // split atoms with "·" also
 window.__out=[...A];}
