#!/bin/bash
# 새 세션 환경에 DM_Claude 자산(agents, skills, rules 등)이 없을 때 복구
set -e
HOME_DIR="$HOME/.claude"
REPO="https://github.com/eastpipl26/DM_Claude.git"

if [ -d "$HOME_DIR/agents" ] && [ "$(ls -A "$HOME_DIR/agents" 2>/dev/null)" ]; then
  echo "이미 agents 존재. 스킵."
  exit 0
fi

cd "$HOME_DIR"
if [ ! -d .git ]; then
  git init
  git remote add origin "$REPO"
fi
git fetch origin
git checkout -f -b master origin/master 2>/dev/null || git checkout -f master
echo "부트스트랩 완료: $(ls agents | wc -l)명 에이전트 로드됨"
