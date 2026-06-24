---
name: 학습-유튜브
description: YouTube 영상 스크립트를 추출해 Obsidian 학습노트로 저장하고, 같은 주제가 3개 이상이면 MOC를 자동 생성/갱신한다.
---

# 학습-유튜브 스킬

## 사용법
```
/학습-유튜브 <YouTube URL> <주제>
```
예시:
```
/학습-유튜브 https://youtu.be/abc123 AI개발
/학습-유튜브 https://www.youtube.com/watch?v=xyz456 건축설계
```

## 동작 순서

### 1단계: 입력 파싱
`$ARGUMENTS`에서 URL(첫 번째 단어)과 주제(나머지)를 파싱한다.
- URL: `https://` 또는 `youtu.be`로 시작하는 문자열
- 주제: URL 뒤 나머지 전체 (공백 포함 가능)
- 주제가 없으면 사용자에게 물어본다.

### 2단계: 스크립트 추출
아래 명령을 실행한다:
```
python "C:\Users\eastp\.claude\scripts\youtube_transcript.py" <URL>
```
결과는 JSON으로 반환된다: `{title, transcript, url, video_id}`
- 오류가 나면 사용자에게 오류 내용을 알리고 중단한다.

### 3단계: 노트 내용 생성
transcript를 읽고 Claude가 직접 아래 형식의 마크다운을 작성한다.

**파일명**: `YYMMDD_유튜브_제목키워드.md`
- 오늘 날짜(YYMMDD) + `_유튜브_` + 제목에서 핵심 키워드 2~3개 (한글 또는 영어, 공백 없이)
- 예: `260624_유튜브_LangChain입문.md`

**파일 내용**:
```markdown
---
title: <영상 제목>
date: <오늘 날짜 YYYY-MM-DD>
type: 학습노트
source: youtube
url: <YouTube URL>
subject: <주제>
tags: [<주제>, youtube, 학습]
---

## 핵심 요약
<transcript를 바탕으로 3~5줄 요약. 핵심 주장·결론 중심으로.>

## 주요 포인트
<bullet로 5~10개. 구체적인 개념·방법·사실 위주.>

## 전체 스크립트
<transcript 원문 전체. 타임스탬프 포함.>
```

### 4단계: 옥순이에게 저장 위임
아래 내용을 포함해 옥순이(obsidian-manager 에이전트)에게 위임한다:
- 저장 경로: `C:\Users\eastp\iCloudDrive\Dongmin\40_Resources\<주제>\<파일명>`
- 폴더가 없으면 생성 후 저장
- 저장 완료 후 경로를 보고할 것

### 5단계: MOC 트리거 확인
옥순이에게 아래 확인을 추가로 요청한다:
- `40_Resources/<주제>/` 폴더에서 frontmatter `type: 학습노트`인 파일 수를 센다
- **3개 이상이면** MOC를 생성/갱신한다

**MOC 파일 경로**: `40_Resources/<주제>/_<주제>_MOC.md`

**MOC가 없으면 새로 생성**:
```markdown
---
title: <주제> 학습 MOC
date: <오늘 날짜 YYYY-MM-DD>
type: MOC
subject: <주제>
tags: [<주제>, MOC, 학습로드맵]
status: active
---

## 학습 노트 목록
| 제목 | 날짜 | 링크 |
|------|------|------|
<폴더 내 학습노트 파일 목록 — 파일명에서 날짜·제목 추출>

```dataview
TABLE date, title FROM "40_Resources/<주제>"
WHERE type = "학습노트" SORT date DESC
```
```

**MOC가 이미 있으면** 테이블에 새 노트 행을 추가한다.

### 6단계: 완료 보고
말숙이가 사용자에게 보고한다:
- 저장된 파일 경로
- MOC 생성/갱신 여부 (해당되면)
