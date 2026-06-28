import http.server, socketserver, os, webbrowser, threading

PORT = 8388
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=DIR, **kw)
    def log_message(self, *a):
        pass

def open_browser():
    import time; time.sleep(0.5)
    webbrowser.open(f'http://localhost:{PORT}')

threading.Thread(target=open_browser, daemon=True).start()
print(f'대시보드 서버 시작: http://localhost:{PORT}')
print('종료: Ctrl+C')
with socketserver.TCPServer(('', PORT), Handler) as httpd:
    httpd.serve_forever()
