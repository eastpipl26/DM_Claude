# -*- coding: utf-8 -*-
"""vault NFC 정규화 + iCloud 충돌본 정리 (재발 방지 정기 루틴)

iCloud(맥/아이폰) ↔ 윈도우 동기화가 주기적으로 만드는 두 가지 유령을 정리한다:
  1. NFD 한글 파일/폴더명 (같은 이름이 탐색기에 2개로 보이는 원인)
  2. "이름 2.확장자" 동기화 충돌 복제본

안전 원칙 (정보 손실 0):
  - 삭제는 '바이트 단위 완전 동일'일 때만
  - 부분집합(한쪽이 다른쪽에 그대로 포함)이면 큰 쪽 유지
  - 내용이 다르면 절대 삭제하지 않고 '_nfd충돌'/'보류' 리포트만 남김

사용: python vault-nfc-cleanup.py          (실행)
      python vault-nfc-cleanup.py --dry    (변경 없이 리포트만)

경로는 config.md의 `vault` 값을 읽는다 (하드코딩 금지 규칙).
"""
import os
import re
import sys
import stat
import shutil
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
DRY = '--dry' in sys.argv
CONFIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.md')

def read_vault_path():
    text = open(CONFIG, encoding='utf-8').read()
    m = re.search(r'^\|\s*`vault`\s*\|\s*`([^`]+)`\s*\|', text, re.M)
    if not m:
        print('[오류] config.md에서 vault 경로를 찾지 못함')
        sys.exit(1)
    return m.group(1)

ROOT = read_vault_path()
LOG = []

def N(s):
    return unicodedata.normalize('NFC', s)

def safe_del(path):
    if DRY:
        return
    try:
        os.remove(path)
    except PermissionError:
        os.chmod(path, stat.S_IWRITE)
        os.remove(path)

def resolve_file_collision(src, existing, label):
    """src(제거후보)와 existing(유지후보) 비교 처리. True=src 정리됨"""
    b1 = open(src, 'rb').read()
    b2 = open(existing, 'rb').read()
    rel = os.path.relpath(src, ROOT)
    if b1 == b2:
        safe_del(src)
        LOG.append(f'동일제거({label}): {rel}')
        return True
    if b1 in b2:
        safe_del(src)
        LOG.append(f'부분집합제거({label}): {rel} ({len(b1)}B ⊂ {len(b2)}B)')
        return True
    if b2 in b1:
        # src가 상위집합 → src 내용을 existing 이름으로 채택
        if not DRY:
            safe_del(existing)
            os.rename(src, existing)
        LOG.append(f'확장본채택({label}): {rel} (상위집합을 정본 이름으로)')
        return True
    LOG.append(f'[!보류]({label}) 내용 상이 — 수동확인: {rel}')
    return False

# ── 1) NFC 정규화 (bottom-up)
for dirpath, dirnames, filenames in os.walk(ROOT, topdown=False):
    relseg = os.path.relpath(dirpath, ROOT).split(os.sep)
    if any(seg in ('.obsidian', '.git') for seg in relseg):
        continue
    for f in filenames:
        if f == N(f):
            continue
        sp = os.path.join(dirpath, f)
        existing = next((os.path.join(dirpath, x) for x in os.listdir(dirpath)
                         if x != f and N(x) == N(f) and os.path.isfile(os.path.join(dirpath, x))), None)
        if existing:
            if not resolve_file_collision(sp, existing, 'NFD'):
                base, ext = os.path.splitext(N(f))
                if not DRY:
                    os.rename(sp, os.path.join(dirpath, base + '_nfd충돌' + ext))
        else:
            if not DRY:
                os.rename(sp, os.path.join(dirpath, N(f)))
            LOG.append(f'NFC개명: {os.path.relpath(sp, ROOT)}')
    for d in dirnames:
        if d == N(d) or d in ('.obsidian', '.git'):
            continue
        sp = os.path.join(dirpath, d)
        if not os.path.isdir(sp):
            continue
        existing = next((os.path.join(dirpath, x) for x in os.listdir(dirpath)
                         if x != d and N(x) == N(d) and os.path.isdir(os.path.join(dirpath, x))), None)
        if existing:
            # 내용물을 NFC 폴더로 병합
            if not DRY:
                for e in list(os.listdir(sp)):
                    s2 = os.path.join(sp, e)
                    d2 = os.path.join(existing, N(e))
                    if os.path.exists(d2) and os.path.isfile(s2) and os.path.isfile(d2):
                        resolve_file_collision(s2, d2, 'NFD병합')
                    elif os.path.exists(d2) and os.path.isdir(s2) and os.path.isdir(d2):
                        for e2 in list(os.listdir(s2)):
                            shutil.move(os.path.join(s2, e2), os.path.join(d2, N(e2)))
                        os.rmdir(s2)
                    else:
                        shutil.move(s2, d2)
                if not os.listdir(sp):
                    os.rmdir(sp)
            LOG.append(f'NFD폴더병합: {os.path.relpath(sp, ROOT)}')
        else:
            if not DRY:
                os.rename(sp, os.path.join(dirpath, N(d)))
            LOG.append(f'NFC폴더개명: {os.path.relpath(sp, ROOT)}')

# ── 2) " 2.확장자" 충돌 복제본 (동일할 때만 삭제)
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in ('.obsidian', '.git', '.trash')]
    for f in filenames:
        m = re.match(r'^(.+) 2(\.[^.]+)$', f)
        if not m:
            continue
        dup = os.path.join(dirpath, f)
        orig = os.path.join(dirpath, m.group(1) + m.group(2))
        if os.path.exists(orig):
            resolve_file_collision(dup, orig, '충돌복제본')
        else:
            LOG.append(f'[!보류](충돌복제본) 원본 없음: {os.path.relpath(dup, ROOT)}')

# ── 3) "이름(1)" 충돌 폴더 리포트 (자동 병합은 위험해서 보고만)
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in ('.obsidian', '.git', '.trash')]
    for d in dirnames:
        if re.match(r'^.+\(\d\)$', d):
            LOG.append(f'[!보류] 충돌폴더 발견(수동확인): {os.path.relpath(os.path.join(dirpath, d), ROOT)}')

mode = '[DRY-RUN] ' if DRY else ''
print(f'{mode}vault-nfc-cleanup: {len(LOG)}건')
for l in LOG:
    print(' ', l)
if not LOG:
    print('  깨끗함 — 처리할 항목 없음')
