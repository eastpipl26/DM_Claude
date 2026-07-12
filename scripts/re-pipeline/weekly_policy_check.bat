@echo off
chcp 65001 >nul
setlocal
set TASKPROMPT="오늘 날짜 기준 이번 주 주간트래커 md 파일을 찾아서(폴더: C:\Users\eastp\iCloudDrive\iCloud~md~obsidian\Dongmin\30_Areas\부동산\트래커, 파일명 패턴 YYMMDD_주간트래커.md, 오늘 날짜 기준 최신 파일) 그 파일 맨 아래에 다음 섹션을 추가하라: '## 이번 주 정책·거시·호재 업데이트'. WebSearch로 다음 4가지를 확인해서 각각 2~3문장으로 요약하고 출처 링크를 붙여라 - 1) 한국은행 기준금리 변동 여부 2) 수도권/인천 부동산 대출규제·세제 정책 변화 3) GTX-B 착공·공정 진행상황 4) 그란테르 등 인접 대규모 분양·상권 개발 소식. 변화가 없으면 '변화 없음'이라고 명시하라. 추측하지 말고 검색 결과 기반으로만 작성하라. 파일 앞부분 내용은 건드리지 말고 맨 아래에 이어서 추가만 하라."
claude -p %TASKPROMPT% --allowedTools "WebSearch,Read,Write" --disallowedTools "Bash,Edit" --permission-mode acceptEdits --model sonnet >> "C:\Users\eastp\.claude\scripts\re-pipeline\weekly_policy_log.txt" 2>&1
