# 옥순이 야간 정리 루틴 — 작업 스케줄러에서 매일 23:00 실행
$env:PATH = "C:\Users\eastp\AppData\Roaming\npm;$env:PATH"

$prompt = @"
너는 옥순이다. C:\Users\eastp\.claude\agents\obsidian-manager.md 파일을 읽고 역할을 확인한 뒤,
야간 정리 루틴을 실행해라:
1. Obsidian vault 00_Inbox 파일 분류
2. 내일 날짜 데일리노트 생성 (없으면)
3. 작업 로그 저장
"@

claude --print -p $prompt 2>&1 | Out-File -Encoding utf8 "C:\Users\eastp\.claude\logs\옥순이-$(Get-Date -Format 'yyyyMMdd').log"
