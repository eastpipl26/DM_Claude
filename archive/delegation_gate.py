#!/usr/bin/env python3
r"""
delegation_gate.py — 말숙이 위임 강제 게이트 (PreToolUse)

feedback_task_delegation 규칙("말숙이는 직접 분석·작성·정리하지 않는다")을
CLAUDE.md 권고가 아니라 물리적으로 강제한다.

원본 아이디어(Fable 오케스트레이션 가이드, WSL/코드파일 기준)를 우리 팀 구조에 맞게 변형:
- 제한 대상 = "코드 파일 확장자"가 아니라 "vault 경로"(회의록·블로그·리서치·노트 등 콘텐츠).
  .claude\ 안의 에이전트·스킬·메모리·설정 파일은 말숙이의 정상 운영 업무라 제한하지 않는다.
- 서브에이전트(강이·문이·옥순이 등)의 호출은 hook payload의 agent_id/agent_type 필드로
  구분해 전부 통과시킨다 — 위임이 곧 정상 실행 경로이기 때문.
- 턴 경계는 prompt_id로 감지(Claude Code v2.1.196+ 필요).
- 오류 시 fail-open(통과) — 게이트 버그가 세션을 마비시키지 않게 한다.

스위치: C:\\Users\\eastp\\.claude\\.delegation-gate-state 파일 내용이 "on"이 아니면 전부 통과.
"""
import json
import os
import re
import sys
import time

LIMIT = 2
STATE_FILE = r"C:\Users\eastp\.claude\.delegation-gate-state"
GATE_STATE_DIR = r"C:\Users\eastp\.claude\gate_state"
CONFIG_MD = r"C:\Users\eastp\.claude\config.md"


def allow():
    sys.exit(0)


def deny(msg):
    sys.stderr.write(msg)
    sys.exit(2)


def get_vault_path():
    """config.md에서 vault 변수 값을 읽는다. 실패하면 알려진 기본값으로 폴백."""
    try:
        text = open(CONFIG_MD, encoding="utf-8").read()
        m = re.search(r"\|\s*`vault`\s*\|\s*`([^`]+)`\s*\|", text)
        if m:
            return m.group(1)
    except OSError:
        pass
    return r"C:\Users\eastp\iCloudDrive\iCloud~md~obsidian\Dongmin"


def main():
    try:
        state = open(STATE_FILE, encoding="utf-8").read().strip()
    except OSError:
        state = "off"
    if state != "on":
        allow()

    data = json.load(sys.stdin)

    # 서브에이전트 호출은 게이트 대상이 아님 — 위임이 실행 경로다
    if data.get("agent_id") or data.get("agent_type"):
        allow()

    tool = data.get("tool_name", "")
    if tool not in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        allow()

    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not path:
        allow()

    vault = get_vault_path()
    try:
        under_vault = os.path.normcase(os.path.abspath(path)).startswith(
            os.path.normcase(os.path.abspath(vault))
        )
    except (OSError, ValueError):
        under_vault = False
    if not under_vault:
        allow()  # .claude\ 등 말숙이 운영 파일은 제한하지 않음

    session = re.sub(r"[^a-zA-Z0-9-]", "", data.get("session_id", "nosession"))
    prompt = data.get("prompt_id", "")

    os.makedirs(GATE_STATE_DIR, exist_ok=True)
    gate_file = os.path.join(GATE_STATE_DIR, session + ".json")
    gate = {"prompt_id": prompt, "files": []}
    try:
        saved = json.load(open(gate_file, encoding="utf-8"))
        if saved.get("prompt_id") == prompt:
            gate = saved
        else:  # 새 턴 — 카운터 리셋 + 오래된 세션 상태 정리
            now = time.time()
            for fn in os.listdir(GATE_STATE_DIR):
                p = os.path.join(GATE_STATE_DIR, fn)
                if now - os.path.getmtime(p) > 86400:
                    os.remove(p)
    except (OSError, ValueError):
        pass

    if path in gate["files"]:
        allow()  # 같은 파일 재수정은 개수에 안 침

    if len(gate["files"]) < LIMIT:
        gate["files"].append(path)
        json.dump(gate, open(gate_file, "w", encoding="utf-8"))
        allow()

    deny(
        "[위임 게이트] 이번 턴에 말숙이가 직접 수정한 vault 콘텐츠 파일이 이미 %d개입니다 (%s). "
        "추가 콘텐츠 작성·정리는 담당 직원에게 위임하세요: 블로그/글쓰기→문이, "
        "리서치→캐순이/탐이/수이, 유튜브 노트→강이, vault 저장·정리→옥순이, "
        "부동산 분석→감이. 위임이 정말 불가능한 상황이면 도요님께 사유를 알리세요."
        % (LIMIT, ", ".join(gate["files"]))
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # fail-open
