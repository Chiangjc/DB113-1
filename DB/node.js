const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json()); // 用於解析 JSON 請求

const pool = new Pool({
  host: '127.0.0.1',
  user: 'postgres',
  password: 'chiang20161231',
  database: 'Final',
  port: 5432
});

pool.connect((err, client, release) => {
  if (err) {
    console.error('Error connecting to database:', err);
    return;
  }
  console.log('Connected to database');
  release();
});

// 根據 e_id 查詢 mgr_id
app.get('/getMgrId/:e_id', async (req, res) => {
  const e_id = req.params.e_id;
  try {
    const result = await pool.query('SELECT mgr_id FROM employee WHERE e_id = $1', [e_id]);
    if (result.rows.length > 0) {
      res.json(result.rows[0]);
    } else {
      res.status(404).json({ error: 'Employee not found' });
    }
  } catch (err) {
    console.error('Error executing query:', err);
    res.status(500).json({ error: 'Database query error' });
  }
});

// 根據 f_id 查詢 super_id
app.get('/getSuperId/:f_id', async (req, res) => {
  const f_id = req.params.f_id;
  try {
    const result = await pool.query('SELECT super_id FROM factory WHERE f_id = $1', [f_id]);
    if (result.rows.length > 0) {
      res.json(result.rows[0]);
    } else {
      res.status(404).json({ error: 'Factory not found' });
    }
  } catch (err) {
    console.error('Error executing query:', err);
    res.status(500).json({ error: 'Database query error' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
