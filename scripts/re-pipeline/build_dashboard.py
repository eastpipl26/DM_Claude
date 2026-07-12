# -*- coding: utf-8 -*-
"""워치리스트 대시보드 HTML 빌드 — 홈(요약) + 단지별 상세 페이지.

데이터는 별도 JS 파일(대시보드_데이터.js)로 뽑아 모든 페이지가 공유하고,
필터링·차트·정렬은 순수 JS(외부 라이브러리 없음)로 처리한다 — 인터넷 없이 file://로 열림.

원칙: 데이터 없는 구간은 공란/null로 두고 추정치로 채우지 않는다.
신호(🟢/🟡/⚪/🔴)와 총평 문장은 이미 계산된 매물비율·증감률·이상징후 판정을
말로 풀어쓴 것일 뿐, 새로운 판단 기준을 추가하는 게 아니다.
"""
import csv
import json
import os
import sys
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from common import load_config
from fetch_asil import RTMS_TO_ASIL
from track_watchlist import WATCHLIST, prev_week_rows, compare_to_prev


def load_policy_update(real_estate):
    """가장 최근 주간트래커.md에서 '## 이번 주 정책·거시·호재 업데이트' 섹션만 추출.

    weekly_policy_check.bat(headless Claude)가 이 섹션을 매주 붙여 넣는다.
    아직 이번 주 실행 전이면(스케줄 08:30 vs 데이터수집 08:00) None 반환.
    """
    tracker_dir = os.path.join(real_estate, "트래커")
    if not os.path.isdir(tracker_dir):
        return None
    cands = sorted(f for f in os.listdir(tracker_dir) if f.endswith("_주간트래커.md"))
    if not cands:
        return None
    path = os.path.join(tracker_dir, cands[-1])
    with open(path, encoding="utf-8") as f:
        content = f.read()
    marker = "## 이번 주 정책·거시·호재 업데이트"
    idx = content.find(marker)
    if idx == -1:
        return None
    return content[idx + len(marker):].strip()


def load_top_rank(data_dir):
    """현재순위_고점대비_*.csv 중 가장 최근 파일에서 단지별 고점대비%를 읽는다."""
    cands = [f for f in os.listdir(data_dir) if f.startswith("현재순위_고점대비_")]
    if not cands:
        return {}
    path = os.path.join(data_dir, sorted(cands)[-1])
    with open(path, encoding="utf-8-sig") as f:
        return {r["단지명"]: r for r in csv.DictReader(f)}


def build_deals(data_dir):
    with open(os.path.join(data_dir, "실거래_매매.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        if r["aptNm"] not in WATCHLIST:
            continue
        area = float(r["excluUseAr"])
        out.append({
            "단지명": r["aptNm"],
            "타입": round(area),
            "일자": f"{r['dealYear']}-{int(r['dealMonth']):02d}-{int(r['dealDay']):02d}",
            "금액만원": int(r["dealAmount"].replace(",", "").strip()),
            "층": r["floor"],
        })
    out.sort(key=lambda d: d["일자"])
    return out


def build_snapshots(data_dir):
    path = os.path.join(data_dir, "워치리스트_주간스냅샷.csv")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        out.append({
            "단지명": r["단지명"],
            "수집일": r["수집일"],
            "매물비율": r["매물비율_%"] or None,
            "증감률": r["증감률_%"] or None,
        })
    out.sort(key=lambda d: d["수집일"])
    return out


def signal_for(comparison, is_alert):
    """전주비교 문장 → (이모지, 라벨). 새 판단기준 아님, 기존 문장을 말로 옮긴 것."""
    if is_alert:
        return "🔴", "주의 — 급변 감지"
    if "매수세 강화" in comparison:
        return "🟢", "매수세 강화"
    if "매물 적체" in comparison:
        return "🟡", "매물 적체·관망"
    if "비교 기준 없음" in comparison:
        return "⚪", "데이터 쌓는 중(첫 주)"
    return "⚪", "변화 없음"


def build_summary(data_dir, snapshots, top_rank):
    today = date.today().isoformat()
    wl_path = os.path.join(data_dir, "워치리스트_주간스냅샷.csv")
    prev_rows = prev_week_rows(wl_path, today)

    latest_by_apt = {}
    for s in snapshots:
        latest_by_apt[s["단지명"]] = s  # 정렬돼 있으므로 마지막이 최신

    summary = []
    alerts = []
    for aptnm, tag in WATCHLIST.items():
        snap = latest_by_apt.get(aptnm, {})
        row = {
            "매물비율_%": snap.get("매물비율", ""),
            "증감률_%": snap.get("증감률", ""),
        }
        prev = prev_rows.get(aptnm)
        comparison, is_alert, alert_reason = compare_to_prev(row, prev)
        emoji, label = signal_for(comparison, is_alert)
        rank = top_rank.get(aptnm, {})
        summary.append({
            "단지명": aptnm,
            "구분": tag,
            "매물비율": snap.get("매물비율"),
            "증감률": snap.get("증감률"),
            "고점대비": rank.get("고점대비_%"),
            "전세가율": rank.get("전세가율_%"),
            "전주비교": comparison,
            "신호": emoji,
            "신호라벨": label,
        })
        if is_alert:
            alerts.append(f"{aptnm}: {alert_reason}")
    return summary, alerts


def build_narrative(summary, alerts):
    """숫자 나열 대신 말로 푼 이번 주 총평 — 요약표 신호 분포를 그대로 문장화."""
    n_good = sum(1 for r in summary if r["신호"] == "🟢")
    n_watch = sum(1 for r in summary if r["신호"] == "🟡")
    n_new = sum(1 for r in summary if "첫 주" in r["신호라벨"])
    n_alert = len(alerts)
    total = len(summary)

    if n_new == total:
        return "이번 주가 첫 수집이라 아직 비교할 전주 데이터가 없어. 다음 주부터 변화가 보이기 시작할 거야."

    clauses = []
    if n_good:
        clauses.append(f"{n_good}개는 매물이 줄며 매수세가 강해지고 있어")
    if n_watch:
        clauses.append(f"{n_watch}개는 매물이 쌓이며 관망 심리가 확산되고 있어")
    if n_alert:
        clauses.append(f"{n_alert}개는 이번 주 급변이 감지돼 주의가 필요해")
    if not clauses:
        return f"워치리스트 {total}개 단지 전부 전주 대비 뚜렷한 변화 없이 안정적인 한 주였어."
    return f"워치리스트 {total}개 단지 중 " + ", ".join(clauses) + "."


def apt_slug(aptnm):
    return aptnm  # 한글 파일명 그대로 사용 (윈도우/NTFS에서 문제 없음)


def main():
    cfg = load_config()
    data_dir = cfg["re_data"]
    real_estate = cfg["real_estate"]

    top_rank = load_top_rank(data_dir)
    deals = build_deals(data_dir)
    snapshots = build_snapshots(data_dir)
    summary, alerts = build_summary(data_dir, snapshots, top_rank)
    narrative = build_narrative(summary, alerts)
    policy_update = load_policy_update(real_estate)

    data = {
        "생성일": date.today().isoformat(),
        "워치리스트": WATCHLIST,
        "거래": deals,
        "스냅샷": snapshots,
        "요약": summary,
        "이상징후": alerts,
        "총평": narrative,
        "정책업데이트": policy_update,
    }

    data_js_path = os.path.join(real_estate, "대시보드_데이터.js")
    with open(data_js_path, "w", encoding="utf-8") as f:
        f.write("const DATA = " + json.dumps(data, ensure_ascii=False) + ";\n")

    with open(os.path.join(real_estate, "대시보드.html"), "w", encoding="utf-8") as f:
        f.write(STYLE + COMMON_JS_TAG + HOME_BODY)

    detail_dir = real_estate
    for aptnm in WATCHLIST:
        slug = apt_slug(aptnm)
        html = (STYLE + COMMON_JS_TAG +
                DETAIL_BODY.replace("__APT_NAME__", json.dumps(aptnm, ensure_ascii=False)))
        path = os.path.join(detail_dir, f"대시보드_단지_{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    print(f"대시보드 생성 → {os.path.join(real_estate, '대시보드.html')} "
          f"(거래 {len(deals)}건, 스냅샷 {len(snapshots)}행, 단지 상세페이지 {len(WATCHLIST)}개)")


STYLE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>워치리스트 대시보드</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: -apple-system, "Malgun Gothic", sans-serif; margin: 0; padding: 24px;
         background: #0f1115; color: #e6e6e6; max-width: 1100px; }
  a { color: #6d93e8; }
  a:hover { color: #9db6ee; }
  h1 { font-size: 20px; font-weight: 500; margin: 0 0 8px; }
  .page-header { background: #15171c; border: 1px solid #23262d; border-radius: 8px;
                 padding: 16px 18px; margin-bottom: 20px; }
  .header-nav { display: flex; align-items: center; gap: 14px; margin-bottom: 8px; }
  .header-nav .logo { color: #6d93e8; font-size: 13px; font-weight: 500; text-decoration: none; }
  .breadcrumb { font-size: 12px; color: #9aa0a6; }
  .breadcrumb a { color: #6d93e8; }
  .meta { color: #9aa0a6; font-size: 13px; margin-bottom: 0; }
  .pagination { display: flex; justify-content: space-between; align-items: center;
                gap: 8px; margin-top: 4px; }
  .nav-btn { padding: 8px 14px; border: 1px solid #3a3f4b; border-radius: 8px;
             color: #6d93e8; text-decoration: none; font-size: 13px; }
  .nav-btn:hover { border-color: #5a6170; background: #1a1d24; }
  .nav-btn.disabled { color: #5a6170; pointer-events: none; border-color: #23262d; }
  .narrative { background: #182437; border: 1px solid #2a4a7a; padding: 14px 18px;
               border-radius: 8px; margin-bottom: 16px; line-height: 1.6; font-size: 14px; }
  .policy-card { background: #1a1d24; border: 1px solid #2a2e37; padding: 14px 18px;
                 border-radius: 8px; margin-bottom: 16px; line-height: 1.7; font-size: 13px;
                 white-space: pre-wrap; }
  .policy-card h3 { margin: 0 0 8px; font-size: 14px; color: #c9cdd3; }
  .policy-card .empty { padding: 0; text-align: left; }
  .alert-banner { background: #4a1414; border: 1px solid #c0392b; color: #ffb3b3;
                  padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; line-height: 1.6; }
  .filters { display: flex; flex-wrap: wrap; gap: 20px; background: #1a1d24; padding: 16px;
             border-radius: 8px; margin-bottom: 20px; }
  .filter-group { display: flex; flex-direction: column; gap: 6px; font-size: 12px; }
  .filter-head { display: flex; align-items: center; gap: 8px; color: #9aa0a6; }
  .filter-head b { font-weight: 500; }
  .filter-head button { background: none; border: none; color: #6d93e8; font-size: 11px;
                          cursor: pointer; padding: 0; text-decoration: underline; }
  .filter-head button:hover { color: #9db6ee; }
  .chips { display: flex; flex-wrap: wrap; gap: 6px; max-width: 360px; }
  .chip { padding: 5px 11px; border: 1px solid #3a3f4b; border-radius: 14px; cursor: pointer;
          font-size: 12px; user-select: none; background: transparent; color: #e6e6e6;
          font-family: inherit; transition: background .1s, border-color .1s; }
  .chip:hover { border-color: #5a6170; }
  .chip.active { background: #3d6bd6; border-color: #3d6bd6; color: #fff; }
  section { margin-bottom: 20px; background: #15171c; border: 1px solid #23262d;
            border-radius: 8px; padding: 16px 18px; }
  h2 { font-size: 14px; color: #c9cdd3; margin: 0 0 12px; font-weight: 600; }
  table { border-collapse: collapse; width: 100%; font-size: 13px; }
  th, td { padding: 7px 10px; text-align: right; border-bottom: 1px solid #23262d; }
  th:first-child, td:first-child { text-align: left; }
  th { cursor: pointer; color: #9aa0a6; font-weight: 500; white-space: nowrap; }
  th:hover { color: #fff; }
  tr.alert-row { background: #241414; }
  tr:hover td { background: #1e222b; }
  .signal { font-size: 15px; }
  svg { background: #1a1d24; border-radius: 8px; display: block; }
  .chart-wrap { overflow-x: auto; }
  .axis-label { fill: #6b7078; font-size: 10px; }
  .legend { font-size: 12px; margin-top: 8px; display: flex; flex-wrap: wrap; gap: 4px 14px; }
  .empty { color: #6b7078; font-size: 13px; padding: 20px; text-align: center; }
  .back-link { display: inline-block; margin-bottom: 12px; font-size: 13px; }
  .detail-header { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
  .detail-header .signal { font-size: 22px; }
</style>
</head>
"""

COMMON_JS_TAG = r"""
<body>
"""

# 홈/상세 공통 JS (fmtWon, fmtDate, lineChart 등) — 두 페이지 모두 body 끝에서 재사용
COMMON_JS = r"""
function fmtWon(manwon) {
  const eok = manwon / 10000;
  return (Math.round(eok * 100) / 100).toLocaleString('ko-KR') + '억';
}
function fmtDate(ts) {
  const d = new Date(ts);
  return `${d.getFullYear()}.${String(d.getMonth()+1).padStart(2,'0')}`;
}
const CHART_COLORS = ['#3d6bd6','#e67e22','#2ecc71','#e74c3c','#9b59b6','#1abc9c','#f1c40f','#95a5a6'];

function lineChart(containerId, series, fmtY) {
  const w = 900, h = 280, pad = 46;
  const el = document.getElementById(containerId);
  const allPoints = series.flatMap(s => s.points);
  if (!allPoints.length) { el.innerHTML = '<div class="empty">데이터 없음</div>'; return; }
  const xs = allPoints.map(p => p.x);
  const ys = allPoints.map(p => p.y);
  const xMin = Math.min(...xs), xMax = Math.max(...xs);
  const yMin = Math.min(0, Math.min(...ys)), yMax = Math.max(...ys) * 1.1 || 1;
  const sx = x => pad + (xMax===xMin ? 0 : (x - xMin) / (xMax - xMin)) * (w - pad*2);
  const sy = y => h - pad - (yMax===yMin ? 0 : (y - yMin) / (yMax - yMin)) * (h - pad*2);

  let svg = `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}">`;
  svg += `<line x1="${pad}" y1="${h-pad}" x2="${w-pad}" y2="${h-pad}" stroke="#3a3f4b"/>`;
  svg += `<line x1="${pad}" y1="${pad}" x2="${pad}" y2="${h-pad}" stroke="#3a3f4b"/>`;
  for (let i = 0; i <= 4; i++) {
    const val = yMin + (yMax - yMin) * i / 4;
    const y = sy(val);
    svg += `<line x1="${pad}" y1="${y}" x2="${w-pad}" y2="${y}" stroke="#20242c"/>`;
    svg += `<text x="${pad-6}" y="${y+3}" text-anchor="end" class="axis-label">${fmtY(val)}</text>`;
  }
  [xMin, (xMin+xMax)/2, xMax].forEach(x => {
    svg += `<text x="${sx(x)}" y="${h-pad+16}" text-anchor="middle" class="axis-label">${fmtDate(x)}</text>`;
  });
  series.forEach((s, i) => {
    if (!s.points.length) return;
    const color = CHART_COLORS[i % CHART_COLORS.length];
    const pts = s.points.map(p => `${sx(p.x)},${sy(p.y)}`).join(' ');
    svg += `<polyline points="${pts}" fill="none" stroke="${color}" stroke-width="2"/>`;
    s.points.forEach(p => {
      svg += `<circle cx="${sx(p.x)}" cy="${sy(p.y)}" r="3" fill="${color}">` +
             `<title>${s.label} ${fmtDate(p.x)}: ${fmtY(p.y)}</title></circle>`;
    });
  });
  svg += `</svg>`;
  const legend = series.map((s,i) =>
    `<span style="color:${CHART_COLORS[i%CHART_COLORS.length]}">● ${s.label}</span>`).join('');
  el.innerHTML = `<div class="chart-wrap">${svg}</div><div class="legend">${legend}</div>`;
}

function renderChips(containerId, items, activeSet, labelFn, onToggle, onRender) {
  const el = document.getElementById(containerId);
  el.innerHTML = '';
  items.forEach(item => {
    const chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'chip' + (activeSet.has(item) ? ' active' : '');
    chip.textContent = labelFn(item);
    chip.onclick = () => { onToggle(item); onRender(); };
    el.appendChild(chip);
  });
}
function toggleSetItem(set, item) { if (set.has(item)) set.delete(item); else set.add(item); }

// 정책 업데이트 섹션은 headless Claude가 마크다운으로 써주므로, 표시용으로만 최소 변환
function mdToHtml(md) {
  const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  return esc(md)
    .replace(/^### (.+)$/gm, '<h4 style="margin:14px 0 4px;color:#c9cdd3">$1</h4>')
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    .replace(/\n{2,}/g, '<br><br>')
    .replace(/\n/g, '<br>');
}
"""

HOME_BODY = r"""
<header class="page-header">
  <div class="header-nav"><span class="logo">📊 워치리스트</span></div>
  <h1>워치리스트 대시보드</h1>
  <div class="meta" id="meta"></div>
</header>
<div class="narrative" id="narrative"></div>
<div id="alertBanner"></div>
<div class="policy-card" id="policyCard"></div>

<div class="filters">
  <div class="filter-group">
    <div class="filter-head"><b>단지</b><button id="apt-all">전체</button><button id="apt-none">해제</button></div>
    <div class="chips" id="f-apt"></div>
  </div>
  <div class="filter-group">
    <div class="filter-head"><b>타입(㎡)</b><button id="type-all">전체</button><button id="type-none">해제</button></div>
    <div class="chips" id="f-type"></div>
  </div>
  <div class="filter-group"><div class="filter-head"><b>기간</b></div><div class="chips" id="f-period"></div></div>
  <div class="filter-group"><div class="filter-head"><b>구분</b></div><div class="chips" id="f-tag"></div></div>
</div>

<section>
  <h2>단지별 비교 (현재 스냅샷, 헤더 클릭 정렬 · 단지명 클릭 시 상세페이지)</h2>
  <table id="summaryTable"><thead></thead><tbody></tbody></table>
</section>

<section>
  <h2>실거래가 추이</h2>
  <div id="dealChart"></div>
</section>

<section>
  <h2>매물비율 · 증감률 추이</h2>
  <div id="snapChart"></div>
</section>

<script src="대시보드_데이터.js"></script>
<script>
""" + COMMON_JS + r"""
document.getElementById('meta').textContent =
  '생성일 ' + DATA.생성일 + ' · 워치리스트 ' + Object.keys(DATA.워치리스트).length + '개 단지';
document.getElementById('narrative').textContent = DATA.총평;

const banner = document.getElementById('alertBanner');
if (DATA.이상징후 && DATA.이상징후.length) {
  const div = document.createElement('div');
  div.className = 'alert-banner';
  div.innerHTML = '<b>⚠ 이상징후</b><br>' + DATA.이상징후.map(a => '- ' + a).join('<br>');
  banner.appendChild(div);
}

const policyCard = document.getElementById('policyCard');
if (DATA.정책업데이트) {
  policyCard.innerHTML = '<h3>이번 주 정책·거시·호재 업데이트</h3>' + mdToHtml(DATA.정책업데이트);
} else {
  policyCard.innerHTML = '<h3>이번 주 정책·거시·호재 업데이트</h3>' +
    '<div class="empty">아직 수집 전이야 — 매주 월요일 08:30 자동 조사 예정(RE_WeeklyPolicyCheck)</div>';
}

const allApts = Object.keys(DATA.워치리스트);
const allTypes = [...new Set(DATA.거래.map(d => d.타입))].sort((a,b) => a-b);
const periods = [
  {label:'최근1년', days:365}, {label:'최근3년', days:365*3},
  {label:'최근5년', days:365*5}, {label:'전체', days:null}
];
const tags = [...new Set(Object.values(DATA.워치리스트).map(t => t.includes('심층') ? '심층' : '대장'))];

const state = { apts: new Set(allApts), types: new Set(allTypes), period: periods[3], tags: new Set(tags) };

function cutoffDate() {
  if (!state.period.days) return null;
  const d = new Date();
  d.setDate(d.getDate() - state.period.days);
  return d.toISOString().slice(0,10);
}

const alertApts = new Set((DATA.이상징후 || []).map(a => a.split(':')[0].trim()));

document.getElementById('apt-all').onclick = () => { state.apts = new Set(allApts); renderAll(); };
document.getElementById('apt-none').onclick = () => { state.apts = new Set(); renderAll(); };
document.getElementById('type-all').onclick = () => { state.types = new Set(allTypes); renderAll(); };
document.getElementById('type-none').onclick = () => { state.types = new Set(); renderAll(); };

let sortKey = '단지명', sortDir = 1;
function renderSummary() {
  const rows = DATA.요약.filter(r =>
    state.apts.has(r.단지명) && state.tags.has(r.구분.includes('심층') ? '심층' : '대장'));
  rows.sort((a,b) => {
    const av = a[sortKey], bv = b[sortKey];
    const an = parseFloat(av), bn = parseFloat(bv);
    let cmp;
    if (!isNaN(an) && !isNaN(bn)) cmp = an - bn;
    else cmp = String(av).localeCompare(String(bv));
    return cmp * sortDir;
  });
  const cols = [
    ['신호','신호'], ['단지명','단지명'], ['구분','구분'], ['매물비율','매물비율%'], ['증감률','10일증감%'],
    ['고점대비','고점대비%'], ['전세가율','전세가율%'], ['전주비교','전주 대비']
  ];
  const thead = document.querySelector('#summaryTable thead');
  thead.innerHTML = '<tr>' + cols.map(([k,label]) =>
    `<th data-key="${k}">${label}${sortKey===k ? (sortDir>0?' ▲':' ▼') : ''}</th>`).join('') + '</tr>';
  thead.querySelectorAll('th').forEach(th => {
    th.onclick = () => {
      const k = th.dataset.key;
      if (sortKey === k) sortDir *= -1; else { sortKey = k; sortDir = 1; }
      renderSummary();
    };
  });
  const tbody = document.querySelector('#summaryTable tbody');
  if (!rows.length) { tbody.innerHTML = '<tr><td colspan="8" class="empty">선택된 단지 없음</td></tr>'; return; }
  tbody.innerHTML = rows.map(r => `<tr class="${alertApts.has(r.단지명) ? 'alert-row' : ''}" title="${r.신호라벨}">
    <td class="signal">${r.신호}</td>
    <td><a href="./대시보드_단지_${r.단지명}.html">${r.단지명}</a></td>
    <td>${r.구분}</td>
    <td>${r.매물비율 != null ? r.매물비율 + '%' : ''}</td>
    <td>${r.증감률 != null ? r.증감률 + '%' : ''}</td>
    <td>${r.고점대비 != null ? r.고점대비 + '%' : ''}</td>
    <td>${r.전세가율 != null ? r.전세가율 + '%' : ''}</td>
    <td style="text-align:left">${r.전주비교 ?? ''}</td>
  </tr>`).join('');
}

function renderDealChart() {
  // 단지 내 평형(타입)마다 가격대가 크게 다르므로, 같은 단지라도 타입별로 선을 나눈다.
  // 안 그러면 59㎡·85㎡ 거래가 한 선에 섞여 지그재그로 왜곡돼 보인다.
  const cutoff = cutoffDate();
  const groups = {};
  DATA.거래.forEach(d => {
    if (!state.apts.has(d.단지명) || !state.types.has(d.타입)) return;
    if (cutoff && d.일자 < cutoff) return;
    const key = d.단지명 + ' · ' + d.타입 + '㎡';
    (groups[key] = groups[key] || []).push({ x: new Date(d.일자).getTime(), y: d.금액만원 });
  });
  const series = Object.keys(groups).sort().map(k => ({ label: k, points: groups[k] }));
  lineChart('dealChart', series, fmtWon);
}
function renderSnapChart() {
  const cutoff = cutoffDate();
  const series = [];
  allApts.forEach(apt => {
    if (!state.apts.has(apt)) return;
    const pts = DATA.스냅샷
      .filter(s => s.단지명 === apt && (!cutoff || s.수집일 >= cutoff) && s.매물비율 !== null)
      .map(s => ({ x: new Date(s.수집일).getTime(), y: parseFloat(s.매물비율) }));
    if (pts.length) series.push({ label: apt, points: pts });
  });
  lineChart('snapChart', series, v => (Math.round(v*10)/10) + '%');
}

function renderAll() {
  renderChips('f-apt', allApts, state.apts, a => a.replace('송도',''), a => toggleSetItem(state.apts, a), renderAll);
  renderChips('f-type', allTypes, state.types, t => t + '㎡', t => toggleSetItem(state.types, t), renderAll);
  renderChips('f-period', periods, new Set([state.period]), p => p.label, p => { state.period = p; }, renderAll);
  renderChips('f-tag', tags, state.tags, t => t, t => toggleSetItem(state.tags, t), renderAll);
  renderSummary();
  renderDealChart();
  renderSnapChart();
}
renderAll();
</script>
</body>
</html>
"""

DETAIL_BODY = r"""
<header class="page-header">
  <div class="header-nav">
    <a class="logo" href="./대시보드.html">📊 워치리스트</a>
    <nav class="breadcrumb" id="breadcrumb"></nav>
  </div>
  <div class="detail-header"><span class="signal" id="apt-signal"></span><h1 id="apt-title"></h1></div>
  <div class="meta" id="meta"></div>
</header>
<div class="narrative" id="apt-narrative"></div>

<div class="filters">
  <div class="filter-group"><div class="filter-head"><b>기간</b></div><div class="chips" id="f-period"></div></div>
  <div class="filter-group">
    <div class="filter-head"><b>타입(㎡)</b><button id="type-all">전체</button><button id="type-none">해제</button></div>
    <div class="chips" id="f-type"></div>
  </div>
</div>

<section>
  <h2>실거래가 추이 (평형별)</h2>
  <div id="dealChart"></div>
</section>

<section>
  <h2>매물비율 · 증감률 추이</h2>
  <div id="snapChart"></div>
</section>

<section>
  <h2>최근 실거래 10건</h2>
  <table id="recentTable"><thead><tr><th>일자</th><th>층</th><th>타입(㎡)</th><th>금액</th></tr></thead><tbody></tbody></table>
</section>

<div class="pagination" id="pagination"></div>

<script src="대시보드_데이터.js"></script>
<script>
""" + COMMON_JS + r"""
const APT = __APT_NAME__;
const row = DATA.요약.find(r => r.단지명 === APT) || {};
document.getElementById('apt-signal').textContent = row.신호 || '';
document.getElementById('apt-title').textContent = APT + ' (' + (DATA.워치리스트[APT] || '') + ')';
document.getElementById('meta').textContent = '생성일 ' + DATA.생성일;
document.getElementById('apt-narrative').textContent =
  (row.신호라벨 || '') + ' — ' + (row.전주비교 || '');
document.getElementById('breadcrumb').innerHTML =
  '<a href="./대시보드.html">홈</a> &gt; ' + APT + ' &gt; 상세';

// 이전/다음 단지 네비게이션 (워치리스트 등록 순서 기준)
(function() {
  const names = Object.keys(DATA.워치리스트);
  const idx = names.indexOf(APT);
  const prev = idx > 0 ? names[idx - 1] : null;
  const next = idx < names.length - 1 ? names[idx + 1] : null;
  const linkOrDisabled = (name, label) => name
    ? `<a class="nav-btn" href="./대시보드_단지_${name}.html">${label}</a>`
    : `<span class="nav-btn disabled">${label}</span>`;
  document.getElementById('pagination').innerHTML =
    linkOrDisabled(prev, '← 이전 단지') +
    '<a class="nav-btn" href="./대시보드.html">전체 요약</a>' +
    linkOrDisabled(next, '다음 단지 →');
})();

const periods = [
  {label:'최근1년', days:365}, {label:'최근3년', days:365*3},
  {label:'최근5년', days:365*5}, {label:'전체', days:null}
];
const allTypes = [...new Set(DATA.거래.filter(d => d.단지명 === APT).map(d => d.타입))].sort((a,b)=>a-b);
const state = { period: periods[3], types: new Set(allTypes) };
function cutoffDate() {
  if (!state.period.days) return null;
  const d = new Date();
  d.setDate(d.getDate() - state.period.days);
  return d.toISOString().slice(0,10);
}

document.getElementById('type-all').onclick = () => { state.types = new Set(allTypes); renderAll(); };
document.getElementById('type-none').onclick = () => { state.types = new Set(); renderAll(); };

function renderDealChart() {
  // 같은 단지라도 59㎡·85㎡ 등 평형마다 가격대가 달라 한 선에 섞으면 왜곡된다 — 타입별로 분리.
  const cutoff = cutoffDate();
  const groups = {};
  DATA.거래.forEach(d => {
    if (d.단지명 !== APT || !state.types.has(d.타입)) return;
    if (cutoff && d.일자 < cutoff) return;
    const key = d.타입 + '㎡';
    (groups[key] = groups[key] || []).push({ x: new Date(d.일자).getTime(), y: d.금액만원 });
  });
  const series = Object.keys(groups)
    .sort((a,b) => parseInt(a) - parseInt(b))
    .map(k => ({ label: k, points: groups[k] }));
  lineChart('dealChart', series, fmtWon);
}
function renderSnapChart() {
  const cutoff = cutoffDate();
  const pts = DATA.스냅샷
    .filter(s => s.단지명 === APT && (!cutoff || s.수집일 >= cutoff) && s.매물비율 !== null)
    .map(s => ({ x: new Date(s.수집일).getTime(), y: parseFloat(s.매물비율) }));
  lineChart('snapChart', pts.length ? [{label: APT, points: pts}] : [], v => (Math.round(v*10)/10) + '%');
}
function renderRecent() {
  const rows = DATA.거래.filter(d => d.단지명 === APT && state.types.has(d.타입)).slice(-10).reverse();
  const tbody = document.querySelector('#recentTable tbody');
  tbody.innerHTML = rows.length ? rows.map(d =>
    `<tr><td>${d.일자}</td><td>${d.층}</td><td>${d.타입}</td><td>${fmtWon(d.금액만원)}</td></tr>`
  ).join('') : '<tr><td colspan="4" class="empty">거래 없음</td></tr>';
}
function renderAll() {
  renderChips('f-period', periods, new Set([state.period]), p => p.label, p => { state.period = p; }, renderAll);
  renderChips('f-type', allTypes, state.types, t => t + '㎡', t => toggleSetItem(state.types, t), renderAll);
  renderDealChart();
  renderSnapChart();
  renderRecent();
}
renderAll();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
