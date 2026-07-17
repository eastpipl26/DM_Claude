---
name: project-norender-studio
description: "NoRender — 블렌더 기반 건축 렌더링 외주 스튜디오. 라이노-블렌더 LiveLink 파이프라인, 자산은 M:\\NoRender_Workspace(구 E:), 문서(마스터플랜·Brand Book)는 Obsidian vault 원본 기준"
metadata: 
  node_type: memory
  type: project
  originSessionId: 882257b7-4ff1-4637-8b9a-ce36b29956f9
---

도요님이 크몽/숨고 건축 렌더링 외주를 위해 **NoRender**(Not only Render) 스튜디오를 준비 중 (2026-07 착수, 원래 제미나이에서 계획하다 성능 문제로 Claude Code로 이관).

- 슬로건: "렌더링, 그 이상의 가치를 짓다" / 포지셔닝: 건축 실무 7년 + 초현실적 렌더링
- 첫 타겟: 아파트 실내 데이라이트 렌더링. 진행 중 프로젝트: `M:\NoRender_Workspace\03_Projects\260709_Apt`
- 파이프라인: 라이노(형태 마스터, EXB 단축키로 FBX 송신) → 블렌더(재질·조명, 애드온 자동 수신). 규칙: 라이노 레이어 1개 = 블렌더 재질 1개. 수신기·애드온은 상대경로 설계라 드라이브 문자 무관
- **드라이브 문자 2026-07-15 E:→M: 변경·고정.** Rhino 별칭(exb/nrlayer)·Search Path의 E:\ 하드코딩은 M:\로 수정 필요(도요님 GUI 작업), blend 텍스처 절대경로는 Find Missing Files로 재연결
- 기준 문서(원본은 vault): 마스터플랜 `C:\Users\eastp\iCloudDrive\iCloud~md~obsidian\Dongmin\20_Projects\NoRender\00_NoRender_Master_Plan.md`, 같은 폴더 `NoRender_Brand_Book.md`(철학·가격·본업 방화벽). 경로 변수는 config.md `norender_*`
- 본업 방화벽: 익명 운영("설계사·건설사 실무 경험"만 표기), SK 계열 의뢰 전면 거절, 건축사시험(2026-09-12) 전 주 5시간 이하·수주 오픈은 시험 후

**Why:** 장기 목표(건설 AI 스타트업)의 수익원 겸 기술 자산. 파이프라인 스크립트가 곧 포트폴리오.

**How to apply:** NoRender 관련 요청 시 vault의 마스터플랜을 먼저 읽고 이어서 진행, 판단이 필요하면 Brand Book 우선. 문서 수정은 vault 원본에, M: 사본은 아카이브 대상. 제미나이식 땜질 반복 금지 — 스크립트 문제는 원인 진단 후 파일 직접 수정.
