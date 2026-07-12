#!/usr/bin/env python3
r"""
build_work_dashboard.py — SK하이닉스 본업 업무 대시보드 생성

원본 데이터(md 표) → HTML 3페이지 렌더링. 표준 라이브러리만 사용.
  - {sk_work}\업무목록.md   → 일일/긴급/추적/일반 업무
  - {sk_work}\공사일정.md   → 마일스톤·마감기한 (건축사시험 등 개인 D-day 포함)
  - {sk_work}\인허가.md     → 인허가 건별 추적
출력: {sk_work}\업무대시보드.html / 업무대시보드_일정.html / 업무대시보드_인허가.html
경로는 전부 config.md에서 읽는다 (하드코딩 금지 규칙).
"""
import datetime
import html
import os
import re
import sys

CONFIG_MD = os.path.join(os.path.expanduser("~"), ".claude", "config.md")


def load_config():
    cfg = {}
    text = open(CONFIG_MD, encoding="utf-8").read()
    for m in re.finditer(r"\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|", text):
        cfg[m.group(1)] = m.group(2)
    # {변수} 치환 (2패스면 중첩 해소됨)
    for _ in range(3):
        for k, v in cfg.items():
            cfg[k] = re.sub(r"\{(\w+)\}", lambda m: cfg.get(m.group(1), m.group(0)), v)
    return cfg


def parse_table(path):
    """md 파일에서 첫 번째 표를 dict 리스트로 파싱."""
    if not os.path.exists(path):
        return [], []
    rows, header = [], []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not header:
            header = cells
            continue
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        row = dict(zip(header, cells + [""] * (len(header) - len(cells))))
        if any(v for v in row.values()):
            rows.append(row)
    return header, rows


def dday(datestr, today):
    """YYYY-MM-DD → (일수, 'D-3' 라벨). 날짜 없으면 (None, '')."""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", datestr or "")
    if not m:
        return None, ""
    d = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    n = (d - today).days
    if n > 0:
        return n, f"D-{n}"
    if n == 0:
        return 0, "D-day"
    return n, f"D+{-n}"


def esc(s):
    return html.escape(s or "")


STYLE = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body{{background:#0f1115;color:#d7dae0;font-family:'Malgun Gothic','Segoe UI',sans-serif;margin:0;padding:20px;max-width:1100px;margin:0 auto}}
.page-header{{background:#15171c;border:1px solid #23262d;border-radius:8px;padding:14px 18px;margin-bottom:16px}}
.header-nav{{display:flex;gap:16px;align-items:center;flex-wrap:wrap}}
.logo{{font-weight:bold;color:#7aa2f7;text-decoration:none;font-size:15px}}
.nav-links a{{color:#9aa0aa;text-decoration:none;margin-right:14px;font-size:13px}}
.nav-links a.active{{color:#e6e9ef;font-weight:bold;border-bottom:2px solid #7aa2f7;padding-bottom:2px}}
h1{{font-size:19px;margin:10px 0 2px}}
.meta{{color:#6b7280;font-size:12px}}
section{{background:#15171c;border:1px solid #23262d;border-radius:8px;padding:16px 18px;margin-bottom:14px}}
h2{{font-size:15px;margin:0 0 10px;color:#e6e9ef}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;color:#9aa0aa;font-weight:normal;border-bottom:1px solid #2a2e37;padding:6px 8px}}
td{{border-bottom:1px solid #1d2027;padding:7px 8px;vertical-align:top}}
tr.done{{opacity:.38}}
.badge{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11.5px;white-space:nowrap}}
.b-urgent{{background:#3b1519;color:#f7768e;border:1px solid #5c2129}}
.b-daily{{background:#16273a;color:#7aa2f7;border:1px solid #234066}}
.b-track{{background:#2b2416;color:#e0af68;border:1px solid #4a3d1f}}
.b-normal{{background:#1e222a;color:#9aa0aa;border:1px solid #2a2e37}}
.b-org{{background:#1a2a22;color:#73daca;border:1px solid #24473a}}
.dd-soon{{color:#f7768e;font-weight:bold}}
.dd-week{{color:#e0af68;font-weight:bold}}
.dd-far{{color:#9aa0aa}}
.dd-over{{color:#f7768e;font-weight:bold;text-decoration:underline}}
.banner{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:14px}}
.dcard{{flex:1;min-width:160px;background:#15171c;border:1px solid #23262d;border-radius:8px;padding:12px 16px}}
.dcard .num{{font-size:22px;font-weight:bold;color:#7aa2f7}}
.dcard .lbl{{font-size:12px;color:#9aa0aa;margin-top:2px}}
.dcard.hot .num{{color:#f7768e}}
.empty{{color:#6b7280;font-size:13px;padding:6px 0}}
.st-done{{color:#73daca}} .st-hold{{color:#6b7280}} .st-delay{{color:#f7768e}}
</style></head><body>
<header class="page-header">
  <div class="header-nav">
    <a class="logo" href="./업무대시보드.html">🏗 업무 대시보드</a>
    <span class="nav-links">
      <a href="./업무대시보드.html" class="{a1}">홈</a>
      <a href="./업무대시보드_일정.html" class="{a2}">공사일정·마감</a>
      <a href="./업무대시보드_인허가.html" class="{a3}">인허가</a>
    </span>
  </div>
  <h1>{h1}</h1>
  <div class="meta">생성: {now} · 원본: 업무목록.md / 공사일정.md / 인허가.md (말숙이에게 말하면 갱신)</div>
</header>
"""

GUBUN_BADGE = {"긴급": "b-urgent", "일일": "b-daily", "추적": "b-track", "일반": "b-normal"}


def dd_class(n):
    if n is None:
        return "dd-far"
    if n < 0:
        return "dd-over"
    if n <= 3:
        return "dd-soon"
    if n <= 7:
        return "dd-week"
    return "dd-far"


def badge(text, cls):
    return f'<span class="badge {cls}">{esc(text)}</span>'


def task_row(t, today):
    n, lbl = dday(t.get("마감일", ""), today)
    done = t.get("상태") in ("완료",)
    cls = ' class="done"' if done else ""
    g = t.get("구분", "일반")
    return (f"<tr{cls}><td>{badge(g, GUBUN_BADGE.get(g, 'b-normal'))}</td>"
            f"<td>{esc(t.get('제목',''))}</td>"
            f"<td>{badge(t.get('대응처','-') or '-', 'b-org')}</td>"
            f"<td><span class=\"{dd_class(n)}\">{esc(t.get('마감일','')) or '-'} {lbl}</span></td>"
            f"<td>{esc(t.get('상태',''))}</td><td>{esc(t.get('메모',''))}</td></tr>")


TASK_HEAD = "<tr><th>구분</th><th>제목</th><th>대응처</th><th>마감</th><th>상태</th><th>메모</th></tr>"


def render_home(tasks, miles, permits, today, now):
    active = [t for t in tasks if t.get("상태") not in ("완료",)]
    urgent = [t for t in active if t.get("구분") == "긴급"]
    daily = [t for t in active if t.get("구분") == "일일"]
    track = [t for t in active if t.get("구분") == "추적"]
    other = [t for t in active if t.get("구분") not in ("긴급", "일일", "추적")]

    # 마감 임박(D-7): 업무 + 일정 + 인허가 통합
    soon = []
    for t in active:
        n, lbl = dday(t.get("마감일", ""), today)
        if n is not None and n <= 7:
            soon.append((n, lbl, "업무", t.get("제목", ""), t.get("대응처", "")))
    for m in miles:
        if m.get("상태") in ("완료",):
            continue
        n, lbl = dday(m.get("마감일", ""), today)
        if n is not None and n <= 7:
            soon.append((n, lbl, "일정", m.get("항목", ""), m.get("구분", "")))
    for p in permits:
        if p.get("상태") in ("승인",):
            continue
        n, lbl = dday(p.get("처리기한", ""), today)
        if n is not None and n <= 7:
            soon.append((n, lbl, "인허가", p.get("건명", ""), p.get("기관", "")))
    soon.sort(key=lambda x: x[0])

    # D-day 카드: 개인 구분 + 가장 가까운 마일스톤
    cards = []
    for m in miles:
        if m.get("상태") in ("완료",):
            continue
        n, lbl = dday(m.get("마감일", ""), today)
        if n is not None:
            cards.append((n, lbl, m.get("항목", ""), m.get("구분", "")))
    cards.sort(key=lambda x: x[0])
    cards = cards[:4]

    out = [STYLE.format(title="업무 대시보드", a1="active", a2="", a3="", h1="오늘의 업무 현황", now=now)]

    if cards:
        out.append('<div class="banner">')
        for n, lbl, name, g in cards:
            hot = " hot" if n <= 7 else ""
            out.append(f'<div class="dcard{hot}"><div class="num">{lbl}</div><div class="lbl">{esc(name)} ({esc(g)})</div></div>')
        out.append("</div>")

    def sec(title, rows, empty_msg):
        out.append(f"<section><h2>{title}</h2>")
        if rows:
            out.append(f"<table>{TASK_HEAD}{''.join(task_row(t, today) for t in rows)}</table>")
        else:
            out.append(f'<div class="empty">{empty_msg}</div>')
        out.append("</section>")

    sec("🔴 긴급", urgent, "긴급 업무 없음 — 좋은 신호다.")

    if soon:
        out.append("<section><h2>⏰ 마감 임박 (7일 이내 · 업무/일정/인허가 통합)</h2><table>")
        out.append("<tr><th>D-day</th><th>출처</th><th>항목</th><th>관련</th></tr>")
        for n, lbl, src, name, rel in soon:
            out.append(f'<tr><td><span class="{dd_class(n)}">{lbl}</span></td><td>{esc(src)}</td><td>{esc(name)}</td><td>{esc(rel)}</td></tr>')
        out.append("</table></section>")

    sec("📌 매일 하는 일", daily, "등록된 일일 업무 없음.")
    sec("👁 추적관찰", track, "추적 중인 건 없음.")
    if other:
        sec("📋 일반 업무", other, "")

    done = [t for t in tasks if t.get("상태") == "완료"]
    if done:
        sec(f"✅ 완료 ({len(done)})", done, "")

    out.append("</body></html>")
    return "".join(out)


def render_schedule(miles, today, now):
    out = [STYLE.format(title="공사일정·마감", a1="", a2="active", a3="", h1="공사일정 · 마감기한", now=now)]
    rows = []
    for m in miles:
        n, lbl = dday(m.get("마감일", ""), today)
        rows.append((n if n is not None else 99999, m, lbl))
    rows.sort(key=lambda x: x[0])
    out.append("<section><h2>마일스톤 (마감 가까운 순)</h2><table>")
    out.append("<tr><th>D-day</th><th>항목</th><th>구분</th><th>시작일</th><th>마감일</th><th>상태</th><th>메모</th></tr>")
    for n, m, lbl in rows:
        st = m.get("상태", "")
        stcls = {"완료": "st-done", "지연": "st-delay", "보류": "st-hold"}.get(st, "")
        done = ' class="done"' if st == "완료" else ""
        nn = None if n == 99999 else n
        out.append(f'<tr{done}><td><span class="{dd_class(nn)}">{lbl or "-"}</span></td>'
                   f"<td>{esc(m.get('항목',''))}</td><td>{badge(m.get('구분','-'), 'b-org')}</td>"
                   f"<td>{esc(m.get('시작일','')) or '-'}</td><td>{esc(m.get('마감일','')) or '-'}</td>"
                   f'<td class="{stcls}">{esc(st)}</td><td>{esc(m.get("메모",""))}</td></tr>')
    out.append("</table></section></body></html>")
    return "".join(out)


def render_permits(permits, today, now):
    out = [STYLE.format(title="인허가 추적", a1="", a2="", a3="active", h1="인허가 추적 보드", now=now)]
    rows = []
    for p in permits:
        n, lbl = dday(p.get("처리기한", ""), today)
        rows.append((n if n is not None else 99999, p, lbl))
    rows.sort(key=lambda x: x[0])
    out.append("<section><h2>인허가 건별 현황 (기한 가까운 순)</h2><table>")
    out.append("<tr><th>D-day</th><th>건명</th><th>기관</th><th>신청일</th><th>처리기한</th><th>상태</th><th>다음 액션</th><th>메모</th></tr>")
    for n, p, lbl in rows:
        st = p.get("상태", "")
        done = ' class="done"' if st == "승인" else ""
        nn = None if n == 99999 else n
        out.append(f'<tr{done}><td><span class="{dd_class(nn)}">{lbl or "-"}</span></td>'
                   f"<td>{esc(p.get('건명',''))}</td><td>{esc(p.get('기관',''))}</td>"
                   f"<td>{esc(p.get('신청일','')) or '-'}</td><td>{esc(p.get('처리기한','')) or '-'}</td>"
                   f"<td>{esc(st)}</td><td>{esc(p.get('다음 액션',''))}</td><td>{esc(p.get('메모',''))}</td></tr>")
    out.append("</table></section></body></html>")
    return "".join(out)


def main():
    cfg = load_config()
    work = cfg.get("sk_work")
    if not work or not os.path.isdir(work):
        print(f"[오류] sk_work 경로 없음: {work}")
        sys.exit(1)
    today = datetime.date.today()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    _, tasks = parse_table(os.path.join(work, "업무목록.md"))
    _, miles = parse_table(os.path.join(work, "공사일정.md"))
    _, permits = parse_table(os.path.join(work, "인허가.md"))

    pages = {
        "업무대시보드.html": render_home(tasks, miles, permits, today, now),
        "업무대시보드_일정.html": render_schedule(miles, today, now),
        "업무대시보드_인허가.html": render_permits(permits, today, now),
    }
    for name, content in pages.items():
        with open(os.path.join(work, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] {name}")
    print(f"업무 {len(tasks)}건 / 일정 {len(miles)}건 / 인허가 {len(permits)}건")


if __name__ == "__main__":
    main()
