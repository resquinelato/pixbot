#funcionando muito bem ao capturar a tela com cv.
import cv2 as cv
import numpy as np
import os
from time import time
#from vision import Vision
from visionOld import findClickPositions
from PIL import Image
import io
from selenium import webdriver
import base64

browser = webdriver.Chrome()
browser.get('http://www.google.com/')

# initialize Vision Class
#vision_dir = Vision('C:/Users/Rodrigo/Documents/bot/pix/pixbot/img/google.png')


loop_time = time()
while(True):

    # captura a tela do browser
    screenshotpng = browser.get_screenshot_as_png()
    imagem_pil = Image.open(io.BytesIO(screenshotpng))
    screenshot = np.array(imagem_pil)
    screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)
    #screenshot = wincap.get_screenshot()

    screenshot = np.array(screenshot)

    # gera a imagem capturada pelo browser
    #cv.imshow('Computer Vision', screenshot)

    #mostra a imagem preocessada
    findClickPositions('C:/Users/Rodrigo/Documents/bot/pix/pixbot/img/google.png',screenshot, 0.5 , 'rectangles')

    # msotra o FPS de execução (pode ser melhorado)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key pressesgi
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


