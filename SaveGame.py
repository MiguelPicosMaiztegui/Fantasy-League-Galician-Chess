import sqlite3

conn = sqlite3.connect("fantasy_chess.db")
cur = conn.cursor()

games_list = []
games_list.append((22,"Miguel","Picos Maiztegui","CFX","HONOR",2024,4,2,1,4))
for g in games_list:
    cur.execute("""
    INSERT OR IGNORE INTO games (id_player, name, surnames, team_name, division,
                            year, round, board, game_result, match_result)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, g)
#id_player INTEGER,
#name TEXT,
#surnames TEXT,
#team_name TEXT,
#division TEXT,
#year INTEGER,
#round INTEGER,
#board INTEGER,
#game_result INTEGER,
#match_result INTEGER

conn.commit()
conn.close()








































