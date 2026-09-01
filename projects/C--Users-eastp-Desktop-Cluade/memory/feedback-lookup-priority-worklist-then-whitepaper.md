---
name: feedback-lookup-priority-worklist-then-whitepaper
description: "업무 관련 질문은 업무리스트(items)를 먼저 검색하고, 없으면 설계백서에서 찾는다"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d0be4cfc-e518-4f78-aac1-2f9e2d6b6eda
  modified: 2026-07-27T09:39:45.374Z
---

도요님이 업무 관련 내용을 물어보면(예: "OO 어떻게 하기로 했지", "OO 기준이 뭐야") 다음 순서로 찾는다.

1. 먼저 `20_Projects\SK하이닉스_용인\업무\items\` (업무리스트)를 Grep으로 검색해 관련 아이템이 있는지 확인.
2. 업무리스트에 없거나 불충분하면 `40_Resources\FAB기술\Y1_FAB_설계Req_백서.md` 등 설계백서에서 찾는다.
3. 둘 다 없으면 없다고 말하고, 추측하지 않는다.

**Why:** 업무리스트는 실제 진행 중인 의사결정·회신 이력이 담긴 현재진행형 자료이고, 설계백서는 프로젝트 초기(Rev.1.0, 2025.10.02) 기준 스펙 문서라 최신 변경사항이 반영 안 됐을 수 있다. 실무 질문은 최신 이력이 있는 업무리스트가 항상 우선이어야 한다.

**How to apply:** 업무 관련 질문을 받으면 바로 백서나 기억에서 답하지 말고, items 폴더 Grep부터 실행한다. [[project-work-item-classification]]과 함께 적용.
