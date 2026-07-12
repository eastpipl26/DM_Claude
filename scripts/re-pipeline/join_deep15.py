# -*- coding: utf-8 -*-
r"""심층 15개 단지 통합표 생성 — 가격모멘텀(단지비교) + 수급(세대수·회전율·매물비율).

사용법:
  python join_deep15.py

출력: {re_data}\심층15_통합_YYMMDD.csv
"""
import csv
import os
import re
import sys
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from common import load_config

DEEP15 = ["송도더샵센트럴시티", "e편한세상송도", "더샵송도마리나베이", "베르디움더퍼스트",
          "송도SKVIEW", "랜드마크시티센트럴더샵", "송도에듀포레푸르지오",
          "송도글로벌파크베르디움", "송도오션파크베르디움", "송도더샵퍼스트파크F14BL",
          "글로벌캠퍼스푸르지오", "더샵그린스퀘어", "송도더샵퍼스트파크F15BL",
          "송도아메리칸타운아이파크", "송도더샵파크애비뉴"]

# RTMS(국토부) 단지명 → 아실 표기명. 브랜드명이 달라 자동 정규화 매칭이 안 되는 건들.
# 세대수+준공년도(K-apt) 교차검증으로 확정 (2026-07-07, 사이클3). fetch_asil.py와 동일 매핑.
RTMS_TO_ASIL = {
    "송도글로벌파크베르디움": "송도국제도시호반베르디움(RC-1블럭)",
    "송도오션파크베르디움": "송도국제도시호반베르디움3차",
    "더샵송도마리나베이": "송도센토피아더샵",
    "송도SKVIEW": "인천송도SK뷰",
    "송도아메리칸타운아이파크": "송도아메리칸타운IPARK",
    "송도더샵센트럴시티": "송도더샵센트럴시티(송도국제도시RM2블록)(주)",
}


def norm(s):
    return re.sub(r"[\s()·\[\]F\-]", "", s).upper()


def run():
    cfg = load_config()
    d = cfg["re_data"]
    tag = date.today().strftime("%y%m%d")

    price_path = os.path.join(d, f"단지비교_{tag}.csv")
    if not os.path.exists(price_path):
        print(f"[중단] {price_path} 없음 — 먼저 calc_metrics.py 실행")
        sys.exit(1)

    turnover = {}
    for r in csv.DictReader(open(price_path, encoding="utf-8-sig")):
        if r["단지명"] in DEEP15 and r["거래회전율_%"]:
            turnover[r["단지명"]] = turnover.get(r["단지명"], 0.0) + float(r["거래회전율_%"])

    today = date.today().isoformat()
    listing_rows = [r for r in csv.DictReader(
        open(os.path.join(d, "아실_매물스냅샷.csv"), encoding="utf-8-sig"))
        if r["거래유형"] == "매매" and r["수집일"] == today]
    if not listing_rows:
        print(f"[경고] 아실 매물스냅샷에 오늘({today}) 데이터 없음 — fetch_asil.py 먼저 실행 권장")

    listing_by_name = {norm(r["아실단지명"]): r for r in listing_rows}

    out = []
    for name in DEEP15:
        asil_name = RTMS_TO_ASIL.get(name, name)
        l = listing_by_name.get(norm(asil_name))
        out.append({
            "단지명": name, "세대수": l["세대수"] if l else "",
            "연회전율_%": round(turnover.get(name, 0), 1) if name in turnover else "",
            "매물비율_%": l["매물비율_%"] if l else "",
            "매물10일증감_%": l["증감률_%"] if l else "",
        })

    out_path = os.path.join(d, f"심층15_통합_{tag}.csv")
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    miss = [r["단지명"] for r in out if not r["세대수"]]
    print(f"완료: {len(out)}개 단지 → {out_path}")
    if miss:
        print(f"매물 데이터 미확보 {len(miss)}건: {', '.join(miss)}")
    for r in sorted(out, key=lambda x: -(x["연회전율_%"] if x["연회전율_%"] != "" else -1)):
        print(f"  {r['단지명']:20s} 세대수 {r['세대수'] or '-':>6} "
              f"회전율 {r['연회전율_%'] or '-':>5}%  매물비율 {r['매물비율_%'] or '-':>6}%  "
              f"10일증감 {r['매물10일증감_%'] or '-':>6}%")


if __name__ == "__main__":
    run()
