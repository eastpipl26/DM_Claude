---
name: feedback_delegation_fallback
description: 위임 대상 에이전트가 현재 환경에서 spawn 불가하면 말숙이가 직접 처리한다
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7fc64c63-f55c-4dc1-9efb-1d2d96d78fcd
---

말숙이는 스킬·저장 작업을 담당 직원에게 위임하는 게 원칙이나, 그 에이전트가 현재 세션의 spawn 가능 목록에 없으면 대기하지 말고 말숙이가 직접 처리한다.

**Why:** obsidian-manager(옥순이)가 스폰 목록에 없어 vault 저장을 옥순이에게 못 넘긴 사례(2026-07-04). 위임 원칙을 고집해 작업을 멈추는 게 더 나쁨.

**How to apply:** 위임 시도 → "agent type not found"면 즉시 말숙이가 직접 수행하고, 원래 담당이 누구였는지만 보고에 명시한다.

[[feedback_task_delegation]]
