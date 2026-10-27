# 개인정보처리방침에 Google 애드센스(광고 쿠키) 안내 추가. html과 backup pre 파일에 같이 적용.
A = '  <h2>브라우저에 저장되는 정보</h2>'
ADD = '''  <h2>광고 (Google 애드센스)</h2>
  <p>이 사이트는 Google 애드센스로 광고를 보여줘요. Google과 광고 파트너는 쿠키를 이용해 이 사이트와 다른 사이트를 방문한 기록을 바탕으로 광고를 보여줄 수 있어요.</p>
  <p>Google 광고 설정에서 맞춤 광고를 끄거나, 브라우저에서 쿠키를 차단할 수 있어요.</p>
  <p><a href="https://adssettings.google.com/" target="_blank" rel="noopener">Google 광고 설정 ↗</a> · <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">Google의 광고 쿠키 사용 ↗</a></p>
'''
for f in ['/home/claude/tabishiori.html', '/home/claude/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    if '광고 (Google 애드센스)' in s: print('skip', f); continue
    assert s.count(A) == 1
    open(f, 'w', encoding='utf-8').write(s.replace(A, ADD + A)); print('patched', f)
