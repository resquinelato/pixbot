#funcionando muito bem ao capturar a tela com cv.
import cv2 as cv
import numpy as np
import os
from vision import Vision
from visionOld import findClickPositions
from PIL import Image
import io
import base64

import json
import time
from time import time, sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
#browser.get('https://www.google.com.br')
browser.get('https://gamesnacks.com/games/aktestgunsandbottles')

# initialize Vision Class
#vision_dir = Vision('C:/Users/Rodrigo/Documents/bot/pix/pixbot/img/google.png')
vision_gunsbottle = Vision('img/bottle2.png')


loop_time = time()
while(True):

    # captura a tela do browser
    screenshotpng = browser.get_screenshot_as_png() #metodo do selenium
    imagem_pil = Image.open(io.BytesIO(screenshotpng))
    screenshot = np.array(imagem_pil)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

    screenshot = np.array(screenshot)

    #mostra a imagem preocessada
    #cv.imshow('Computer Vision', screenshot)
    #findClickPositions('img/bottle2.png',screenshot, 0.5 , 'rectangles')
    points = vision_gunsbottle.find(screenshot, 0.7 , 'points')
    cv.waitKey(1)

    #sleep(8)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,  '/html/body/c-wiz/div/div/div[2]/div/div[2]/section/div/button/span[3]'))).click() 
    #sleep(8) 
    #WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz/div/div/div[2]/div/header/div/div[3]/div/button/div'))).click()

    # msotra o FPS de execução (pode ser melhorado)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key pressesgi
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


