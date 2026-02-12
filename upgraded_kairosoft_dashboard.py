import subprocess
import json
import re
from flask import Flask, jsonify
import time
from datetime import datetime, timedelta

app = Flask(__name__)

def get_active_sessions():
    try:
        output = subprocess.check_output(['openclaw', 'sessions', 'list'], text=True)
        lines = output.split('\n')
        active_count = 0
        now = datetime.now()
        for line in lines:
            if 'ago' in line and 'm' in line:
                # Parse age, e.g. "1m ago"
                match = re.search(r'(\d+)m ago', line)
                if match:
                    minutes = int(match.group(1))
                    if minutes <= 5:  # Active if less than 5 min
                        active_count += 1
            elif 'just now' in line:
                active_count += 1
        return min(active_count, 6)  # Max 6
    except:
        return 4  # Default

@app.route('/sessions.json')
def sessions():
    active = get_active_sessions()
    return jsonify({'active': active})

@app.route('/')
def index():
    with open('upgraded_kairosoft_dashboard.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)