import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constantes
LIMITE_PRECO_BARATO = 3300

# Configurar opções do navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")  # Nova API headless

# Iniciar navegador com as opções configuradas
try:
    driver = webdriver.Chrome(options=chrome_options)
except Exception as e:
    print(f"Erro ao iniciar o WebDriver: {e}")
    exit(1)

# Abrir site
link = "https://www.google.com/travel/flights/search?tfs=CBwQAhopEgoyMDI1LTAyLTEwag0IAhIJL20vMDIycGZtcgwIAxIIL20vMGg3aDYaKRIKMjAyNS0wMi0yN2oMCAMSCC9tLzBoN2g2cg0IAhIJL20vMDIycGZtQAFIAWoEEAEYAHABggELCP___________wGYAQE&tfu=EgoIABAAGAAgASgC"
driver.get(link)

# Espera explícita para carregar os elementos necessários
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.ogfYpf"))
    )
except Exception as e:
    print(f"Erro ao carregar a página ou elementos: {e}")
    driver.quit()
    exit(1)

# Obtem as informações da passagem aérea mais barata
try:
    voo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.ogfYpf"))
    ).text
except Exception as e:
    print(f"Erro ao encontrar o elemento voo: {e}")
    driver.quit()
    exit(1)

preco = driver.find_element("css selector", "div.YMlIz.FpEdX").text
agencia = driver.find_element("css selector", "div.sSHqwe.tPgKwe.ogfYpf").text
tempo = driver.find_element("css selector", "div.gvkrdb.AdWm1c.tPgKwe.ogfYpf").text
escalas = driver.find_element(
    "css selector", "div.EfT7Ae.AdWm1c.tPgKwe > span.ogfYpf"
).text

def info_voo():
    """
    Exibe as informações do voo, incluindo detalhes como voo, preço, agência,
    tempo de viagem e escalas. Utiliza seletores CSS para extrair informações
    da página de resultados de voos.
    """

    print("<<< Informações do voo >>>")
    print(
        f"""
VOO: {voo}
PREÇO: {preco}
AGÊNCIA: {agencia}
TEMPO DE VIAGEM: {tempo}
ESCALAS: {escalas}
"""
    )

def formatar_preco(preco):
    # Remove "R$" e pontos do valor
    preco = preco.replace("R$", "").replace(".", "").strip()

    # Converte o preço para float
    preco_float = float(
        preco.replace(",", ".")
    )  # Substitui vírgula decimal por ponto decimal
    return preco_float

def analise_preco():
    preco_float = formatar_preco(preco)

    # Define o caminho para o arquivo no mesmo diretório do script
    arquivo_path = Path(__file__).parent / "preco.txt"

    # preco.txt (armazena os preços)
    with open(arquivo_path, "a") as arquivo:
        arquivo.write(f"{preco_float:.2f}\n")

    # Verificar se o preço está menos que o limite definido
    if preco_float < LIMITE_PRECO_BARATO:
        print("Passagem barata")
        print(f"Preço: R$ {preco_float:.2f}")
    elif preco_float > LIMITE_PRECO_BARATO:
        print("Passagem cara")
        print(f"Preço: R$ {preco_float:.2f}")
    elif preco_float == LIMITE_PRECO_BARATO:
        print("Passagem normal")
        print(f"Preço: R$ {preco_float:.2f}")
    else:
        print("Erro")

def main():
    info_voo()
    analise_preco()

if __name__ == "__main__":
    main()
