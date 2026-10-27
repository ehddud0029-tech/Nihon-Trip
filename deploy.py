#!/usr/bin/env python3
"""Nihon Trip 배포: 원본 백업(source 브랜치) + 사이트 생성 + 사이트 배포(main 브랜치)

사용법: python3 /home/claude/deploy.py "커밋 메시지"
  1) /home/claude 의 원본·작업 도구를 /home/claude/nihon-src (source 브랜치)로 복사
  2) sitegen/gen.py 로 전체 페이지 생성
  3) 결과(sitegen/dist)를 /home/claude/nihon-trip (main 브랜치, GitHub Pages)에 반영
  4) 두 브랜치를 같은 메시지로 커밋하고 push
"""
import os, shutil, subprocess, sys

ROOT = '/home/claude'
SRC_REPO = f'{ROOT}/nihon-src'      # source 브랜치 작업 폴더
SITE_REPO = f'{ROOT}/nihon-trip'    # main 브랜치 작업 폴더 (배포되는 사이트)
TRAILER = ''  # 커밋 끝에 붙일 줄 (필요하면 실행할 때 --trailer 로 전달)

# 원본으로 백업할 것: (원본 경로, 저장소 안 경로)
ITEMS = ['tabishiori.html', 'site', 'sitegen', 'i18n_work', 'deploy.py', 'restore.py', 'CLAUDE.md']
SKIP_DIRS = {'dist', '__pycache__', '.git'}

def run(cmd, cwd):
    print('$', ' '.join(cmd)); subprocess.run(cmd, cwd=cwd, check=True)

def copytree(src, dst):
    for base, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(base, src)
        os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in files:
            shutil.copy2(os.path.join(base, f), os.path.join(dst, rel, f))

def clean(repo, keep=('.git',)):
    for name in os.listdir(repo):
        if name in keep: continue
        p = os.path.join(repo, name)
        shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)

def commit_push(repo, msg, branch):
    run(['git', 'add', '-A'], repo)
    if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=repo).returncode == 0:
        print(f'[{branch}] 바뀐 내용 없음'); return
    run(['git', 'commit', '-q', '-m', msg], repo)
    run(['git', 'push', '-q', 'origin', branch], repo)

def main():
    args = sys.argv[1:]
    trailer = ''
    if '--trailer' in args:
        i = args.index('--trailer'); trailer = args[i + 1]; del args[i:i + 2]
    if not args: sys.exit('커밋 메시지를 적어 주세요: python3 deploy.py "메시지"')
    msg = args[0] + (('\n\n' + trailer) if trailer else '')
    # 0) GitHub 쪽 변경(예: Pages 설정이 만든 CNAME 커밋)을 먼저 받아요
    run(['git', 'pull', '-q', '--rebase', 'origin', 'source'], SRC_REPO)
    run(['git', 'pull', '-q', '--rebase', 'origin', 'main'], SITE_REPO)
    # 1) 원본 백업
    clean(SRC_REPO)
    for it in ITEMS:
        s = os.path.join(ROOT, it)
        if not os.path.exists(s): continue
        d = os.path.join(SRC_REPO, it)
        copytree(s, d) if os.path.isdir(s) else shutil.copy2(s, d)
    # 2) 페이지 생성
    run([sys.executable, 'gen.py'], f'{ROOT}/sitegen')
    # 3) 사이트 반영
    clean(SITE_REPO)
    copytree(f'{ROOT}/sitegen/dist', SITE_REPO)
    shutil.copy2(f'{ROOT}/site/README.md', SITE_REPO)
    # 4) 커밋·push (원본 먼저)
    commit_push(SRC_REPO, msg, 'source')
    commit_push(SITE_REPO, msg, 'main')

if __name__ == '__main__':
    main()
