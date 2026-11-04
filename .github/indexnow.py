# 바뀐 페이지만 IndexNow로 알려요 (스크립트·CSS 버전 번호만 바뀐 페이지는 빼요)
import json, os, re, subprocess, urllib.request, urllib.error
key, origin = os.environ['INDEXNOW_KEY'], os.environ['SITE_ORIGIN'].rstrip('/')
if subprocess.run(['git', 'rev-parse', 'HEAD~1'], capture_output=True).returncode:
    print('no previous commit'); raise SystemExit
out = subprocess.run(['git', 'diff', '-U0', 'HEAD~1', 'HEAD', '--', '*.html'], capture_output=True, text=True).stdout
ver = re.compile(r'\?v=[0-9a-f]+|jstclock')   # 버전 번호·현재 시각 줄은 무시
changed, cur = set(), None
for line in out.split('\n'):
    if line.startswith('+++ '):
        cur = line[6:] if line.startswith('+++ b/') else None
    elif line.startswith('--- '):
        continue
    elif cur and line[:1] in '+-' and not ver.search(line):
        changed.add(cur)
# GitHub Pages에 이번 버전이 올라갈 때까지 기다려요 (build.txt 비교, 최대 20분)
import time
want = open('build.txt').read().strip()
for _ in range(80):
    try:
        with urllib.request.urlopen(f'{origin}/build.txt?t={time.time()}', timeout=20) as r:
            if r.read().decode().strip() == want: print('live:', want); break
    except Exception as e:
        pass
    time.sleep(15)
else:
    print('new version not live yet; giving up'); raise SystemExit
if os.path.exists('.github/indexnow_full'):   # 한 번 전체 제출 (배포할 때 INDEXNOW_FULL=1)
    changed = set(subprocess.run(['git', 'ls-files', '*index.html'], capture_output=True, text=True).stdout.split())
urls = []
for f in sorted(changed):
    if f == '404.html' or not f.endswith('index.html'): continue
    urls.append(origin + '/' + f[:-len('index.html')])
print(len(urls), 'changed pages')
host = origin.split('://')[1]
for i in range(0, len(urls), 10000):
    body = json.dumps({'host': host, 'key': key, 'keyLocation': f'{origin}/{key}.txt', 'urlList': urls[i:i + 10000]}).encode()
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, headers={'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'GoNihonTrip-IndexNow/1.0 (+https://gonihontrip.com/)'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: print('IndexNow', r.status)
    except urllib.error.HTTPError as e:
        print('IndexNow error', e.code, e.read()[:300])
    except Exception as e:
        print('IndexNow error', e)
