from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import sqlite3

chrome_options = Options()
chrome_options.add_argument("--headless")        # Oculta el navegador
chrome_options.add_argument("--disable-gpu")     # Mejora estabilidad
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-dev-shm-usage")

years = [2018,2019,2020,2022,2023,2024,2025]
leagues = ["HONRA","PREFERENTE","PRIMEIRA","SEGUNDA"]
#years = [2018]
#leagues = ["HONRA"]
for sel_year in years:
    for sel_league in leagues:
        print(f'Working on year {sel_year} in league {sel_league}')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://xefega.fegaxa.org/')
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "dropdownMenu1"))
        )
        dropdown.click()
        enlace_year = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{sel_year}']"))
        )
        enlace_year.click()
        try:
            enlace = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//h5[contains(text(),'"+ sel_league +"')]/following::td//a[contains(text(),'Resultados Equipos por Taboleiro')]")
                )
            )
        except TimeoutException:
            driver.quit()
            continue
        enlace.click()
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cal_grupo_selector"))
        )
        select_div = Select(select_element)
        divisiones = [o.text for o in select_div.options]  # solo los textos = select_div.options
        divisiones = divisiones[:-1]
        for div in divisiones:
            select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "cal_grupo_selector"))
            )
            select_div = Select(select_element)
            select_div.select_by_visible_text(div)
            time.sleep(1)    
            equipos = driver.find_elements(By.XPATH, "//*[@id='contenido_principal']//div[@class='alert alert-warning text-center']")
            for equipo in equipos:
                nombre_equipo = equipo.text
                #print("\n==============================")
                #print("Equipo:", nombre_equipo)
                #print("==============================")
                tabla_jugadores = equipo.find_elements(
                    By.XPATH,
                    "following-sibling::div[@class='table-responsive indexada'][1]//table/tbody"
                )
                if len(tabla_jugadores) == 0:
                    print("Este equipo NO tiene tabla de jugadores.")
                    continue
                tabla = tabla_jugadores[0]
                filas = tabla.find_elements(By.TAG_NAME, "tr")
                if len(filas) == 0:
                    continue
                columnas = filas[0].find_elements(By.TAG_NAME, "td")
                n_rounds = len(columnas) - 7
                games = []
                boards = [1] * n_rounds
                match_results = [0] * n_rounds
                for fila in filas:
                    columnas = fila.find_elements(By.TAG_NAME, "td")
                    if all(c.text=='' for c in columnas):
                        continue
                    try:
                        id_player = int(columnas[1].text)
                    except ValueError:
                        id_player = 0
                    name = columnas[2].text
                    surnames= columnas[3].text
                    #jugador = [col.text for col in columnas]
                    #print(jugador)
                    for i in range(n_rounds):
                        if columnas[5+i].text == '0.0':
                            result = 0
                        elif columnas[5+i].text == '0.5':
                            result = 1
                        elif columnas[5+i].text == '1.0':
                            result = 2
                        else:
                            continue
                        games.append((id_player,name,surnames,nombre_equipo,sel_league,sel_year,i+1,boards[i],result,0))
                        boards[i] += 1
                        match_results[i] += result
                for idx, g in enumerate(games):
                    round = g[6]
                    games[idx] = g[:-1] + (match_results[round-1],)
                conn = sqlite3.connect("fantasy_chess.db")
                cur = conn.cursor()
                for g in games:
                    cur.execute("""
                    INSERT OR IGNORE INTO games (id_player, name, surnames, team_name, division,
                                            year, round, board, game_result, match_result)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, g)
                conn.commit()
                conn.close()
        ## Cerrar navegador
        driver.quit()
