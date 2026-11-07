# 여행 준비 > 통신 > eSIM에 마이리얼트립 제휴 링크(2026-11 사용자 제공).
# 제휴 링크는 한국어·영어 페이지에만 보이고(사용자 결정), 아래에 제휴 수수료 안내를 붙여요.
# guide_data.js·html·backup pre·guide_view.js에 같이 적용 (여러 번 돌려도 안전)
W = '/home/claude'
LINK = 'https://myrealt.rip/10FBq6a'
DATA = [f'{W}/sitegen/guide_data.js', f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
VIEW = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html', f'{W}/sitegen/guide_view.js']
A = '"key": "esim", "name": "eSIM", "link": ""'
B = f'"key": "esim", "name": "eSIM", "link": "{LINK}"'
VA = '''if(b.type==="compare") return `<div class="gblk">${h}<div class="gopts">${b.opts.map(o=>`<article class="go go-${o.key}"><h5>${esc(o.name)}</h5><dl><dt>${esc(b.pros)}</dt><dd>${esc(o.pros)}</dd><dt>${esc(b.cons)}</dt><dd>${esc(o.cons)}</dd><dt>${esc(b.for)}</dt><dd>${esc(o.for)}</dd></dl>${o.link?`<a class="gbuy" href="${esc(o.link)}" target="_blank" rel="noopener sponsored">${esc(b.buy)} ↗</a>`:""}</article>`).join("")}</div></div>`;'''
VB = '''if(b.type==="compare"){ const adL=(window.I18N&&window.I18N.lang)||"ko", ad=adL==="ko"||adL==="en", anyL=ad&&b.opts.some(o=>o.link); return `<div class="gblk">${h}<div class="gopts">${b.opts.map(o=>`<article class="go go-${o.key}"><h5>${esc(o.name)}</h5><dl><dt>${esc(b.pros)}</dt><dd>${esc(o.pros)}</dd><dt>${esc(b.cons)}</dt><dd>${esc(o.cons)}</dd><dt>${esc(b.for)}</dt><dd>${esc(o.for)}</dd></dl>${ad&&o.link?`<a class="gbuy" href="${esc(o.link)}" target="_blank" rel="noopener sponsored">${esc(b.buy)} ↗</a>`:""}</article>`).join("")}</div>${anyL?`<p class="sisrc">이 링크로 구매하면 Go Nihon Trip이 제휴 수수료를 받을 수 있어요. 가격은 같아요.</p>`:""}</div>`; }'''
for f in sorted(set(DATA + VIEW)):
    s = open(f, encoding='utf-8').read()
    if f in DATA and B not in s:
        assert s.count(A) == 1, (f, 'data', s.count(A)); s = s.replace(A, B)
    if f in VIEW and VB not in s:
        assert s.count(VA) == 1, (f, 'view', s.count(VA)); s = s.replace(VA, VB)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
