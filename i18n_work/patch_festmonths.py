# 축제 화면: 도시를 고르면 맨 위 '축제 달력' 칸과 아래 월 버튼이 같은 내용이라 아래 월 버튼은 숨김 (일본 전체 화면에서는 그대로) (2026-11 사용자 요청)
# html·backup pre에 같이 적용, 여러 번 돌려도 안전.
W = '/home/claude'
A = '   <div class="months" role="group" aria-label="월 선택">${counts.map((n,i)=>`<button class="month${i+1===NOW_M?" now":""}" type="button" data-month="${i+1}" aria-pressed="${st.month===i+1}"><b>${i+1}월</b><span>${n?n+"개":"–"}</span></button>`).join("")}</div>'
B = '   ${st.city==="all"?`<div class="months" role="group" aria-label="월 선택">${counts.map((n,i)=>`<button class="month${i+1===NOW_M?" now":""}" type="button" data-month="${i+1}" aria-pressed="${st.month===i+1}"><b>${i+1}월</b><span>${n?n+"개":"–"}</span></button>`).join("")}</div>`:""}'
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    if B not in s: assert s.count(A) == 1, f; s = s.replace(A, B)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
