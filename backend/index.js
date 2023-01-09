const express = require('express');
const app = express();
const cors = require('cors');

const db = require('better-sqlite3')('stats.db')
const port = 3001;



const corsOptions = {
  origin: '*',
  credentials: true,
  optionSuccessStatus: 200
}

app.use(cors(corsOptions));

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.get('/analyze', (req, res) => {
  res.send('this is the analyze endpoint');
});

app.get('/stats/:game_id', (req, res) => {
    // this is where we would collect stats about each game
});

// returns a list of captains and their names
app.get('/teams', (req, res) => {
  let rows = db.prepare("SELECT id, captain, name FROM teams").all();
  console.log('sending teams');
  res.json({rows});
});

// take an id and return that team's roster and games
app.get('/teams/:teamId', (req, res) => {
  let id = req.params.teamId;
  if(isNaN(id)) {
    return res.status(400).send("Invalid team id");
  }

  let teamInfo = db.prepare("SELECT captain, name FROM teams WHERE id == ?").get(id);

  let matches = db.prepare("SELECT week, score, teams.name AS enemy, enemy_score FROM matches\
                          INNER JOIN teams ON matches.enemy_team_id == teams.id\
                          WHERE matches.team_id == ?").all(id);

  let games = db.prepare("SELECT games.week, games.id, maps.name AS map, team_stats.score, team_stats.enemy_score FROM games\
                        INNER JOIN maps ON games.map_id == maps.id\
                        INNER JOIN team_stats ON team_stats.game_id == games.id\
                        WHERE team_stats.team_id == ?").all(id);


  let players = db.prepare("SELECT x.id, (\
                              SELECT name FROM player_names\
                              WHERE player_names.player_id == x.id\
                              GROUP BY name\
                              ORDER BY count(1) DESC\
                              LIMIT 1\
                            ) AS name, players.round_pick AS round\
                            FROM (SELECT id FROM players WHERE players.team_id == ?) x\
                            INNER JOIN players ON players.id == x.id\
                            ORDER BY round").all(id);

  // TODO: is it possible to integrate this into the sql statement above?
  // I already tried for hours to get where I'm at now lol
  for(let i = 0; i < players.length; i++) {
    let player_id = players[i]['id'];
    players[i]['aliases'] = db.prepare("SELECT name FROM player_names\
                                        WHERE player_names.player_id == ?\
                                        GROUP BY name").all(player_id);
  }
  console.log(players);

  // let players = db.prepare("").all();
  res.json({
    team_name: teamInfo['name'],
    captain: teamInfo['captain'],
    matches: matches,
    games: games,
    players: players,
  });
});