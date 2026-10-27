import sys
CSS_A = '.cities{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}'
CSS_B = CSS_A + '''
.cityscroll{position:relative}
.cityscroll[hidden]{display:none}
.cityscroll .cnav{position:absolute;top:0;bottom:4px;width:56px;display:flex;align-items:center;border:0;padding:0;cursor:pointer;z-index:2;background:none}
.cityscroll .cnav[hidden]{display:none}
.cityscroll .cnav.prev{left:0;justify-content:flex-start;background:linear-gradient(90deg,var(--paper) 45%,transparent)}
.cityscroll .cnav.next{right:0;justify-content:flex-end;background:linear-gradient(270deg,var(--paper) 45%,transparent)}
.cityscroll .cnav span{width:32px;height:32px;border-radius:50%;border:1px solid var(--line);background:var(--surface);color:var(--ink);display:grid;place-items:center;box-shadow:0 1px 4px rgba(0,0,0,.12)}
.cityscroll .cnav:hover span{border-color:var(--ink-2)}
.cityscroll .cnav:focus-visible span{outline:2px solid var(--ai);outline-offset:2px}'''
HTML_A = '  <div class="cities" id="cities" role="group" aria-label="지역 선택"></div>'
HTML_B = '''  <div class="cityscroll" id="cityscroll"><button type="button" class="cnav prev" id="cityPrev" aria-label="이전 지역 보기" hidden><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg></span></button><div class="cities" id="cities" role="group" aria-label="지역 선택"></div><button type="button" class="cnav next" id="cityNext" aria-label="다음 지역 보기" hidden><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></span></button></div>'''
JS_A = '''  $("#cities").hidden = st.view==="home";
  $("#cities").innerHTML = list.map(([k,ko,jp])=>`<button class="city" type="button" data-city="${k}" aria-pressed="${st.city===k}">${ko}<span class="jp">${jp}</span></button>`).join("");'''
JS_B = '''  $("#cityscroll").hidden = st.view==="home";
  $("#cities").innerHTML = list.map(([k,ko,jp])=>`<button class="city" type="button" data-city="${k}" aria-pressed="${st.city===k}">${ko}<span class="jp">${jp}</span></button>`).join("");
  cityScrollInit();'''
FN_A = 'function renderCities(){'
FN_B = '''/* 도시 칩 줄: 넘치면 양옆 화살표로 넘겨 보기 */
function cityArrows(){
  const el=$("#cities"); if(!el) return;
  const max=el.scrollWidth-el.clientWidth;
  $("#cityPrev").hidden = el.scrollLeft<=2;
  $("#cityNext").hidden = el.scrollLeft>=max-2;
}
let cityScrollReady=false;
function cityScrollInit(){
  const el=$("#cities");
  if(!cityScrollReady){
    cityScrollReady=true;
    el.addEventListener("scroll",cityArrows,{passive:true});
    window.addEventListener("resize",cityArrows);
    const go=d=>el.scrollBy({left:d*Math.max(160,el.clientWidth*0.7),behavior:"smooth"});
    $("#cityPrev").addEventListener("click",()=>go(-1));
    $("#cityNext").addEventListener("click",()=>go(1));
  }
  // 고른 도시가 가려져 있으면 보이게
  const on=el.querySelector('[aria-pressed="true"]');
  if(on && (on.offsetLeft<el.scrollLeft || on.offsetLeft+on.offsetWidth>el.scrollLeft+el.clientWidth)){
    el.scrollLeft = Math.max(0, on.offsetLeft - (el.clientWidth-on.offsetWidth)/2);
  }
  requestAnimationFrame(cityArrows);
}
function renderCities(){'''
for p in sys.argv[1:]:
    s=open(p,encoding='utf-8').read()
    if 'cityScrollInit' in s: print('already',p); continue
    for a,b in [(CSS_A,CSS_B),(HTML_A,HTML_B),(JS_A,JS_B),(FN_A,FN_B)]:
        assert s.count(a)==1,(p,a[:40],s.count(a)); s=s.replace(a,b)
    open(p,'w',encoding='utf-8').write(s); print('patched',p)
