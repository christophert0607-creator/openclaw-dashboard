import subprocess
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import json

def get_sessions():
    result = subprocess.run(['openclaw', 'sessions', 'list'], capture_output=True, text=True)
    if result.returncode != 0:
        return []
    lines = result.stdout.strip().split('\n')
    sessions = []
    for line in lines[2:]:  # skip headers and empty
        if line.strip() and not line.startswith('Doctor'):
            parts = re.split(r'\s{2,}', line.strip())
            if len(parts) >= 4:
                kind = parts[0]
                key = parts[1]
                age = parts[2]
                model = parts[3] if len(parts) > 3 else ''
                sessions.append({'kind': kind, 'key': key, 'age': age, 'model': model})
    return sessions

def is_busy(age):
    if 'just now' in age.lower():
        return True
    if 'm ago' in age:
        minutes = int(re.search(r'(\d+)m', age).group(1))
        return minutes < 5
    return False

def generate_html(sessions):
    main = next((s for s in sessions if ':main:main' in s['key']), None)
    subs = [s for s in sessions if 'subag' in s['key']]
    subs = subs[:8]  # limit to 8 positions

    # Positions for sub desks: around center
    positions = [
        {'left': '100px', 'top': '150px'},
        {'left': '200px', 'top': '50px'},
        {'left': '500px', 'top': '50px'},
        {'left': '650px', 'top': '150px'},
        {'left': '650px', 'top': '350px'},
        {'left': '500px', 'top': '450px'},
        {'left': '200px', 'top': '450px'},
        {'left': '100px', 'top': '350px'}
    ]

    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>OpenClaw Kairosoft-style Office Dashboard</title>
    <style>
        body {
            background-color: #f0f8ff;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
        }
        .office {
            position: relative;
            width: 800px;
            height: 600px;
            background-image: url('assets/OGA/Background/background.png');
            background-size: cover;
            margin: 0 auto;
            border: 4px solid #333;
            image-rendering: pixelated;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }
        .desk {
            position: absolute;
            width: 64px;
            height: 32px;
            background-color: #8B4513;
            border: 2px solid #654321;
            image-rendering: pixelated;
        }
        .boss-desk {
            left: 368px;
            top: 284px;
        }
        .sub-desk {
            /* positions set inline */
        }
        .character {
            position: absolute;
            width: 32px;
            height: 32px;
            image-rendering: pixelated;
            border: 1px solid #000;
        }
        .boss-char {
            left: 384px;
            top: 252px;
            background-image: url('assets/OGA/Chars/people_boss.png');
            background-size: 32px 32px;
            animation: typing 1s infinite alternate;
        }
        @keyframes typing {
            0% { transform: translateY(0); }
            100% { transform: translateY(-2px); }
        }
        .sub-char {
            /* positions set inline */
            background-size: 32px 32px;
        }
        .working {
            animation: work 2s infinite;
            background-image: url('assets/OGA/Chars/people_1.png'); /* assume working */
        }
        .idle {
            background-image: url('assets/OGA/Chars/people_2.png'); /* assume idle */
            opacity: 0.7;
        }
        @keyframes work {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        .zzz {
            position: absolute;
            font-size: 12px;
            color: #666;
            animation: float 3s infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        .logo {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 28px;
            color: #000;
            font-weight: bold;
            text-shadow: 2px 2px #fff;
        }
        .poster {
            position: absolute;
            width: 80px;
            height: 120px;
            background-color: #fff;
            border: 2px solid #000;
            top: 20px;
            left: 20px;
        }
        .poster:after {
            content: 'Team Vibes';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 10px;
        }
        .status {
            position: absolute;
            bottom: -20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 12px;
            color: #333;
        }
    </style>
</head>
<body>
    <h1 style="text-align: center;">OpenClaw Office Dashboard - Kairosoft Style</h1>
    <div class="office">
        <div class="logo">OpenClaw Inc.</div>
        <div class="poster"></div>
        <div class="poster" style="right: 20px; left: auto;"></div>
        <div class="desk boss-desk"></div>
        <div class="character boss-char"></div>
    '''

    for i, sub in enumerate(subs):
        if i >= len(positions):
            break
        pos = positions[i]
        state_class = 'working' if is_busy(sub['age']) else 'idle'
        zzz = '<div class="zzz">ZZZ</div>' if not is_busy(sub['age']) else ''
        char_id = f"sub_{i}"
        html += f'''
        <div class="desk sub-desk" style="left: {pos['left']}; top: {pos['top']};"></div>
        <div class="character sub-char {state_class}" style="left: {str(int(float(pos['left'][:-2])) + 16)}px; top: {str(int(float(pos['top'][:-2])) - 16)}px;" id="{char_id}">{zzz}</div>
        <div class="status" style="left: {pos['left']};">{sub['key'][:20]}{' (Busy)' if is_busy(sub['age']) else ' (Idle)'}</div>
        '''

    # For main status
    main_state = 'Busy' if main and is_busy(main['age']) else 'Leading'
    html += f'''
        <div class="status" style="left: 368px;">Main Agent ({main_state})</div>
    </div>
    <p style="text-align: center;">Refresh the page to update sessions.</p>
</body>
</html>
    '''
    return html

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='dashboard', **kwargs)

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            sessions = get_sessions()
            html = generate_html(sessions)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
            return
        super().do_GET()

def run_server():
    os.chdir('/home/tsukii0607/.openclaw/workspace/dashboard')
    server = HTTPServer(('localhost', 8080), DashboardHandler)
    print("Dashboard server started at http://localhost:8080")
    print("Press Ctrl+C to stop.")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
