---
name: feedback-status-waiting-on-reply
description: 우리 쪽 액션 끝나고 상대방(타부서/외부) 회신만 기다리는 업무항목은 상태를 🟡진행이 아니라 ⏳대기로 표기
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b2602db1-caa4-43d7-a043-e3fd5c7be3d7
---

업무목록 항목에서 우리(서동민/팀) 쪽에서 할 일을 다 하고 정림·설비·시공팀 등 상대방의 회신/검토 결과만 기다리는 상태라면, 상태값을 🟡진행이 아니라 ⏳대기로 바꾼다.

**Why:** 2026-07-15, 039(과압배출구 우수유입 대책)·073(CR코어 E/V배기 벽체오프닝)이 둘 다 "우리는 요청 다 했고 상대 회신 대기 중"인 상태였는데 🟡진행으로 남아있어서 도요님이 ⏳대기로 정정, "유사한 내용도 항상 반영해줘"라고 표준화 요청.

**How to apply:** 새 항목 등록이나 로그 추가 시, 메모 로그 마지막 줄이 "~회신 필요", "~검토 요청함", "~회신 대기" 류(우리 액션 끝, 상대 응답 대기)면 상태를 ⏳대기로 설정한다. 우리 쪽에서 아직 할 일이 남아있으면(검토 중, 자료 준비 중 등) 🟡진행 유지. [feedback_status_continuous_management.md](feedback_status_continuous_management.md)(지속관리 상태값 규칙)와 함께 참고.
