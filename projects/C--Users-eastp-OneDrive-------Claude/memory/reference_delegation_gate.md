---
name: reference_delegation_gate
description: 위임 강제 게이트(delegation_gate.py) 설치됨 — 말숙이 직접 vault 콘텐츠 수정을 턴당 2개로 물리 제한
metadata:
  node_type: memory
  type: reference
  originSessionId: 7fc64c63-f55c-4dc1-9efb-1d2d96d78fcd
---

2026-07-07 설치. `scripts/delegation_gate.py` — PreToolUse(Write|Edit|MultiEdit|NotebookEdit) 훅. 외부 "Fable 오케스트레이션 가이드"(WSL/코드파일 기준)를 우리 팀에 맞게 변형: 제한 기준이 "코드 확장자"가 아니라 **vault 경로**(config.md의 `vault` 값 아래). `.claude\` 내 에이전트·스킬·메모리·설정 파일은 말숙이 운영 업무라 제한 없음.

- 턴당 vault 콘텐츠 파일 2개까지 직접 수정 허용, 3개째부터 차단 → 담당 직원(문이/캐순이/강이/옥순이/감이 등)에게 위임 유도
- 서브에이전트 호출(payload의 agent_id/agent_type)은 전부 통과 — 위임이 정상 실행 경로
- 같은 파일 재수정은 카운트 안 됨, 새 턴(prompt_id 변경)에 카운터 리셋
- 스위치: `C:\Users\eastp\.claude\.delegation-gate-state` 파일 내용이 "on"이 아니면 전부 통과 (현재 on)
- fail-open: 스크립트 오류 시 무조건 통과, 세션 마비 방지
- **주의**: 설정 변경은 다음 세션부터 적용(이 세션엔 미적용). prompt_id는 Claude Code v2.1.196+ 필요(현재 v2.1.201 확인).

[[project_agent_model_tier_applied]] [[feedback_task_delegation]]
