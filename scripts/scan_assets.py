"""
scan_assets.py - 말숙이 팀 자산 스캔 -> catalog.json
agents/*.md frontmatter + skills/ + 작업 스케줄러 상태 읽어서 catalog.json 생성
"""
import json, os, re, subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"C:\Users\eastp\.claude")
OUT  = BASE / "dashboard2" / "catalog.json"

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta

def read_agents():
    agents = []
    agents_dir = BASE / "agents"
    for f in sorted(agents_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        meta = parse_frontmatter(text)
        name = meta.get("name", f.stem)
        desc = meta.get("description", "")
        # 직원목록에서 직급 파싱 (간단히 파일명으로 매핑)
        rank_map = {
            "말숙이": "비서실장", "강이": "과장", "문이": "과장",
            "옥순이": "대리", "새벽이": "대리", "재이": "대리",
            "캐순이": "사원", "물색이": "사원", "손질이": "사원",
            "탐이": "사원", "수이": "사원",
            "선우": "대기발령"
        }
        rank = rank_map.get(f.stem, "사원")
        agents.append({
            "id": f.stem,
            "name": f.stem,
            "rank": rank,
            "status": "standby" if rank == "대기발령" else "idle",
            "task": "",
            "description": desc[:80] if desc else "",
            "file": str(f)
        })
    return agents

def read_skills():
    skills = []
    skills_dir = BASE / "skills"
    if skills_dir.exists():
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir():
                skill_file = d / "SKILL.md"
                if not skill_file.exists():
                    skill_file = d / "skill.md"
                if skill_file.exists():
                    text = skill_file.read_text(encoding="utf-8", errors="ignore")
                    first_line = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
                    desc = first_line[0][:80] if first_line else ""
                    skills.append({
                        "id": d.name,
                        "name": f"/{d.name}",
                        "description": desc,
                        "last_used": None
                    })
    # 플러그인 스킬 추가 (하드코딩 몇 개)
    skills.append({"id": "회의록-정리", "name": "/회의록-정리", "description": "예정 (미구현)", "last_used": None})
    return skills

def read_schedules():
    schedules = []
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "Get-ScheduledTask -TaskName '말숙이팀-*' | Select-Object TaskName,State,@{N='NextRun';E={(Get-ScheduledTaskInfo $_.TaskName).NextRunTime}} | ConvertTo-Json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if isinstance(data, dict):
                data = [data]
            for t in data:
                schedules.append({
                    "name": t.get("TaskName", ""),
                    "state": t.get("State", ""),
                    "next_run": str(t.get("NextRun", ""))
                })
    except Exception as e:
        schedules.append({"name": "스케줄러 읽기 실패", "state": str(e), "next_run": ""})
    return schedules

catalog = {
    "generated_at": datetime.now().isoformat(),
    "agents": read_agents(),
    "skills": read_skills(),
    "schedules": read_schedules()
}

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"catalog.json 생성 완료: {len(catalog['agents'])}명 에이전트, {len(catalog['skills'])}개 스킬")
