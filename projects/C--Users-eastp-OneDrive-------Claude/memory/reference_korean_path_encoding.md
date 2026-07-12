---
name: reference_korean_path_encoding
description: Python에서 한글 vault 경로는 raw Windows 경로로 — bash /c/ 변환 시 인코딩 깨짐
metadata:
  node_type: memory
  type: reference
  originSessionId: 7fc64c63-f55c-4dc1-9efb-1d2d96d78fcd
---

Windows에서 Python 스크립트로 한글 폴더(vault) 경로를 다룰 때, bash 스타일 `/c/Users/.../커리어_AI전환/...` 경로를 쓰면 인코딩이 깨진다(예: `Ŀ����_AI��ȯ`). 

**해결:** 스크립트에 raw Windows 경로 `r"C:\Users\eastp\iCloudDrive\...\커리어_AI전환\..."` 를 직접 사용한다. 2026-07 이력서·법규 크롤링 작업에서 확인.

---

**NFC/NFD 문제 (2026-07 학습-유튜브 작업에서 확인):** iCloud(맥 기원) vault의 한글 **파일명**은 NFD(자모 분해)로 저장된다. 반면 Read 도구·PowerShell `Get-Content`는 NFC로 조회 → 기존 한글 파일명 노트를 열면 "does not exist"로 실패한다(Glob은 찾아냄).

- **읽기:** Python으로 `os.listdir(folder)` 한 뒤, 원하는 이름과 각 항목을 `unicodedata.normalize('NFC', x)`로 비교해 실제 on-disk 이름을 찾아 open. (폴더 경로 자체는 NFC로 줘도 매칭됨 — 실패하는 건 파일명 컴포넌트.)
- **쓰기:** 신규 파일은 Python으로 실제 폴더에 직접 write. Write/Edit 도구로 한글 파일명 신규 생성 시 NFC로 저장돼 중복·불일치 위험.
- 요약: **한글 vault 파일 I/O는 Read/Write/PowerShell 대신 Python + NFC 정규화 매칭**을 쓴다.
