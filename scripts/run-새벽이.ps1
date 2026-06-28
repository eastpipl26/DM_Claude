# 새벽이 아침 브리핑 — 작업 스케줄러에서 매일 07:00 실행
$env:PATH = "C:\Users\eastp\AppData\Roaming\npm;$env:PATH"

$prompt = @"
너는 새벽이다. C:\Users\eastp\.claude\agents\새벽이.md 파일을 읽고 역할을 확인한 뒤,
오늘 아침 브리핑을 작성해 데일리노트에 삽입하고 카카오톡으로 전송해라.
작업 완료 후 결과를 C:\Users\eastp\.claude\logs\새벽이-$(Get-Date -Format 'yyyyMMdd').log 에 저장해라.
"@

claude --print -p $prompt 2>&1 | Out-File -Encoding utf8 "C:\Users\eastp\.claude\logs\새벽이-$(Get-Date -Format 'yyyyMMdd').log"
