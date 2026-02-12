const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

app.get('/api/session_status', async (req, res) => {
  try {
    const { stdout } = await execPromise('openclaw session_status --json');
    const data = JSON.parse(stdout);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/sessions_list', async (req, res) => {
  try {
    const { stdout } = await execPromise('openclaw sessions_list --json');
    const data = JSON.parse(stdout);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/users', (req, res) => {
  res.json([{ id: 1, name: 'User1' }]); // Mock
});

app.get('/api/projects', (req, res) => {
  res.json([{ id: 1, name: 'Project1' }]); // Mock
});

app.listen(port, () => {
  console.log(`Backend running on http://localhost:${port}`);
});
