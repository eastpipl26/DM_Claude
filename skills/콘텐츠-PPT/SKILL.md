---
name: 콘텐츠-PPT
description: 주제 텍스트나 블로그 글을 입력하면 대본 작성 → Marp 슬라이드 생성 파이프라인으로 PPT를 자동 생성한다. 유튜브/SNS 콘텐츠 제작용.
---

# 콘텐츠-PPT 스킬

## 사용법

```
/콘텐츠-PPT <주제 텍스트>
/콘텐츠-PPT <기존 파일 경로.md>
```

---

## 동작: 단일 서브에이전트 파이프라인

메인 세션은 입력 파싱(파일 경로 vs 주제 텍스트) 후 general-purpose 서브에이전트를 `run_in_background: true`로 스폰해 아래 파이프라인 전체를 위임한다.

## 파이프라인 (서브에이전트 수행)

시작 전 `{claude_home}\config.md` Read — `content_script`, `content_ppt`, `claude_home` 변수 확인.

### 1. 대본 작성
- 주제 텍스트(또는 입력 .md 파일)를 슬라이드 1장 단위로 분리된 나레이션 대본으로 작성.
- 저장: `{content_script}\YYMMDD_{키워드}_대본.md`

### 2. Marp 변환
- 대본을 Marp 마크다운으로 변환 (슬라이드 단위 `---` 구분).
- 테마: `{claude_home}\design\dark-card-theme.css` (다크 배경·카드형 레이아웃) 기본 적용. 주제 톤이 안 맞으면(밝은 톤 등) 테마 CSS를 변형해 새로 만든다 — 시각 산출물이므로 `{claude_home}\design\DESIGN.md` 디자인 기준 준수.
- Marp CLI로 출력:
```
npx @marp-team/marp-cli@latest <marp.md> --theme <theme.css> --pptx -o <출력.pptx>
npx @marp-team/marp-cli@latest <marp.md> --theme <theme.css> --html -o <출력.html>
```
- 저장: `{content_ppt}\YYMMDD_{키워드}\`

### 3. 완료 보고
- 대본 파일 경로, .pptx/.html 경로(절대경로), 슬라이드 수, 적용 테마명.
- 파일 실제 존재 확인 후 보고.
