---
name: feedback-weekly-review-and-decision-tag
description: "업무리스트 운영규칙 — 월요일 주간 리뷰 정례화 + 의사결정은 [결정] 태그로 기록"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b2602db1-caa4-43d7-a043-e3fd5c7be3d7
---

2026-07-16 도요님 승인으로 도입된 업무리스트 운영규칙 2가지 (GTD 주간리뷰 + Decision Log 관행 기반):

**1. 월요일 주간 리뷰:** 매주 월요일 아침, 미결 업무항목(items\*.md 중 ✅완료 제외) 전수를 스캔해서 ①회신기한 도과 ⏳대기 → F/U 필요 목록 ②마감 지난 🟡진행 → 지연/대기/완료 재분류 ③날짜 없는 "확인 필요" 로그 → 이번주 배치. 결과를 그날 데일리노트 '오늘 할 일'에 체크리스트로 심는다. 정기 태스크(weekly-work-review, 월 08:00)로 자동화됨.

**2. [결정] 태그:** 의사결정이 내려진 사항은 메모 로그에 `- [MM-DD] [결정] 내용 — 사유: ...` 형식으로 기록한다. 경과 로그와 구분해 나중에 grep 한 번으로 프로젝트 의사결정 이력을 추출할 수 있게 한다 (인수인계·보고서·분쟁 대응용).

**Why:** 웹 조사 결과 건설 PM·설계조율 직무의 공통 관행 3가지(회신기한 관리·주간 리뷰·의사결정 분리) 중 도요님 시스템에 없던 것. 회신기한 규칙은 [feedback_status_waiting_on_reply.md](feedback_status_waiting_on_reply.md)에 통합됨.

**How to apply:** 업무 등록·수정 시 결정사항이면 [결정] 접두어 자동 적용. 주간 리뷰는 정기 태스크가 돌지만, 도요님이 월요일에 "오늘 할 일" 물어보면 리뷰 결과를 겸해서 답한다.
