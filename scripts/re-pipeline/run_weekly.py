# -*- coding: utf-8 -*-
"""주간 트래커 오케스트레이터 — 실거래 증분수집 → 세대수 갱신 → 아실 매물 → 워치리스트 리포트.

사용법: python run_weekly.py
(Windows 작업 스케줄러에 이 스크립트를 매주 1회 등록해서 사용)

각 단계는 독립 실패해도 다음 단계를 계속 진행한다(예: K-apt 게이트웨이 지연).
단, fetch_rtms.py·fetch_asil.py 실패는 그대로 로그에 남기고 워치리스트는
있는 데이터로만 생성한다(추정치로 채우지 않는다는 원칙 유지).
"""
import subprocess
import sys
from datetime import datetime

STEPS = [
    ("실거래 증분 수집", ["fetch_rtms.py"]),
    ("K-apt 세대수 갱신", ["fetch_kapt.py"]),
    ("아실 매물 수집", ["fetch_asil.py"]),
    ("워치리스트 리포트 생성", ["track_watchlist.py"]),
    ("대시보드 생성", ["build_dashboard.py"]),
]


def main():
    print(f"=== 주간 트래커 실행 시작: {datetime.now().isoformat(timespec='seconds')} ===")
    for name, args in STEPS:
        print(f"\n--- {name} ({args[0]}) ---")
        result = subprocess.run([sys.executable] + args, cwd=__file__.rsplit("\\", 1)[0])
        if result.returncode != 0:
            print(f"[경고] {name} 실패(exit {result.returncode}) — 다음 단계로 계속 진행")
    print(f"\n=== 주간 트래커 실행 종료: {datetime.now().isoformat(timespec='seconds')} ===")


if __name__ == "__main__":
    main()
