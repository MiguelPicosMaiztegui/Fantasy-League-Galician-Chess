import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("Fantasy_Chess.db")
cursor = conn.cursor()

# Crear tabla players si no existe
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

# Comprobar que la tabla games existe y tiene datos
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='games'")
if cursor.fetchone() is None:
    print("La tabla games no existe.")
    conn.close()
    exit()

cursor.execute("SELECT COUNT(*) FROM games")
if cursor.fetchone()[0] == 0:
    print("La tabla games está vacía.")
    conn.close()
    exit()

# Obtener todos los jugadores únicos
cursor.execute("SELECT DISTINCT id_player FROM games")
players = cursor.fetchall()

for player in players:
    id_player = player[0]
    if id_player < 10: 
        continue
    # Obtener años disponibles para ese jugador
    cursor.execute("SELECT DISTINCT year FROM games WHERE id_player=?", (id_player,))
    years = [row[0] for row in cursor.fetchall()]
    if not years:
        continue

    last_year_player = max(years)

    cursor.execute("SELECT DISTINCT year FROM games")
    years= [row[0] for row in cursor.fetchall()]
    last_year = max(years)
    prev_year = last_year - 1
    cursor.execute("Select name, surnames, team_name, division FROM games WHERE id_player=? AND year=?", (id_player,last_year_player))
    row = cursor.fetchone()
    if row is None:
        continue
    else:
        name, surnames, team_name, division = row

    cursor.execute(
        "SELECT SUM(fantasy_points) FROM games WHERE id_player=? AND year=? AND division=?",
        (id_player, last_year, division)
    )
    total_points_actual = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT COUNT(DISTINCT round) FROM games WHERE year=? AND division=?",
        (last_year, division)
    )
    total_rounds_actual = cursor.fetchone()[0] or 1  # evitar división por cero

    media_fantasy_actual = total_points_actual / total_rounds_actual

    # Calcular media_fantasy_previous normalizada por número de rondas
    cursor.execute(
        "SELECT SUM(fantasy_points) FROM games WHERE id_player=? AND year=? AND division=?",
        (id_player, prev_year, division)
    )
    total_points_previous = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT COUNT(DISTINCT round) FROM games WHERE year=? AND division=?",
        (prev_year, division)
    )
    total_rounds_previous = cursor.fetchone()[0] or 1

    media_fantasy_previous = total_points_previous / total_rounds_previous

    # Calcular valor_mercado (ejemplo: suma de fantasy_points totales)
    cursor.execute(
        "SELECT SUM(fantasy_points) FROM games WHERE id_player=?",
        (id_player,)
    )
    valor_mercado = cursor.fetchone()[0] or 0

    # Insertar o actualizar en la tabla players
    cursor.execute("""
        INSERT INTO players (id_player, name, surnames, equipo, media_fantasy_actual, media_fantasy_previous, valor_mercado)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id_player) DO UPDATE SET
            name=excluded.name,
            surnames=excluded.surnames,
            equipo=excluded.equipo,
            media_fantasy_actual=excluded.media_fantasy_actual,
            media_fantasy_previous=excluded.media_fantasy_previous,
            valor_mercado=excluded.valor_mercado
    """, (id_player, name, surnames, team_name, media_fantasy_actual, media_fantasy_previous, valor_mercado))

# Guardar cambios y cerrar
conn.commit()
conn.close()

print("Tabla players actualizada correctamente.")
