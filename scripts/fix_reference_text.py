import urllib.request, json, sqlite3, os

sample_audio = "C:/Users/eastp/voicebox/data/profiles/4ec915dd-2cf5-442c-921e-1f8304faa54f/d26c1680-bae1-4093-abd6-8bde4bcde91d.wav"
db_path = "C:/Users/eastp/voicebox/data/voicebox.db"
sample_id = "d26c1680-bae1-4093-abd6-8bde4bcde91d"

# Voicebox transcription API로 샘플 트랜스크립트
print("트랜스크립트 요청 중...")
with open(sample_audio, "rb") as f:
    audio_data = f.read()

boundary = "----FormBoundary7MA4YWxkTrZu0gW"
body = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="audio"; filename="sample.wav"\r\n'
    f"Content-Type: audio/wav\r\n\r\n"
).encode() + audio_data + f"\r\n--{boundary}--\r\n".encode()

req = urllib.request.Request(
    "http://localhost:8765/transcription/transcribe",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    method="POST"
)
try:
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())
    transcript = result.get("text") or result.get("transcript") or str(result)
    print("트랜스크립트 결과:", transcript)
except Exception as e:
    print("트랜스크립트 API 오류:", e)
    print("수동 입력으로 대체합니다.")
    transcript = "SK하이닉스 용인 반도체 클러스터 설계 검토 회의를 시작하겠습니다. 오늘 안건은 Y-1 Phase 1 클린룸 도면 조율 건입니다. 각 담당자 확인 부탁드립니다."

# DB 업데이트
print(f"\nDB 업데이트: reference_text = {transcript[:50]}...")
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute(
    "UPDATE profile_samples SET reference_text = ? WHERE id = ?",
    (transcript, sample_id)
)
conn.commit()

# 확인
row = cur.execute("SELECT reference_text FROM profile_samples WHERE id = ?", (sample_id,)).fetchone()
print("업데이트 후 DB:", row[0][:80] if row else "없음")
conn.close()
print("완료")
