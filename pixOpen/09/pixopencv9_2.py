#pyautogui automation
# Evitando variavel global

import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture9_2 import WindowCapture
from detection import Detection
from vision import Vision
import pyautogui
from threading import Thread

DEBUG = True

# Inicializa window capture class
# adiciona o nome da janela em str para ser capturada ou apenas deixa None para capturar tela toda
wincap = WindowCapture()

#carrega classe vision 
#vision_bottle = Vision('img/bottle2.png')
#careca o detector
detector = Detection('img/bottle2.png')

vision = Vision(None)


# Essa variavel global avisa o loop principal
# que as ações do bot foram completadas
is_bot_in_action = False

#############
# Automação #
#############
def bot_actions(rectangles):
    if len(rectangles) > 0:
        targets = vision.get_click_points(rectangles)
        # targets[0] -> cord(x,y) da img original
        # nao significa que é a mesma posição da tela
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(x = target[0], y = target[1])
        pyautogui.click()
        sleep(5)

    # Avisa o loop prinncipal que a ação foi completada
    global is_bot_in_action
    is_bot_in_action = False

wincap.start()
detector.start()

loop_time = time()
while(True):

    # se ainda nao foi possivel capturar uma screenshot
    if wincap.screenshot is None:
        continue

    # pega imagem atualizada da tela
    #screenshot = wincap.get_screenshot()
    # agora ocorre dentro do metodo

    #realiza detecção do objeto
    #rectangles = vision_bottle.find(screenshot, 0.7)
    detector.update(wincap.screenshot)


    if DEBUG:
        #desenha os retangulos sobre a imagem original
        detection_image = vision.draw_rectangles(wincap.screenshot, detector.rectangles)
        #mostra a imagem processada
        cv.imshow('Processado', detection_image)

    # Realição a ação do bot
    # Essa função roda em uma thread separada da tread principal
    # então o codigo daqui continua enquanto o bot realiza as ações
    if not is_bot_in_action:
        is_bot_in_action = True
        t = Thread(target=bot_actions, args=(detector.rectangles,))
        t.start()
       

    # msotra o FPS de execução (pode ser melhorado)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key pressesgi
    key = cv.waitKey(1)
    if key == ord('q'):
        detector.stop()
        wincap.stop()
        cv.destroyAllWindows()
        break

print('Done')



