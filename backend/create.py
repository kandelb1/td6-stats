import sqlite3

con = sqlite3.connect('stats.db')
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS servers')
cur.execute('DROP TABLE IF EXISTS maps')
cur.execute('DROP TABLE IF EXISTS players')
cur.execute('DROP TABLE IF EXISTS player_names')
# cur.execute('DROP TABLE IF EXISTS player_weapon_stats')
cur.execute('DROP TABLE IF EXISTS weeks')
cur.execute('DROP TABLE IF EXISTS games')

cur.execute('CREATE TABLE servers (id INTEGER PRIMARY KEY, name TEXT)')
cur.execute('CREATE TABLE maps (id INTEGER PRIMARY KEY, name TEXT)')
cur.execute('CREATE TABLE players (id INTEGER PRIMARY KEY)')
cur.execute('CREATE TABLE player_names (player_id INTEGER, game_id INTEGER, name TEXT)')
cur.execute('CREATE TABLE weeks (week_num INTEGER, game_id INTEGER, red_captain TEXT, red_team TEXT, red_score INTEGER, blue_captain TEXT, blue_team TEXT, blue_score INTEGER)')
cur.execute('CREATE TABLE games (id INTEGER PRIMARY KEY, server_id INTEGER, gametype TEXT, map_id INTEGER)')

print('Done creating database stats.db')

cur.close()
con.close()