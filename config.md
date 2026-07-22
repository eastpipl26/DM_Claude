# 말숙이 팀 전역 설정 (config.md)

> 모든 직원(에이전트)·스킬은 작업 시작 시 이 파일을 먼저 읽고 아래 값을 사용한다.
> 경로·설정 변경 시 **이 파일만** 수정하면 전체에 반영된다.

---

## 경로

| 변수 | 값 |
|---|---|
| `vault` | `C:\Users\eastp\iCloudDrive\iCloud~md~obsidian\Dongmin` |
| `claude_home` | `C:\Users\eastp\.claude` |
| `blog_attachments` | `{vault}\90_System\Attachments\블로그` |
| `inbox` | `{vault}\00_Inbox` |
| `projects` | `{vault}\20_Projects` |
| `sk_hynix` | `{vault}\20_Projects\SK하이닉스_용인` |
| `areas` | `{vault}\30_Areas` |
| `blog_notes` | `{vault}\30_Areas\블로그` |
| `real_estate` | `{vault}\30_Areas\부동산` |
| `re_data` | `{vault}\30_Areas\부동산\데이터` |
| `re_scripts` | `{claude_home}\scripts\re-pipeline` |
| `re_tracker` | `{real_estate}\트래커` |
| `resources` | `{vault}\40_Resources` |
| `system` | `{vault}\90_System` |
| `daily_notes` | `{vault}\10_Daily` |
| `daily_note_file` | `{daily_notes}\{YYYY}\{YYYY-MM}\{YYMMDD} 데일리노트.md` (예: `10_Daily\2026\2026-07\260720 데일리노트.md`) |
| `scripts` | `{claude_home}\scripts` |
| `content_script` | `{vault}\30_Areas\콘텐츠\대본` |
| `content_ppt` | `{vault}\30_Areas\콘텐츠\PPT` |

---

## 모델

| 변수 | 값 |
|---|---|
| `default_model` | `sonnet` |

---

## 파일명 규칙

| 변수 | 값 |
|---|---|
| `date_format` | `YYMMDD` (예: 260627) |
| `meeting_filename` | `{YYMMDD}_{phase}_{building}_{키워드}.md` |
| `blog_filename` | `{YYMMDD}_{키워드}.md` |
| `youtube_filename` | `{YYMMDD}_유튜브_{키워드}.md` |

---

## 직원-스킬 매핑

| 스킬 | 담당 직원 |
|---|---|
| `/블로그-작성` | 문이 |
| `/학습-유튜브` | 강이 |
| `/콘텐츠-PPT` | 줄이(대본) → 채린이(테마) → 판이(PPT) |
| Obsidian 저장·정리 | 옥순이 |
| 아침 브리핑 | 새벽이 |

---

## 회사 프로젝트 경로

| 변수 | 값 |
|---|---|
| `meeting_notes` | `{sk_hynix}\회의록` |
| `issues` | `{sk_hynix}\이슈` |
| `sk_work` | `{sk_hynix}\업무` |

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
| `norender_root` | `E:\NoRender_Workspace` |
| `norender_scripts` | `{norender_root}\00_Automations_&_Scripts` |
| `norender_assets` | `{norender_root}\01_Library_&_Assets` |
| `norender_templates` | `{norender_root}\02_Templates` |
| `norender_projects` | `{norender_root}\03_Projects` |
| `norender_plan` | `{norender_root}\00_NoRender_Master_Plan.md` |
| `norender_branding` | `E:\NoRender_Branding` |
| `norender_logo_source` | `{norender_branding}\01_Logo_Source` |
| `norender_brand_guide` | `{norender_branding}\02_Brand_Guide` |
| `norender_brand_sheet` | `{norender_branding}\03_Brand_Sheet` |
| `norender_marketing` | `{norender_branding}\04_Marketing_Assets` |
| `norender_website` | `E:\NoRender_Website` |
| `norender_website_data` | `{norender_website}\data\projects.json` |
| `norender_website_images` | `{norender_website}\public\projects` |
