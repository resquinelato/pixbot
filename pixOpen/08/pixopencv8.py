#cascade_classifier
#https://docs.opencv.org/4.2.0/dc/d88/tutorial_traincascade.html
#https://docs.opencv.org/4.2.0/db/d28/tutorial_cascade_classifier.html

import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision

# initialize the WindowCapture class
# adiciona o nome da janela em str para ser capturada ou apenas deixa None para capturar tela toda
wincap = WindowCapture()

#carrega o modelo treinado
cascade_bottle = cv.CascadeClassifier('c:/Users/Acer/Documents/Progamacao/pixbot/pixOpen/08/cascade/cascade.cascade.xml')

#carrega classe vision vazia
vision_bottle = Vision(None)

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # precisa ser um argumento matematico no imashow
    screenshot = np.array(screenshot)


    #realiza detecção do objeto
    rectangles = cascade_bottle.detectMultiScale(screenshot)

    #desenha os retangulos sobre a imagem original
    detection_image = vision_bottle.draw_rectangles(screenshot, rectangles)

    #mostra a imagem processada
    cv.imshow('Unprocessed', detection_image)

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

