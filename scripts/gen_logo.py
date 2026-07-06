"""
묘이 로고 생성 스크립트 (BuildRight 브랜드)
사용법: python gen_logo.py --concept 1|2|3 --count 2|3 --filename_base buildright_concept1
"""
import os, sys, argparse, base64, json, urllib.request
from pathlib import Path
from typing import Tuple

API_KEY = None
DEEP_NAVY = "#0f1b2d"
GOLDEN_AMBER = "#d9a441"

CONCEPT_PROMPTS = {
    1: (
        "A minimalist flat vector logo icon for an architecture brand. "
        "A modern geometric building/tower silhouette whose form subtly incorporates "
        "the capital letterforms 'B' and 'R'. Bold, symmetrical, clean. "
        f"Golden amber (warm ochre gold, {GOLDEN_AMBER}) building shape centered on "
        f"a deep navy blue ({DEEP_NAVY}) background. Small windows as negative space. "
        "Flat design, no gradients, no shadows, single centered icon, professional, high contrast, "
        "1:1 square aspect ratio, 1024x1024 resolution."
    ),
    2: (
        "A minimalist geometric monogram logo fusing the capital letters 'B' and 'R' "
        "into one unified balanced mark. Modern bold geometric sans-serif construction "
        "with an architectural feel. "
        f"Golden amber (warm ochre gold, {GOLDEN_AMBER}) monogram centered on "
        f"a deep navy blue ({DEEP_NAVY}) square background. "
        "Flat vector, clean lines, no gradients, no extra text, iconic, high contrast, "
        "1:1 square aspect ratio, 1024x1024 resolution."
    ),
    3: (
        "A distinctive memorable minimalist logo mark for a brand about architecture and building regulations. "
        "An abstract geometric symbol evoking construction and precision — stacked architectural blocks "
        "or an angular structural / blueprint-inspired form. "
        f"Golden amber (warm ochre, {GOLDEN_AMBER}) and deep navy blue ({DEEP_NAVY}). "
        "Flat vector, modern, clean, single centered icon, no text, professional, high contrast, "
        "simple enough to work as a small app icon, 1:1 square aspect ratio, 1024x1024 resolution."
    ),
}

def load_api_key():
    global API_KEY
    env_path = Path(r"C:\Users\eastp\.claude\secrets\gemini.env")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
            return API_KEY
    raise ValueError("GEMINI_API_KEY not found in gemini.env")

def call_api(prompt: str) -> bytes:
    """Call Gemini Imagen API and return image bytes"""
    # Use official Gemini Imagen API endpoint
    url = (f"https://generativelanguage.googleapis.com/v1beta/"
           f"imagegeneration:generateImage?key={API_KEY}")

    payload = {
        "prompt": prompt
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            response = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"API Error ({e.code}): {error_body}")

    # Extract image from Imagen API response
    try:
        # Imagen returns a different response structure
        if "images" in response:
            # New format
            img_data = response["images"][0].get("imageBase64")
            if img_data:
                return base64.b64decode(img_data)

        if "candidates" in response:
            # Fallback for other formats
            for part in response["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    return base64.b64decode(part["inlineData"]["data"])

        raise ValueError(f"No image data in response: {response}")
    except (KeyError, IndexError, TypeError) as e:
        raise ValueError(f"Invalid response structure: {response}") from e

def validate_and_save(img_bytes: bytes, save_path: Path) -> Tuple[bool, str]:
    """Validate image with PIL and save. Returns (success, message)"""
    try:
        from PIL import Image
        import io

        # Open and verify
        img = Image.open(io.BytesIO(img_bytes))
        img.verify()

        # Re-open to check dimensions
        img = Image.open(io.BytesIO(img_bytes))
        w, h = img.size

        if w < 512 or h < 512:
            return False, f"Resolution too low: {w}x{h}"

        # Save as PNG
        img.save(save_path, "PNG")
        return True, f"Saved: {save_path} ({w}x{h})"

    except ImportError:
        # Fallback: save without validation
        save_path.write_bytes(img_bytes)
        return True, f"Saved (no PIL validation): {save_path}"
    except Exception as e:
        return False, f"Validation failed: {e}"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--concept", type=int, required=True, choices=[1, 2, 3],
                  help="Concept number (1-3)")
    p.add_argument("--count", type=int, default=2, choices=[1, 2, 3],
                  help="How many variations to generate per concept")
    p.add_argument("--filename-base", required=True,
                  help="Base filename (e.g., buildright_concept1)")
    args = p.parse_args()

    # Setup
    api_key = load_api_key()
    save_dir = Path(r"C:\Users\eastp\iCloudDrive\iCloud~md~obsidian\Dongmin\20_Projects\애드센스_블로그\90_에셋\로고-탐색")
    save_dir.mkdir(parents=True, exist_ok=True)

    concept_num = args.concept
    prompt_base = CONCEPT_PROMPTS[concept_num]
    results = []

    print(f"[로고 생성] Concept {concept_num}, {args.count}장")
    print(f"저장 경로: {save_dir}")
    print("-" * 60)

    for i in range(1, args.count + 1):
        # Add variation hint for multi-image requests
        if args.count > 1:
            variation = f" Variation {i}: unique geometric approach, fresh perspective."
            prompt = prompt_base + variation
        else:
            prompt = prompt_base

        filename = f"{args.filename_base}_{i}.png"
        save_path = save_dir / filename

        print(f"\n[{i}/{args.count}] {filename}")
        print(f"Prompt: {prompt[:100]}...")

        for attempt in range(1, 3):
            try:
                print(f"  시도 {attempt}/2...", end=" ")
                img_bytes = call_api(prompt)
                success, msg = validate_and_save(img_bytes, save_path)

                if success:
                    print(f"성공 ✓")
                    results.append({
                        "file": str(save_path),
                        "concept": concept_num,
                        "number": i,
                        "status": "success",
                        "message": msg
                    })
                    break
                else:
                    print(f"검증 실패: {msg}")
                    if attempt == 1:
                        continue
                    else:
                        results.append({
                            "file": filename,
                            "concept": concept_num,
                            "number": i,
                            "status": "failed",
                            "message": msg
                        })
            except Exception as e:
                print(f"실패: {e}")
                if attempt == 2:
                    results.append({
                        "file": filename,
                        "concept": concept_num,
                        "number": i,
                        "status": "error",
                        "message": str(e)
                    })

    # Summary
    print("\n" + "=" * 60)
    print("[생성 완료]")
    success_count = sum(1 for r in results if r["status"] == "success")
    print(f"성공: {success_count}/{args.count}")

    if success_count > 0:
        print("\n생성된 파일:")
        for r in results:
            if r["status"] == "success":
                print(f"  - {r['file']}")

    failed = [r for r in results if r["status"] != "success"]
    if failed:
        print(f"\n실패 ({len(failed)}):")
        for r in failed:
            print(f"  - {r['file']}: {r['message']}")

    return 0 if success_count == args.count else 1

if __name__ == "__main__":
    sys.exit(main())
