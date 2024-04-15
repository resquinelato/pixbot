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
from bot import BottleBot, BotState

DEBUG = True

# Inicializa window capture class
# adiciona o nome da janela em str para ser capturada ou apenas deixa None para capturar tela toda
wincap = WindowCapture()

#carega o detector
detector = Detection('img/fogao.png')
detector2 = Detection('img/omelet.PNG')

vision = Vision(None)
#inicia o bot
bot = BottleBot((wincap.offset_x, wincap.offset_y),(wincap.w,wincap.h))


wincap.start()
detector.start()
bot.start()

#loop_time = time()
while(True):

    # se ainda nao foi possivel capturar uma screenshot
    if wincap.screenshot is None:
        continue

    #realiza detecção do objeto
    detector.update(wincap.screenshot)


    ##########################################################################################
    # atualiza o bot com as informações que precisa agora
    if bot.state == BotState.INITIALIZING:
        # enquanto o bot está esperando para começar, vá em frente e
        # comece a dar-lhe alguns alvos para trabalhar imediatamente quando ele começar
        targets = vision.get_click_points(detector.rectangles)
        bot.update_targets(targets)
        # isso de baixo nao estava aqui #funcinou
        bot.update_screenshot(wincap.screenshot)
    
        

    elif bot.state == BotState.SEARCHING:
        
        # ao procurar algo para clicar em seguida, o bot precisa saber quais são os pontos 
        # de clique para os resultados de detecção atuais. ele também precisa de uma captura 
        # de tela atualizada para verificar a dica de ferramenta instantânea depois de mover o 
        # mouse para essa posição
        targets = vision.get_click_points(detector.rectangles)
        bot.update_target(targets)
        bot.update_screenshot(wincap.screenshot)
        
    elif bot.state == BotState.MOVING:
        # ao nos movermos, precisamos de novas capturas de tela para determinar quando 
        # paramos de nos mover
        targets = vision.get_click_points(detector2.rectangles)
        bot.update_target(targets)
        bot.update_screenshot(wincap.screenshot)

    elif bot.state == BotState.MINING:
        # nada é necessário enquanto esperamos a mineração terminar
        pass
    ############################################################################################



    if DEBUG:
        #desenha os retangulos sobre a imagem original
        detection_image = vision.draw_rectangles(wincap.screenshot, detector.rectangles)
        #mostra a imagem processada
        cv.imshow('Processado', detection_image)

    # Realição a ação do bot
    # Essa função Roda em uma thread separada da tread principal
    # então o codigo daqui continuar enquanto o bot realiza as ações
    #if not is_bot_in_action:
    #    is_bot_in_action = True
    #    t = Thread(target=bot_actions, args=(detector.rectangles,))
    #    t.start()
       

    # msotra o FPS de execução (pode ser melhorado)
    #print('FPS {}'.format(1 / (time() - loop_time)))
    #loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key pressesgi
    key = cv.waitKey(1)
    if key == ord('q'):
        detector.stop()
        wincap.stop()
        bot.stop()
        cv.destroyAllWindows()
        break

print('Done')



