const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

app.get('/api/users', (req, res) => {
  res.json({ users: 1234 });
});

app.get('/api/projects', (req, res) => {
  res.json({ projects: 56 });
});

app.get('/api/session_status', (req, res) => {
  exec('openclaw status', (error, stdout, stderr) => {
    if (error) {
      res.status(500).json({ error: stderr });
      return;
    }
    res.json({ status: stdout });
  });
});

app.get('/api/sessions_list', (req, res) => {
  exec('openclaw sessions', (error, stdout, stderr) => {
    if (error) {
      res.status(500).json({ error: stderr });
      return;
    }
    res.json({ sessions: stdout });
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
