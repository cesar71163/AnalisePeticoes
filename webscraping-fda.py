from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ← Atualize com seu caminho local do chromedriver
service = Service("CAMINHO/para/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--headless")

# Inicializa navegador
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)

# URL da ferramenta FDA
url = "https://datadashboard.fda.gov/oii/fd/fser.htm"
driver.get(url)
time.sleep(5)

# --- Entrar com nome da empresa ou FEI ---
empresa_ou_fei = "Pfizer"  # ← substitua pelo nome ou número FEI desejado

# Localiza campo de busca e insere valor
try:
    campo_busca = wait.until(EC.presence_of_element_located((By.ID, "searchInput")))  # ← confirmar o ID real
    campo_busca.clear()
    campo_busca.send_keys(empresa_ou_fei)
    time.sleep(2)

    botao_buscar = driver.find_element(By.ID, "searchButton")  # ← confirmar o ID real
    botao_buscar.click()
    time.sleep(8)

    # Captura resultados da tabela
    resultados = driver.find_elements(By.CLASS_NAME, "result-row")  # ← ajustar para estrutura real
    for item in resultados:
        print(item.text)

except Exception as e:
    print("Erro ao buscar empresa:", e)

driver.quit()