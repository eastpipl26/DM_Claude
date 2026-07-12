# -*- coding: utf-8 -*-
"""아실(asil.kr) 매물 데이터 수집 — 기준서 B수급 요소.

사용법:
  python fetch_asil.py              # 동 매물추이 + 단지별 스냅샷 수집 (송도동)
  python fetch_asil.py --area 2818510600

수집물 (re_data 폴더):
- 아실_매물추이_동.csv   : 동 단위 일별 매물 수 (매매/전세/월세, 2024-01~) — 전체 갱신
- 아실_매물스냅샷.csv    : 단지별 매물 수 스냅샷 (매매/전세, 수집일 기록) — 누적 append

원칙: 수집 실패 시 그럴듯한 값으로 채우지 않고 에러 종료 (기준서 신뢰성 원칙 3).
비고: 브라우저 XHR 엔드포인트 직접 호출. 과도한 호출 금지 (사이클당 1회, 요청 간 1초 대기).
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.request
from datetime import date, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from common import load_config

BASE = "https://asil.kr"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
DEAL_NAMES = {"1": "매매", "2": "전세"}

# RTMS(국토부) 단지명 → 아실 표기명. 브랜드명이 달라 자동 정규화 매칭이 안 되는 건들.
# 세대수+준공년도(K-apt) 교차검증으로 확정 (2026-07-07, 사이클3).
RTMS_TO_ASIL = {
    "송도글로벌파크베르디움": "송도국제도시호반베르디움(RC-1블럭)",  # 1,153세대·2017년 일치
    "송도오션파크베르디움": "송도국제도시호반베르디움3차",          # 1,530세대·2020년 일치
    "더샵송도마리나베이": "송도센토피아더샵",                      # 3,100세대·2020년 일치
    "송도SKVIEW": "인천송도SK뷰",                                # 2,100세대·2019년 일치
    "송도더샵퍼스트파크F13-1BL": "송도더샵퍼스트파크(F13-1BL)",
    "송도더샵퍼스트파크F14BL": "송도더샵퍼스트파크(F14BL)",
    "송도더샵퍼스트파크F15BL": "송도더샵퍼스트파크(F15BL)",
    "송도더샵센트럴시티": "송도더샵센트럴시티(송도국제도시RM2블록)(주)",
}


def http_get(path, referer):
    req = urllib.request.Request(BASE + path, headers={
        "User-Agent": UA, "Referer": BASE + referer})
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status}: {path}")
        return resp.read()


def fetch_trend(area):
    """동 단위 일별 매물추이 (data_offer_sum.jsp). VM=매매 VJ=전세 VW=월세."""
    today = date.today()
    path = (f"/app/data/data_offer_sum.jsp?t={int(time.time()*1000)}"
            f"&apt=&area={area}&c_apt=&c_area=&c_apt2=&c_area2="
            f"&deal=1&mode=2&sSize=&eSize="
            f"&sY=2024&sM=1&eY={today.year}&eM={today.month}")
    txt = http_get(path, f"/app/offer_sum_chart.jsp?area={area}").decode("utf-8")
    rows = []
    for m in re.finditer(r'listData\[\d+\]=(\{[^}]+\})', txt):
        d = json.loads(m.group(1))
        yy, mm, dd = d["Date"].split("/")
        rows.append({"날짜": f"20{yy}-{mm}-{dd}", "매매": d["VM"],
                     "전세": d["VJ"], "월세": d["VW"]})
    rows.sort(key=lambda r: r["날짜"])
    return rows


def fetch_snapshot(area, deal):
    """단지별 현재 매물 수 (data_deal_count.jsp). total=현재, value=기준일.

    아실의 today 파라미터는 조회일이 아니라 데이터 기준일(보통 어제)이어야
    결과가 반환된다. 어제 기준 0건이면 그제로 한 번 더 시도.
    """
    for back in (1, 2):
        ref = date.today() - timedelta(days=back)
        baseline = ref - timedelta(days=10)
        path = (f"/app/data/data_deal_count.jsp?mode=3&area={area}"
                f"&today={ref:%Y%m%d}&yyyymm={baseline:%Y%m%d}"
                f"&deal={deal}&order=2&daily=true")
        data = json.loads(http_get(
            path, f"/app/deal_count.jsp?os=pc&area={area[:5]}").decode("utf-8"))
        if data:
            break
    rows = []
    for d in data:
        rows.append({
            "수집일": date.today().isoformat(), "거래유형": DEAL_NAMES[deal],
            "아실단지ID": d["apt"], "아실단지명": d["aptname"],
            "naver단지ID": d.get("naverapt", ""),
            "매물수_현재": d["total"], "매물수_기준일": d["value"],
            "기준일": baseline.isoformat(), "증감률_%": d["rate"]})
    return rows


def fetch_households(area):
    """단지 메뉴(data_napt_list_menu.jsp)에서 seq→세대수 맵 (매물비율 분모)."""
    body = http_get(f"/app/data/data_napt_list_menu.jsp?dong={area}",
                    "/app/sub/menu_area_of_offer.jsp").decode("utf-8")
    return {d["seq"]: d.get("household", "") for d in json.loads(body)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--area", default="2818510600", help="법정동 코드 10자리")
    args = ap.parse_args()
    data_dir = load_config()["re_data"]

    # 1) 동 매물추이 — 전체 이력을 매번 새로 받으므로 덮어쓰기
    trend = fetch_trend(args.area)
    if not trend:
        raise RuntimeError("매물추이 파싱 결과 0건 — 엔드포인트 구조 변경 의심")
    trend_path = os.path.join(data_dir, "아실_매물추이_동.csv")
    with open(trend_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["날짜", "매매", "전세", "월세"])
        w.writeheader()
        w.writerows(trend)
    print(f"동 매물추이: {len(trend)}일 ({trend[0]['날짜']}~{trend[-1]['날짜']}) → {trend_path}")

    # 2) 단지별 스냅샷 — 매매·전세 각각, 누적 append (같은 수집일 재실행 시 교체)
    households = fetch_households(args.area)
    snap = []
    for deal in ("1", "2"):
        time.sleep(1)
        rows = fetch_snapshot(args.area, deal)
        if not rows:
            raise RuntimeError(f"단지 스냅샷({DEAL_NAMES[deal]}) 0건 — 구조 변경 의심")
        for r in rows:
            hh = households.get(r["naver단지ID"], "")
            r["세대수"] = hh
            r["매물비율_%"] = (round(int(r["매물수_현재"]) / int(hh) * 100, 2)
                             if hh and int(hh) > 0 else "")
        snap.extend(rows)
        print(f"단지 스냅샷({DEAL_NAMES[deal]}): {len(rows)}개 단지")

    fields = ["수집일", "거래유형", "아실단지ID", "아실단지명", "naver단지ID",
              "세대수", "매물수_현재", "매물수_기준일", "기준일",
              "매물비율_%", "증감률_%"]
    snap_path = os.path.join(data_dir, "아실_매물스냅샷.csv")
    old = []
    if os.path.exists(snap_path):
        with open(snap_path, encoding="utf-8-sig", newline="") as f:
            today = date.today().isoformat()
            old = [r for r in csv.DictReader(f) if r["수집일"] != today]
    with open(snap_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(old + snap)
    print(f"단지 스냅샷 저장: 신규 {len(snap)}행 + 기존 {len(old)}행 → {snap_path}")


if __name__ == "__main__":
    main()
