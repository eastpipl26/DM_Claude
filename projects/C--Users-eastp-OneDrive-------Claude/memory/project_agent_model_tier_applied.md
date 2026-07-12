---
name: project_agent_model_tier_applied
description: 2026-07-06 판단직 10명 haiku→sonnet 승격 적용 완료 (강이 품질 문제 계기)
metadata:
  node_type: memory
  type: project
  originSessionId: 7fc64c63-f55c-4dc1-9efb-1d2d96d78fcd
---

`rules/agent-delegation.md`의 "판단 필요한 작업만 sonnet" 규칙이 있었지만 실제로는 전 직원이 haiku로 박혀 있었음. 강이(유튜브 노트) 실제 산출물을 열어보니 트랜스크립트 원문 덤프·플래시카드 누락·영어 제목 등 품질 문제 확인 → haiku 모델 한계로 진단.

**2026-07-06 적용:** 판단직 10명(문이·감이·손질이·캐순이·조이·재이·찬우·줄이·물색이·강이) → `model: sonnet` 승격. 단순 실행직(탐이·수이·판이·묘이·옥순이·새벽이·채린이)은 haiku 유지. 선우는 동결이라 미변경.

강이는 추가로 dedup 체크·한글 제목 강제·트랜스크립트 덤프 금지 규칙도 `agents/강이.md`에 추가함.

**Why:** "팀원들이 일을 잘하고 있나" 물었을 때 감이 아니라 실제 산출물(vault 노트)을 직접 열어 확인한 게 정확한 진단으로 이어짐 — 앞으로도 팀 성과 점검은 추측이 아니라 실제 파일 확인으로.

**주의:** 이미 만들어진 부실 노트(강이의 옛 유튜브 노트들)는 자동으로 안 고쳐짐. 재작성은 별도 요청 필요.

[[project_team_roadmap]]
