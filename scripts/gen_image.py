"""
묘이 이미지 생성 스크립트
사용법: python gen_image.py --topic X --section X --mood X --style X [--avoid X] --filename X
"""
import os, sys, argparse, base64, json, urllib.request
from pathlib import Path

MOOD_MAP = {
    "따뜻한": "warm, cozy, soft light, pastel tones, heartwarming",
    "정보전달형": "clean, minimal, professional, infographic-style",
    "신뢰감": "trustworthy, calm blue tones, professional, stable",
    "밝은 가족 일상": "bright, cheerful, family life, everyday moments",
}
STYLE_MAP = {
    "일러스트": "flat illustration, digital art, vector-style",
    "사진풍": "photorealistic, lifestyle photography style",
    "인포그래픽": "infographic, icons, data visualization style",
}

def load_api_key():
    env_path = Path(r"C:\Users\eastp\.claude\secrets\gemini.env")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise ValueError("GEMINI_API_KEY not found in gemini.env")

def build_prompt(topic, section, mood, style, avoid):
    mood_en = MOOD_MAP.get(mood, mood)
    style_en = STYLE_MAP.get(style, style)
    base = (f"A {style_en} image for a Korean blog post about '{topic}', "
            f"specifically for the '{section}' section. "
            f"Mood: {mood_en}. High quality, 1024x1024 or larger.")
    if avoid:
        avoid_parts = []
        for item in avoid.split(","):
            item = item.strip()
            if "텍스트" in item or "글자" in item:
                avoid_parts.append("no text overlay")
            elif "실제 인물" in item or "사람" in item:
                avoid_parts.append("no real people, illustrated characters only")
            else:
                avoid_parts.append(item)
        base += " Avoid: " + ", ".join(avoid_parts) + "."
    return base

def call_api(prompt, api_key):
    url = (f"https://generativelanguage.googleapis.com/v1beta/"
           f"models/gemini-2.0-flash-exp-image-generation:generateContent?key={api_key}")
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

def extract_image(response):
    for part in response["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])
    raise ValueError("No image data in response")

def validate_and_save(img_bytes, save_path):
    try:
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(img_bytes))
        img.verify()
        img = Image.open(io.BytesIO(img_bytes))
        w, h = img.size
        if w < 512 or h < 512:
            raise ValueError(f"Resolution too low: {w}x{h}")
        img.save(save_path, "PNG")
    except ImportError:
        save_path.write_bytes(img_bytes)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--topic", required=True)
    p.add_argument("--section", required=True)
    p.add_argument("--mood", required=True)
    p.add_argument("--style", required=True)
    p.add_argument("--avoid", default="")
    p.add_argument("--filename", required=True)
    args = p.parse_args()

    api_key = load_api_key()
    save_dir = Path(r"C:\Users\eastp\.claude\assets\images")
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / f"{args.filename}.png"

    prompt = build_prompt(args.topic, args.section, args.mood, args.style, args.avoid)
    print(f"Prompt: {prompt[:80]}...")

    for attempt in range(1, 3):
        try:
            resp = call_api(prompt, api_key)
            img_bytes = extract_image(resp)
            validate_and_save(img_bytes, save_path)
            print(f"[성공] {save_path} (시도 {attempt})")
            sys.exit(0)
        except Exception as e:
            print(f"[시도 {attempt} 실패] {e}")
            if attempt == 1:
                prompt = (f"A simple {STYLE_MAP.get(args.style, args.style)} image about '{args.topic}'. "
                          f"Mood: {MOOD_MAP.get(args.mood, args.mood)}. Clean, high quality.")

    print("[최종 실패] 2회 모두 실패")
    sys.exit(1)

if __name__ == "__main__":
    main()
