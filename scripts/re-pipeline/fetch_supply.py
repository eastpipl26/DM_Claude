# -*- coding: utf-8 -*-
r"""아실(asil.kr) 미분양·입주물량 수집 — 기준서 B수급 요소.

사용법:
  python fetch_supply.py            # 인천·연수구 미분양(월별) + 연수구 입주물량(연도별)

수집물 (re_data 폴더, 매 실행 전체 갱신):
- 미분양_월별.csv   : 인천(28)·연수구(28185) 월별 미분양 세대수 (2015-01~)
- 입주물량_연도별.csv : 연수구 연도별 입주(예정) 물량 + 적정수요 기준선

원칙: 수집 실패 시 추정치로 채우지 않고 에러 종료 (기준서 신뢰성 원칙 3).
비고: Referer 헤더 필수. 미분양 V1=세대수, 입주물량 V1=세대수·line=적정수요.
"""
import csv
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from common import load_config

BASE = "https://asil.kr"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
AREAS_UNSOLD = [("28", "인천"), ("28185", "연수구")]
AREA_SUPPLY = ("28185", "연수구")


def http_get(path, referer):
    req = urllib.request.Request(BASE + path, headers={
        "User-Agent": UA, "Referer": BASE + referer})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_unsold(area):
    """월별 미분양 (XML: <Date>YYYY/M</Date><V1>세대수</V1>)."""
    today = date.today()
    path = (f"/app/data/data_unsoldapt.jsp?t={int(time.time()*1000)}"
            f"&area={area}&sdate=201501&edate={today:%Y%m}")
    txt = http_get(path, f"/app/unsoldapt.jsp?os=pc&area={area}")
    rows = []
    for item in ET.fromstring(txt).findall(".//item"):
        y, m = item.findtext("Date").split("/")
        rows.append({"연월": f"{y}-{int(m):02d}", "미분양": int(item.findtext("V1"))})
    return rows


def fetch_supply(area):
    """연도별 입주물량 (JS: chartData[i]={"Date":"YYYY",V1:"세대수"}; line=적정수요)."""
    path = (f"/rts_m/chart/data_household.jsp?t={int(time.time()*1000)}"
            f"&area={area}&mode=2&sY=2015&sM=1&eY=2030&eM=12")
    txt = http_get(path, f"/app/household_rts.jsp?os=pc&area={area}")
    rows = []
    for m in re.finditer(r'chartData\[\d+\]\s*=\s*(\{[^}]+\})', txt):
        # V1 키가 따옴표 없이 오므로 보정 후 파싱
        d = json.loads(re.sub(r'([,{])\s*V1\s*:', r'\1"V1":', m.group(1)))
        rows.append({"연도": d["Date"], "입주물량": int(d["V1"])})
    demand = re.search(r'line\s*=\s*(\d+)', txt)
    return rows, (int(demand.group(1)) if demand else "")


def main():
    data_dir = load_config()["re_data"]

    # 1) 미분양 (인천 + 연수구)
    unsold = []
    for area, name in AREAS_UNSOLD:
        rows = fetch_unsold(area)
        if not rows:
            raise RuntimeError(f"미분양({name}) 0건 — 엔드포인트 구조 변경 의심")
        for r in rows:
            r["지역"] = name
        unsold.extend(rows)
        print(f"미분양({name}): {len(rows)}개월 ({rows[0]['연월']}~{rows[-1]['연월']})")
        time.sleep(1)
    path = os.path.join(data_dir, "미분양_월별.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["지역", "연월", "미분양"])
        w.writeheader()
        w.writerows(unsold)
    print(f"저장 → {path}")

    # 2) 입주물량 (연수구, 미래 예정 포함)
    area, name = AREA_SUPPLY
    supply, demand = fetch_supply(area)
    if not supply:
        raise RuntimeError("입주물량 0건 — 엔드포인트 구조 변경 의심")
    for r in supply:
        r["지역"] = name
        r["적정수요"] = demand
    path = os.path.join(data_dir, "입주물량_연도별.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["지역", "연도", "입주물량", "적정수요"])
        w.writeheader()
        w.writerows(supply)
    print(f"입주물량({name}): {supply[0]['연도']}~{supply[-1]['연도']}, "
          f"적정수요 {demand}세대/년 → {path}")
    for r in supply:
        if int(r["연도"]) >= date.today().year:
            flag = "⚠️초과" if demand and r["입주물량"] > demand else ""
            print(f"  {r['연도']}: {r['입주물량']:,}세대 {flag}")


if __name__ == "__main__":
    main()
