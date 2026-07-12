# -*- coding: utf-8 -*-
r"""K-apt 공동주택 API로 단지마스터 세대수 채우기.

사용법:
  python fetch_kapt.py            # 단지목록 수집 + 세대수 조회 + 단지마스터 매칭
  python fetch_kapt.py --list     # 단지목록 수집만 (기본정보 API 미승인 시)

- 단지목록: AptListService3 (승인 확인됨, JSON)
- 세대수: AptBasisInfoServiceV4 getAphusBassInfoV4 → kaptdaCnt
- 중간 산출물: {re_data}\kapt단지목록.csv
- 최종: 단지마스터.csv의 세대수·출처URL 채움 (기존 수기 입력값 보존)
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from common import load_config, get_api_key

SIGUNGU = "28185"  # 인천 연수구
UMD = "송도동"
LIST_URL = "https://apis.data.go.kr/1613000/AptListService3/getSigunguAptList3"
BASIS_URL = "https://apis.data.go.kr/1613000/AptBasisInfoServiceV4/getAphusBassInfoV4"


def api_json(url, params):
    q = urllib.parse.urlencode(params, safe="=%+/")
    try:
        with urllib.request.urlopen(f"{url}?{q}", timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            raise RuntimeError("게이트웨이 거부: 403 (활용신청 반영 대기)") from e
        raise
    if body.strip() in ("Forbidden", "Unexpected errors"):
        raise RuntimeError(f"게이트웨이 거부: {body.strip()} (활용신청/반영 대기 확인)")
    return json.loads(body)


def fetch_list(key):
    """연수구 전체 단지목록 → 송도동 필터."""
    rows, page = [], 1
    while True:
        data = api_json(LIST_URL, {"serviceKey": key, "sigunguCode": SIGUNGU,
                                   "pageNo": str(page), "numOfRows": "100"})
        body = data["response"]["body"]
        for it in body["items"]:
            if it.get("as3") == UMD:
                rows.append({"kaptCode": it["kaptCode"], "kaptName": it["kaptName"],
                             "bjdCode": it["bjdCode"]})
        if page * 100 >= body["totalCount"]:
            break
        page += 1
        time.sleep(0.1)
    return rows


def fetch_basis(key, kapt_code):
    """단지 기본정보 → 세대수 등."""
    data = api_json(BASIS_URL, {"serviceKey": key, "kaptCode": kapt_code})
    item = data["response"]["body"]["item"]
    return {"세대수": item.get("kaptdaCnt", ""), "동수": item.get("kaptDongCnt", ""),
            "사용승인일": item.get("kaptUsedate", "")}


def norm(name):
    """단지명 정규화: 공백·괄호·특수문자 제거, 블록 표기 통일."""
    s = re.sub(r"[\s()\[\]·.-]", "", name)
    s = s.replace("블록", "BL").replace("블럭", "BL")
    s = re.sub(r"아파트$", "", s)
    return s.upper()


def run(list_only):
    cfg = load_config()
    key = get_api_key()
    if not key:
        print("[중단] API 키 없음 (secrets\\molit.env)")
        sys.exit(1)
    data_dir = cfg["re_data"]

    # 1. 단지목록
    apts = fetch_list(key)
    list_path = os.path.join(data_dir, "kapt단지목록.csv")
    with open(list_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["kaptCode", "kaptName", "bjdCode"])
        w.writeheader()
        w.writerows(apts)
    print(f"[목록] {UMD} {len(apts)}개 단지 → {list_path}")
    if list_only:
        return

    # 2. 세대수 조회
    for a in apts:
        try:
            a.update(fetch_basis(key, a["kaptCode"]))
        except Exception as e:
            print(f"  {a['kaptName']}: 기본정보 실패 — {e}")
            if "게이트웨이 거부" in str(e):
                print("[중단] 기본정보 API 미승인 상태. 승인 후 재실행.")
                sys.exit(1)
        time.sleep(0.1)

    # 3. 단지마스터 매칭 (기존 수기 입력값 보존)
    master_path = os.path.join(data_dir, "단지마스터.csv")
    with open(master_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        master = list(reader)

    kapt_by_norm = {norm(a["kaptName"]): a for a in apts}
    matched = 0
    for m in master:
        if m.get("세대수"):  # 수기 입력 보존
            continue
        n = norm(m["단지명"])
        hit = kapt_by_norm.get(n)
        if not hit:  # 부분 포함 매칭 (양방향)
            cands = [a for k, a in kapt_by_norm.items() if n in k or k in n]
            hit = cands[0] if len(cands) == 1 else None
        if hit and hit.get("세대수"):
            m["세대수"] = hit["세대수"]
            m["출처URL"] = f"K-apt API kaptCode={hit['kaptCode']}"
            matched += 1

    with open(master_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(master)

    unmatched = [m["단지명"] for m in master if not m.get("세대수")]
    print(f"[매칭] 세대수 채움 {matched}건 / 미매칭 {len(unmatched)}건 → {master_path}")
    if unmatched:
        print("미매칭 목록 (수기 확인 필요):")
        for u in unmatched:
            print(f"  - {u}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="단지목록 수집만")
    args = ap.parse_args()
    run(args.list)
