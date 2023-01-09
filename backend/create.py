import sqlite3

con = sqlite3.connect('stats.db')
cur = con.cursor()




# cur.execute('DROP TABLE IF EXISTS game_stats')
# con.commit('')

cur.execute('DROP TABLE IF EXISTS players')
cur.execute('CREATE TABLE players (id INTEGER PRIMARY KEY, round_pick INTEGER, team_id INTEGER)')

cur.execute('DROP TABLE IF EXISTS player_names')
cur.execute('CREATE TABLE player_names (player_id INTEGER, game_id INTEGER, name TEXT)')

cur.execute('DROP TABLE IF EXISTS player_stats')
cur.execute('CREATE TABLE player_stats (player_id INTEGER, etc FUCK)')

cur.execute('DROP TABLE IF EXISTS maps')
cur.execute('CREATE TABLE maps (id INTEGER PRIMARY KEY, name TEXT)')

cur.execute('DROP TABLE IF EXISTS servers')
cur.execute('CREATE TABLE servers (id INTEGER PRIMARY KEY, name TEXT)')

cur.execute('DROP TABLE IF EXISTS games')
cur.execute('CREATE TABLE games (id INTEGER PRIMARY KEY, server_id INTEGER, map_id INTEGER, week INTEGER)')

cur.execute('DROP TABLE IF EXISTS teams')
cur.execute('CREATE TABLE teams (id INTEGER PRIMARY KEY AUTOINCREMENT, captain TEXT, name TEXT)')

cur.execute('DROP TABLE IF EXISTS team_stats')
cur.execute('CREATE TABLE team_stats (game_id INTEGER, team_id INTEGER, score INTEGER, enemy_team_id INTEGER, enemy_score INTEGER)')

cur.execute('DROP TABLE IF EXISTS matches')
cur.execute('CREATE TABLE matches (id INTEGER PRIMARY KEY AUTOINCREMENT, week INTEGER, team_id INTEGER, score INTEGER, enemy_team_id INTEGER, enemy_score INTEGER)')

print('Done creating database stats.db')

cur.close()
con.close()