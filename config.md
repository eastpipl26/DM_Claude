# 전역 설정 (config.md)

> 모든 에이전트·스킬은 작업 시작 시 이 파일을 먼저 읽고 아래 값을 사용한다.
> 경로·설정 변경 시 **이 파일만** 수정하면 전체에 반영된다.
> 다른 파일에 경로 하드코딩 금지 — 반드시 `{변수}` 참조.

---

## 경로 (v2 목표 체계)

> vault PARA 재편(Phase 2, `{claude_home}\docs\v2-재구축-가이드.md`) 완료 전까지
> `legacy_*` 변수가 실제 위치인 항목이 있다. 이사 완료 시 legacy 변수를 삭제한다.

| 변수 | 값 |
|---|---|
| `vault` | `C:\Users\eastp\iCloudDrive\iCloud~md~obsidian\Dongmin` |
| `claude_home` | `C:\Users\eastp\.claude` |
| `knowledge` | `{claude_home}\knowledge` |
| `scripts` | `{claude_home}\scripts` |
| `inbox` | `{vault}\00_Inbox` |
| `projects` | `{vault}\20_Projects` |
| `sk` | `{projects}\SK하이닉스_용인(1)` (Phase 2에서 "(1)" 제거 rename 예정) |
| `meeting_notes` | `{sk}\1_회의록` |
| `issues` | `{sk}\2_이슈` |
| `sk_work` | `{sk}\3_업무` |
| `sk_reports` | `{sk}\4_보고서` |
| `blog` | `{projects}\애드센스_블로그` |
| `areas` | `{vault}\30_Areas` |
| `daily` | `{areas}\1_데일리` — **legacy(현재 실위치)**: `{vault}\01-1_개인기록\1_데일리` |
| `daily_note_file` | `{daily}\{YYYY}\{YYYY-MM}\{YYMMDD} 데일리노트.md` |
| `health` | `{areas}\2_건강` — legacy: `{vault}\01-1_개인기록\3_운동기록` |
| `finance` | `{areas}\3_재무` — legacy: `{vault}\01-3_개인자산\1_재무` |
| `realty` | `{areas}\4_부동산` — legacy: `{vault}\01-3_개인자산\2_부동산` |
| `career` | `{areas}\5_커리어` — legacy: `{vault}\02_업무\0_이력사항`, `{areas}\커리어_AI전환` |
| `content` | `{areas}\6_콘텐츠제작` — legacy: `{vault}\03_부업\1_콘텐츠제작` |
| `blog_notes` | `{content}\2_블로그` — legacy: `{vault}\03_부업\1_콘텐츠제작\2_블로그` |
| `content_script` | `{content}\3_대본` — legacy: `{vault}\03_부업\1_콘텐츠제작\3_대본` |
| `content_ppt` | `{content}\4_PPT` — legacy: `{vault}\03_부업\1_콘텐츠제작\4_PPT` |
| `resources` | `{vault}\40_Resources` — legacy(대부분 실위치): `{vault}\09_데이터` |
| `fab_docs` | `{resources}\FAB기술` — legacy: `{vault}\09_데이터\FAB기술` |
| `study` | `{resources}\학습노트` — legacy: `{vault}\01-2_개인공부`, `{vault}\09_데이터` 대주제 폴더들 |
| `system` | `{vault}\90_System` |
| `archive` | `{vault}\99_Archive` |
| `re_data` | `{realty}\1_데이터` |
| `re_tracker` | `{realty}\3_트래커` |
| `re_scripts` | `{scripts}\re-pipeline` |

> **legacy 규칙**: 대상 폴더가 새 경로에 아직 없으면 legacy 경로를 사용하고, 이사 여부가 불확실하면 둘 다 Glob으로 확인 후 실제 존재하는 쪽을 쓴다.

---

## 모델

| 변수 | 값 |
|---|---|
| `default_model` | `sonnet` |

에이전트별 모델은 각 md frontmatter `model:` 값을 따른다 (단순 정리형 haiku, 판단형 sonnet).

---

## 파일명 규칙

| 변수 | 값 |
|---|---|
| `date_format` | `YYMMDD` (예: 260627) |
| `meeting_filename` | `{YYMMDD}_{phase}_{building}_{키워드}.md` |
| `blog_filename` | `{YYMMDD}_{키워드}.md` |
| `youtube_filename` | `{YYMMDD}_유튜브_{키워드}.md` |

---

## 에이전트-스킬 매핑

| 스킬/작업 | 담당 |
|---|---|
| `/블로그-작성` | piper |
| `/부동산-분석` | terra |
| `/fab-panel`, FAB 설계 검토 | archie |
| `/학습-유튜브` | general-purpose 서브에이전트 (파이프라인은 스킬에 내장) |
| `/콘텐츠-PPT` | general-purpose 서브에이전트 (파이프라인은 스킬에 내장) |
| 사실·수치 검증 | vera |
| 재무 / 건강 / 이력서 | penny / vita / hunter |
| Obsidian 저장·정리, 아침 브리핑 | 메인 세션 직접 또는 general-purpose 서브에이전트 |

---

## 구글캘린더 (공사일정·업무·인허가 동기화)

| phase/구분 | calendarId |
|---|---|
| Y1P1 | `7935853b9f6b41a7dceeb9f5828e083c497426d1ce1f65ee50531284830718a6@group.calendar.google.com` (SKEP_Y1P1) |
| Y1P4 | `ae686b88a0a7738600a8d60070d544fae76e0a45f925e12e5e4c2f86e6b55b52@group.calendar.google.com` (SKEP_Y1P4) |
| Y2P1 | `12a559163bdc64cc172ac0538f5d81805ff6bc5119a9ccaa7cd1619f41f23ba6@group.calendar.google.com` (SKEP_Y2P1) |
| 공통 | `02f9a3d9495a079554edbd48b5a5fe42a4ad200e4f2b4db8a89deef607b42120@group.calendar.google.com` (SKEP_Repeat) |
| 개인 | `8fa43a9c9fd4880c02472abf34eebb0845f47194728d9f1611df2d76e10e2e8e@group.calendar.google.com` (DM_자기개발) |

---

## NoRender (건축 렌더링 외주 스튜디오)

| 변수 | 값 |
|---|---|
| `norender_root` | `M:\NoRender_Workspace` (2026-07-15 E:→M: 드라이브 문자 고정) |
| `norender_docs` | `{projects}\NoRender` — 문서(마스터플랜·Brand Book) 원본은 vault. M:은 자산(blend·3dm·렌더) 전용 |
| `norender_scripts` | `{norender_root}\00_Automations_&_Scripts` |
| `norender_assets` | `{norender_root}\01_Library_&_Assets` |
| `norender_templates` | `{norender_root}\02_Templates` |
| `norender_projects` | `{norender_root}\03_Projects` |
| `norender_plan` | `{norender_docs}\00_NoRender_Master_Plan.md` |
| `norender_brand_book` | `{norender_docs}\NoRender_Brand_Book.md` |
| `norender_branding` | `M:\NoRender_Branding` |
| `norender_logo_source` | `{norender_branding}\01_Logo_Source` |
| `norender_brand_guide` | `{norender_branding}\02_Brand_Guide` |
| `norender_brand_sheet` | `{norender_branding}\03_Brand_Sheet` |
| `norender_marketing` | `{norender_branding}\04_Marketing_Assets` |
| `norender_website` | `M:\NoRender_Website` |
| `norender_website_data` | `{norender_website}\data\projects.json` |
| `norender_website_images` | `{norender_website}\public\projects` |
