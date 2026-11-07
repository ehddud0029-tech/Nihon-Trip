# 축제 공식 사이트 버튼 (2026-11). site/fest_urls.json: 축제 id -> 공식 사이트(주최·신사/절·관광협회 공식). 링크 확인은 photo-job 브랜치 linkcheck.py.
# html·backup pre에 같이 적용, 여러 번 돌려도 안전 (데이터 블록만 교체). region_inject 뒤에 다시 돌려 주세요.
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_weather import block
W = '/home/claude'
U = json.load(open(f'{W}/site/fest_urls.json', encoding='utf-8'))
BLK = ('/*FESTURL_BEGIN*/\nconst FEST_URL = ' + json.dumps(U, ensure_ascii=False, separators=(',', ':')) + ';\n'
       'function festBtn(it){ const u = it.type==="fest" && FEST_URL[it.id]; return u ? `<a class="btn" href="${u}" target="_blank" rel="noopener">공식 사이트 ↗</a>` : ""; }\n/*FESTURL_END*/\n')
A = '   ${typeof shopBtn==="function"?shopBtn(it):""}\n'
B = A + '   ${typeof festBtn==="function"?festBtn(it):""}\n'
for f in [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']:
    s = open(f, encoding='utf-8').read()
    s = block(s, '/*FESTURL_BEGIN*/', '/*FESTURL_END*/', BLK, 'function detailHTML(it, htag, inDrawer){')
    if B not in s: assert s.count(A) == 1, f; s = s.replace(A, B)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f, len(U))
