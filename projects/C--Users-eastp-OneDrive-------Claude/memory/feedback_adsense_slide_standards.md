---
name: feedback-adsense-slide-standards
description: 애드센스 슬라이드 제작 표준(흰 표+어두운 글씨·div표·색통일·간격) — 새 글에 미리 반영
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e8699199-dea7-4b06-89e5-66282670be85
---

애드센스 블로그([[project-adsense-blog]]) 슬라이드(Marp) 제작 시 아래 표준을 **미리 반영**한다. 매번 지적받지 말 것.

1. 어두운 배경 = 흰 글씨 / 표는 흰 배경 + 어두운 글씨.
2. **마크다운 표 금지** — marp이 width 무시. `.dtable`(div 기반) 사용해 폭 채움.
3. 표·박스 여러 개면 `.grid-2`로 나란히 + 간격.
4. 박스 색상 통일(흰). 강조는 `.card.note`(앰버 좌측 라인)만.
5. 카드 `height:100%` 금지(내용 높이 auto) → 그룹 간 간격 유지.
6. HTML div 안 markdown은 앞뒤 빈 줄(literal `**` 방지).

**Why:** 도요가 v1~v2에서 같은 지적(대비·표폭·색·간격)을 반복해서 함 → 표준화로 재작업 제거.

**How to apply:** 새 글 슬라이드는 `{vault}\20_Projects\애드센스_블로그\90_에셋\슬라이드-제작가이드.md`의 규칙·스니펫과 `marp-theme.css`를 그대로 재사용. 렌더는 `npx @marp-team/marp-cli --no-stdin --html --theme-set marp-theme.css --images png`.
