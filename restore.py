#!/usr/bin/env python3
"""새 작업 공간에서 Nihon Trip 작업 환경을 되살려요.

사용법 (빈 작업 공간에서):
  git clone -b source https://github.com/ehddud0029-tech/Nihon-Trip.git /home/claude/nihon-src
  python3 /home/claude/nihon-src/restore.py
→ /home/claude 에 tabishiori.html · site · sitegen · i18n_work · deploy.py 를 복사하고,
  main 브랜치(배포 사이트)를 /home/claude/nihon-trip 에 받아요.
"""
import os, shutil, subprocess
ROOT = '/home/claude'
HERE = os.path.dirname(os.path.abspath(__file__))
REMOTE = 'https://github.com/ehddud0029-tech/Nihon-Trip.git'
for name in os.listdir(HERE):
    if name == '.git': continue
    s, d = os.path.join(HERE, name), os.path.join(ROOT, name)
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)
if not os.path.isdir(f'{ROOT}/nihon-trip/.git'):
    subprocess.run(['git', 'clone', '-b', 'main', REMOTE, f'{ROOT}/nihon-trip'], check=True)
# 로컬 테스트(file://)용 사본
for f in ['areas.js', 'autoreserve.js', 'google_picks.js', 'geo.js']:
    shutil.copy2(f'{ROOT}/site/{f}', f'{ROOT}/{f}')
shutil.copytree(f'{ROOT}/site/i18n', f'{ROOT}/i18n', dirs_exist_ok=True)
print('복원 완료. 이제 python3 /home/claude/deploy.py "메시지" 로 배포할 수 있어요.')
