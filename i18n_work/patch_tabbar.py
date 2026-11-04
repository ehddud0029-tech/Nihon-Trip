# 모바일 하단 탭바를 페이지 배경과 구별되게 (배경색·테두리·그림자·선택 표시) + 날씨 탭 추가
# tabishiori.html 과 backup/tabishiori.pre.html 두 곳에 같은 패치
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
CSS = ('/*TABBAR*/:root{--bar:#E9EDF4;--bar-line:#C3CCDA}'
       '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bar:#27324A;--bar-line:#3E4C66}}'
       ':root[data-theme="dark"]{--bar:#27324A;--bar-line:#3E4C66}'
       'nav.tabs{background:var(--bar);border-top:1px solid var(--bar-line);box-shadow:0 -6px 18px rgba(0,0,0,.18);grid-template-columns:repeat(11,minmax(0,1fr))}'
       'nav.tabs a{color:var(--ink);opacity:.78;min-width:0;overflow:hidden}'
       'nav.tabs a[aria-current="page"]{opacity:1;color:var(--shu)}'
       'nav.tabs a[aria-current="page"] i{background:var(--surface);border-radius:999px;width:42px;box-shadow:0 1px 3px rgba(0,0,0,.18)}\n')
TAB = ('  <a href="#weather" data-view="weather"><i><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" '
       'stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="3.2"/><path d="M9 2.5v1.3M3.8 4.8l.9.9M2.5 9h1.3M14.2 4.8l-.9.9"/>'
       '<path d="M8 19.5h9.5a3.5 3.5 0 0 0 .3-7 5 5 0 0 0-9.4 1.3A2.9 2.9 0 0 0 8 19.5z"/></svg></i>날씨</a>\n')
ADD_OLD = '@media (max-width:599px){html:not(:lang(ko)):not(:lang(ja)):not(:lang(zh-Hans)):not(:lang(zh-Hant)) nav.tabs{display:flex;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}}html:not(:lang(ko)):not(:lang(ja)):not(:lang(zh-Hans)):not(:lang(zh-Hant)) nav.tabs::-webkit-scrollbar{display:none}html:not(:lang(ko)):not(:lang(ja)):not(:lang(zh-Hans)):not(:lang(zh-Hant)) nav.tabs a{flex:1 0 auto;padding:8px 9px 6px;font-size:10.5px;overflow:visible;text-overflow:clip}'
ADD = '@media (max-width:599px){nav.tabs{display:flex;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}nav.tabs::-webkit-scrollbar{display:none}nav.tabs a{flex:1 0 auto;min-width:58px;padding:8px 8px 6px;white-space:nowrap;overflow:visible;text-overflow:clip}html:not(:lang(ko)):not(:lang(ja)):not(:lang(zh-Hans)):not(:lang(zh-Hant)) nav.tabs a{padding:8px 9px 6px;font-size:10.5px}}'
JS_A = '  $("#savedN").textContent = saved.length;\n}'
JS_B = '  $("#savedN").textContent = saved.length;\n  const tb=document.querySelector("nav.tabs"), ta=tb&&tb.querySelector("a[aria-current]"); if(tb&&ta&&tb.scrollWidth>tb.clientWidth) tb.scrollLeft=ta.offsetLeft-(tb.clientWidth-ta.offsetWidth)/2;\n}'
for f in FILES:
    s = open(f, encoding='utf-8').read()
    if '/*TABBAR*/' not in s:
        a = '@media (min-width:600px){nav.tabs{display:none}}'
        assert s.count(a) == 1; s = s.replace(a, CSS + a)
    if 'data-view="weather"><i>' not in s:
        i = s.index('<nav class="tabs"'); j = s.index('  <a href="#guide" data-view="guide"><i>', i)
        s = s[:j] + TAB + s[j:]
        a = '@media (min-width:600px){nav.tabs{display:none}}'
    if ADD_OLD in s: s = s.replace(ADD_OLD, ADD)
    a = '@media (min-width:600px){nav.tabs{display:none}}'
    if 'nav.tabs{display:flex;overflow-x:auto' not in s: s = s.replace(a, ADD + a)
    if 'tb.scrollLeft' not in s: s = s.replace(JS_A, JS_B)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
