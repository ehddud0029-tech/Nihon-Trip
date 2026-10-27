{const H=/[가-힣]/; const out=[]; const seen=new Set();
 const add=(src,v,jp)=>{ if(typeof v!=="string"||!H.test(v)) return; v=v.trim(); if(seen.has(v)) return; seen.add(v); out.push([src,v,jp||""]); };
 const walk=(src,v,d)=>{ if(d>8||v==null) return; if(typeof v==="string") return add(src,v); if(typeof v==="function") return; if(Array.isArray(v)) v.forEach(x=>walk(src,x,d+1)); else if(typeof v==="object") Object.values(v).forEach(x=>walk(src,x,d+1)); };
 // names with jp first
 Object.entries(CITIES).forEach(([k,c])=>add("cityname",c.ko,c.jp));
 Object.values(AREA).forEach(a=>add("areaname",a.ko,a.jp));
 [...SPOTS].forEach(x=>add("spotname",x.name,x.jp));
 FESTS.forEach(x=>add("festname",x.name,x.jp)); SHOPS.forEach(x=>add("shopname",x.name,x.jp)); FOODS.forEach(x=>add("foodname",x.name,x.jp)); GIFTS.forEach(x=>add("giftname",x.name,x.jp));
 Object.values(window.AR_SHOPS).forEach(x=>add("arname",x.n));
 Object.values(window.GOOGLE_PICKS||{}).forEach(o=>Object.values(o).forEach(arr=>arr.forEach(r=>add("gpname",r[0],r[1]))));
 // labels
 walk("label",{MENU,SPOT_CAT,FOOD_CAT,PAGE_LABEL,MOVE_LABEL,WXTABS,DOW},0);
 // data
 [...SPOTS].forEach(x=>{ add("spot.area",x.area); add("spot.station",x.station); add("spot.desc",x.desc); add("spot.tip",x.tip); });
 FESTS.forEach(x=>{ walk("fest",[x.when,x.area,x.desc,x.tip],0); });
 SHOPS.forEach(x=>{ walk("shop",[x.cat,x.station,x.desc,x.tip],0); });
 FOODS.forEach(x=>{ walk("food",[x.area,x.desc,x.tip],0); });
 GIFTS.forEach(x=>{ walk("gift",[x.cat,x.desc,x.where.map(w=>w[0])],0); });
 Object.values(window.AR_SHOPS).forEach(x=>{ add("ar.dish",x.dish); });
 Object.values(window.AR_SHOPS).forEach(x=>{ add("ar.feat",x.feat); });
 Object.values(window.GOOGLE_PICKS||{}).forEach(o=>Object.values(o).forEach(arr=>arr.forEach(r=>{ add("gp.dish",r[2]); add("gp.feat",r[3]); add("gp.b",r[4]); })));
 walk("guide",AREA_GUIDE,0); walk("ic",IC_CARDS,0); walk("eats",LOCAL_EATS,0); walk("souvenir",SOUVENIR,0);
 walk("month",[MONTH_MOOD,MONTH_PICKS,MONTH_ONLY,MONTH_NOTES,SEASON],0); walk("theme",THEME_INTRO,0);
 walk("transport",[TRANSPORT,AREA_ROUTE,TO_AREA,AIRPORT,ICBUY,ICMAP],0); walk("cities",CITIES,0);
 walk("misc",{HUM},0);
 window.__out=out;}
