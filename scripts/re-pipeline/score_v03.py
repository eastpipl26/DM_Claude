# -*- coding: utf-8 -*-
r"""매매시그널 종합 점수화 v0.3 — 심층 15개 단지 GO/WAIT/NO 순위.

사용법:
  python score_v03.py

전제: calc_metrics.py, join_deep15.py를 먼저 실행해 최신 CSV를 만들어둘 것.

방법론 (기준서 v0.3 대응):
- 5개 요소를 심층15 내에서 min-max 정규화(0~100) 후 가중합
- 가격모멘텀(고점대비, 낮을수록 좋음) 30%, 매물비율(낮을수록 좋음) 20%,
  매물10일증감(더 많이 감소할수록 좋음) 20%, 회전율(높을수록 좋음) 15%,
  전세가율(높을수록 좋음) 15%
- 가중치 근거는 사이클1~4에서 실제로 신호가 된 요소 순 (고점대비·매물동향이
  가장 먼저 방향을 보여줬음) — 초안이며 사이클마다 회고로 조정 예정
- 표본부족 요소가 있는 단지는 그 요소를 심층15 평균으로 대체하고 표시(⚠️대체)
- 결과 = GO(70점+) / WAIT(40~70) / NO(40 미만) — 임계값도 초안, 사이클 누적 후 보정

원칙: 여기 숫자는 전부 CSV 원본에서 계산. 가중치·임계값은 방법론이며 정량 데이터가 아님 — 리포트에 이 구분을 명시할 것.
"""
import csv
import os
import sys
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from common import load_config

WEIGHTS = {"가격모멘텀": 0.30, "매물비율": 0.20, "매물증감": 0.20,
           "회전율": 0.15, "전세가율": 0.15}


def load_price_agg(data_dir, tag, deep15):
    """단지별 평형대 가중평균 (거래건수 가중치) — 고점대비·전년대비·전세가율."""
    from collections import defaultdict
    buckets = defaultdict(list)
    path = os.path.join(data_dir, f"단지비교_{tag}.csv")
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        if r["단지명"] not in deep15:
            continue
        buckets[r["단지명"]].append(r)

    agg = {}
    for name, rows in buckets.items():
        def wavg(field):
            num = den = 0.0
            for r in rows:
                w = float(r["최근6개월_거래건수"] or 0)
                v = r.get(field)
                if v in (None, "", "표본부족"):
                    continue
                num += float(v) * w
                den += w
            return num / den if den else None
        agg[name] = {"고점대비": wavg("고점대비_%"), "전년대비": wavg("전년대비_%"),
                     "전세가율": wavg("전세가율_%")}
    return agg


def load_supply(data_dir, tag):
    path = os.path.join(data_dir, f"심층15_통합_{tag}.csv")
    out = {}
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        out[r["단지명"]] = {
            "매물비율": float(r["매물비율_%"]) if r["매물비율_%"] else None,
            "매물증감": float(r["매물10일증감_%"]) if r["매물10일증감_%"] else None,
            "회전율": float(r["연회전율_%"]) if r["연회전율_%"] else None,
        }
    return out


def normalize(values, invert=False):
    """min-max → 0~100. invert=True면 값이 작을수록 100."""
    vals = [v for v in values.values() if v is not None]
    if not vals or max(vals) == min(vals):
        return {k: 50.0 for k in values}
    lo, hi = min(vals), max(vals)
    out = {}
    for k, v in values.items():
        if v is None:
            out[k] = None
            continue
        s = (v - lo) / (hi - lo) * 100
        out[k] = 100 - s if invert else s
    return out


def run():
    cfg = load_config()
    data_dir = cfg["re_data"]
    tag = date.today().strftime("%y%m%d")

    deep15 = ["송도더샵센트럴시티", "e편한세상송도", "더샵송도마리나베이", "베르디움더퍼스트",
              "송도SKVIEW", "랜드마크시티센트럴더샵", "송도에듀포레푸르지오",
              "송도글로벌파크베르디움", "송도오션파크베르디움", "송도더샵퍼스트파크F14BL",
              "글로벌캠퍼스푸르지오", "더샵그린스퀘어", "송도더샵퍼스트파크F15BL",
              "송도아메리칸타운아이파크", "송도더샵파크애비뉴"]

    price = load_price_agg(data_dir, tag, deep15)
    supply = load_supply(data_dir, tag)

    raw = {"가격모멘텀": {}, "전세가율": {}, "매물비율": {}, "매물증감": {}, "회전율": {}}
    for n in deep15:
        raw["가격모멘텀"][n] = price.get(n, {}).get("고점대비")
        raw["전세가율"][n] = price.get(n, {}).get("전세가율")
        raw["매물비율"][n] = supply.get(n, {}).get("매물비율")
        raw["매물증감"][n] = supply.get(n, {}).get("매물증감")
        raw["회전율"][n] = supply.get(n, {}).get("회전율")

    norm = {
        "가격모멘텀": normalize(raw["가격모멘텀"], invert=True),   # 낮을수록 좋음
        "매물비율": normalize(raw["매물비율"], invert=True),       # 낮을수록 좋음
        "매물증감": normalize(raw["매물증감"], invert=True),       # 더 감소할수록 좋음(음수가 큰 게 좋음 → invert)
        "회전율": normalize(raw["회전율"], invert=False),          # 높을수록 좋음
        "전세가율": normalize(raw["전세가율"], invert=False),      # 높을수록 좋음
    }

    results = []
    for n in deep15:
        score, used_weight, missing = 0.0, 0.0, []
        for factor, w in WEIGHTS.items():
            v = norm[factor].get(n)
            if v is None:
                missing.append(factor)
                continue
            score += v * w
            used_weight += w
        final = score / used_weight * sum(WEIGHTS.values()) if used_weight else 0
        label = "GO" if final >= 70 else ("WAIT" if final >= 40 else "NO")
        results.append({"단지명": n, "점수": round(final, 1), "판정": label,
                        "결측요소": ",".join(missing) if missing else ""})

    results.sort(key=lambda x: -x["점수"])
    out_path = os.path.join(data_dir, f"종합점수_{tag}.csv")
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["단지명", "점수", "판정", "결측요소"])
        w.writeheader()
        w.writerows(results)

    print(f"종합점수 산출 완료 → {out_path}\n")
    print(f"{'순위':>3} {'단지명':22s} {'점수':>6} {'판정':4} {'결측요소'}")
    for i, r in enumerate(results, 1):
        print(f"{i:3d} {r['단지명']:22s} {r['점수']:6.1f} {r['판정']:4s} {r['결측요소']}")


if __name__ == "__main__":
    run()
