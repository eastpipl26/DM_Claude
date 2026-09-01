---
name: feedback-mail-assignee-judgment
description: 업무 메일 등록 시 담당자를 도요님으로 단정하지 말고 수신자 구조로 판단
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d0be4cfc-e518-4f78-aac1-2f9e2d6b6eda
  modified: 2026-07-24T07:45:06.174Z
---

메일 내용을 업무 항목(담당자/상태)으로 등록할 때, 발신 대상이 도요님 한 명이 아니라
"각 담당자께서" 식으로 여러 phase(Ph-1/Ph-2/Ph-4 등) 담당자에게 broadcast된 경우
도요님을 자동으로 담당자로 잡으면 안 된다.

**Why:** 096_Y1P1_AMR_회신 건에서 안세희 프로가 FAB/CUB 전체 phase 담당자에게 보낸
broadcast 메일을 도요님 담당으로 잘못 등록했다가, 실제로는 나광식 프로(Ph-2 건축)가
지금까지 검토·PPT 작성을 주도해온 건이고 도요님은 단순 수신자 중 1인이었음이 드러났다.
메일 수신인 = 담당자가 아니다.

**How to apply:** 새 업무 항목 등록·상태판정 전에 메일의 To/Cc 구조를 먼저 확인한다.
- 수신자가 도요님 단독이거나, 도요님에게 특정 액션을 명시적으로 요청한 경우만 담당자=서동민(본인).
- "각 담당자", "관계자 전원" 등 복수 대상 broadcast면, 실제로 그동안 작업을 수행해온 사람이
  누구인지 메일 스레드(RE:/FW: 이력)를 거슬러 확인해 그 사람을 담당자로 기록한다.
- 도요님이 직접 할 액션이 없으면 상태는 🟡진행이 아니라 🔵지속관리(결과 공유만 확인) 등으로 낮춘다.
관련: [상태판정 기준](feedback-status-ball-rule.md)
