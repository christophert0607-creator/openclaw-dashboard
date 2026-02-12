from flask import Flask, render_template, jsonify, request
import json
import os
import time
from datetime import datetime
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='dashboard.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Path to sessions.json
SESSIONS_PATH = '/home/tsukii0607/.openclaw/agents/main/sessions/sessions.json'

def load_sessions():
    logging.info(f"Loading sessions from {SESSIONS_PATH}")
    if not os.path.exists(SESSIONS_PATH):
        logging.warning("Sessions file not found, using default")
        return {'ceo': {'status': 'idle', 'age': 'unknown'}, 'employees': [], 'projects': []}
    
    try:
        with open(SESSIONS_PATH, 'r', encoding='utf-8') as f:
            sessions = json.load(f)
        logging.info("Sessions loaded successfully")
    except Exception as e:
        logging.error(f"Error loading sessions: {e}")
        return {'ceo': {'status': 'error', 'age': 'unknown'}, 'employees': [], 'projects': []}
    
    # Get updatedAt from command for ageMs, but since we have updatedAt, calculate age
    now = time.time() * 1000  # ms
    ceo = sessions.get('agent:main:main', {})
    ceo_age_ms = now - ceo.get('updatedAt', 0)
    ceo_status = 'busy' if ceo_age_ms < 600000 else 'idle'  # 10 min
    
    employees = []
    projects = []
    
    for key, data in sessions.items():
        if key.startswith('agent:main:subagent:'):
            label = data.get('label', 'Unnamed Project')
            updated_at = data.get('updatedAt', 0)
            age_ms = now - updated_at
            status = 'busy' if age_ms < 600000 else 'idle'
            
            # Get totalTokens if available, else from sessionFile if possible
            total_tokens = data.get('totalTokens', 0)
            context_tokens = data.get('contextTokens', 200000)
            progress = min(100, (total_tokens / context_tokens) * 100) if total_tokens else 0
            
            session_id = data.get('sessionId', '')
            position = {'x': 100 + len(employees) * 100, 'y': 350}  # simple positions
            
            employees.append({
                'id': session_id,
                'name': label[:10] + '...' if len(label) > 10 else label,  # short name
                'status': status,
                'age_ms': age_ms,
                'position': position,
                'animation': 'working' if status == 'busy' else 'idle',
                'project': label,
                'progress': progress
            })
            
            projects.append({
                'id': session_id,
                'name': label,
                'progress': progress,
                'assigned_employee': session_id
            })
    
    logging.info(f"Processed {len(employees)} subagents")
    return {
        'ceo': {'status': ceo_status, 'age_ms': ceo_age_ms},
        'employees': employees,
        'projects': projects
    }

@app.route('/')
def index():
    logging.info("Index page requested")
    return render_template('index.html')

@app.route('/api/dashboard')
def api_dashboard():
    logging.info("API dashboard called")
    data = load_sessions()
    return jsonify(data)

# Keep existing endpoints for simulation if needed, but focus on real

if __name__ == '__main__':
    logging.info("Starting Flask app on port 5004")
    app.run(debug=True, port=5004, host='0.0.0.0')