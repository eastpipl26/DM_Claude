import requests
import base64
import json
import sys
from pathlib import Path

import os
API_KEY = os.environ.get("GEMINI_API_KEY", "")
OUTPUT_PATH = r"C:\Users\eastp\.claude\assets\images\260628_신생아특례대출_도입부.png"

PROMPT = (
    "A warm and heartwarming flat illustration of a young Korean couple holding a newborn baby at home. "
    "Soft pastel tones, cozy interior, gentle sunlight through curtains. "
    "Digital art, vector-style, flat illustration. "
    "No text, no labels, no real people, illustrated characters only."
)

def try_generatecontent(model):
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": PROMPT}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
    }
    print(f"[generateContent] {model}")
    r = requests.post(url, json=payload, timeout=60)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    return part["inlineData"]["data"]
    else:
        print(f"  {r.text[:300]}")
    return None

def try_predict(model):
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:predict?key={API_KEY}"
    payload = {
        "instances": [{"prompt": PROMPT}],
        "parameters": {"sampleCount": 1}
    }
    print(f"[predict] {model}")
    r = requests.post(url, json=payload, timeout=60)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        preds = data.get("predictions", [])
        if preds:
            return preds[0].get("bytesBase64Encoded") or preds[0].get("imageBytes")
    else:
        print(f"  {r.text[:300]}")
    return None

image_data = None

# 1차: gemini-2.5-flash-image (generateContent)
image_data = try_generatecontent("models/gemini-2.5-flash-image")

# 2차: imagen-4.0-generate-001 (predict)
if not image_data:
    image_data = try_predict("models/imagen-4.0-generate-001")

# 3차: gemini-3.1-flash-image-preview (generateContent)
if not image_data:
    image_data = try_generatecontent("models/gemini-3.1-flash-image-preview")

if not image_data:
    print("모든 시도 실패")
    sys.exit(1)

img_bytes = base64.b64decode(image_data)
Path(OUTPUT_PATH).write_bytes(img_bytes)
print(f"저장 완료: {OUTPUT_PATH}")

try:
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(img_bytes))
    print(f"이미지 크기: {img.width} x {img.height}")
except ImportError:
    print(f"파일 크기: {len(img_bytes)} bytes")
