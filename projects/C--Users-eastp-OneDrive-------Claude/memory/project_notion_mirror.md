---
name: project-notion-mirror
description: Obsidian 업무목록·인허가·설계백서를 노션으로 미러링하는 계획 — 회사컴퓨터에서 Obsidian 사용 불가라 노션으로 조회
metadata: 
  node_type: memory
  type: project
  originSessionId: b2602db1-caa4-43d7-a043-e3fd5c7be3d7
---

도요님 회사컴퓨터에서 Obsidian이 안 되기 때문에, Obsidian(원본)의 업무목록·인허가·설계백서 내용을 노션에도 지속적으로 미러링해서 회사에서 조회 가능하게 만들 계획.

**결정된 방향 (2026-07-14):**
- 노션 구조: 데이터베이스로 미러링 (항목 1건 = 노션 DB row 1개, Obsidian items\*.md의 frontmatter 그대로 대응)
- 동기화 시점: ~~항목 추가·수정 때마다 즉시 반영~~ → 2026-07-15 정정: Obsidian은 즉시, Notion은 도요님이 요청할 때 일괄 반영. 상세: [feedback_notion_sync_batched.md](feedback_notion_sync_batched.md)
- Obsidian이 원본(source of truth), 노션은 조회용 미러 — 노션에서 직접 수정하는 흐름은 아직 미정

**Why:** 도요님이 옵시디언에서 최종 관리하지만 회사PC에서 접근 불가, 노션은 웹이라 회사에서도 볼 수 있음.

**How to apply:**
- 2026-07-14 인증 완료, DB 구축 완료:
  - 상위 페이지: `SK하이닉스 용인 업무관리` (https://app.notion.com/p/39d33e1ede8a81899158d568cec0abf8)
  - 업무목록 DB data_source_id: `369e5db0-9023-4b52-bf77-8c428a4d0dc8` (67건 등록, Obsidian items\*.md 1:1 대응)
  - 인허가 DB data_source_id: `5500533f-659a-439e-bb81-78cd82631cda` (1건 등록)
  - 노션 페이지 생성 시 날짜 속성은 반드시 확장 키(`date:필드명:start`) 사용 — 일반 문자열로 넘기면 validation_error. Number형 커스텀 필드(ID 등)는 노션이 자동으로 `userDefined:필드명`으로 리네임하므로 그 키로 다시 보내야 함.
- **확정 규칙(2026-07-14) → 2026-07-15 수정:** 업무 항목 추가·수정 시 Obsidian items\*.md는 항상 즉시 반영. Notion은 매번 자동 반영하지 않고 도요님이 "노션 업데이트해줘" 요청 시 밀린 변경분을 일괄 반영한다 (rate limit 이슈로 변경, [feedback_notion_sync_batched.md](feedback_notion_sync_batched.md) 참조).
- 아직 안 한 것: `/업무-관리`, `/설계백서` 스킬에 "저장 시 노션도 갱신" 단계 반영 (다음 세션 작업).
- 설계백서(FAB기술) DB는 아직 미생성 — 필요시 같은 방식으로 추가.
- [project_fab_design_whitebook](project_fab_design_whitebook.md), 업무-관리·설계백서 스킬과 연계됨.
