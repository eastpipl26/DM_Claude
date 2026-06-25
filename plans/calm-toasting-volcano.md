# 플랜: 블로그-작성 스킬 — 이미지 Obsidian 내장

## Context
현재 블로그-작성 스킬은 이미지를 `file:///` 절대경로로 참조해서 Obsidian에서 사진이 표시되지 않는다.
Obsidian에서 이미지를 제대로 표시하려면 사진을 vault 안으로 복사하고 `![[파일명.jpg]]` 내부 링크로 참조해야 한다.

---

## 변경 사항

**Obsidian 첨부파일 설정 확인 결과:**
- vault: `C:\Users\eastp\iCloudDrive\Dongmin\`
- 첨부파일 경로: `90_System/Attachments` (app.json에 명시됨)

**변경 전:**
```markdown
![사진1](file:///C:/Users/eastp/OneDrive/.../마베럽 (3).jpg)
```

**변경 후:**
```markdown
![[마베럽 (3).jpg]]
```
→ 이미지를 vault `90_System/Attachments/블로그/YYMMDD_키워드/` 하위로 복사 후 내부링크 사용

---

## 구현 계획

### 수정 파일
`C:\Users\eastp\.claude\skills\블로그-작성\SKILL.md` — 2단계와 4단계 수정

### 수정 내용

**2단계에 추가 (사진 분석 전):**
- 이미지 파일을 vault attachment 폴더로 복사
- 복사 경로: `90_System/Attachments/블로그/YYMMDD_키워드/`
- 복사 명령 (PowerShell):
  ```
  New-Item -ItemType Directory -Force "<vault>\90_System\Attachments\블로그\<폴더명>"
  Copy-Item "<원본 이미지들>" "<위 경로>"
  ```
- 복사 후 내부 참조명만 기억 (파일명 그대로 사용)

**4단계 포맷 A 변경 (Obsidian MD):**
```markdown
![[마베럽 (3).jpg]]
*사진 캡션*
```
→ `file://` 대신 `![[파일명]]` 사용

**4단계 포맷 B (네이버 복붙):** 변경 없음 — 파일명만 표시

---

## 수정 파일 목록

| 파일 | 작업 |
|------|------|
| `C:\Users\eastp\.claude\skills\블로그-작성\SKILL.md` | 수정 (이미지 복사 + 내부링크) |

---

## 검증 방법
1. `/블로그-작성 <폴더경로>` 실행
2. `90_System/Attachments/블로그/<날짜_키워드>/` 폴더에 이미지 복사됐는지 확인
3. Obsidian에서 블로그 파일 열어 사진이 렌더링되는지 확인
