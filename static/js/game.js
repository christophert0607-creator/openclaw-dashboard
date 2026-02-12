const canvas = document.getElementById('office-canvas');
const ctx = canvas.getContext('2d');
const employeesList = document.getElementById('employees-list');
const projectsList = document.getElementById('projects-list');
const hireBtn = document.getElementById('hire-btn');
const newProjectBtn = document.getElementById('new-project-btn');
const eventsLog = document.getElementById('events-log');

// Game state
let employees = [];
let projects = [];
let animationFrameId;

// Draw office background (simple pixel art style, adjusted for 600x480)
function drawOffice() {
    ctx.fillStyle = '#f0f8ff'; // Light blue-gray for office
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw desks (brown rectangles)
    ctx.fillStyle = '#8B4513';
    for (let i = 0; i < 4; i++) {
        ctx.fillRect(50 + i * 120, 300, 100, 60);
    }
    // CEO desk central top
    ctx.fillStyle = '#654321';
    ctx.fillRect(150, 100, 300, 80);
    
    // Water cooler right
    ctx.fillStyle = '#00BFFF';
    ctx.fillRect(550, 300, 40, 100);
}

// Draw employee (simple colored square, nicer colors)
function drawEmployee(emp) {
    ctx.fillStyle = emp.status === '忙碌' ? '#FF6B6B' : '#4ECDC4'; // Reddish for busy, teal for idle
    const bob = Math.sin(Date.now() / 200 + emp.id) * 2;
    ctx.fillRect(emp.position.x, emp.position.y + bob, 20, 20);
    
    // If idle at desk, add Zzz
    if (emp.status === '閒置' && emp.position.y > 300) {
        ctx.fillStyle = '#000';
        ctx.font = '12px Arial';
        ctx.fillText('Zzz', emp.position.x + 5, emp.position.y - 5);
    }
    
    // Add name label if space
    ctx.fillStyle = '#000';
    ctx.font = '10px Arial';
    ctx.fillText(emp.name, emp.position.x - 10, emp.position.y - 10);
}

// Removed drawProjects() - now in HTML

// Update UI
function updateStats() {
    employeesList.innerHTML = employees.map(emp => 
        `<div>
            <strong>${emp.name}</strong> - 
            <span class="status-badge ${emp.status === '忙碌' ? 'busy' : 'idle'}">${emp.status}</span>
            <br>
            <button title="指派到項目" onclick="assignEmployee(${emp.id})" style="font-size: 12px; margin: 2px;">➡️ 指派項目</button>
            <button title="解雇員工" onclick="fireEmployee(${emp.id})" style="font-size: 12px; margin: 2px; background: #ff4444; color: white;">➖ 解雇</button>
        </div>`
    ).join('');
    
    projectsList.innerHTML = projects.map(proj => `
        <div class="project-item">
            <div><strong>${proj.name}</strong></div>
            <div class="project-progress">
                <div class="project-fill" style="width: ${proj.progress}%"></div>
            </div>
            <div>進度: ${proj.progress}%</div>
            <div class="assigned-employees">指派員工: ${proj.assigned.length > 0 ? proj.assigned.map(id => employees.find(e => e.id === id)?.name || 'Unknown').join(', ') : '無'}</div>
        </div>
    `).join('');
}

// API calls
async function fetchData() {
    try {
        const empRes = await fetch('/api/employees');
        employees = await empRes.json();
        
        const projRes = await fetch('/api/projects');
        projects = await projRes.json();
        
        updateStats();
    } catch (e) {
        console.error('Fetch error:', e);
    }
}

// Event handlers
hireBtn.onclick = async () => {
    try {
        await fetch('/api/hire', {method: 'POST'});
        fetchData();
    } catch (e) {
        console.error(e);
    }
};

newProjectBtn.onclick = async () => {
    try {
        await fetch('/api/new_project', {method: 'POST'});
        fetchData();
    } catch (e) {
        console.error(e);
    }
};

async function assignEmployee(empId) {
    // For now, assign to first project; in future, could prompt for selection
    const projId = projects.length > 0 ? projects[0].id : 1;
    try {
        await fetch('/api/assign', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({employee_id: empId, project_id: projId})
        });
        fetchData();
    } catch (e) {
        console.error(e);
    }
}

async function fireEmployee(empId) {
    try {
        await fetch('/api/fire', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({employee_id: empId})
        });
        fetchData();
    } catch (e) {
        console.error(e);
    }
}

async function createProject() {
    try {
        await fetch('/api/new_project', {method: 'POST'});
        fetchData();
    } catch (e) {
        console.error(e);
    }
}

// Animation loop - removed projects drawing
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawOffice();
    employees.forEach(drawEmployee);
    // drawProjects(); removed
    animationFrameId = requestAnimationFrame(animate);
}

// Simulate events (translated)
setInterval(() => {
    const events = ['新想法！+10 進度', '發現錯誤！-5 進度', '會議時間！', '員工加班！', '項目延遲！'];
    const event = events[Math.floor(Math.random() * events.length)];
    eventsLog.innerHTML += `<p>${new Date().toLocaleTimeString('zh-HK')} - ${event}</p>`;
    // Keep log to last 10
    const ps = eventsLog.querySelectorAll('p');
    if (ps.length > 10) ps[0].remove();
}, 5000);

// Init
fetchData();
animate();
setInterval(fetchData, 10000); // Refresh every 10s
