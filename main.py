import time
from pathlib import Path

from selenium import webdriver

# Configurar opções do navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")  # Nova API headless

# Iniciar navegador com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)

# Abrir site
link = "https://www.google.com/travel/flights/search?tfs=CBwQAhopEgoyMDI1LTAyLTEwag0IAhIJL20vMDIycGZtcgwIAxIIL20vMGg3aDYaKRIKMjAyNS0wMi0yN2oMCAMSCC9tLzBoN2g2cg0IAhIJL20vMDIycGZtQAFIAWoEEAEYAHABggELCP___________wGYAQE&tfu=EgoIABAAGAAgASgC"
driver.get(link)
time.sleep(5)

# Obtem as informações da passagem aérea mais barata
voo = driver.find_element("css selector", "span.ogfYpf").text
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
    with open(arquivo_path, "w") as arquivo:
        arquivo.write(f"{preco_float:.2f}")

    # Verificar se o preço está menos que R$ 3300
    if preco_float < 3300:
        print("Passagem barata")
        print(f"Preço: R$ {preco_float:.2f}")
    elif preco_float > 3300:
        print("Passagem cara")
        print(f"Preço: R$ {preco_float:.2f}")
    elif preco_float == 3300:
        print("Passagem normal")
        print(f"Preço: R$ {preco_float:.2f}")
    else:
        print("Erro")


def main():
    info_voo()
    analise_preco()


if __name__ == "__main__":
    main()
