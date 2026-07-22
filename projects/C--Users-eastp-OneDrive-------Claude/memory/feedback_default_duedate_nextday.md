---
name: feedback-default-duedate-nextday
description: 업무목록.md 마감일 미지정 시 기본값은 등록일 다음날
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b2602db1-caa4-43d7-a043-e3fd5c7be3d7
---

업무목록.md에 새 항목을 등록할 때, 도요님이 마감일을 별도로 언급하지 않으면 마감일(Plan)을 등록일 다음날로 채운다. 빈 칸으로 남기지 않는다.

**Why:** 도요님이 2026-07-13에 "업무 리스트 추가할 때 별도 언급 없으면 다음날로 지정해줘"라고 명시적으로 요청.

**How to apply:** 새 항목 등록 시 마감일 언급 없으면 등록일+1일을 마감일(Plan)로 채운다. 명시적 기한이 언급되면 그 날짜를 그대로 쓴다. PMT 등 외부 자료 대량 반영 건은 원본 DueDate_Plan을 그대로 쓰고 이 기본값 규칙 적용 대상이 아님. [[feedback_default_owner_self]]와 같은 종류의 기본값 규칙.
