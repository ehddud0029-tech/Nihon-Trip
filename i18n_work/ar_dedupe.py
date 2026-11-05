# 맛집 목록(autoreserve.js)에서 여러 가게에 똑같이 붙은 틀 문장 특징(feat)을 비워요.
# (예: "후라노의 가볍게 한 끼 하기 좋은 라멘집" 5곳) 같은 문장 반복은 검색 품질에 불리해요.
# region_inject.py 가 autoreserve.js 를 다시 만들기 때문에, region_inject 뒤에 다시 돌려 주세요. 여러 번 돌려도 안전해요.
import re, json, subprocess, collections
F = '/home/claude/site/autoreserve.js'
src = open(F, encoding='utf-8').read()
feats = json.loads(subprocess.run(['node', '-e', f'global.window={{}};eval(require("fs").readFileSync("{F}","utf8"));console.log(JSON.stringify(Object.values(window.AR_SHOPS).map(x=>x.feat||"")))'], capture_output=True, text=True, check=True).stdout)
cnt = collections.Counter(f for f in feats if f)
rep = {f for f, c in cnt.items() if c > 1}
n = 0
def sub(m):
    global n
    if m.group(2) in rep: n += 1; return m.group(1) + '""'
    return m.group(0)
src = re.sub(r'("feat":\s*)"([^"]*)"', sub, src)
open(F, 'w', encoding='utf-8').write(src)
print('cleared', n, 'repeated texts', len(rep))
