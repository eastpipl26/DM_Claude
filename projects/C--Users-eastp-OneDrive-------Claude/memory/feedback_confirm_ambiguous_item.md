---
name: feedback-confirm-ambiguous-item
description: 업무목록 등에서 어떤 항목을 가리키는지 불확실하면 임의 추측 대신 먼저 확인
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b2602db1-caa4-43d7-a043-e3fd5c7be3d7
---

업무목록.md 등에서 사용자가 언급한 내용이 여러 항목 중 어디를 가리키는지 확실하지 않으면, 그럴듯한 항목에 임의로 추측 반영하지 말고 먼저 사용자에게 확인한다.

**Why:** 2026-07-13, "PR 변경사항 반영완료"를 ID21(PR Room 냉장 System)로 잘못 추측해 반영했다가, 실제로는 ID33(F04 12F 덕트랙 변경)이었음. 도요님이 "확실하지 않은 아이템은 확인 후에 변경"하라고 명시적으로 요청.

**How to apply:** 참조가 모호하면(약어, 유사 키워드, 여러 후보 존재) 짧게 되물어서 ID를 확정한 뒤 수정한다. 명확한 경우(ID 직접 언급, 최근 대화에서 다룬 단일 항목)는 바로 반영해도 된다.
