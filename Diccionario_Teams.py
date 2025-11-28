import sqlite3

# Conectamos a la base de datos
conn = sqlite3.connect("Fantasy_Chess.db")
cursor = conn.cursor()

# Obtenemos todos los nombres de equipos distintos
cursor.execute("SELECT DISTINCT team_name FROM matches")
teams = [row[0] for row in cursor.fetchall()]

# Diccionario para mapear nombres a ids
team_ids = {}
# Lista de ids ya usados
used_ids = []

for team_name in teams:
    if team_name in team_ids:
        continue  # ya procesado

    while True:
        print(f"\nEquipo: {team_name}")
        respuesta = input("¿Crear nuevo id? (Enter = sí / cualquier otra cosa = no): ").strip()
        
        if respuesta == "":
            # Crear nuevo id
            new_id = max(used_ids, default=0) + 1
            team_ids[team_name] = new_id
            used_ids.append(new_id)
            print(f"Asignado id {new_id} a {team_name}")
            break
        else:
            # Mostrar ids actuales con los nombres asociados
            print("IDs actuales y sus equipos:")
            for tid in sorted(used_ids):
                asociados = [name for name, idd in team_ids.items() if idd == tid]
                print(f"{tid}: {', '.join(asociados)}")
            
            # Preguntar a cuál id asignarlo
            while True:
                id_existente = input("Escribe el id al que asignar este equipo: ").strip()
                if id_existente.isdigit() and int(id_existente) in used_ids:
                    team_ids[team_name] = int(id_existente)
                    print(f"Asignado id {id_existente} a {team_name}")
                    break
                else:
                    print("ID inválido, inténtalo de nuevo.")
            break

print("\nDiccionario final de equipos:")
for name, tid in team_ids.items():
    print(tid, ":", name)

import json
# Guardar
with open("team_ids.json", "w", encoding="utf-8") as f:
    json.dump(team_ids, f, ensure_ascii=False, indent=2)

# Cargar
#with open("team_ids.json", "r", encoding="utf-8") as f:
#    team_ids = json.load(f)
conn.close()
