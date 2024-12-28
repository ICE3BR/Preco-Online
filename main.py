import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Constantes
LIMITE_PRECO_BARATO = 3300  # Limite para determinar se a passagem é barata

# Configurar opções do navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    "--headless=new"
)  # Utiliza o modo headless para não abrir o navegador

# Iniciar navegador com as opções configuradas
try:
    driver = webdriver.Chrome(options=chrome_options)
except Exception as e:
    print(f"Erro ao iniciar o WebDriver: {e}")
    exit(1)  # Encerra o programa em caso de erro

# Abrir site
link = "https://www.google.com/travel/flights/search?tfs=CBwQAhopEgoyMDI1LTAyLTEwag0IAhIJL20vMDIycGZtcgwIAxIIL20vMGg3aDYaKRIKMjAyNS0wMi0yN2oMCAMSCC9tLzBoN2g2cg0IAhIJL20vMDIycGZtQAFIAWoEEAEYAHABggELCP___________wGYAQE&tfu=EgoIABAAGAAgASgC"
driver.get(link)

# Espera explícita para carregar os elementos necessários
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.ogfYpf"))
    )  # Aguarda até 10 segundos pelo elemento especificado
except Exception as e:
    print(f"Erro ao carregar a página ou elementos: {e}")
    driver.quit()
    exit(1)  # Fecha o navegador e encerra o programa

# Obtem as informações da passagem aérea mais barata
try:
    voo = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.ogfYpf")))
        .text  # Extrai o texto do elemento do voo
    )
except Exception as e:
    print(f"Erro ao encontrar o elemento voo: {e}")
    driver.quit()
    exit(1)  # Encerra o programa caso o elemento não seja encontrado

# Extração de outros elementos diretamente
preco = driver.find_element("css selector", "div.YMlIz.FpEdX").text  # Preço da passagem
agencia = driver.find_element(
    "css selector", "div.sSHqwe.tPgKwe.ogfYpf"
).text  # Nome da agência
tempo = driver.find_element(
    "css selector", "div.gvkrdb.AdWm1c.tPgKwe.ogfYpf"
).text  # Duração do voo
escalas = driver.find_element(
    "css selector", "div.EfT7Ae.AdWm1c.tPgKwe > span.ogfYpf"
).text  # Detalhes das escalas


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
    # Remove "R$" e pontos do valor para converter em formato numérico
    preco = preco.replace("R$", "").replace(".", "").strip()

    # Converte o preço para float
    preco_float = float(
        preco.replace(",", ".")  # Substitui vírgula decimal por ponto decimal
    )
    return preco_float


def analise_preco():
    preco_float = formatar_preco(preco)  # Formata o preço para números
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d")  # Data atual
    hora_atual = datetime.datetime.now().strftime("%H:%M:%S")  # Hora atual

    # Define o caminho para o arquivo no mesmo diretório do script
    arquivo_path = Path(__file__).parent / "registro.txt"

    # Formatação do voo para substituir caracteres indesejados
    voo_f = voo.replace("–", "-")

    # Criar dicionário com informações do voo
    informacoes = {
        "Preco": preco_float,
        "Data": data_atual,
        "Hora": hora_atual,
        "Voo": voo_f,
        "Agencia": agencia,
        "Tempo de Viagem": tempo,
        "Escalas": escalas,
    }

    # Armazena as informações no arquivo de registro
    with open(arquivo_path, "a") as arquivo:
        arquivo.write(f"{informacoes}\n")

    # Verificação do preço da passagem com base no limite
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
    info_voo()  # Exibe as informações do voo
    analise_preco()  # Analisa o preço e armazena os dados


if __name__ == "__main__":
    main()  # Ponto de entrada do programa
