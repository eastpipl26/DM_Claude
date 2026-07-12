# -*- coding: utf-8 -*-
"""단지별 매매시그널 지표 계산.

사용법:
  python calc_metrics.py            # 지표 계산 → 단지비교_YYMMDD.csv + 콘솔 마크다운 요약
  python calc_metrics.py --master   # 단지마스터.csv 골격 생성/갱신만

지표 (단지 × 평형대 기준):
- 최근 6개월 중위 평당가(전용평 기준, 만원) / 거래건수
- 고점(분기 중위 평당가 최고) 대비 현재 위치 %
- 전년 동기(12~18개월 전) 대비 변동 %
- 전세가율: 최근 6개월 순수전세(월세 0) 중위 ㎡당 보증금 ÷ 매매 중위 ㎡당가
- 최근 12개월 거래회전율: 거래건수 ÷ 세대수 (단지마스터에 세대수 있을 때만)

원칙: 취소(cdealType=O)건 제외. 표본 3건 미만 구간은 "표본부족" 표기 (추정 금지).
"""
import argparse
import csv
import os
import statistics
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from collections import defaultdict
from datetime import date

from common import load_config

PYEONG = 3.3058  # ㎡ → 평

BUCKETS = [(0, 60, "~59㎡(소형)"), (60, 85, "60~84㎡(중소형)"),
           (85, 115, "85~114㎡(중형)"), (115, 9999, "115㎡~(대형)")]


def bucket(ar):
    for lo, hi, name in BUCKETS:
        if lo <= ar < hi:
            return name
    return "?"


def ym_int(y, m):
    return int(y) * 12 + int(m)


def load_trades(data_dir):
    rows = []
    path = os.path.join(data_dir, "실거래_매매.csv")
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r.get("cdealType", "").strip() == "O":  # 해제건 제외
                continue
            try:
                ar = float(r["excluUseAr"])
                amt = float(r["dealAmount"].replace(",", ""))
            except (ValueError, KeyError):
                continue
            rows.append({"apt": r["aptNm"].strip(), "ar": ar, "amt": amt,
                         "ymi": ym_int(r["dealYear"], r["dealMonth"]),
                         "build": r.get("buildYear", "")})
    return rows


def load_rents(data_dir):
    rows = []
    path = os.path.join(data_dir, "실거래_전월세.csv")
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            try:
                ar = float(r["excluUseAr"])
                dep = float(r["deposit"].replace(",", ""))
                mr = float((r["monthlyRent"] or "0").replace(",", ""))
            except (ValueError, KeyError):
                continue
            if mr > 0:  # 순수 전세만
                continue
            rows.append({"apt": r["aptNm"].strip(), "ar": ar, "dep": dep,
                         "ymi": ym_int(r["dealYear"], r["dealMonth"])})
    return rows


def load_master(data_dir):
    path = os.path.join(data_dir, "단지마스터.csv")
    master = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                master[r["단지명"].strip()] = r
    return master


def build_master(data_dir):
    """매매 CSV에서 단지 목록 추출 → 단지마스터.csv 골격 생성 (기존 입력값 보존)."""
    trades = load_trades(data_dir)
    existing = load_master(data_dir)
    apts = {}
    for t in trades:
        info = apts.setdefault(t["apt"], {"build": t["build"], "n": 0})
        info["n"] += 1
    path = os.path.join(data_dir, "단지마스터.csv")
    fields = ["단지명", "준공년", "누적거래건수", "세대수", "역거리_도보분",
              "초등학군", "비고", "출처URL"]
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for apt in sorted(apts):
            old = existing.get(apt, {})
            w.writerow({
                "단지명": apt, "준공년": apts[apt]["build"],
                "누적거래건수": apts[apt]["n"],
                "세대수": old.get("세대수", ""),
                "역거리_도보분": old.get("역거리_도보분", ""),
                "초등학군": old.get("초등학군", ""),
                "비고": old.get("비고", ""), "출처URL": old.get("출처URL", "")})
    print(f"단지마스터 갱신: {len(apts)}개 단지 → {path}")


def med_ppp(rows):
    """평당가(만원/전용평) 중위값."""
    return statistics.median(r["amt"] / (r["ar"] / PYEONG) for r in rows)


def calc(data_dir):
    trades = load_trades(data_dir)
    rents = load_rents(data_dir)
    master = load_master(data_dir)
    now = ym_int(date.today().year, date.today().month)

    groups = defaultdict(list)
    for t in trades:
        groups[(t["apt"], bucket(t["ar"]))].append(t)
    rent_groups = defaultdict(list)
    for r in rents:
        rent_groups[(r["apt"], bucket(r["ar"]))].append(r)

    out = []
    for (apt, bk), rows in sorted(groups.items()):
        recent6 = [r for r in rows if now - r["ymi"] < 6]
        recent12 = [r for r in rows if now - r["ymi"] < 12]
        yoy_base = [r for r in rows if 12 <= now - r["ymi"] < 18]

        rec = {"단지명": apt, "평형대": bk, "준공년": rows[0]["build"],
               "최근6개월_거래건수": len(recent6),
               "최근12개월_거래건수": len(recent12)}

        if len(recent6) >= 3:
            cur = med_ppp(recent6)
            rec["최근6개월_중위평당가_만원"] = round(cur)
            # 고점: 분기(3개월) 중위 평당가의 최대 (표본 3건 이상 분기만)
            q = defaultdict(list)
            for r in rows:
                q[r["ymi"] // 3].append(r)
            peaks = [med_ppp(v) for v in q.values() if len(v) >= 3]
            if peaks:
                peak = max(peaks)
                rec["고점_중위평당가_만원"] = round(peak)
                rec["고점대비_%"] = round(cur / peak * 100, 1)
            if len(yoy_base) >= 3:
                rec["전년대비_%"] = round((cur / med_ppp(yoy_base) - 1) * 100, 1)
        else:
            rec["최근6개월_중위평당가_만원"] = "표본부족"

        r6 = [r for r in rent_groups.get((apt, bk), []) if now - r["ymi"] < 6]
        if len(r6) >= 3 and len(recent6) >= 3:
            jeonse_sqm = statistics.median(r["dep"] / r["ar"] for r in r6)
            trade_sqm = statistics.median(r["amt"] / r["ar"] for r in recent6)
            rec["전세가율_%"] = round(jeonse_sqm / trade_sqm * 100, 1)
        else:
            rec["전세가율_%"] = "표본부족"

        m = master.get(apt, {})
        if m.get("세대수"):
            try:
                rec["거래회전율_%"] = round(len(recent12) / float(m["세대수"]) * 100, 1)
            except ValueError:
                pass
        out.append(rec)

    fields = ["단지명", "평형대", "준공년", "최근6개월_거래건수", "최근12개월_거래건수",
              "최근6개월_중위평당가_만원", "고점_중위평당가_만원", "고점대비_%",
              "전년대비_%", "전세가율_%", "거래회전율_%"]
    tag = date.today().strftime("%y%m%d")
    path = os.path.join(data_dir, f"단지비교_{tag}.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)
    print(f"지표 계산 완료: {len(out)}개 (단지×평형대) → {path}")

    # 심층 후보: 최근 12개월 거래 10건 이상, 표본 충분 구간을 평당가 순 출력
    deep = [r for r in out if r["최근12개월_거래건수"] >= 10
            and isinstance(r["최근6개월_중위평당가_만원"], int)]
    deep.sort(key=lambda r: -r["최근6개월_중위평당가_만원"])
    print(f"\n심층 분석 후보 (12개월 거래 10건+): {len(deep)}개 구간")
    for r in deep[:20]:
        print(f"  {r['단지명']} {r['평형대']}: 평당 {r['최근6개월_중위평당가_만원']}만, "
              f"고점대비 {r.get('고점대비_%', '-')}%, 전세가율 {r['전세가율_%']}")

    # 판정 분포 자동 집계 — 리포트는 반드시 이 수치를 그대로 사용할 것
    # (에이전트가 표를 눈으로 세다 집계 오류 낸 사이클 1 사고 재발 방지)
    def dist(rows, label):
        g = y = r_ = s = 0
        for x in rows:
            p = x.get("고점대비_%")
            if not isinstance(x["최근6개월_중위평당가_만원"], int) or p is None:
                s += 1
            elif p < 85:
                g += 1
            elif p < 95:
                y += 1
            else:
                r_ += 1
        total = len(rows)
        print(f"  {label}: 총 {total}개 라인 — 🟢<85%: {g} / 🟡85~95%: {y} / "
              f"🔴95%+: {r_} / 표본부족·고점없음: {s}")

    print("\n판정 분포 (고점대비, 자동 집계):")
    dist(out, "전체")
    dist(deep, "심층 후보")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", action="store_true", help="단지마스터 골격 생성만")
    args = ap.parse_args()
    cfg = load_config()
    if args.master:
        build_master(cfg["re_data"])
    else:
        calc(cfg["re_data"])
