"""
serve.py - 말숙이 팀 대시보드 로컬 서버 (포트 8390)
- 정적 파일 서빙
- /api/catalog   : catalog.json (정적 자산)
- /api/state     : state.json  (실시간 상태)
- /api/events    : SSE — state.json 변경 시 push
- /api/run       : POST — claude --print 헤드리스 실행
"""
import http.server, socketserver, json, os, sys, threading, time, subprocess, webbrowser
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT    = 8390
BASE    = Path(r"C:\Users\eastp\.claude")
DASH    = BASE / "dashboard2"
CATALOG = DASH / "catalog.json"
STATE   = DASH / "state.json"
SCRIPTS = BASE / "scripts"

def get_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return {}

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(DASH), **kw)

    def log_message(self, *a):
        pass

    def do_GET(self):
        p = urlparse(self.path).path

        if p == "/api/catalog":
            self.send_json(get_json(CATALOG))
        elif p == "/api/state":
            self.send_json(get_json(STATE))
        elif p == "/api/events":
            self.sse_stream()
        else:
            super().do_GET()

    def do_POST(self):
        p = urlparse(self.path).path
        if p == "/api/run":
            length = int(self.headers.get("Content-Length", 0))
            body   = json.loads(self.rfile.read(length)) if length else {}
            prompt = body.get("prompt", "")
            if not prompt:
                self.send_json({"error": "prompt 없음"}, 400)
                return
            try:
                result = subprocess.run(
                    ["powershell", "-Command",
                     f'$env:PATH = "C:\\Users\\eastp\\AppData\\Roaming\\npm;$env:PATH"; claude --print -p "{prompt.replace(chr(34), chr(39))}"'],
                    capture_output=True, text=True, timeout=120
                )
                self.send_json({"output": result.stdout, "error": result.stderr})
            except subprocess.TimeoutExpired:
                self.send_json({"error": "타임아웃 (120초)"}, 500)
        else:
            self.send_error(404)

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def sse_stream(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        last_mtime = 0
        try:
            while True:
                try:
                    mtime = STATE.stat().st_mtime if STATE.exists() else 0
                    if mtime != last_mtime:
                        last_mtime = mtime
                        data = json.dumps(get_json(STATE), ensure_ascii=False)
                        self.wfile.write(f"data: {data}\n\n".encode("utf-8"))
                        self.wfile.flush()
                except:
                    break
                time.sleep(0.5)
        except:
            pass

def rescan():
    """catalog.json 주기적 갱신 (5분마다)"""
    while True:
        time.sleep(300)
        subprocess.run([sys.executable, str(SCRIPTS / "scan_assets.py")], capture_output=True)

if __name__ == "__main__":
    # 최초 스캔
    subprocess.run([sys.executable, str(SCRIPTS / "scan_assets.py")])
    # 주기 스캔 스레드
    threading.Thread(target=rescan, daemon=True).start()
    # 브라우저 열기
    threading.Thread(target=lambda: (time.sleep(0.8), webbrowser.open(f"http://localhost:{PORT}")), daemon=True).start()
    print(f"대시보드 서버: http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
