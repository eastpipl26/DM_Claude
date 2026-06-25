param(
    [Parameter(Mandatory=$true)]
    [string]$Text,
    [string]$VoiceProfile = "4ec915dd-2cf5-442c-921e-1f8304faa54f",
    [string]$OutputPath = ""
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

if (-not $OutputPath) {
    $timestamp = Get-Date -Format "yyMMdd_HHmm"
    $OutputPath = "C:\Users\eastp\voicebox-output\${timestamp}_tts.wav"
}

$outputDir = Split-Path $OutputPath
New-Item -ItemType Directory -Force $outputDir | Out-Null

$portCheck = Test-NetConnection -ComputerName localhost -Port 8765 -WarningAction SilentlyContinue
if (-not $portCheck.TcpTestSucceeded) {
    Write-Error "Voicebox 서버가 실행 중이지 않습니다."
    exit 1
}

# 1단계: 생성 요청
$bodyObj = @{
    profile_id = $VoiceProfile
    text       = $Text
    language   = "ko"
    engine     = "qwen"
    model_size = "1.7B"
}
$bodyBytes = [System.Text.Encoding]::UTF8.GetBytes(($bodyObj | ConvertTo-Json -Compress))

$gen = Invoke-RestMethod -Uri "http://localhost:8765/generate" -Method POST -ContentType "application/json; charset=utf-8" -Body $bodyBytes
$genId = $gen.id
Write-Output "생성 시작: $genId"

# 2단계: 완료 대기 (폴링)
$maxWait = 120
$elapsed = 0
while ($elapsed -lt $maxWait) {
    Start-Sleep -Seconds 2
    $elapsed += 2

    $history = Invoke-RestMethod -Uri "http://localhost:8765/history/$genId" -Method GET
    $status = $history.status

    if ($status -eq "completed") {
        Write-Output "생성 완료 (${elapsed}초)"
        break
    } elseif ($status -eq "failed") {
        Write-Error "생성 실패: $($history.error)"
        exit 1
    } else {
        Write-Output "생성 중... ($elapsed 초)"
    }
}

if ($elapsed -ge $maxWait) {
    Write-Error "시간 초과 (${maxWait}초)"
    exit 1
}

# 3단계: 오디오 파일 다운로드
$audioResponse = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8765/history/$genId/export-audio" -Method GET
[System.IO.File]::WriteAllBytes($OutputPath, $audioResponse.Content)
Write-Output "저장 완료: $OutputPath"
