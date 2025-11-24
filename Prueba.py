from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Inicializar el navegador
driver = webdriver.Chrome()  # o Firefox()

# Abrir la página
driver.get('https://xefega.fegaxa.org/')
#driver.get("https://xefega.fegaxa.org/index.php/competiciones/resultados_tablero/1")

# Esperar a que se cargue la página
time.sleep(1)

# Seleccionar un grupo (por ejemplo "DIVISIÓN DE HONRA")
driver.find_element(By.ID, "dropdownMenu1").click()
time.sleep(1)

# Clic en el año 2025 dentro del menú
driver.find_element(By.XPATH, "//a[text()='2025']").click()

# Esperar a que se carguen los datos
time.sleep(1)

#driver.find_element(By.XPATH, "//h5[text()='DIVISION DE HONRA']")
#Entrar en el enlace: 
enlace = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//h5[contains(text(),"+ "'PRIMEIRA'" +")]/following::td//a[contains(text(),'Resultados Equipos por Taboleiro')]")
    )
)

enlace.click()
#driver.find_element(By.LINK_TEXT, "Resultados Equipos por Taboleiro").click()

# Buscar los nombres de los equipos en la tabla
time.sleep(1)
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
    print(div)
#select_div.select_by_visible_text("DIVISIÓN DE HONRA")
time.sleep(1)

equipos = driver.find_elements(By.XPATH, "//*[@id='contenido_principal']//div[@class='alert alert-warning text-center']")

for equipo in equipos:
    nombre_equipo = equipo.text
    print("\n==============================")
    print("Equipo:", nombre_equipo)
    print("==============================")

    # Buscar la tabla asociada (siguiente bloque)
    tabla_jugadores = equipo.find_elements(
        By.XPATH,
        "following-sibling::div[@class='table-responsive indexada'][1]//table/tbody"
    )
    if len(tabla_jugadores) == 0:
        print("⚠️  Este equipo NO tiene tabla de jugadores.")
        continue
    tabla = tabla_jugadores[0]
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    for fila in filas:
        columnas = fila.find_elements(By.TAG_NAME, "td")
        jugador = [col.text for col in columnas]
        print(jugador)

## Cerrar navegador
driver.quit()
