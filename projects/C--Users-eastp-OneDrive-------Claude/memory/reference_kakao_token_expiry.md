---
name: reference-kakao-token-expiry
description: 카카오톡 전송 스크립트(kakao-send.ps1)의 액세스 토큰 만료 이슈 — 자동 갱신 스크립트 없음
metadata: 
  node_type: memory
  type: reference
  originSessionId: e2a88699-02ab-43fa-a6ad-4e35dca691f8
---

`C:\Users\eastp\.claude\scripts\kakao-send.ps1`은 `C:\Users\eastp\.claude\secrets\kakao.env`의
`KAKAO_ACCESS_TOKEN`을 읽어 카카오 "나에게 메시지" API로 전송한다.

카카오 액세스 토큰은 주기적으로 만료되며(보통 몇 시간~하루 단위), 이 토큰을 자동으로 갱신하는
refresh 스크립트가 `scripts` 폴더에 존재하지 않는다. 만료 시 API가 401 Unauthorized를 반환한다.

**Why:** 2026-07-05 새벽이 아침 브리핑 스케줄 실행 중 카톡 전송 6단계에서 401 오류로 실패.
토큰 재발급은 카카오 개발자 콘솔에서 도요님이 직접 OAuth 재인증해야 하는 절차로, 에이전트가
자동으로 해결할 수 없음.

**How to apply:** 카톡 전송 실패 시 401 Unauthorized라면 토큰 만료가 원인일 가능성이 높음 —
재시도 루프 돌리지 말고 즉시 "토큰 만료로 카톡 전송 실패, 재인증 필요"로 보고할 것. 만약 refresh
토큰 자동 갱신 스크립트가 나중에 추가되면 이 메모를 갱신한다.
