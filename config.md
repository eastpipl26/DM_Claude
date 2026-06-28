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
| `resources` | `{vault}\40_Resources` |
| `system` | `{vault}\90_System` |
| `daily_notes` | `{vault}\90_System\DailyNotes` |
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
