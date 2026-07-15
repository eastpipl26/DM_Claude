---
name: reference-vault-path-stale
description: "vault는 iCloud~md~obsidian\\Dongmin 하나뿐 — iCloudDrive\\Dongmin은 구볼트 보관본, 절대 쓰지 말 것"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6e8db039-fa3e-4d2d-af98-8eef6c987b16
---

**진짜 vault는 `C:\Users\eastp\iCloudDrive\iCloud~md~obsidian\Dongmin` 하나다** (config.md `vault`와 일치).

과거 이 메모리는 `C:\Users\eastp\iCloudDrive\Dongmin\`이 실제 vault라고 잘못 기록했었다.
그 경로는 **그림자 볼트**(에이전트들이 iCloud 미다운로드 상태 때 착각해 만들어 쓰던 별도 사본)였고,
2026-07-13 대정리에서 고유 콘텐츠(업무목록 29KB·인허가 실데이터·구조 3/5/9강·FAB기술 노트·아침브리핑)를
전부 메인 vault로 병합한 뒤 `C:\Users\eastp\iCloudDrive\Dongmin_구볼트보관_260713`으로 개명했다.

**Why:** iCloud Files-on-Demand 때문에 vault 폴더가 간헐적으로 비어 보이고, 그때 에이전트가
"다른 경로가 진짜"라고 판단해 그림자 볼트에 쓰기 시작했다. 데일리노트 3중 분산·업무 데이터 이원화의 근본 원인.

**How to apply:** vault 경로가 비어 보여도 다른 경로를 vault로 간주하지 말 것 — iCloud 미다운로드 가능성.
작업 중단 후 보고가 정답. `Dongmin_구볼트보관_260713`은 읽기 전용 보관본으로만 취급, 절대 쓰지 않는다.
데일리노트 표준: `{vault}\10_Daily\YYYY\YYYY-MM\YYMMDD 데일리노트.md` (config.md `daily_note_file`).
정리 전 전체 백업: `C:\Users\eastp\VaultBackups\Dongmin_정리전백업_260713_2100.zip`. [[project-team-roadmap]]
