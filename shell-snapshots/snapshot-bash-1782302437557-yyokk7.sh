# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
shopt -s expand_aliases
# Check for rg availability
if ! (unalias rg 2>/dev/null; command -v rg) >/dev/null 2>&1; then
  function rg {
  local _cc_bin="${CLAUDE_CODE_EXECPATH:-}"
  [[ -x $_cc_bin ]] || _cc_bin=/c/Users/eastp/.local/bin/claude.exe
  if [[ ! -x $_cc_bin ]]; then command rg ${1+"$@"}; return; fi
  if [[ -n ${ZSH_VERSION:-} ]]; then
    ARGV0=rg "$_cc_bin" ${1+"$@"}
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    ARGV0=rg "$_cc_bin" ${1+"$@"}
  else
    (exec -a rg "$_cc_bin" ${1+"$@"})
  fi
}
fi
export PATH='/c/Users/eastp/bin:/mingw64/bin:/usr/local/bin:/usr/bin:/bin:/mingw64/bin:/usr/bin:/c/Users/eastp/bin:/c/WINDOWS/system32:/c/WINDOWS:/c/WINDOWS/System32/Wbem:/c/WINDOWS/System32/WindowsPowerShell/v1.0:/c/WINDOWS/System32/OpenSSH:/c/Program Files/nodejs:/cmd:/c/Users/eastp/AppData/Local/Programs/Python/Python312/Scripts:/c/Users/eastp/AppData/Local/Programs/Python/Python312:/c/Users/eastp/AppData/Local/Programs/Python/Python314/Scripts:/c/Users/eastp/AppData/Local/Programs/Python/Python314:/c/Users/eastp/AppData/Local/Programs/Python/Launcher:/c/Users/eastp/AppData/Local/Microsoft/WindowsApps:/c/Users/eastp/AppData/Local/Programs/Antigravity/bin:/c/Users/eastp/AppData/Roaming/npm:/c/Users/eastp/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1-full_build/bin:/c/Users/eastp/AppData/Local/Programs/Antigravity IDE/bin:/usr/bin/vendor_perl:/usr/bin/core_perl'
