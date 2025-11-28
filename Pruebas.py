import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("Fantasy_Chess.db")
cursor = conn.cursor()
id_player = 0
cursor.execute("SELECT DISTINCT name FROM games WHERE id_player=?", (id_player,))

rows = cursor.fetchall()

for row in rows:
    print(row)