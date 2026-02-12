import json
from flask import Flask, jsonify
import re
from datetime import datetime

app = Flask(__name__)

def parse_progress_md(md_path='/home/tsukii0607/.openclaw/workspace/Office_Block_Progress.md'):
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return {'error': 'Progress file not found'}

    # Parse floor progress table
    floors = []
    table_match = re.search(r'### 🏗️ 樓層施工進度.*?\|.*?\n(.*?)\n', content, re.DOTALL)
    if table_match:
        lines = table_match.group(1).strip().split('\n')
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = [p.strip() for p in re.split(r'\|', line) if p.strip()]
                if len(parts) >= 4:
                    floors.append({
                        'floor': parts[0],
                        'project': parts[1],
                        'progress': parts[2],
                        'notes': parts[3]
                    })

    # Parse schedule table
    schedules = []
    schedule_match = re.search(r'### 📅 下週工作/停機安排.*?\|.*?\n(.*?)\n', content, re.DOTALL)
    if schedule_match:
        lines = schedule_match.group(1).strip().split('\n')
        for line in lines[1:]:
            if line.strip():
                parts = [p.strip() for p in re.split(r'\|', line) if p.strip()]
                if len(parts) >= 3:
                    schedules.append({
                        'date': parts[0],
                        'matter': parts[1],
                        'details': parts[2]
                    })

    # Extract WhatsApp summary
    whatsapp = re.search(r'### 📱 WhatsApp 監控摘要\n(.*?)(?=###|$)', content, re.DOTALL)
    whatsapp_summary = whatsapp.group(1).strip() if whatsapp else ''

    return {
        'last_updated': re.search(r'更新日期: (.*)', content).group(1) if re.search(r'更新日期: (.*)', content) else 'Unknown',
        'floors': floors,
        'schedules': schedules,
        'whatsapp': whatsapp_summary
    }

@app.route('/progress.json')
def progress():
    data = parse_progress_md()
    return jsonify(data)

@app.route('/')
def index():
    return '''
    <h1>Office Block Progress API</h1>
    <p><a href="/progress.json">Get Progress JSON</a></p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)