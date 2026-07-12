---
name: project_mobile_remote_control
description: 도요는 서버 PC 상시가동 + Remote Control(/rc)로 폰에서 Claude Code 조작 지향
metadata:
  node_type: memory
  type: project
  originSessionId: 7fc64c63-f55c-4dc1-9efb-1d2d96d78fcd
---

도요 목표: 서버용 PC를 켜두고 모바일(Claude 앱)에서 Claude Code를 조작·피드백받기.

방법은 Claude Code 정식 기능 **Remote Control** — 서버 PC에서 `claude remote-control`(또는 세션 중 `/rc`) → QR → 폰 Claude 앱 Code 탭에서 같은 로컬세션 조작. 로컬 실행 유지(클라우드 아님), 인바운드 포트 안 열림. 전제: Pro/Max 이상(API키 불가), v2.1.51+, `/login` claude.ai 인증. 별도 대시보드 개발 불필요.

[[project_team_roadmap]]
