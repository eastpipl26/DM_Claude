# -*- coding: utf-8 -*-
r"""국토부 실거래가 수집 스크립트 (매매 + 전월세).

사용법:
  python fetch_rtms.py                  # 증분 수집 (최근 3개월 재수집 포함)
  python fetch_rtms.py --full           # 전체 백필 (매매 2006-01~, 전월세 2011-01~)
  python fetch_rtms.py --dataset trade  # 매매만 (trade|rent|all)

- 대상: 연수구(28185) → 송도동 필터
- 저장: {re_data}\실거래_매매.csv / 실거래_전월세.csv (utf-8-sig)
- 상태: {re_data}\_state.json (마지막 수집월)
- 취소(해제)건도 저장하고 cdealType 컬럼으로 표시 — 지표 계산에서 제외
"""
import argparse
import csv
import json
import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

from common import load_config, get_api_key

LAWD_CD = "28185"   # 인천 연수구
UMD_NM = "송도동"

DATASETS = {
    "trade": {
        "url": "http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev",
        "csv": "실거래_매매.csv",
        "start": "200601",
        "fields": ["sggCd", "umdNm", "aptNm", "jibun", "excluUseAr",
                   "dealYear", "dealMonth", "dealDay", "dealAmount", "floor",
                   "buildYear", "aptDong", "cdealType", "cdealDay",
                   "dealingGbn", "rgstDate"],
    },
    "rent": {
        "url": "http://apis.data.go.kr/1613000/RTMSDataSvcAptRent/getRTMSDataSvcAptRent",
        "csv": "실거래_전월세.csv",
        "start": "201101",
        "fields": ["sggCd", "umdNm", "aptNm", "jibun", "excluUseAr",
                   "dealYear", "dealMonth", "dealDay", "deposit", "monthlyRent",
                   "floor", "buildYear", "contractType", "contractTerm"],
    },
}


def month_range(start_ym, end_ym):
    y, m = int(start_ym[:4]), int(start_ym[4:])
    while f"{y:04d}{m:02d}" <= end_ym:
        yield f"{y:04d}{m:02d}"
        m += 1
        if m > 12:
            y, m = y + 1, 1


def minus_months(ym, n):
    y, m = int(ym[:4]), int(ym[4:])
    m -= n
    while m < 1:
        y, m = y - 1, m + 12
    return f"{y:04d}{m:02d}"


def fetch_month(url, key, ym, fields):
    """한 달치 수집 (페이지네이션 포함). 실패 시 예외."""
    rows, page = [], 1
    while True:
        q = urllib.parse.urlencode({
            "serviceKey": key, "LAWD_CD": LAWD_CD, "DEAL_YMD": ym,
            "numOfRows": "1000", "pageNo": str(page)}, safe="=%+/")
        with urllib.request.urlopen(f"{url}?{q}", timeout=30) as resp:
            body = resp.read().decode("utf-8")
        root = ET.fromstring(body)
        code = (root.findtext(".//resultCode") or "").strip()
        if code not in ("00", "000"):
            msg = (root.findtext(".//resultMsg") or "").strip()
            raise RuntimeError(f"{ym} API 오류 resultCode={code} msg={msg}")
        items = root.findall(".//item")
        for it in items:
            if (it.findtext("umdNm") or "").strip() != UMD_NM:
                continue
            rows.append({f: (it.findtext(f) or "").strip() for f in fields})
        total = int(root.findtext(".//totalCount") or "0")
        if page * 1000 >= total:
            break
        page += 1
    return rows


def run(dataset, full):
    cfg = load_config()
    key = get_api_key()
    if not key:
        print("[중단] API 키 없음. C:\\Users\\eastp\\.claude\\secrets\\molit.env 에 "
              "MOLIT_API_KEY=<키> 저장 후 재실행.")
        sys.exit(1)

    data_dir = cfg["re_data"]
    os.makedirs(data_dir, exist_ok=True)
    state_path = os.path.join(data_dir, "_state.json")
    state = {}
    if os.path.exists(state_path):
        with open(state_path, encoding="utf-8") as f:
            state = json.load(f)

    spec = DATASETS[dataset]
    csv_path = os.path.join(data_dir, spec["csv"])
    end_ym = date.today().strftime("%Y%m")

    if full or f"{dataset}_last" not in state:
        start_ym = spec["start"]
    else:
        # 신고 지연·해제 반영 위해 마지막 수집월 포함 3개월 재수집
        start_ym = minus_months(state[f"{dataset}_last"], 2)

    # 기존 CSV 로드 후 재수집 구간 제거 (멱등성)
    existing = []
    if os.path.exists(csv_path) and not full:
        with open(csv_path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                ym = f"{r['dealYear']}{int(r['dealMonth']):02d}"
                if ym < start_ym:
                    existing.append(r)

    print(f"[{dataset}] {start_ym} ~ {end_ym} 수집 시작 (기존 유지 {len(existing)}건)")
    new_rows, fails = [], 0
    for ym in month_range(start_ym, end_ym):
        try:
            got = fetch_month(spec["url"], key, ym, spec["fields"])
            new_rows.extend(got)
            fails = 0
            if got:
                print(f"  {ym}: {len(got)}건")
        except Exception as e:
            fails += 1
            print(f"  {ym}: 실패 — {e}")
            if fails >= 3:
                print("[중단] 3개월 연속 실패. 원인 확인 필요 (키 활성화 대기 중일 수 있음).")
                sys.exit(1)
            time.sleep(2)
            continue
        time.sleep(0.15)

    all_rows = existing + new_rows
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=spec["fields"])
        w.writeheader()
        w.writerows(all_rows)

    state[f"{dataset}_last"] = end_ym
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"[{dataset}] 완료: 신규 {len(new_rows)}건, 총 {len(all_rows)}건 → {csv_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=["trade", "rent", "all"], default="all")
    ap.add_argument("--full", action="store_true", help="전체 백필")
    args = ap.parse_args()
    for ds in (["trade", "rent"] if args.dataset == "all" else [args.dataset]):
        run(ds, args.full)
