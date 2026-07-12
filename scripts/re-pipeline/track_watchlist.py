# -*- coding: utf-8 -*-
"""워치리스트(심층단지 + 공구별 대장단지) 주간 스냅샷 생성.

실거래_매매.csv + 아실_매물스냅샷.csv를 워치리스트 단지 기준으로 추려
워치리스트_주간스냅샷.csv에 이번 주 행을 append하고,
전주 대비 변동을 계산해 트래커\\YYMMDD_주간트래커.md를 생성한다.

원칙: 매칭 실패·데이터 없음은 공란("")으로 남기고 추정치로 채우지 않는다.
"""
import csv
import os
import sys
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from common import load_config
from fetch_asil import RTMS_TO_ASIL

# 공구는 IFEZ 자료 기반 best-effort 매핑 — 확인 안 된 공구는 "확인필요"로 표기.
# (심층단지는 별도 명시하고 공구는 참고용으로만 붙인다)
WATCHLIST = {
    "송도더샵퍼스트파크F13-1BL": "6·8공구(랜드마크시티) — 심층",
    "송도더샵퍼스트파크F14BL": "6·8공구(랜드마크시티) — 심층",
    "송도더샵퍼스트파크F15BL": "6·8공구(랜드마크시티) — 심층",
    "송도글로벌파크베르디움": "5·7공구(스마트밸리/바이오) — 심층",
    "송도더샵센트럴시티": "1·3공구(IBD) — 심층",
    "랜드마크시티센트럴더샵": "6·8공구(랜드마크시티) — 대장",
    "송도풍림아이원1단지": "2공구(최초개발지) — 대장",
    "더샵그린스퀘어": "4공구(확인필요) — 대장 후보",
}


ALERT_RATIO_REL_PCT = 20.0   # 매물비율 전주 대비 상대변화 임계값(%) — 초안, 데이터 쌓이면 재검증
ALERT_PRICE_REL_PCT = 3.0    # 최근거래1 금액 전주 대비 상대변화 임계값(%) — 초안


def latest_deals(rows, aptnm, n=3):
    sub = [r for r in rows if r["aptNm"] == aptnm]
    for r in sub:
        r["_ymd"] = f"{r['dealYear']}-{int(r['dealMonth']):02d}-{int(r['dealDay']):02d}"
    sub.sort(key=lambda r: r["_ymd"], reverse=True)
    return sub[:n]


def prev_week_rows(wl_path, today):
    """워치리스트_주간스냅샷.csv에서 오늘 이전 가장 최근 수집일의 단지별 행을 반환."""
    if not os.path.exists(wl_path):
        return {}
    with open(wl_path, encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f) if r["수집일"] != today]
    if not rows:
        return {}
    prev_date = max(r["수집일"] for r in rows)
    return {r["단지명"]: r for r in rows if r["수집일"] == prev_date}


def _to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def compare_to_prev(row, prev):
    """(해석문장, 이상징후여부, 이상징후사유) 반환. prev 없으면 첫 주 처리."""
    if prev is None:
        return "비교 기준 없음(첫 주)", False, ""

    cur_ratio = _to_float(row.get("매물비율_%"))
    prev_ratio = _to_float(prev.get("매물비율_%"))
    cur_delta = _to_float(row.get("증감률_%"))
    prev_delta = _to_float(prev.get("증감률_%"))
    cur_price = _to_float(row.get("최근거래1_금액만원"))
    prev_price = _to_float(prev.get("최근거래1_금액만원"))

    parts = []
    alert = False
    alert_reasons = []

    if cur_ratio is not None and prev_ratio is not None:
        ratio_diff = cur_ratio - prev_ratio
        parts.append(f"매물비율 {prev_ratio}%→{cur_ratio}%({ratio_diff:+.2f}%p)")
        if prev_ratio > 0 and abs(ratio_diff) / prev_ratio * 100 >= ALERT_RATIO_REL_PCT:
            alert = True
            alert_reasons.append(f"매물비율 전주 대비 {ratio_diff:+.2f}%p 급변")

        if cur_delta is not None and prev_delta is not None:
            if ratio_diff < 0 and cur_delta <= prev_delta:
                parts.append("→ 매수세 강화(매물 소진 가속)")
            elif ratio_diff > 0:
                parts.append("→ 매물 적체(관망 심리 확산)")
            else:
                parts.append("→ 뚜렷한 변화 없음")
    else:
        parts.append("매물비율 비교 불가(데이터 없음)")

    if cur_price is not None and prev_price is not None and prev_price > 0:
        price_pct = (cur_price - prev_price) / prev_price * 100
        parts.append(f"최근거래가 {prev_price:,.0f}→{cur_price:,.0f}만원({price_pct:+.1f}%)")
        if abs(price_pct) >= ALERT_PRICE_REL_PCT:
            alert = True
            alert_reasons.append(f"최근거래가 전주 대비 {price_pct:+.1f}% 변동")

    return " ".join(parts), alert, "; ".join(alert_reasons)


def main():
    cfg = load_config()
    data_dir = cfg["re_data"]
    real_estate = cfg["real_estate"]

    with open(os.path.join(data_dir, "실거래_매매.csv"), encoding="utf-8") as f:
        deals = list(csv.DictReader(f))

    snap_path = os.path.join(data_dir, "아실_매물스냅샷.csv")
    snap_by_name = {}
    if os.path.exists(snap_path):
        with open(snap_path, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                snap_by_name.setdefault(r["아실단지명"], []).append(r)

    today = date.today().isoformat()
    wl_path = os.path.join(data_dir, "워치리스트_주간스냅샷.csv")
    prev_rows = prev_week_rows(wl_path, today)

    out_rows = []
    body_lines = []
    alert_lines = []

    for aptnm, tag in WATCHLIST.items():
        asil_name = RTMS_TO_ASIL.get(aptnm, aptnm)
        snaps = snap_by_name.get(asil_name, [])
        maemae_snaps = [s for s in snaps if s["거래유형"] == "매매"]
        maemae_snaps.sort(key=lambda r: r["수집일"], reverse=True)
        latest_snap = maemae_snaps[0] if maemae_snaps else None

        row = {
            "수집일": today,
            "단지명": aptnm,
            "구분": tag,
            "매물수_현재": latest_snap["매물수_현재"] if latest_snap else "",
            "매물비율_%": latest_snap["매물비율_%"] if latest_snap else "",
            "증감률_%": latest_snap["증감률_%"] if latest_snap else "",
        }
        recent = latest_deals(deals, aptnm)
        for i, r in enumerate(recent, 1):
            row[f"최근거래{i}_일자"] = r["_ymd"]
            row[f"최근거래{i}_금액만원"] = r["dealAmount"].replace(",", "").strip()
        out_rows.append(row)

        prev = prev_rows.get(aptnm)
        comparison, is_alert, alert_reason = compare_to_prev(row, prev)
        if is_alert:
            alert_lines.append(f"- **{aptnm}**({tag}): {alert_reason}")

        body_lines.append(f"## {aptnm} ({tag})")
        if latest_snap:
            body_lines.append(
                f"- 매물수 {latest_snap['매물수_현재']}건, 매물비율 "
                f"{latest_snap['매물비율_%'] or '미확보'}%, 10일 증감 {latest_snap['증감률_%']}%"
            )
        else:
            body_lines.append("- 아실 매물 스냅샷 미확보 (단지명 매칭 실패 가능성 — 확인 필요)")
        body_lines.append(f"- 전주 대비: {comparison}")
        if recent:
            body_lines.append("- 최근 실거래:")
            for r in recent:
                amt = r["dealAmount"].replace(",", "").strip()
                body_lines.append(f"  - {r['_ymd']} {r['floor']}층 {int(amt):,}만원")
        else:
            body_lines.append("- 최근 실거래 없음")
        body_lines.append("")

    report_lines = [f"# {today} 주간 트래커\n"]
    if alert_lines:
        report_lines.append("## ⚠ 이상징후\n")
        report_lines.extend(alert_lines)
        report_lines.append("")
    report_lines.extend(body_lines)

    fields = ["수집일", "단지명", "구분", "매물수_현재", "매물비율_%", "증감률_%"] + [
        f"최근거래{i}_{k}" for i in (1, 2, 3) for k in ("일자", "금액만원")
    ]
    wl_path = os.path.join(data_dir, "워치리스트_주간스냅샷.csv")
    old = []
    if os.path.exists(wl_path):
        with open(wl_path, encoding="utf-8-sig") as f:
            old = [r for r in csv.DictReader(f) if r["수집일"] != today]
    with open(wl_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(old + out_rows)
    print(f"워치리스트 스냅샷: {len(out_rows)}개 단지 → {wl_path}")

    tracker_dir = os.path.join(real_estate, "트래커")
    os.makedirs(tracker_dir, exist_ok=True)
    ymmdd = date.today().strftime("%y%m%d")
    report_path = os.path.join(tracker_dir, f"{ymmdd}_주간트래커.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"주간 리포트 → {report_path}")


if __name__ == "__main__":
    main()
