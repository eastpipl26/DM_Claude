"""
make_ics.py — 일정 목록을 ICS 파일로 빠르게 변환

사용법:
    python make_ics.py

이벤트를 EVENTS 리스트에 추가하고 실행하면 output.ics 생성됨.
구글 캘린더 설정 → 가져오기/내보내기 → output.ics 업로드 → 캘린더 선택 → 가져오기

이벤트 형식:
    종일 이벤트: date는 "YYYYMMDD"
    시간 지정:   date는 "YYYYMMDDTHHMMSS", end_date 필요
"""

from datetime import datetime, date
import uuid

EVENTS = [
    # 예시 — 실제 일정으로 교체
    {
        "title": "예시 이벤트",
        "date": "20260708",          # 종일: YYYYMMDD / 시간: YYYYMMDDTHHmmSS
        "end_date": "20260709",      # 종일 이벤트는 +1일 (구글 캘린더 표준)
        "description": "설명 (선택)",
    },
]

def make_ics(events: list, output_path: str = "output.ics"):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//말순이//ICS Generator//KO",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]

    for ev in events:
        uid = str(uuid.uuid4())
        title = ev["title"]
        date_str = ev["date"]
        end_str = ev.get("end_date", "")
        desc = ev.get("description", "")

        is_allday = "T" not in date_str

        lines.append("BEGIN:VEVENT")
        lines.append(f"UID:{uid}")
        lines.append(f"SUMMARY:{title}")

        if is_allday:
            lines.append(f"DTSTART;VALUE=DATE:{date_str}")
            if end_str:
                lines.append(f"DTEND;VALUE=DATE:{end_str}")
            else:
                # 기본: 하루짜리
                d = datetime.strptime(date_str, "%Y%m%d").date()
                from datetime import timedelta
                next_d = d + timedelta(days=1)
                lines.append(f"DTEND;VALUE=DATE:{next_d.strftime('%Y%m%d')}")
        else:
            lines.append(f"DTSTART;TZID=Asia/Seoul:{date_str}")
            if end_str:
                lines.append(f"DTEND;TZID=Asia/Seoul:{end_str}")

        if desc:
            lines.append(f"DESCRIPTION:{desc}")

        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\r\n".join(lines))

    print(f"✅ {len(events)}개 이벤트 → {output_path}")
    print("→ 구글 캘린더 설정 > 가져오기/내보내기 > 파일 선택 > 캘린더 선택 > 가져오기")


if __name__ == "__main__":
    make_ics(EVENTS)
