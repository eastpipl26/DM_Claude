"""
YouTube 영상에서 자막(스크립트)과 제목을 추출해 JSON으로 출력한다.
Usage: python youtube_transcript.py <YouTube URL>
Output: {"title": "...", "transcript": "...", "url": "...", "video_id": "..."}
"""

import sys
import json
import re
import urllib.request

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def extract_video_id(url: str) -> str:
    patterns = [
        r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
        r"(?:shorts/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"YouTube URL에서 video ID를 찾을 수 없음: {url}")


def get_video_title(video_id: str) -> str:
    try:
        req = urllib.request.Request(
            f"https://www.youtube.com/watch?v={video_id}",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        match = re.search(r'<title>(.+?) - YouTube</title>', html)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    return f"YouTube_{video_id}"


def get_transcript(video_id: str) -> str:
    api = YouTubeTranscriptApi()
    try:
        transcript_list = api.list(video_id)

        # 수동 자막 우선
        try:
            t = transcript_list.find_manually_created_transcript(["ko", "en", "en-US"])
            entries = t.fetch()
        except Exception:
            # 자동생성 자막
            try:
                t = transcript_list.find_generated_transcript(["ko", "en"])
                entries = t.fetch()
            except Exception:
                entries = api.fetch(video_id, languages=["ko", "en"])

    except (TranscriptsDisabled, NoTranscriptFound) as e:
        raise RuntimeError(f"자막을 가져올 수 없음: {e}")

    lines = []
    for entry in entries:
        start = int(entry.start)
        minutes, seconds = divmod(start, 60)
        timestamp = f"[{minutes:02d}:{seconds:02d}]"
        text = entry.text.replace("\n", " ").strip()
        if text:
            lines.append(f"{timestamp} {text}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "URL이 필요합니다. Usage: python youtube_transcript.py <URL>"}))
        sys.exit(1)

    url = sys.argv[1]
    try:
        video_id = extract_video_id(url)
        title = get_video_title(video_id)
        transcript = get_transcript(video_id)
        print(json.dumps({
            "title": title,
            "transcript": transcript,
            "url": url,
            "video_id": video_id,
        }, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
