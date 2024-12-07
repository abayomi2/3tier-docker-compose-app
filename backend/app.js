const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');  // Import CORS middleware

const app = express();
app.use(express.json());

// Enable CORS for all origins
app.use(cors());

// Or, if you want to limit it to a specific origin (e.g., frontend running on localhost:3000)
// app.use(cors({
  origin: 'http://54.166.23.106:3000'  // Allow requests only from the frontend
// }));

// Create a pool to manage database connections
const db = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: 'ecommerce_db',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

// Example route to fetch all products
app.get('/products', async (req, res) => {
  try {
    const [results] = await db.promise().query('SELECT * FROM products');
    res.json(results);
  } catch (err) {
    console.error('Error fetching products:', err);
    res.status(500).send('Server error');
  }
});

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
