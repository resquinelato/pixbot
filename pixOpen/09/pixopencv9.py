#pyautogui automation

import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
from threading import Thread

# Inicializa window capture class
# adiciona o nome da janela em str para ser capturada ou apenas deixa None para capturar tela toda
wincap = WindowCapture()

#carrega classe vision 
vision_bottle = Vision('img/bottle2.png')

# Essa variavel global avisa o loop principal
# que as ações do bot foram completadas
is_bot_in_action = False

#############
# Automação #
#############
def bot_actions(rectangles):
    if len(rectangles) > 0:
        targets = vision_bottle.get_click_points(rectangles)
        # targets[0] -> cord(x,y) da img original
        # nao significa que é a mesma posição da tela
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(x = target[0], y = target[1])
        pyautogui.click()
        sleep(5)

    # Avisa o loop prinncipal que a ação foi completada
    global is_bot_in_action
    is_bot_in_action = False


loop_time = time()
while(True):

    # pega imagem atualizada da tela
    screenshot = wincap.get_screenshot()
    # precisa ser um argumento matematico no imashow
    screenshot = np.array(screenshot)

    #realiza detecção do objeto
    rectangles = vision_bottle.find(screenshot, 0.7)

    #desenha os retangulos sobre a imagem original
    detection_image = vision_bottle.draw_rectangles(screenshot, rectangles)

    #mostra a imagem processada
    cv.imshow('Processado', detection_image)

    # Realição a ação do bot
    # Essa função roda em uma thread separada da tread principal
    # então o codigo daqui continuar enquanto o bot realiza as ações
    if not is_bot_in_action:
        is_bot_in_action = True
        t = Thread(target=bot_actions, args=(rectangles,))
        t.start()
       

    # msotra o FPS de execução (pode ser melhorado)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key pressesgi
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), screenshot)

print('Done')



