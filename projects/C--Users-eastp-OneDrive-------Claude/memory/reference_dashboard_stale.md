---
name: reference_dashboard_stale
description: dashboard/agents.json은 2026-06-27에 멈춰있는 낡은 파일 — 실시간 팀 상태 확인용으로 쓰지 말 것
metadata:
  node_type: memory
  type: reference
  originSessionId: 7fc64c63-f55c-4dc1-9efb-1d2d96d78fcd
---

`C:\Users\eastp\.claude\dashboard\agents.json`은 2026-06-27 09:00 시점에서 멈춰 있고, 옛 직급(과장/대리)·선우 대기발령 등 낡은 정보를 담고 있다. Agent/Stop hook(`hook_update.py`)이 갱신하는 걸로 보이나 실제로는 최신 상태를 반영하지 않음(2026-07-06 확인).

**적용:** "팀원이 지금 뭐 하고 있나/일을 잘하고 있나" 같은 질문에 이 파일을 근거로 답하지 않는다. 실제 vault 산출물이나 직원목록.md(정적 카탈로그)를 확인해서 답한다.

[[project_agent_model_tier_applied]]
