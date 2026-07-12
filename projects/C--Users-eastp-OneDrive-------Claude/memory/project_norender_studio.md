---
name: project-norender-studio
description: "NoRender — 블렌더 기반 건축 렌더링 외주 스튜디오. 라이노-블렌더 LiveLink 파이프라인, E:\\NoRender_Workspace, 마스터 플랜 문서 기준으로 진행"
metadata: 
  node_type: memory
  type: project
  originSessionId: 882257b7-4ff1-4637-8b9a-ce36b29956f9
---

도요님이 크몽/숨고 건축 렌더링 외주를 위해 **NoRender**(Not only Render) 스튜디오를 준비 중 (2026-07 착수, 원래 제미나이에서 계획하다 성능 문제로 Claude Code로 이관).

- 슬로건: "렌더링, 그 이상의 가치를 짓다" / 포지셔닝: 건축 실무 7년 + 초현실적 렌더링
- 첫 타겟: 아파트 실내 데이라이트 렌더링. 진행 중 프로젝트: `E:\NoRender_Workspace\03_Projects\260709_Apt`
- 파이프라인: 라이노(형태 마스터, EXB 단축키로 FBX 송신) → 블렌더(재질·조명, 타이머 수신기). 규칙: 라이노 레이어 1개 = 블렌더 재질 1개
- 기준 문서: `E:\NoRender_Workspace\00_NoRender_Master_Plan.md` (Phase 0~3 to-do 포함). 경로 변수는 config.md `norender_*`에 등록됨

**Why:** 장기 목표(건설 AI 스타트업)의 수익원 겸 기술 자산. 파이프라인 스크립트가 곧 포트폴리오.

**How to apply:** NoRender 관련 요청 시 마스터 플랜 문서를 먼저 읽고 이어서 진행. 제미나이식 땜질 반복 금지 — 스크립트 문제는 원인 진단 후 파일 직접 수정. 남은 최우선: 블렌더 수신기 코드 파일화(T1) + 연동 스트레스 테스트(T2).
