# Remote Control server - lets the phone (Claude app > Code tab) drive this PC.
# Runs in C:\Users\eastp\claude-workspace (ASCII path; Korean paths break the CLI trust check).
# Global CLAUDE.md (Malsuki persona), agents, skills, and the vault are all reachable from here.
Set-Location "C:\Users\eastp\claude-workspace"
while ($true) {
    cmd /c "echo y| claude remote-control --remote-control-session-name-prefix doyo-pc"
    Write-Host "RC server exited. Restarting in 30s... (Ctrl+C to stop)"
    Start-Sleep -Seconds 30
}
