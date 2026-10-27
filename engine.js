/* 번역 엔진: 화면에 그려진 한국어 글자를 사전·문장 틀로 바꿔요. 데이터는 한국어 그대로 두고 화면만 바꿉니다 */
(function(){
  var I=window.I18N; if(!I) return;
  var H=/[가-힣]/, D=I.D, memo=new Map(), FR=I.lang==="fr";
  var TT=I.T.map(function(t){
    var toks=t[0].split(/(\{x\}|\{n\})/).filter(function(x){return x!=="";});
    var lits=toks.filter(function(x){return x!=="{x}"&&x!=="{n}";});
    var generic=lits.join("").replace(/[\s·,()~]/g,"")==="";
    return {toks:toks,lits:lits,out:t[1],generic:generic};
  });
  function fmt(out,g){
    var r=out.replace(/\{[^{}]*\}/g,function(m){
      var s=m.slice(1,-1), mm, k, n, v;
      if((mm=s.match(/^(\d+)\?([^|]*)\|(.*)$/))){ k=+mm[1]; return (g[k]==="1"?mm[2]:mm[3]).split("{"+k+"}").join(g[k]); }
      if((mm=s.match(/^(M|MC|MS|MSC)(\d+)$/))){ k=+mm[2]; n=+g[k]-1;
        if(I.lang==="ja"||I.lang==="zh"||I.lang==="tw") return g[k]+"月";
        if(!(n>=0&&n<12)) return g[k];
        if(mm[1]==="MS") return I.MS[n];
        if(mm[1]==="MSC") return I.MS[n].charAt(0).toUpperCase()+I.MS[n].slice(1);
        v=I.MON[n]; return mm[1]==="MC"?v.charAt(0).toUpperCase()+v.slice(1):v; }
      if(/^\d+$/.test(s)) return g[+s];
      return m;
    });
    if(FR) r=r.replace(/\b([dD])e ([AEIOUaeiouÉé])/g,"$1'$2").replace("du 1 ","du 1er ");
    return r;
  }
  function match(t,i,s,pos){
    var toks=t.toks; if(i===toks.length) return pos===s.length?[]:null;
    var k=toks[i], r, e, sub, v, m;
    if(k==="{n}"){ m=/^\d+/.exec(s.slice(pos)); if(!m) return null; r=match(t,i+1,s,pos+m[0].length); return r?[m[0]].concat(r):null; }
    if(k==="{x}"){
      var nx=toks[i+1], ends=[];
      if(nx===undefined) ends=[s.length];
      else if(nx==="{x}"||nx==="{n}"){ for(e=pos+1;e<s.length;e++) ends.push(e); }
      else { e=s.indexOf(nx,pos+1); while(e!==-1){ ends.push(e); e=s.indexOf(nx,e+1); } }
      for(var j=0;j<ends.length;j++){
        sub=s.slice(pos,ends[j]); if(!sub||sub===s) continue;
        v=tr(sub); if(v==null) continue;
        r=match(t,i+1,s,ends[j]); if(r) return [v].concat(r);
      }
      return null;
    }
    return s.startsWith(k,pos)?match(t,i+1,s,pos+k.length):null;
  }
  function tr(s){
    if(!H.test(s)) return s;
    if(memo.has(s)) return memo.get(s);
    var r=tr0(s); memo.set(s,r); return r;
  }
  function tr0(s){
    if(Object.prototype.hasOwnProperty.call(D,s)) return D[s];
    var st=s.trim(), r, i, p, parts;
    if(st!==s){ if(!st) return s; r=tr(st); return r==null?null:s.slice(0,s.length-s.trimStart().length)+r+s.slice(s.trimEnd().length); }
    for(i=0;i<TT.length;i++){
      var t=TT[i]; if(t.generic&&s.length>48) continue;
      if(t.lits.some(function(l){return s.indexOf(l)<0;})) continue;
      var g=match(t,0,s,0); if(g) return fmt(t.out,g);
    }
    var PRE=["· ","📍 ","↳ "], SUF=[" ↗"," ↓"," →"," ·",":"], SEP=[" · "," → ","→"," / "];
    for(i=0;i<PRE.length;i++) if(s.startsWith(PRE[i])){ r=tr(s.slice(PRE[i].length)); return r==null?null:PRE[i]+r; }
    for(i=0;i<SUF.length;i++) if(s.endsWith(SUF[i])){ r=tr(s.slice(0,-SUF[i].length)); return r==null?null:r+SUF[i]; }
    for(i=0;i<SEP.length;i++) if(s.indexOf(SEP[i])>=0){ parts=s.split(SEP[i]).map(tr); if(parts.every(function(x){return x!=null;})) return parts.join(SEP[i]); }
    return null;
  }
  var DESC={en:"Sights, festivals, restaurants, transport and shopping in Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa and nearby cities, with live weather.",
    ja:"東京・大阪・名古屋・広島・四国・福岡・北海道・沖縄と近郊都市の観光地、祭り、グルメ、交通、ショッピング情報とリアルタイムの天気。",
    es:"Lugares, festivales, restaurantes, transporte y compras en Tokio, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa y ciudades cercanas, con el tiempo en directo.",
    fr:"Sites, fêtes, restaurants, transports et shopping à Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa et dans les villes voisines, avec la météo en direct.",zh:"东京、大阪、名古屋、广岛、四国、福冈、北海道、冲绳及周边城市的景点、节庆、美食、交通、购物信息与实时天气。",tw:"東京、大阪、名古屋、廣島、四國、福岡、北海道、沖繩及周邊城市的景點、節慶、美食、交通、購物資訊與即時天氣。"};
  [["meta[name=description]",DESC[I.lang]],["meta[property='og:description']",DESC[I.lang]],["meta[property='og:title']",I.D["Go Nihon Trip · 일본 여행 가이드"]],["meta[property='og:locale']",{en:"en_US",ja:"ja_JP",es:"es_ES",fr:"fr_FR",zh:"zh_CN",tw:"zh_TW"}[I.lang]]].forEach(function(x){ var m=document.querySelector(x[0]); if(m&&x[1]) m.setAttribute("content",x[1]); });
  window.__tr=function(s){ var r=tr(String(s==null?"":s)); return r==null?s:r; };
  var ATTR=["placeholder","aria-label","title","alt","label"];
  function tnode(n){ var v=n.nodeValue; if(!v||!H.test(v)) return; var r=tr(v); if(r!=null&&r!==v) n.nodeValue=r; }
  function tel(el){ for(var i=0;i<ATTR.length;i++){ var v=el.getAttribute(ATTR[i]); if(v&&H.test(v)){ var r=tr(v); if(r!=null&&r!==v) el.setAttribute(ATTR[i],r); } } }
  function skip(el){ return el.nodeName==="SCRIPT"||el.nodeName==="STYLE"||(el.classList&&el.classList.contains("notranslate")); }
  function inSkip(n){ for(var p=n.parentNode;p&&p.nodeType===1;p=p.parentNode) if(skip(p)) return true; return false; }
  function walk(root){
    if(root.nodeType===3){ if(!inSkip(root)) tnode(root); return; }
    if(root.nodeType!==1||skip(root)||inSkip(root)) return;
    tel(root);
    var w=document.createTreeWalker(root,5,{acceptNode:function(n){ return n.nodeType===1&&skip(n)?2:1; }}), n;
    while((n=w.nextNode())){ if(n.nodeType===3) tnode(n); else tel(n); }
  }
  new MutationObserver(function(recs){
    for(var i=0;i<recs.length;i++){ var r=recs[i];
      if(r.type==="childList") for(var j=0;j<r.addedNodes.length;j++) walk(r.addedNodes[j]);
      else if(r.type==="characterData"){ if(!inSkip(r.target)) tnode(r.target); }
      else if(r.type==="attributes") tel(r.target);
    }
  }).observe(document.documentElement,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:ATTR});
  document.addEventListener("DOMContentLoaded",function(){ walk(document.documentElement); });
})();
