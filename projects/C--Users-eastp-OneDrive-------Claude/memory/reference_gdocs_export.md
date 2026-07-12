---
name: reference_gdocs_export
description: 마크다운→Google Docs 내보내기는 base64 임베드 HTML로 Drive create_file
metadata:
  node_type: memory
  type: reference
  originSessionId: 7fc64c63-f55c-4dc1-9efb-1d2d96d78fcd
---

vault 마크다운(이미지 포함)을 Google Docs로 내보낼 때: 이미지를 **base64로 임베드한 HTML**을 만들어 Google Drive MCP `create_file`로 업로드한다.

**주의:** base64 대신 "PLACEHOLDER" 같은 텍스트를 넣으면 이미지 없는 깨진 문서가 생성됨(2026-07 이력서 내보내기 실수). 반드시 실제 base64 데이터로 생성할 것. 깨진 문서 삭제는 도요가 직접(파기 작업은 말숙이가 실행 안 함).
