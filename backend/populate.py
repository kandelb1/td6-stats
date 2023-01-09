import sqlite3
import csv
import requests
import json

print('hello my name is python')
print('i am going to parse this csv, get the results, and put it into a database')

con = sqlite3.connect('stats.db')
cur = con.cursor()

# index + 1 == id
team_names = []

with open('team_names.csv') as file:
  reader = csv.DictReader(file)
  for row in reader:
    team_values = (row['captain'], row['teamname'])
    team_names.append(team_values[1])
    cur.execute('INSERT INTO teams (captain, name) VALUES (?, ?)', team_values)
    con.commit()

with open('tournament_results.csv') as file:
  reader = csv.DictReader(file)
  for row in reader:
    match_values = (row['week'], row['redTeamId'], row['redScore'], row['blueTeamId'], row['blueScore'])
    cur.execute('INSERT INTO matches (week, team_id, score, enemy_team_id, enemy_score) VALUES (?, ?, ?, ?, ?)', match_values)
    match_values = (row['week'], row['blueTeamId'], row['blueScore'], row['redTeamId'], row['redScore'])
    cur.execute('INSERT INTO matches (week, team_id, score, enemy_team_id, enemy_score) VALUES (?, ?, ?, ?, ?)', match_values)
    con.commit()

round_one_ids = {}
players = {}
with open('players.csv') as file:
  reader = csv.DictReader(file)
  for row in reader:
    if(row['roundPick']) == '1':
      round_one_ids[row['playerId']] = row['teamId']
    players[row['playerId']] = row['teamId']
    player_values = (row['playerId'], row['roundPick'], row['teamId'])
    cur.execute('INSERT INTO players (id, round_pick, team_id) VALUES (?, ?, ?)', player_values)
    con.commit()

# print(round_one_ids)
print(players)
game_ids = set()

with open('matches.csv') as file:
  reader = csv.DictReader(file)
  i = 0
  for row in reader:
    r = requests.get(url = row['link'] + '.json')
    data = r.json()
    # print(data)
    print('##############################')

    map = data['map']
    game = data['game']
    server = data['server']
    pgstats = data['pgstats']
    team_stats = data['tgstats']
    
    map_values = (map['map_id'], map['name'])
    cur.execute('SELECT * FROM maps WHERE id == ?', map_values[0:1])
    rows = cur.fetchall()
    # TODO we need to add image blobs to the MAPS table. I have the levelshots ready and I want them in the database.
    if len(rows) == 0: # only put this map into the db if it wasn't already there
      # ------------------------- INSERT INTO MAPS TABLE -------------------------
      cur.execute('INSERT INTO maps (id, name) VALUES (?, ?)', map_values)
      con.commit()

    server_values = (server['server_id'], server['name'])
    cur.execute('SELECT * FROM servers WHERE id == ?', server_values[0:1])
    rows = cur.fetchall()
    if len(rows) == 0: # only put this server into the db if it wasn't already there
      # ------------------------- INSERT INTO SERVERS TABLE -------------------------
      cur.execute('INSERT INTO servers (id, name) VALUES (?, ?)', server_values)
      con.commit()
    
    stop = False

    red_score = team_stats[0]['rounds'] if team_stats[0]['team'] == 1 else team_stats[1]['rounds']
    blue_score = team_stats[0]['rounds'] if team_stats[0]['team'] == 2 else team_stats[1]['rounds']
    print(f"red vs. blue: {red_score} to {blue_score}")
    
    # print(data['stats_by_team']['1'])
    red_ids = []
    blue_ids = []
    for p in data['stats_by_team']['1']:
      red_ids.append(str(p['player_id']))
    for p in data['stats_by_team']['2']:
      blue_ids.append(str(p['player_id']))
          
    red_team_id = -1
    blue_team_id = -1
    for id in red_ids:
      if id in players:
        print('ya')
        red_team_id = players[id]
        break
    for id in blue_ids:
      if id in players:
        blue_team_id = players[id]
        break
    # now we have everything we need...jeez
    print(f"red team id {red_team_id}, score {red_score}")
    print(f"blue team id {blue_team_id}, score {blue_score}")
    team_stats_values = (game['game_id'], blue_team_id, blue_score, red_team_id, red_score)
    cur.execute('INSERT INTO team_stats (game_id, team_id, score, enemy_team_id, enemy_score) VALUES (?, ?, ?, ?, ?)', team_stats_values)
    con.commit()
    team_stats_values = (game['game_id'], red_team_id, red_score, blue_team_id, blue_score)
    cur.execute('INSERT INTO team_stats (game_id, team_id, score, enemy_team_id, enemy_score) VALUES (?, ?, ?, ?, ?)', team_stats_values)
    con.commit()

    pwstats = data['pwstats']
    player_ids = red_ids + blue_ids
    for id in player_ids:
      name = pwstats[id]['nick']
      print(f"player_id {id} has name {name}")
      cur.execute('INSERT INTO player_names (player_id, game_id, name) VALUES (?, ?, ?)', (id, game['game_id'], name))
      con.commit()
      # cur.execute('SELECT * FROM player_names WHERE game_id == ?', game['game_id'])
      # rows = cur.fetchall()
      # if len(rows) == 0: # only put this server into the db if it wasn't already there
      # # ------------------------- INSERT INTO SERVERS TABLE -------------------------
      #   cur.execute('INSERT INTO player_names (player_id, game_id, name) VALUES (?, ?, ?)', (id, game['game_id'], name))
      #   con.commit()


      

    # for pbobject in data['stats_by_team']['1']:
    #   print(pbobject)
    #   if stop: 
    #     break
    #   print(f"is {pbobject['player_id']} in the round one ids?")
    #   if pbobject['player_id'] in round_one_ids:
    #     team_id = round_one_ids[pbobject['player_id']]        
    #     team_score = team_stats[0]['rounds'] if team_stats[0]['team'] == '1' else team_stats[1]['rounds']
    #     print(f"{pbobject['player_id']}  is a round one player, so thus the team is {team_id} and our score is {team_score}")
    #     for pboject2 in data['stats_by_team']['2']:
    #       if pboject2['player_id'] in round_one_ids:
    #         enemy_team_id = round_one_ids[pboject2['player_id']]
    #         enemy_team_score = team_stats[0]['rounds'] if team_stats[0]['team'] == '2' else team_stats[1]['rounds']
    #         print(f"{pbobject['player_id']}  is a round one player, so thus the enemy team is {enemy_team_id} and our score is {enemy_team_score}")
    #         team_stats_values = (game['game_id'], team_id, team_score, enemy_team_id, enemy_team_score)
    #         cur.execute('INSERT INTO team_stats (game_id, team_id, score, enemy_team_id, enemy_score) VALUES (?, ?, ?, ?, ?)', team_stats_values)
    #         con.commit()
    #         team_stats_values = (game['game_id'], enemy_team_id, enemy_team_score, team_id, team_score)
    #         cur.execute('INSERT INTO team_stats (game_id, team_id, score, enemy_team_id, enemy_score) VALUES (?, ?, ?, ?, ?)', team_stats_values)
    #         con.commit()
    #         stop = True
    #         break

    
    # score = team_stats[0]['rounds']
    # enemy_score = team_stats[1]['rounds']
    # team_stats_values = (game['game_id'], row['team1'], score, row['team2'], enemy_score)
    # cur.execute('INSERT INTO team_stats (game_id, team_id, score, enemy_team_id, enemy_score) VALUES (?, ?, ?, ?, ?)', team_stats_values)
    # con.commit()
    # team_stats_values = (game['game_id'], row['team2'], enemy_score, row['team1'], score)
    # cur.execute('INSERT INTO team_stats (game_id, team_id, score, enemy_team_id, enemy_score) VALUES (?, ?, ?, ?, ?)', team_stats_values)
    # con.commit()

    # team_stats_values = (game['game_id'], row['team1'], team_stats[0])
    # cur.execute('INSERT INTO team_stats (game_id, team_id, team_score, enemy_team_id, enemy_score) VALUES (?, ?, ?, ?, ?)', team_stats_values)
    # con.commit()

    # team_stats_values = (game['game_id'], )
    # cur.execute('INSERT INTO team_stats (game_id, team_id, team_score, enemy_team_id, enemy_score) VALUES (?, ?, ?, ?, ?)', team_stats_values)
    # con.commit()

    # # in the json, team 1 == red, team 2 == blue
    # # TODO: grab a player id and use it to verify the red/blue teams are correct (some of them are DEFINITELY wrong so...figure that out)
    # if team_stats[0]['team'] == 1: # red team
    #   rscore = team_stats[0]['rounds']
    #   bscore = team_stats[1]['rounds']
    # else: # blue team
    #   bscore = team_stats[0]['rounds']
    #   rscore = team_stats[1]['rounds']
    game_values = (game['game_id'], server['server_id'], map['map_id'], row['week'])
    cur.execute('INSERT INTO games (id, server_id, map_id, week) VALUES (?, ?, ?, ?)', game_values)
    con.commit()

    # server = data['server']
    # server_values = (server['server_id'], server['name'])

    # cur.execute('SELECT * FROM servers WHERE id == ?', server_values[0:1])
    # rows = cur.fetchall()
    # if len(rows) == 0: # only put this server into the db if it wasn't already there
    #   # ------------------------- INSERT INTO SERVERS TABLE -------------------------
    #   cur.execute('INSERT INTO servers (id, name) VALUES (?, ?)', server_values)
    #   con.commit()
    
    # map = data['map']
    # map_values = (map['map_id'], map['name'])
    
    # cur.execute('SELECT * FROM maps WHERE id == ?', map_values[0:1])
    # rows = cur.fetchall()
    # # TODO we need to add image blobs to the MAPS table. I have the levelshots ready and I want them in the database.
    # if len(rows) == 0: # only put this map into the db if it wasn't already there
    #   # ------------------------- INSERT INTO MAPS TABLE -------------------------
    #   cur.execute('INSERT INTO maps (id, name) VALUES (?, ?)', map_values)
    #   con.commit()

    # game = data['game']
    # # TODO: double check whether the team colors are always correct
    # # it looks like it is but we can always pull the data from the game.
    # # in the json, team 1 == red, team 2 == blue
    # game_values = (game['game_id'], server['server_id'], game['game_type_cd'], map['map_id'], row['team1'], row['team2'])
    # cur.execute('SELECT * FROM games WHERE id == ?', game_values[0:1])
    # rows = cur.fetchall()
    # if len(rows) == 0: # only put this game into the db if it wasn't already there
    #         # ------------------------- INSERT INTO GAMES TABLE -------------------------
    #   cur.execute('INSERT INTO games (id, server_id, gametype, map_id, red_team_id, blue_team_id) VALUES (?, ?, ?, ?, ?, ?)', game_values)
    #   con.commit()

    # player_game_stats = data['pgstats']
    # player_ids = [d.get('player_id') for d in player_game_stats]

    # player_weapon_stats = data['pwstats']
    # for id in player_ids:
    #   name = player_weapon_stats[str(id)]['nick']
    #   print("player id {} has name {}".format(id, name))
    #   player_name_values = (id, game['game_id'], name)
    #   cur.execute('INSERT INTO player_names (player_id, game_id, name) VALUES (?, ?, ?)', player_name_values)
    #   con.commit()

print('Done populating database.')
cur.close()
con.close()