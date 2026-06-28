"""
hook_update.py - Claude Code Hook에서 호출됨
stdin으로 Hook JSON을 받아 state.json을 갱신한다.

settings.json hooks:
  PreToolUse  → 에이전트 spawn 시 status=working
  Stop        → 세션 종료 시 모두 idle로
"""
import json, sys
from pathlib import Path
from datetime import datetime

STATE_FILE = Path(r"C:\Users\eastp\.claude\dashboard2\state.json")

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except:
            pass
    return {"agents": {}, "log": [], "usage": {"today": 0, "week": 0}, "updated_at": ""}

def save_state(state):
    state["updated_at"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    try:
        raw = sys.stdin.read()
        hook_data = json.loads(raw) if raw.strip() else {}
    except:
        hook_data = {}

    state = load_state()
    event = hook_data.get("hook_event_name", "")
    tool  = hook_data.get("tool_name", "")

    now = datetime.now().strftime("%H:%M:%S")

    if event == "PreToolUse" and tool == "Agent":
        inp   = hook_data.get("tool_input", {})
        desc  = inp.get("description", "에이전트 작업")
        prompt_preview = inp.get("prompt", "")[:40]
        # 에이전트 이름 추정 (subagent_type 또는 description에서)
        agent_type = inp.get("subagent_type", "claude")
        state["agents"][agent_type] = {
            "status": "working",
            "task": desc,
            "started_at": datetime.now().isoformat()
        }
        state["log"].insert(0, {"time": now, "msg": f"{agent_type} → {desc} 시작"})
        state["usage"]["today"] = state["usage"].get("today", 0) + 1
        state["usage"]["week"]  = state["usage"].get("week", 0) + 1

    elif event == "Stop":
        # 세션 종료 — 모든 working 에이전트 idle로
        for k in state["agents"]:
            if state["agents"][k].get("status") == "working":
                state["agents"][k]["status"] = "idle"
                state["agents"][k]["task"] = ""
        state["log"].insert(0, {"time": now, "msg": "세션 종료 — 전 직원 대기"})

    # 로그 최대 100개 유지
    state["log"] = state["log"][:100]
    save_state(state)

if __name__ == "__main__":
    main()
