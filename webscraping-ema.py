from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

# Parâmetros de busca
empresa = "Pfizer"
pais = "Germany"
numero_mia = ""  # Se quiser buscar pelo número, insira aqui

# Caminho do ChromeDriver
service = Service("CAMINHO/para/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--headless")

# Inicializa navegador
driver = webdriver.Chrome(service=service, options=options)

# Acessa o site
url = "https://eudragmdp.ema.europa.eu/inspections/mia/searchMIA.do"
driver.get(url)
time.sleep(3)

# Preenche o campo de nome da empresa
driver.find_element(By.NAME, "companyName").send_keys(empresa)

# Seleciona o país
select_country = Select(driver.find_element(By.NAME, "country"))
select_country.select_by_visible_text(pais)

# Número MIA (opcional)
if numero_mia:
    driver.find_element(By.NAME, "miaNumber").send_keys(numero_mia)

# Clica no botão de busca
driver.find_element(By.NAME, "submit").click()
time.sleep(5)

# Extrai dados da tabela
rows = driver.find_elements(By.CSS_SELECTOR, "table.reportTable > tbody > tr")

dados = []
for row in rows[1:]:  # Ignora cabeçalho
    cols = row.find_elements(By.TAG_NAME, "td")
    dados.append([col.text.strip() for col in cols])

# Cria DataFrame
colunas = ["Company Name", "MIA Number", "Address", "City", "Postal Code", "Country", "Type of Authorisation", "Operations"]
df = pd.DataFrame(dados, columns=colunas)
print(df.head())

driver.quit()