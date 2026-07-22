---
name: reference-daily-notes-folder-cleanup
description: 10_Daily 폴더에 있던 iCloud 충돌 중복폴더 2026(1) 정리 내역 — 재발 시 참고
metadata: 
  node_type: memory
  type: reference
  originSessionId: b2602db1-caa4-43d7-a043-e3fd5c7be3d7
---

2026-07-15 기준, `10_Daily` 아래 `2026(1)` 이라는 iCloud 동기화 충돌 중복 폴더가 있었음:
- `2026(1)\2026-06 2\` — 260617~260630 데일리노트 13건이 여기에만 존재(메인 `2026\` 트리엔 6월 폴더 자체가 없었음). 이걸 정상 위치인 `10_Daily\2026\2026-06\`로 이동.
- `2026(1)\2026-07 3\` — 260714·260715 두 파일이 있었으나 내용이 거의 빈 템플릿(아침 브리핑 없음, 체크리스트 없음) — 메인 `10_Daily\2026\2026-07\`의 같은 파일이 더 최신·완전한 버전이라 이 스테일 사본은 삭제.
- 처리 후 `2026(1)` 폴더 전체 삭제.

**원인 확인:** Obsidian 자체 자동화 문제는 아니었음 — periodic-notes 플러그인 설정(`daily: {folder: "10_Daily", format: "YYYY/YYYY-MM/YYMMDD 데일리노트"}`)이 정상적으로 동적 경로를 쓰고 있었고, core "daily-notes" 플러그인은 애초에 비활성화(`false`) 상태였음. 다만 core plugin의 inert 설정 파일(`daily-notes.json`)이 구버전 고정 경로(`10_Daily/2026/2026-06`)를 남긴 채로 남아있어 혼란 요소였고, 이건 삭제함. 실제 폴더 중복 원인은 iCloud 동기화 충돌(디바이스 간 동시 쓰기)로 추정.

**표준 경로:** 데일리노트는 항상 `10_Daily\YYYY\YYYY-MM\YYMMDD 데일리노트.md` 하나로 통일. 관련: [saebyeoki-morning-briefing 스킬](C:\Users\eastp\.claude\scheduled-tasks\saebyeoki-morning-briefing\SKILL.md)도 이 패턴을 사용 중.
