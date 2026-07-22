---
name: reference-google-calendar-ids
description: 도요님 구글캘린더 목록과 프로젝트별 캘린더 ID
metadata: 
  node_type: memory
  type: reference
  originSessionId: b2602db1-caa4-43d7-a043-e3fd5c7be3d7
---

`list_calendars` 결과(2026-07-13 기준):

| 캘린더명 | ID |
| --- | --- |
| SKEP_Y1P1 | 7935853b9f6b41a7dceeb9f5828e083c497426d1ce1f65ee50531284830718a6@group.calendar.google.com |
| SKEP_Y1P4 | ae686b88a0a7738600a8d60070d544fae76e0a45f925e12e5e4c2f86e6b55b52@group.calendar.google.com |
| SKEP_Y2P1 | 12a559163bdc64cc172ac0538f5d81805ff6bc5119a9ccaa7cd1619f41f23ba6@group.calendar.google.com |
| SKEP_Repeat | 02f9a3d9495a079554edbd48b5a5fe42a4ad200e4f2b4db8a89deef607b42120@group.calendar.google.com |
| DM_유하 (기본/primary) | eastpipl26@gmail.com |
| DM_약속 | 10663205097cbbec6727051f1fe6d0b0a8e1b5b93859513eba0a2bfed9fb6d57@group.calendar.google.com |
| DM_자기개발 | 8fa43a9c9fd4880c02472abf34eebb0845f47194728d9f1611df2d76e10e2e8e@group.calendar.google.com |

**Why:** SK하이닉스 업무 일정은 기본(primary) 캘린더가 아니라 프로젝트별 SKEP_* 캘린더에 등록해야 함(한 번 primary에 잘못 등록해서 정정한 적 있음). [[feedback_calendar_sync_always]] 참고.

**How to apply:** 캘린더 등록 시 프로젝트(Y1P1/Y1P4/Y2P1)를 확인해 맞는 calendarId를 사용한다. 목록이 바뀌었을 수 있으니 확신이 안 서면 `list_calendars`로 재확인한다.
