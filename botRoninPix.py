import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MNEMONIC = 'security curve swallow few tilt attract donor tuition matter place spoon major'
PASSWORD = '11111111'

extensao = "C:/Users/Acer/Documents/Progamacao/botpix2/pixbot/Ronin-Wallet.crx"

playFree ='/html/body/div[1]/div[1]/div/a/strong'

conectRonin = '/html/body/div[1]/div/div[3]/div[2]/div[1]/button[2]'
walletExtension = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[3]/button[1]'
nextWalet = '/html/body/section/div[1]/div/div[3]/div/div/button[2]'
conectWalet = '/html/body/section/div[1]/div/div[3]/div/div/button[2]'
signatureWalet = '/html/body/section/div[1]/div/div[2]/div/div[2]/div[2]/div/button[2]'
startGame = '/html/body/div[1]/div/div[3]/div[2]/button[1]'


chrome_options = Options()
#chrome_options.add_argument('--headless') #hide (sem isso fica normal)

print('Implementando extensao 1/1')
chrome_options.add_extension(extensao)

servico = Service()
options=webdriver.ChromeOptions()
 
browser = webdriver.Chrome(service=servico, options=chrome_options)

browser.get('chrome-extension://fnjhmkhhmkbjkkabndcnnogagogbneec/full-page.html#/welcome')
browser.maximize_window()
time.sleep(1)

print('Configurando carteira 1/7')
browser.find_element('xpath', '//*[@id="root"]/div/div/div[2]/div/div/div[1]/button[2]/div').click() # i aready have a wallet 
time.sleep(2) 

print('Configurando carteira 2/7')
browser.find_element('xpath', '//*[@id="root"]/div/div/div[2]/div/div/div[1]/button[2]/div').click() # dont alow tracking
time.sleep(2)

print('Configurando carteira 3/7')
browser.find_element('xpath', '//*[@id="root"]/div/div/div[2]/div/button[1]/span').click()  #use secret revovery frase
time.sleep(2)

print('Configurando carteira 4/7')
browser.find_element('xpath', "/html/body/section/div/div/div[2]/div/label[1]/div/div/span/input").send_keys(MNEMONIC) # envia frase minemonica
time.sleep(1)

print('Configurando carteira 5/7')
webdriver.ActionChains(browser).send_keys(Keys.TAB).send_keys(PASSWORD).perform() #digita a senha
time.sleep(1)

print('Configurando carteira 6/7')
webdriver.ActionChains(browser).send_keys(Keys.TAB).send_keys(PASSWORD).perform() #repete a senha
time.sleep(1)

print('Configurando carteira 7/7')
webdriver.ActionChains(browser).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform() #import
time.sleep(3)

print('Acessando site 1/2')
browser.get('https://www.pixels.xyz/')
time.sleep(3)

print('Acessando site 2/2')
browser.find_element('xpath', playFree).click()  # clica no botao play free
time.sleep(2)

print('Conectando carteira 1/5')
browser.find_element('xpath', conectRonin).click()  # clica no botao concet a ronin
time.sleep(2)

print('Conectando carteira 2/5')
browser.find_element('xpath', walletExtension).click()  # clica no botao para escolher extensao ronin
time.sleep(2)

print('Conectando carteira 3/5')
browser.switch_to.window(browser.window_handles[1]) #mudar o foco para a nova janela
time.sleep(0.5)

WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, nextWalet))).click() #janela da carteira vai abrir pra isso precisa ser carregada
time.sleep(2)

print('Conectando carteira 4/5')
browser.find_element('xpath', conectWalet).click()  # clica no botao connect da carteira
time.sleep(2)

browser.switch_to.window(browser.window_handles[1]) #mudar o foco para a nova janela (novamente)
time.sleep(0.5)

print('Conectando carteira 5/5')
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, signatureWalet))).click() #assinar a nova janela
time.sleep(2)

browser.switch_to.window(browser.window_handles[0]) #mudar o foco para a nova janela (novamente) estava [1] mudei rpa [0]
time.sleep(0.5)

print('Entrando no jogo')
browser.find_element('xpath', startGame).click()  # comeca o jogo
time.sleep(2)

print('Estou Online\nComeçar OpeCV')
