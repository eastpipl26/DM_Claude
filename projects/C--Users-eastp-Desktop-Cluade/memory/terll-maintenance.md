---
name: terll-maintenance
description: TER/LL(Trouble Error Report/Lessons Learned) 사례 데이터 위치와 지속 업데이트 규칙
metadata: 
  node_type: memory
  type: project
  originSessionId: 13c66935-61c2-44bd-b555-bc7eb1fba0f9
  modified: 2026-07-20T10:52:35.499Z
---

TER/LL 원본데이터는 Obsidian vault에 공종별로 분리 저장되어 있고, 신규 사례가 생기면 계속 추가되어야 하는 살아있는 자료다.

- 원본 데이터: `Dongmin\20_Projects\SK하이닉스_용인\TER_LL_원본데이터\{건축,설비,UT배관,전기,자동제어,토목,기계,환경,소방}.md` — 공종별 파일, 각 행은 No/PJT/단계/항목/위치/현재상태/원인/해결방안/바람직한모습/반영내용 컬럼.
- 가공 요약본: `Dongmin\20_Projects\SK하이닉스_용인\설계단계별_대응계획_TER-LL_가공자료.md` — 통계·패턴·체크리스트 정리본.
- items(업무일지)의 개별 사건 중 TER/LL 성격(사고·오류·재발방지 교훈)이면 frontmatter `카테고리`에 `TER` 또는 `LL` 태그 추가, `TER_LL.base`로 조회.

**How to apply:** 도요가 새로운 TER/LL성 사례(트러블/오류/교훈)를 이야기하면, 해당 공종 파일에 같은 컬럼 구조로 신규 행을 추가하고, 필요시 요약본(패턴/체크리스트)도 갱신을 검토한다. 원본은 raw 그대로 두지 말고 표(테이블) 형태로 정리해 가독성을 유지한다 (2026-07-20에 raw bullet 덤프를 마크다운 표로 재정리함).
