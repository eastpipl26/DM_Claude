# Voicebox 백엔드 설치 + 완료 시 카카오톡 알림
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
# 사용법: & "C:\Users\eastp\.claude\scripts\voicebox-install.ps1"
# 참고: Tauri(데스크톱앱) 빌드 없이 Python 백엔드만 설치. TTS API 사용에 충분.

$env:PATH = "C:\Users\eastp\.bun\bin;" + $env:PATH
$backendDir = "C:\Users\eastp\voicebox\backend"

Write-Output "📦 [1/2] Python 의존성 설치 시작..."
Write-Output "   (torch 포함 — 수 분 소요될 수 있습니다)"

pip install uvicorn fastapi sqlalchemy alembic pydantic transformers accelerate huggingface_hub torch --quiet
if (-not $?) {
    Write-Error "pip install 단계에서 오류가 발생했습니다."
    exit 1
}

Write-Output "📦 [2/2] qwen-tts 설치 중... (한국어 TTS 엔진)"
pip install qwen-tts --quiet

Write-Output ""
Write-Output "✅ 설치 완료!"
Write-Output ""
Write-Output "▶ 서버 실행 명령:"
Write-Output "   cd C:\Users\eastp\voicebox"
Write-Output "   python -m uvicorn backend.main:app --reload --port 17493"
