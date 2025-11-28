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
    media_fantasy_actual REAL DEFAULT 0,
    media_fantasy_previous REAL DEFAULT 0,
    valor_mercado REAL DEFAULT 0,
    UNIQUE(id_player)
)
""")
# Crear tabla jugadores
cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id_team INTEGER,
    name TEXT NOT NULL,
    division TEXT,
    media_fantasy_actual REAL DEFAULT 0,
    media_fantasy_previous REAL DEFAULT 0,
    valor_mercado REAL DEFAULT 0,
    UNIQUE(id_team)
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
    result INTEGER,
    fantasy_points INTEGER DEFAULT 0,
    UNIQUE(team_name, year, round)
)
""")

# Crear tabla partidas
cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    id_player INTEGER,
    name TEXT,
    surnames TEXT,
    team_name TEXT,
    division TEXT,
    year INTEGER,
    round INTEGER,
    board INTEGER,
    game_result INTEGER,
    match_result INTEGER,
    fantasy_points INTEGER DEFAULT 0,
    UNIQUE(id_player, year, round)
)
""")

conn.commit()
