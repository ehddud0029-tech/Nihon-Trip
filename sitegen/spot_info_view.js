/* 입장료·운영 시간 표시 (언어별로 바로 만들어요) */
const SIV = (()=>{
 const W = (ko,en,ja,es,fr)=>({ko,en,ja,es,fr});
 const LB = {
  adult:W("어른","Adults","大人","Adultos","Adultes"), grounds_free:W("경내 무료","Grounds free","境内無料","Recinto gratis","Enceinte gratuite"),
  park_free:W("공원 무료","Park free","公園無料","Parque gratis","Parc gratuit"), beach_free:W("해변 무료","Beach free","海浜無料","Playa gratis","Plage gratuite"),
  island_free:W("섬 둘러보기 무료","Island free to explore","島内散策無料","Isla gratis","Île gratuite"), street_free:W("거리 무료","Street free","街歩き無料","Calle gratis","Rue gratuite"),
  deck:W("전망대","Observation deck","展望台","Mirador","Observatoire"), tower:W("타워","Tower","タワー","Torre","Tour"),
  keep:W("천수각","Main keep","天守閣","Torre del homenaje","Donjon"), paid_area:W("유료 구역","Paid area","有料区域","Zona de pago","Zone payante"),
  rt:W("왕복","Round trip","往復","Ida y vuelta","Aller-retour"), rt_both:W("로프웨이+미니 케이블카 왕복","Ropeway + mini cable car, round trip","ロープウェイ＋ミニケーブルカー往復","Teleférico + minifunicular, ida y vuelta","Téléphérique + mini-funiculaire, aller-retour"),
  rt_herb:W("로프웨이 왕복+허브원","Ropeway round trip + Herb Gardens","ロープウェイ往復＋ハーブ園","Teleférico i/v + jardín de hierbas","Téléphérique A/R + jardin d'herbes"),
  combo7:W("지옥 7곳 공통권 (이틀 유효)","Combined ticket for 7 hells (valid 2 days)","7地獄共通券（2日間有効）","Entrada combinada a 7 infiernos (2 días)","Billet combiné 7 enfers (valable 2 jours)"),
  bath:W("입욕","Bath","入浴","Baño","Bain"), sand:W("모래찜질","Sand bath","砂湯","Baño de arena","Bain de sable"),
  halls_add:W("건물 내부 추가","Halls (extra)","諸堂参拝（追加）","Pabellones (extra)","Pavillons (supplément)"),
  museum:W("국보전","Treasure hall","国宝殿","Sala del tesoro","Salle du trésor"), treasure:W("국보관","Treasure hall","国宝館","Sala del tesoro","Salle du trésor"),
  chukondo:W("중금당","Central Golden Hall","中金堂","Pabellón Dorado Central","Pavillon d'or central"), daibutsuden:W("대불전","Great Buddha Hall","大仏殿","Pabellón del Gran Buda","Pavillon du Grand Bouddha"),
  central:W("중심가람","Central precinct","中心伽藍","Recinto central","Enceinte centrale"), garden:W("정원","Garden","庭園","Jardín","Jardin"),
  zoo:W("동물원","Zoo","動物園","Zoo","Zoo"), nishinomaru:W("니시노마루 정원","Nishinomaru Garden","西の丸庭園","Jardín Nishinomaru","Jardin Nishinomaru"),
  ride:W("1회 탑승","Per ride","1回","Por viaje","Par tour"), houses:W("이진칸 내부 (집마다 다름)","Houses (priced separately)","異人館（館ごとに異なる）","Casas (precio por casa)","Maisons (prix par maison)"),
  candle:W("씨캔들 전망등대","Sea Candle","シーキャンドル","Sea Candle","Sea Candle"), exhibit:W("전시실 (1층 상점은 무료)","Exhibition rooms (1F shop free)","展示室（1階ショップは無料）","Salas de exposición (tienda de la 1.ª planta gratis)","Salles d'exposition (boutique du RDC gratuite)"),
  maindeck:W("메인 데크","Main Deck","メインデッキ","Main Deck","Main Deck"), topdeck:W("톱 데크 투어","Top Deck Tour","トップデッキツアー","Top Deck Tour","Top Deck Tour"),
  oneday:W("1데이 스튜디오 패스","1-Day Studio Pass","1デイ・スタジオ・パス","Pase de 1 día","Pass 1 jour"), nijo:W("입성+니노마루 어전","Castle + Ninomaru Palace","入城＋二の丸御殿","Castillo + Palacio Ninomaru","Château + palais Ninomaru"),
  shinen:W("신엔(정원)","Shin-en garden","神苑","Jardín Shin-en","Jardin Shin-en"), sanmon:W("산몬·호조 정원 각각","Sanmon Gate or Hojo Garden, each","三門・方丈庭園 各","Puerta Sanmon o jardín Hojo, cada uno","Porte Sanmon ou jardin Hojo, chacun"),
  tsutenkyo:W("쓰텐쿄","Tsutenkyo Bridge","通天橋","Puente Tsutenkyo","Pont Tsutenkyo"), honbo:W("본방 정원","Honbo Garden","本坊庭園","Jardín Honbo","Jardin Honbo"),
  kondo:W("금당·강당","Kondo & Kodo halls","金堂・講堂","Pabellones Kondo y Kodo","Pavillons Kondo et Kodo"), gardenmuseum:W("정원+박물관","Garden + museum","庭園＋鳳翔館","Jardín + museo","Jardin + musée"),
  phoenix:W("봉황당 내부 추가","Phoenix Hall interior (extra)","鳳凰堂内部（追加）","Interior del Pabellón del Fénix (extra)","Intérieur du pavillon du Phénix (supplément)"),
  yuzen:W("유젠엔","Yuzen-en Garden","友禅苑","Jardín Yuzen-en","Jardin Yuzen-en"), hojo:W("호조 정원","Hojo Garden","方丈庭園","Jardín Hojo","Jardin Hojo"),
  day:W("낮","Day","昼","Día","Jour"), night:W("밤","Night","夜","Noche","Nuit"), factory:W("유료 구역 (공장 견학 등)","Paid area (factory tour, etc.)","有料エリア（工場見学など）","Zona de pago (visita a la fábrica, etc.)","Zone payante (visite de l'usine, etc.)"),
  grounds:W("경내","Grounds","境内","Recinto","Enceinte"), mainhall:W("본당","Main hall","本堂","Pabellón principal","Pavillon principal"), south:W("남쪽 전망실","South observatory","南展望室","Mirador sur","Observatoire sud"),
  gardens:W("정원","Gardens","庭園","Jardines","Jardins")
 };
 const TX = {
  free:W("무료","Free","無料","Gratis","Gratuit"), h24:W("24시간","Open 24 hours","24時間","Abierto 24 h","Ouvert 24 h/24"),
  sun:W("해 뜰 때부터 해 질 때까지","Sunrise to sunset","日の出から日没まで","Del amanecer al atardecer","Du lever au coucher du soleil"),
  shops:W("가게마다 달라요","Varies by shop","店舗により異なる","Varía según la tienda","Selon les boutiques"), date:W("날짜마다 달라요","Varies by date","日により異なる","Varía según el día","Selon le jour"),
  wd:W("평일","Weekdays","平日","Entre semana","En semaine"), we:W("주말·공휴일","Weekends & holidays","土日祝","Fines de semana y festivos","Week-ends et jours fériés"),
  wkday:W("평일 당일권 기준이고 주말·공휴일은 더 비싸요","Weekday walk-up price; higher on weekends and holidays","平日当日券の料金。土日祝は高め","Precio de taquilla entre semana; más caro en fines de semana y festivos","Tarif guichet en semaine ; plus cher le week-end et les jours fériés"),
  online:W("온라인 예매가 더 싸요","Cheaper online","オンライン購入がお得","Más barato en línea","Moins cher en ligne"), vary:W("시기·날짜에 따라 달라요","Varies by date","時期・日付により変動","Varía según la fecha","Varie selon la date"),
  show:W("공연마다 요금이 달라요","Prices vary by performance","公演により異なる","Varía según la función","Selon la représentation"), fare:W("구간마다 요금이 달라요","Fares vary by section","区間により運賃が異なる","La tarifa depende del tramo","Tarif selon le trajet"),
  hfp:W("하코네 프리패스로 탈 수 있어요","Covered by the Hakone Free Pass","箱根フリーパスで乗車可","Incluido en el Hakone Free Pass","Inclus dans le Hakone Free Pass"),
  month:W("달마다 달라요","Varies by month","月により異なる","Varía según el mes","Varie selon le mois"), seas:W("계절에 따라 달라요","Varies by season","季節により変動","Varía según la estación","Varie selon la saison"),
  night:W("야간 특별 관람 기간엔 밤까지 열어요","Open late during special night viewings","夜間特別拝観期間は夜まで","Abre de noche en las visitas nocturnas especiales","Ouvert le soir lors des visites nocturnes"),
  paid30:W("유료 구역은 30분 늦게 열고 30분 일찍 닫아요","The paid area opens 30 min later and closes 30 min earlier","有料区域は30分遅く開き30分早く閉まる","La zona de pago abre 30 min más tarde y cierra 30 min antes","La zone payante ouvre 30 min plus tard et ferme 30 min plus tôt"),
  l30:W("입장은 닫기 30분 전까지","Last entry 30 min before closing","入園は閉園30分前まで","Última entrada 30 min antes del cierre","Dernière entrée 30 min avant la fermeture"),
  volc:W("화산 활동에 따라 출입이 제한될 수 있어요","Access may be restricted due to volcanic activity","火山活動により立入規制あり","El acceso puede restringirse por actividad volcánica","Accès parfois limité en raison de l'activité volcanique"),
  extwe:W("주말·여름에는 밤까지 연장해요","Extended into the evening on weekends and in summer","週末・夏は夜まで延長","Ampliado por la noche en fines de semana y verano","Prolongé le soir le week-end et l'été"),
  sunset:W("경치 관람은 해 질 때까지","Viewing until sunset","景観の観覧は日没まで","Vistas hasta el atardecer","Vue jusqu'au coucher du soleil"),
  none:W("연중무휴","Open every day","年中無休","Abierto todos los días","Ouvert tous les jours"), irr:W("부정기 휴무","Irregular closures","不定休","Cierres irregulares","Fermetures irrégulières"),
  maint:W("점검일·악천후 시 쉬어요","Closed for maintenance or bad weather","点検日・悪天候時は休止","Cerrado por mantenimiento o mal tiempo","Fermé pour maintenance ou mauvais temps"),
  ny:W("연말연시","New Year holidays","年末年始","Fin de año","Fêtes de fin d'année"), rain:W("비 오는 날","Rainy days","雨天時","Días de lluvia","Jours de pluie"),
  mkt:W("일요일·공휴일·휴시일 (주로 수요일)","Sundays, holidays and market holidays (mostly Wednesdays)","日曜・祝日・休市日（主に水曜）","Domingos, festivos y días sin mercado (sobre todo miércoles)","Dimanches, jours fériés et jours de fermeture du marché (surtout le mercredi)"),
  closedNow:W("현재 휴관 중","Currently closed","現在休館中","Cerrado actualmente","Actuellement fermé")
 };
 const WD = {mon:W("월요일","Mondays","月曜","lunes","lundi"),tue:W("화요일","Tuesdays","火曜","martes","mardi"),wed:W("수요일","Wednesdays","水曜","miércoles","mercredi"),thu:W("목요일","Thursdays","木曜","jueves","jeudi"),fri:W("금요일","Fridays","金曜","viernes","vendredi")};
 const WD1 = {mon:W("월요일","Monday","月曜","lunes","lundi"),wed:W("수요일","Wednesday","水曜","miércoles","mercredi")};
 const NEXT = W(" (공휴일이면 다음 날)"," (next day if a holiday)","（祝日の場合は翌日）"," (si es festivo, el día siguiente)"," (le lendemain si férié)");
 const NEXTWD = W(" (공휴일이면 다음 평일)"," (next weekday if a holiday)","（祝日の場合は翌平日）"," (si es festivo, el siguiente día laborable)"," (le jour ouvré suivant si férié)");
 const MON = {en:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],es:["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"],fr:["janv.","févr.","mars","avr.","mai","juin","juil.","août","sept.","oct.","nov.","déc."]};
 const L = () => (window.I18N&&window.I18N.lang)||"ko";
 const t = o => o ? (o[L()]||(window.I18N&&window.I18N.D&&window.I18N.D[o.ko])||o.ko) : "";
 const num = n => { const l=L(), s=String(n).replace(/[^\d]/g,""), f=Number(s).toLocaleString(l==="ko"?"ko-KR":l==="ja"?"ja-JP":l==="es"?"es-ES":l==="fr"?"fr-FR":l==="zh"?"zh-CN":l==="tw"?"zh-TW":"en-US").replace(/ | /g," "); return f; };
 const yen = v => { const l=L(), from=String(v).includes("~"), n=num(v);
   if(l==="ko") return n+"엔"+(from?"~":""); if(l==="ja") return n+"円"+(from?"〜":""); if(l==="zh") return n+"日元"+(from?"起":""); if(l==="tw") return n+"日圓"+(from?"起":"");
   if(l==="en") return (from?"from ":"")+"¥"+n; if(l==="es") return (from?"desde ":"")+n+" ¥"; return (from?"à partir de ":"")+n+" ¥"; };
 const md = ([m,d]) => { const l=L(); if(l==="ko"||l==="ja"||l==="zh"||l==="tw") return `${m}/${d}`; if(l==="en") return `${MON.en[m-1]} ${d}`; return `${d} ${MON[l][m-1]}`; };
 const mrange = ([a,b]) => { const l=L(); if(a===b){ return l==="ko"?`${a}월`:(l==="ja"||l==="zh"||l==="tw")?`${a}月`:MON[l][a-1]; }
   if(l==="ko") return `${a}~${b}월`; if(l==="ja") return `${a}〜${b}月`; if(l==="zh"||l==="tw") return `${a}～${b}月`; return `${MON[l][a-1]}–${MON[l][b-1]}`; };
 const per = p => !p ? "" : p==="wd"||p==="we" ? t(TX[p]) : Array.isArray(p[0]) ? (p[0][0]===p[1][0]&&p[0][1]===p[1][1] ? md(p[0]) : `${md(p[0])}${L()==="ja"?"〜":(L()==="zh"||L()==="tw")?"～":L()==="ko"?"~":"–"}${md(p[1])}`) : mrange(p);
 const last = x => { const l=L(); return l==="ko"?` (입장 ${x}까지)`:l==="ja"?`（最終入場${x}）`:l==="zh"?`（最后入场${x}）`:l==="tw"?`（最後入場${x}）`:l==="en"?` (last entry ${x})`:l==="es"?` (última entrada ${x})`:` (dernière entrée ${x})`; };
 const lbl = k => k ? (typeof k==="object" ? t(k) : t(LB[k])) : "";
 const colon = L2 => (L2==="ja"||L2==="zh"||L2==="tw"?"：":L2==="fr"?" : ":": ");
 function fee(si){
   const out = [];
   if(si.f==="F") out.push(t(TX.free));
   else (si.f||[]).forEach(([k,v,p])=>{ const nm = k==="adult" && (si.f.length===1) ? "" : lbl(k);
     if(v==null){ out.push(nm); return; }
     out.push((nm?nm+(p?` (${per(p)})`:"")+colon(L()):(p?`${per(p)}${colon(L())}`:"")) + yen(v)); });
   (si.fx||[]).forEach(k=>out.push(typeof k==="object"?t(k):t(TX[k])));
   return out;
 }
 function hours(si){
   const out = [];
   (si.h||[]).forEach(([o,c,la,p,lb])=>{
     let s = o==="24h"?t(TX.h24):o==="sun"?t(TX.sun):o==="shops"?t(TX.shops):o==="date"?t(TX.date):`${o}–${c}${la?last(la):""}`;
     const pre = [lbl(lb), per(p)].filter(Boolean).join(" · ");
     out.push(pre ? pre+colon(L())+s : s);
   });
   (si.hx||[]).forEach(k=>out.push(typeof k==="object"?t(k):t(TX[k])));
   return out;
 }
 function closed(si){
   return (si.c||[]).map(c=>{
     if(typeof c==="string"){ const m=c.match(/^(mon|tue|wed|thu|fri)(\+)?$/); if(m) return t(WD[m[1]])+(m[2]?t(NEXT):""); return t(TX[c]); }
     if(c.t) return t(c.t);
     if(c.d) return per(c.d);
     if(c.n){ const l=L(), w=t(WD1[c.w]); const s = l==="ko"?`매월 ${["","첫째","둘째","셋째","넷째"][c.n]} ${w}`:l==="ja"?`毎月第${c.n}${w}`:l==="zh"?`每月第${c.n}个${w}`:l==="tw"?`每月第${c.n}個${w}`:l==="en"?`${["","1st","2nd","3rd","4th"][c.n]} ${w} of each month`:l==="es"?`${c.n}.º ${w} de cada mes`:`${c.n}${c.n===1?"er":"e"} ${w} du mois`;
       return s + (c.x==="wdnext"?t(NEXTWD):c.x==="next"?t(NEXT):""); }
     return "";
   }).filter(Boolean);
 }
 return { rows(id){
   const si = SPOT_INFO[id]; if(!si) return null;
   const r = [];
   if(si.closed) r.push(["status",[t(TX.closedNow)]]);
   const f=fee(si); if(f.length) r.push(["fee",f]);
   const h=hours(si); if(h.length) r.push(["hours",h]);
   const c=closed(si); if(c.length) r.push(["closed",c]);
   return {rows:r, note: si.x ? t(si.x) : ""};
 }};
})();
