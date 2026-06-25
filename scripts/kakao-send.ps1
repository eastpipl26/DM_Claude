# 카카오톡 나에게 메시지 전송 스크립트
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
# 사용법: .\kakao-send.ps1 -Message "보낼 내용"

param(
    [Parameter(Mandatory=$true)]
    [string]$Message,
    [string]$Title = ""
)

# 토큰 로드
$envPath = "C:\Users\eastp\.claude\secrets\kakao.env"
$envContent = Get-Content $envPath -Raw
$token = ($envContent -split "`n" | Where-Object { $_ -match "^KAKAO_ACCESS_TOKEN=" }) -replace "KAKAO_ACCESS_TOKEN=", "" | ForEach-Object { $_.Trim() }

if (-not $token) {
    Write-Error "액세스 토큰이 없습니다. kakao.env 확인하세요."
    exit 1
}

# 메시지 구성
$fullText = if ($Title) { "${Title}`n`n${Message}" } else { $Message }

$template = @{
    object_type = "text"
    text = $fullText
    link = @{
        web_url = "https://developers.kakao.com"
        mobile_web_url = "https://developers.kakao.com"
    }
} | ConvertTo-Json -Compress

Add-Type -AssemblyName System.Web
$encodedTemplate = [System.Web.HttpUtility]::UrlEncode($template)

try {
    $response = Invoke-RestMethod `
        -Uri "https://kapi.kakao.com/v2/api/talk/memo/default/send" `
        -Method POST `
        -Headers @{ Authorization = "Bearer $token" } `
        -ContentType "application/x-www-form-urlencoded" `
        -Body "template_object=$encodedTemplate"

    if ($response.result_code -eq 0) {
        Write-Output "✅ 카카오톡 전송 완료"
    } else {
        Write-Warning "전송 실패: $($response | ConvertTo-Json)"
    }
} catch {
    Write-Error "전송 오류: $_"
}
