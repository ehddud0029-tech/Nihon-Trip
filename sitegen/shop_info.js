/*SHOPINFO_BEGIN*/
/* 쇼핑 장소의 영업시간·공식 사이트 (2026년 11월, 각 시설 공식 사이트 기준). h=매장 영업시간, r=식당가, hs=일요일·공휴일, u=공식 사이트, f=층별 안내가 있는 시설 */
const SHOP_INFO = {
 yodobashi_umeda:{h:"9:30–22:00",u:"https://www.yodobashi.com/ec/store/0081/",f:1},
 yodobashi_shinjuku:{h:"9:30–22:00",u:"https://www.yodobashi.com/ec/store/0011/",f:1},
 iwataya:{h:"10:00–20:00",u:"https://www.iwataya-mitsukoshi.mistore.jp/iwataya.html",f:1},
 hakatahankyu:{h:"10:00–20:00",u:"https://www.hankyu-dept.co.jp/hakata/",f:1},
 amu_hakata:{h:"10:00–20:00",r:"11:00–22:00",u:"https://www.jrhakatacity.com/",f:1},
 s109:{h:"10:00–21:00",u:"https://shibuya109.jp/",f:1},
 nambaparks:{h:"11:00–21:00",r:"11:00–22:00",u:"https://nambaparks.com/",f:1},
 daimaru_sapporo:{h:"10:00–20:00",r:"11:00–22:00",u:"https://www.daimaru.co.jp/sapporo/",f:1},
 kitte:{h:"11:00–20:00",r:"11:00–22:00",u:"https://marunouchi.jp-kitte.jp/",f:1},
 umie:{h:"10:00–20:00",u:"https://umie.jp/",f:1},
 worldporters:{h:"10:30–21:00",r:"11:00–23:00",u:"https://www.yim.co.jp/",f:1},
 itosaisai:{h:"9:00–18:00",u:"https://ja-itoshima.or.jp/itosaisai/"},
 isetan:{h:"10:00–20:00",u:"https://www.mistore.jp/store/shinjuku.html",f:1},
 solamachi:{r:"11:00–23:00",u:"https://www.tokyo-solamachi.jp/",f:1},
 itoya:{h:"10:00–20:00",hs:"10:00–19:00",u:"https://www.ito-ya.co.jp/ext/store/ginza/ginza/index.html",f:1},
 canal:{h:"10:00–21:00",r:"11:00–23:00",u:"https://canalcity.co.jp/",f:1},
 floral:{h:"9:30–17:30",u:"https://floral-village.com/"},
 harukas:{h:"10:00–20:00",u:"https://abenoharukas.d-kintetsu.co.jp/",f:1},
 hepfive:{h:"11:00–21:00",r:"11:00–22:30",u:"https://www.hepfive.jp/",f:1},
 scramble:{h:"10:00–21:00",r:"11:00–23:00",u:"https://www.shibuya-scramble-square.com/",f:1},
 omohills:{h:"11:00–20:00",r:"11:00–22:30",u:"https://www.omotesandohills.com/",f:1},
 ginzasix:{h:"10:30–20:30",r:"11:00–23:00",u:"https://ginza6.tokyo/",f:1},
 gotemba:{h:"10:00–20:00",u:"https://www.premiumoutlets.co.jp/gotemba/",f:1},
 factory:{h:"10:00–20:00",r:"11:00–22:00",u:"https://sapporofactory.jp/",f:1},
 orgel:{h:"9:00–18:00",u:"https://www.otaru-orgel.co.jp/"},
 kanemori_shop:{h:"9:30–19:00",u:"https://hakodate-kanemori.com/"},
 pineapple:{h:"10:00–18:00",u:"https://www.nagopine.com/"},
 stellar:{u:"https://www.stellarplace.net/",f:1},
 grandfront:{u:"https://www.grandfront-osaka.jp/",f:1},
 p_meieki:{u:"https://www.jr-takashimaya.co.jp/",f:1},
 marinoa:{u:"https://www.marinoacity.com/",f:1},
 p_ekie:{u:"https://www.ekie.jp/",f:1},
 tomita_shop:{u:"https://www.farm-tomita.co.jp/"}
};
const shopInfo = it => (it && it.type==="shop" && SHOP_INFO[it.id]) || null;
function shopFacts(it, facts){ const s=shopInfo(it); if(!s) return;
  if(s.h) facts.push(["영업 시간", s.h]); if(s.hs) facts.push(["일요일·공휴일", s.hs]); if(s.r) facts.push(["식당가", s.r]); }
function shopNote(it){ const s=shopInfo(it); return s&&(s.h||s.r) ? `<p class="sisrc">2026년 11월 기준 · 매장마다 영업시간이 다를 수 있으니 방문 전에 공식 사이트에서 확인하세요.</p>` : ""; }
function shopBtn(it){ const s=shopInfo(it); return s&&s.u ? `<a class="btn" href="${s.u}" target="_blank" rel="noopener">${s.f?"공식 사이트·층별 안내 ↗":"공식 사이트 ↗"}</a>` : ""; }
/*SHOPINFO_END*/
