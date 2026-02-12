const canvas = document.getElementById('dashboard');
const ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false; // pixelated

let data = {};
let animationFrame = 0;

// Load assets - placeholders for now
const assets = {
    background: 'static/images/office_bg.png', // TODO: download office background
    employeeIdle: 'static/images/employee_idle.png',
    employeeWorking: 'static/images/employee_working.png',
    boss: 'static/images/boss.png',
    button: 'static/images/button.png',
    desk: 'static/images/desk.png'
};

// Preload images
function preloadImages() {
    const promises = Object.values(assets).map(src => {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = () => resolve(null); // placeholder if not found
            img.src = src;
        });
    });
    return Promise.all(promises);
}

async function loadData() {
    try {
        const response = await fetch('/api/dashboard');
        data = await response.json();
        draw();
    } catch (e) {
        console.error(e);
        document.getElementById('status').textContent = '加载失败';
    }
}

function draw() {
    // Clear
    ctx.fillStyle = '#e0ffff';
    ctx.fillRect(0, 0, 600, 480);

    // Background - draw office
    // ctx.drawImage(assets.background, 0, 0, 600, 480); // TODO

    // Draw desks with shadows
    data.employees.forEach(emp => {
        const x = emp.position.x;
        const y = emp.position.y;
        // Desk shadow
        ctx.fillStyle = 'rgba(0,0,0,0.3)';
        ctx.fillRect(x-10, y+20, 80, 10);
        // Desk
        ctx.fillStyle = '#8b4513'; // brown
        ctx.fillRect(x, y+10, 80, 40);
        // Employee glow/shadow
        if (emp.status === 'busy') {
            ctx.shadowColor = '#00ff00';
            ctx.shadowBlur = 10;
        } else {
            ctx.shadowBlur = 0;
        }
        // Draw employee sprite
        const sprite = emp.animation === 'working' ? assets.employeeWorking : assets.employeeIdle;
        if (sprite) {
            // Animate frame
            const frame = Math.floor(animationFrame / 10) % 4; // assume 4 frames
            ctx.drawImage(sprite, frame * 32, 0, 32, 32, x+24, y-32, 32, 32);
        } else {
            // Placeholder
            ctx.fillStyle = emp.status === 'busy' ? '#ff0000' : '#0000ff';
            ctx.fillRect(x+24, y-32, 32, 32);
        }
        ctx.shadowBlur = 0;

        // Progress bar
        ctx.fillStyle = '#000';
        ctx.fillRect(x, y+50, 80, 8);
        ctx.fillStyle = '#00ff00';
        ctx.fillRect(x, y+50, (emp.progress / 100) * 80, 8);
    });

    // Boss at top
    const ceo = data.ceo;
    const bossX = 300;
    const bossY = 50;
    // Boss desk
    ctx.fillStyle = '#8b4513';
    ctx.fillRect(bossX-20, bossY+10, 120, 40);
    // Boss sprite
    if (ceo.status === 'busy') {
        ctx.shadowColor = '#ff00ff';
        ctx.shadowBlur = 15;
    }
    const bossSprite = assets.boss;
    if (bossSprite) {
        ctx.drawImage(bossSprite, bossX-16, bossY-32, 32, 32);
    } else {
        ctx.fillStyle = '#ffff00';
        ctx.fillRect(bossX-16, bossY-32, 32, 32);
    }
    ctx.shadowBlur = 0;

    // Text labels in Chinese
    ctx.fillStyle = '#00ff00';
    ctx.font = '8px Press Start 2P';
    ctx.fillText('CEO: ' + (ceo.status === 'busy' ? '忙碌' : '空闲'), 10, 20);
    data.employees.forEach((emp, i) => {
        ctx.fillText(emp.name + ': ' + (emp.status === 'busy' ? '工作' : '空闲'), 10, 100 + i*30);
    });

    // Projects list
    ctx.fillText('项目:', 500, 20);
    data.projects.forEach((proj, i) => {
        ctx.fillText(proj.name, 500, 50 + i*20);
    });

    animationFrame++;
    requestAnimationFrame(draw);
}

document.getElementById('refresh').addEventListener('click', loadData);

preloadImages().then(() => {
    loadData();
    setInterval(loadData, 30000); // refresh every 30s
});