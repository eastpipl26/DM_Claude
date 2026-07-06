import sys, json, time, os

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    session_id = data.get("session_id", "default")
    state_dir = os.path.join(os.path.expanduser("~"), ".claude", ".memory-hook-state")
    os.makedirs(state_dir, exist_ok=True)
    state_file = os.path.join(state_dir, f"{session_id}.ts")

    now = time.time()
    threshold = 3600  # 1시간

    last = None
    if os.path.exists(state_file):
        try:
            with open(state_file) as f:
                last = float(f.read().strip())
        except Exception:
            last = None

    with open(state_file, "w") as f:
        f.write(str(now))

    if last is not None and (now - last) >= threshold:
        gap_min = int((now - last) / 60)
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"[자동 메모리 점검] 마지막 활동 이후 약 {gap_min}분간 쉬었다가 돌아왔습니다. 지금까지 대화에서 저장할 만한 새 사실/피드백/프로젝트 진행상황이 있으면 auto-memory 규칙에 따라 저장하세요. 없으면 무시하고 넘어가세요."
            }
        }
        print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
