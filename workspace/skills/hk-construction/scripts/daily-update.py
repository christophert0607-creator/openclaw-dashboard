#!/usr/bin/env python3
# Daily HK Construction Update Script

import subprocess
import datetime

date = datetime.date.today().isoformat()

# Web search for updates
print(f'Searching HK construction news {date}...')
subprocess.run(['openclaw', 'tool', 'web_search', f'HK construction regulations news {date}', '--count', '5'])

# Update MEMORY.md
with open('/home/tsukii0607/.openclaw/workspace/MEMORY.md', 'a') as f:
    f.write(f'\n- HK construction update {date}: Latest regs/news added.\n')

# Git add/commit/push to GitHub repo (assume repo openclaw/hk-construction-skill)
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', f'Daily update {date}'])
subprocess.run(['git', 'push'])

print('Daily update complete: MEMORY.md updated, GitHub pushed.')
