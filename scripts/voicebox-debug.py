# -*- coding: utf-8 -*-
import urllib.request, json, time, os, sys

profile_id = "4ec915dd-2cf5-442c-921e-1f8304faa54f"

# 텍스트를 파일에서 읽기 (인코딩 문제 우회)
text_file = "C:/Users/eastp/.claude/scripts/voicebox-text.txt"
if os.path.exists(text_file):
    with open(text_file, encoding="utf-8") as f:
        text = f.read().strip()
else:
    text = "SK하이닉스 용인 반도체 클러스터 설계 검토 회의를 시작하겠습니다"

print("text length:", len(text))

body = json.dumps({
    "profile_id": profile_id,
    "text": text,
    "language": "ko",
    "engine": "qwen",
    "model_size": "1.7B"
}).encode("utf-8")

req = urllib.request.Request(
    "http://localhost:8765/generate",
    data=body,
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req) as r:
    gen = json.loads(r.read())

gen_id = gen["id"]
print("id:", gen_id)

for i in range(60):
    time.sleep(3)
    req2 = urllib.request.Request("http://localhost:8765/history/" + gen_id)
    with urllib.request.urlopen(req2) as r:
        h = json.loads(r.read())
    elapsed = (i + 1) * 3
    print(f"{elapsed}s | status={h['status']} | duration={h['duration']}")
    if h["status"] in ("completed", "failed"):
        if h["status"] == "failed":
            print("failed:", h.get("error"))
            sys.exit(1)
        out = "C:/Users/eastp/voicebox-output/debug_test.wav"
        os.makedirs("C:/Users/eastp/voicebox-output", exist_ok=True)
        req3 = urllib.request.Request("http://localhost:8765/history/" + gen_id + "/export-audio")
        with urllib.request.urlopen(req3) as r:
            data = r.read()
        with open(out, "wb") as f:
            f.write(data)
        print("saved:", out, "size:", len(data), "bytes")
        break
else:
    print("timeout")
