from flask import Flask, render_template, jsonify, request
import subprocess
import json
import random
import time

app = Flask(__name__)

# Simulated data for demo
employees = [
    {'id': 1, 'name': 'Dev1', 'status': 'idle', 'position': {'x': 100, 'y': 200}, 'animation': 'idle'},
    {'id': 2, 'name': 'Dev2', 'status': 'idle', 'position': {'x': 200, 'y': 200}, 'animation': 'idle'}
]

projects = [
    {'id': 1, 'name': 'Game Project A', 'progress': 30, 'assigned': []},
    {'id': 2, 'name': 'Game Project B', 'progress': 10, 'assigned': []}
]

# Function to get real sessions (placeholder)
def get_openclaw_sessions():
    try:
        result = subprocess.run(['openclaw', 'sessions', 'list'], capture_output=True, text=True)
        # Parse result to get subagents and projects
        # For now, return simulated
        return employees, projects
    except:
        return employees, projects

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/employees')
def api_employees():
    employees, _ = get_openclaw_sessions()
    return jsonify(employees)

@app.route('/api/projects')
def api_projects():
    _, projects = get_openclaw_sessions()
    return jsonify(projects)

@app.route('/api/assign', methods=['POST'])
def api_assign():
    data = request.json
    emp_id = data['employee_id']
    proj_id = data['project_id']
    # Simulate assignment
    for emp in employees:
        if emp['id'] == emp_id:
            emp['status'] = 'working'
            emp['assigned_project'] = proj_id
            emp['position'] = {'x': random.randint(300, 500), 'y': 300}  # Move to project area
            break
    for proj in projects:
        if proj['id'] == proj_id:
            if emp_id not in proj['assigned']:
                proj['assigned'].append(emp_id)
    # In real: spawn or assign task to session
    # subprocess.run(['openclaw', 'sessions', 'spawn', '--task', f'Work on project {proj_id}'])
    return jsonify({'success': True})

@app.route('/api/fire', methods=['POST'])
def api_fire():
    data = request.json
    emp_id = data['employee_id']
    global employees
    employees = [e for e in employees if e['id'] != emp_id]
    # In real: openclaw sessions kill <id>
    return jsonify({'success': True})

@app.route('/api/hire', methods=['POST'])
def api_hire():
    global employees
    new_id = max(e['id'] for e in employees) + 1 if employees else 1
    new_emp = {'id': new_id, 'name': f'Dev{new_id}', 'status': 'idle', 'position': {'x': random.randint(50, 150), 'y': 200}, 'animation': 'idle'}
    employees.append(new_emp)
    # In real: openclaw sessions spawn --task 'Employee subagent'
    return jsonify(new_emp)

# Simulate progress
def update_progress():
    for proj in projects:
        if proj['assigned']:
            proj['progress'] += random.randint(1, 5)
            if proj['progress'] >= 100:
                proj['progress'] = 100
    # In real: poll sessions for productivity

if __name__ == '__main__':
    # Run in background? For testing: app.run(debug=True, port=5000)
    app.run(debug=True, port=5000)