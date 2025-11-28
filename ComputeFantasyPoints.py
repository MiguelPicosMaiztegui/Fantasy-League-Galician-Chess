import sqlite3

DB_NAME = "fantasy_chess.db"

def table_exists(cursor, table_name):
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    )
    return cursor.fetchone() is not None


def table_has_rows(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0] > 0


def update_matches(cursor):
    cursor.execute("""
        SELECT rowid, division, result
        FROM matches
    """)
    rows = cursor.fetchall()
    for rowid, division, result in rows:
        if 'HONRA' in division:
            ratio_D = 4.
        elif 'PREFERENTE' in division:
            ratio_D = 2.
        elif 'PRIMEIRA' in division:
            ratio_D = 1.
        else:
            ratio_D = 0.5
        if 'HONRA' in division or 'PREFERENTE' in division:
            if result == 12:
                match_points = 10
            elif result > 8:
                match_points = 8
            elif result > 6:
                match_points = 5
            elif result == 6:
                match_points = 3
            elif result > 3:
                match_points = 1
            else:
                match_points = 0
        else:
            if result == 8:
                match_points = 10
            elif result > 5:
                match_points = 8
            elif result > 3:
                match_points = 5
            elif result == 3:
                match_points = 3
            elif result > 2:
                match_points = 1
            else:
                match_points = 0
        fantasy_points = int(round(ratio_D*match_points))
        cursor.execute("""
                UPDATE matches
                SET fantasy_points = ?
                WHERE rowid = ?
            """, (fantasy_points, rowid))

def update_games(cursor):
    cursor.execute("""
        SELECT rowid, division, board, game_result, match_result
        FROM games
    """)
    rows = cursor.fetchall()

    for rowid, division, board, game_result, match_result in rows:
        if 'HONRA' in division:
            ratio_D = 2.
        elif 'PREFERENTE' in division:
            ratio_D = 1.5
        elif 'PRIMEIRA' in division:
            ratio_D = 1.
        else:
            ratio_D = 0.5
        if 'HONRA' in division or 'PREFERENTE' in division:
            ratio_B = 1. + 1. * (6. - board)/5.
            if match_result == 12:
                match_points = 10
            elif match_result > 8:
                match_points = 8
            elif match_result > 6:
                match_points = 5
            elif match_result == 6:
                match_points = 3
            elif match_result > 3:
                match_points = 1
            else:
                match_points = 0
        else:
            ratio_B = 1. + 1. * (4. - board)/3.
            if match_result == 8:
                match_points = 10
            elif match_result > 5:
                match_points = 8
            elif match_result > 3:
                match_points = 5
            elif match_result == 3:
                match_points = 3
            elif match_result > 2:
                match_points = 1
            else:
                match_points = 0
        if game_result == 2:
            game_points = 10
        elif game_result == 1:
            game_points = 5
        else:
            game_points = 2

        fantasy_points = int(round((game_points+match_points)*ratio_B*ratio_D))

        cursor.execute("""
            UPDATE games
            SET fantasy_points = ?
            WHERE rowid = ?
        """, (fantasy_points, rowid))


def main():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ============================
    # 1. Comprobar que las tablas existen
    # ============================
    required_tables = ["matches", "games"]
    missing_tables = [t for t in required_tables if not table_exists(cursor, t)]

    if missing_tables:
        print("❌ ERROR: Las siguientes tablas NO existen:", missing_tables)
        print("No se hace ningún cálculo.")
        conn.close()
        return

    # ============================
    # 2. Comprobar que ambas tablas tienen datos
    # ============================
    empty_tables = [t for t in required_tables if not table_has_rows(cursor, t)]

    if empty_tables:
        print("⚠️ AVISO: Las siguientes tablas NO tienen datos:", empty_tables)
        print("No se hace ningún cálculo.")
        conn.close()
        return

    # ============================
    # 3. Si todo está OK → Actualizar fantasy points
    # ============================
    print("✔️ Tablas correctas. Actualizando puntos...")

    update_matches(cursor)
    update_games(cursor)

    conn.commit()
    conn.close()

    print("✔️ Actualización completada.")


if __name__ == "__main__":
    main()
