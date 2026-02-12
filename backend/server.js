const express = require('express');
const cors = require('cors');
const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

app.get('/api/users', (req, res) => {
  res.json({ users: 1234 });
});

app.get('/api/projects', (req, res) => {
  res.json({ projects: 56 });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
