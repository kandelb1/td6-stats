const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.get('/analyze', (req, res) => {
  res.send('this is the analyze endpoint');
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});

app.get('/stats/:game_id', (req, res) => {
    // this is where we would collect stats about each game
});