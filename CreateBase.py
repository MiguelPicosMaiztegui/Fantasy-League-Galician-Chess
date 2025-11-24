import sqlite3

# Conexión a la base de datos (se crea si no existe)
conn = sqlite3.connect("Fantasy_Chess.db")
cursor = conn.cursor()

# Crear tabla jugadores
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id_player INTEGER,
    name TEXT NOT NULL,
    surnames TEXT NOT NULL,
    equipo TEXT,
    puntos INTEGER,
    valor_mercado REAL
)
""")

# Crear tabla encuentros
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    team_name TEXT,
    enemy_team TEXT,
    division TEXT,
    year INTEGER,
    round INTEGER,
    result INTEGER
)
""")

# Crear tabla partidas
cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    id_player INTEGER,
    name TEXT,
    surnames TEXT,
    division TEXT,
    year INTEGER,
    round INTEGER,
    board INTEGER,
    game_result INTEGER,
    match_result INTEGER
)
""")

conn.commit()
