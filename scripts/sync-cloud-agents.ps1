# 클라우드(폰 앱 깃 연동) 세션용 에이전트 미러 동기화
# 클라우드는 저장소 루트 agents\ 가 아니라 .claude\agents\ 를 읽는다.
# 에이전트를 추가·수정한 뒤 push 전에 이 스크립트를 실행한다.
robocopy "C:\Users\eastp\.claude\agents" "C:\Users\eastp\.claude\.claude\agents" *.md /MIR /NJH /NJS /NDL
if ($LASTEXITCODE -le 7) { exit 0 } else { exit $LASTEXITCODE }
