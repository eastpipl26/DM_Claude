---
name: reference-blogger-api-automation
description: "BuildRight 블로그 원고→임시저장 자동화(Blogger API), 인증정보 위치, API 한계"
metadata: 
  node_type: memory
  type: reference
  originSessionId: e8699199-dea7-4b06-89e5-66282670be85
---

[[project-adsense-blog]] BuildRight 블로그 발행 자동화. 원고.md → 블로거 임시저장(초안)까지 API로 자동 등록.

## 사용법
```
python 90_에셋/scripts/publish_draft.py "원고.md 경로"
```
경로: `Dongmin/20_Projects/애드센스_블로그/90_에셋/scripts/publish_draft.py`

## 인증정보
- Google Cloud 프로젝트: `ai-agency` (cosmic-reserve-492902-h9), 계정 buildrightkr@gmail.com
- OAuth 클라이언트 시크릿: `~/.claude/secrets/blogger_client_secret.json`
- 토큰 캐시(자동 생성/갱신): `~/.claude/secrets/blogger_token.json`
- OAuth 동의화면: 외부/테스트 모드, 테스트 사용자에 buildrightkr@gmail.com 등록됨
- 블로그 ID: `4797443046941864730`

## API 한계 (2026-07-07 실측 확인)
- **이미지 업로드 불가**: Blogger API v3에 업로드 엔드포인트 없음 → 본문에 이미지 위치 주석만 남기고, 발행 후 블로거 에디터에서 수동 삽입 필요.
- **검색 설명(searchDescription) 저장 안 됨**: 비공식 필드라 API로 보내도 무시됨(0/150자로 확인) → 수동 입력 필수.
- 라벨·제목·본문(클린 HTML)은 API로 완전 자동화됨.

## Why
Obsidian에서 원고 직접 복사(특히 읽기모드)하면 배경색·CSS가 통째로 딸려와 오염되는 문제가 반복 발생([[feedback-adsense-post-footer-meta]]와 별개 이슈). API 자동화로 이 문제 자체를 원천 차단.

## How to apply
새 글 작성 완료 후 발행 단계에서 이 스크립트부터 실행. 이미지·검색설명만 수동으로 마무리.
