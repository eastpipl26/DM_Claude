---
name: feedback_config_variables
description: "경로·설정값은 config.md 변수로 관리, 에이전트·스킬에 하드코딩 금지"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7fc64c63-f55c-4dc1-9efb-1d2d96d78fcd
---

경로·모델명·파일명 규칙 등 변동 가능한 값은 `C:\Users\eastp\.claude\config.md` 하나에서 관리한다. 새 에이전트·스킬·자동화를 만들 때 경로를 직접 쓰지 말고 config.md 변수를 참조하도록 작성한다.

**Why:** vault 경로가 바뀔 때 전 파일을 다 수정해야 하는 문제를 겪음. config.md 하나만 바꾸면 전체에 반영되도록 구조 변경.

**How to apply:** 에이전트·스킬 작성 시 "시작 시 config.md Read 후 변수 사용" 블록을 상단에 추가. 경로 리터럴(`C:\Users\eastp\iCloudDrive\...`) 직접 기재 금지.
