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
                    (By.XPATH, "//h5[contains(text(),'"+ sel_league +"')]/following::td//a[contains(text(),'Calendario de xogo')]")
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
            rounds = driver.find_elements(By.XPATH, "//*[@id='contenido_principal']//div[@class='alert alert-warning text-center']")
            matches = []
            for sel_round in rounds:
                num_round = int(sel_round.text.split()[0].split('-')[1])
                table_teams = sel_round.find_elements(
                    By.XPATH,
                    "following-sibling::div[@class='table-responsive'][1]"
                )
                if len(table_teams) == 0:
                    print("Esta ronda no tiene tabla de encuentros.")
                    continue
                tabla = table_teams[0]
                filas = tabla.find_elements(By.TAG_NAME, "tbody")
                if len(filas) == 0:
                    continue
                for fila in filas:
                    columnas = fila.find_elements(By.TAG_NAME, "td")
                    #encuentro = [col.text for col in columnas]
                    #print(encuentro)
                    if all(c.text=='' for c in columnas):
                        continue
                    team_name = columnas[1].text
                    resultraw = columnas[2].text
                    result = int(2*float(resultraw.split()[0].strip()))
                    result2 = int(2*float(resultraw.split()[2].strip()))
                    enemy_team= columnas[3].text
                    matches.append((team_name,enemy_team,sel_league,sel_year,num_round,result))
                    matches.append((enemy_team,team_name,sel_league,sel_year,num_round,result2))
                conn = sqlite3.connect("fantasy_chess.db")
                cur = conn.cursor()
                for m in matches:
                    cur.execute("""
                    INSERT OR IGNORE INTO matches (team_name, enemy_team, division,
                                            year, round, result)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, m)
                conn.commit()
                conn.close()
        ## Cerrar navegador
        driver.quit()
