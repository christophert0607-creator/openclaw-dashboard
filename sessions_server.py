import subprocess
import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

def get_sessions():
    try:
        result = subprocess.run(['openclaw', 'sessions', 'list'], capture_output=True, text=True, timeout=10)
        output = result.stdout
        sessions = []
        lines = output.split('\n')
        started = False
        for line in lines:
            if 'Kind   Key                        Age       Model          Tokens (ctx %)       Flags' in line:
                started = True
                continue
            if started and line.strip() and not line.startswith('│') and not line.startswith('◇'):
                parts = re.split(r'\s{2,}', line.strip())
                if len(parts) >= 3:
                    kind = parts[0]
                    key = parts[1]
                    age = parts[2]
                    model = parts[3] if len(parts) > 3 else ''
                    # add more if needed
                    sessions.append({'kind': kind, 'key': key, 'age': age, 'model': model})
        return sessions[:6]  # limit to 6
    except Exception as e:
        return [{'error': str(e)}]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/sessions':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = json.dumps(get_sessions())
            self.wfile.write(data.encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server = HTTPServer(('localhost', 8000), Handler)
    print('Server running on http://localhost:8000/api/sessions')
    server.serve_forever()

if __name__ == '__main__':
    run_server()