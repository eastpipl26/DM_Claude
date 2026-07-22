---
name: feedback-notion-sync-batched
description: Notion 업무목록 미러링은 항목마다 즉시 하지 말고 도요님이 요청할 때 일괄로 처리
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b2602db1-caa4-43d7-a043-e3fd5c7be3d7
---

업무 항목(Obsidian items\*.md)을 추가·수정할 때마다 Notion을 자동으로 즉시 반영하지 않는다. Obsidian만 먼저 업데이트해두고, 도요님이 "노션 업데이트해줘" 등으로 명시 요청하면 그때 밀린 변경분을 일괄로 Notion에 반영한다.

**Why:** 2026-07-15, 여러 항목을 연달아 수정하는 중 Notion API가 반복 호출로 rate limit(429)에 걸림. 도요님이 "노션에 업데이트는 내가 요청하면 일괄로 하는게 좋겠다"고 직접 정정.

**How to apply:** [project_notion_mirror.md](project_notion_mirror.md)에 있던 "매 수정마다 즉시 Notion도 반영" 규칙을 대체한다. Obsidian은 항상 즉시 반영(source of truth), Notion은 배치 반영 대상. 일괄 반영 시에는 변경된 항목들을 모아 정리 후 순차 호출.
