import sqlite3
import csv
import requests
import json

print('hello my name is python')
print('i am going to parse this csv, get the results, and put it into a database')

con = sqlite3.connect('stats.db')
cur = con.cursor()


with open('test_matches.csv') as file:
  reader = csv.DictReader(file)
  # next(reader) # skip the header
  for row in reader:
    print(row)
    # print(row['link'])
    red_captain = row['team1']
    blue_captain = row['team2']
    r = requests.get(url = row['link'] + '.json')
    data = r.json()

    server = data['server']
    server_values = (server['server_id'], server['name'])

    cur.execute('SELECT * FROM servers WHERE id == ?', server_values[0:1])
    rows = cur.fetchall()
    if len(rows) == 0: # only put this server into the db if it wasn't already there
      # ------------------------- INSERT INTO SERVERS TABLE -------------------------
      cur.execute('INSERT INTO servers (id, name) VALUES (?, ?)', server_values)
      con.commit()
    
    map = data['map']
    map_values = (map['map_id'], map['name'])
    
    cur.execute('SELECT * FROM maps WHERE id == ?', map_values[0:1])
    rows = cur.fetchall()
    # TODO we need to add image blobs to the MAPS table. I have the levelshots ready and I want them in the database.
    if len(rows) == 0: # only put this map into the db if it wasn't already there
      # ------------------------- INSERT INTO MAPS TABLE -------------------------
      cur.execute('INSERT INTO maps (id, name) VALUES (?, ?)', map_values)
      con.commit()

    game = data['game']
    game_values = (game['game_id'], server['server_id'], game['game_type_cd'], map['map_id'])
    cur.execute('SELECT * FROM games WHERE id == ?', game_values[0:1])
    rows = cur.fetchall()
    if len(rows) == 0: # only put this game into the db if it wasn't already there
            # ------------------------- INSERT INTO GAMES TABLE -------------------------
      cur.execute('INSERT INTO games (id, server_id, gametype, map_id) VALUES (?, ?, ?, ?)', game_values)
      con.commit()

    player_game_stats = data['pgstats']
    player_ids = [d.get('player_id') for d in player_game_stats]

    player_weapon_stats = data['pwstats']
    for id in player_ids:
      name = player_weapon_stats[str(id)]['nick']
      print("player id {} has name {}".format(id, name))
      player_name_values = (id, game['game_id'], name)
      cur.execute('INSERT INTO player_names (player_id, game_id, name) VALUES (?, ?, ?)', player_name_values)
      con.commit()

    
    # for id in player_ids:
    #   cur.execute('SELECT * FROM players WHERE id == ?', (id,))
    #   rows = cur.fetchall()
    #   if len(rows) == 0: # only put this player into the db if it wasn't already there
    #     cur.execute('INSERT INTO players (id) VALUES (?)')
    #     con.commit()

    # player_ids = map(lambda x: x['player_id'], players. )
    # print(player_ids)

    # filename = "W{} {} vs. {} Map #{}.json".format(row['week'], row['team1'], row['team2'], row['mapnum'])
    # with open(filename, 'w') as file:
    #   pretty = json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True)
    #   print(pretty)
    #   file.write(pretty)

print('Done populating database.')
cur.close()
con.close()