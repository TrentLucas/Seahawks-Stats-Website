// Backend of Seahawks Seasonal Performance Database
// 
// Communicates with front end and server/database
// - get tables from database
// - accepts queries from front end and sends them to the server
// 
// ***ALL CODE TO BE USED TO VIEWING PURPOSES ONLY. NO REUSING CODE FROM PROJECT***
///////////////////////////////////////////////////////////////////////////////////////



const express = require('express');
const bodyParser = require('body-parser');
const sql = require('mssql');
const cors = require('cors');

const app = express();
app.use(bodyParser.json());
app.use(cors());



// database login details
const dbConfig = {
  server: 'seahawks-server.database.windows.net',
  user: 'OogahBoogah',
  password: 'CSS475Fall2023',
  database: 'seahawksdatabase',
  options: {
    encrypt: true,
  }
};

// set pool
const pool = new sql.ConnectionPool(dbConfig);

// list of all tables in database
const tables = {
    seasonal: 'seasonal_performance',
    offensive: 'offensive_team_performance',
    defensive: 'defensive_team_performance',
    specialTeams: 'special_team_performance',
    kicker: 'kicker_performance',
    wideReceiver: 'wide_receiver_performance',
    quarterback: 'quarterback_performance',
    cornerback: 'cornerback_performance'
}

// function to make a query on the database
const executeQuery = async (tableName, res) => {
  let connection;

  try {
    // establish a connection to the database
    connection = await pool.connect();

    // results from the query
    const result = await connection.request().query(`SELECT * FROM ${tableName}`);

    // res = results as a json
    res.json(result.recordset);
  } catch (err) {

    console.error('Error executing SQL query:', err);
    res.status(500).json({ error: 'Internal Server Error' });

  } finally {

    // end the connection
    if (connection) {
      connection.release();
    }
  }
};



// log when a request is asked from front end
app.use((req, res, next) => {
  console.log(`Received request for: ${req.url}`);
  next();
});

// output onto the webpage the back end is connected is online
app.get('/', (req, res) => {
    res.send('Server is running!');
});

// return seasonal_performance table
app.get('/seasonal_performance', (req, res) => {
    executeQuery(tables.seasonal, res);
});

// return offensive_team_performance table
app.get('/offensive_team_performance', (req, res) => {
    executeQuery(tables.offensive, res);
});

// return defensive_team_performance table
app.get('/defensive_team_performance', (req, res) => {
    executeQuery(tables.defensive, res);
});

// return special_team_performance table
app.get('/special_team_performance', (req, res) => {
    executeQuery(tables.specialTeams, res);
});

// return kicker_performance table
app.get('/kicker_performance', (req, res) => {
    executeQuery(tables.kicker, res);
});

// return wide_receiver_performance table
app.get('/wide_receiver_performance', (req, res) => {
    executeQuery(tables.wideReceiver, res);
});

// return quarterback_performance table
app.get('/quarterback_performance', (req, res) => {
    executeQuery(tables.quarterback, res);
});

// return cornerback_performance table
app.get('/cornerback_performance', (req, res) => {
    executeQuery(tables.cornerback, res);
});

// post a query to the database to modify or search data
app.post('/executeQuery', async (req, res) => {
  const { query } = req.body;

  // fail case: query is empty
  if (!query) {
    return res.status(400).json({ error: 'Query cannot be empty' });
  }

  let connection;

  try {
    // establish a connection to the database
    connection = await pool.connect();

    // results from the query
    const result = await connection.request().query(query);

    // res = results as a json
    res.json(result.recordset);
  } catch (err) {

    console.error('Error executing custom SQL query:', err);
    res.status(500).json({ error: 'Internal Server Error' });

  } finally {

    // end the connection
    if (connection) {
      connection.release();
    }
  }
});

// console log if server is working on 'x' port
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
