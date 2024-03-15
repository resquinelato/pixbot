"""
Importando extensao ao Chrome no modo oculto --headless
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def iniciar_bot_escondido_com_extensao(extensao_path):
    # Configura as opções do Chrome para carregar a extensão e modo headless
    chrome_options = Options()
    chrome_options.add_extension(extensao_path)
    chrome_options.add_argument('--headless=new')  # Executa em modo headless
    # Inicializa o driver do Chrome com as opções configuradas
    driver = webdriver.Chrome(options=chrome_options)
    # Retorna o driver inicializado
    return driver

# Caminho para a extensão
caminho_da_extensao = 'Ronin-Wallet.crx'

# Inicializa o bot com a extensão e em modo headless
print('Instalando a extensao')
bot = iniciar_bot_escondido_com_extensao(caminho_da_extensao)
print('Extensao Instalada')
time.sleep(2)
print('Abrindo Extensão')
bot.get('chrome-extension://fnjhmkhhmkbjkkabndcnnogagogbneec/full-page.html#/welcome')
time.sleep(2)
print('Clicando na Extensão')
time.sleep(1)
bot.find_element('xpath', '/html/body/section/div/div/div[2]/div/div/div[1]/button[1]').click()
print('Interação realizada com sucesso')
time.sleep(100)
