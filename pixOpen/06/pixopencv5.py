import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision

#WindowCapture.list_window_names()
#exit()

# initialize the WindowCapture class
# adiciona o nome da janela em str para ser capturada ou apenas deixa None para capturar tela toda
wincap = WindowCapture('Documentos')
# initialize Vision Class
vision_dir = Vision('img/dir.png')


loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # precisa ser um argumento matematico no imashow
    screenshot = np.array(screenshot)

    #mostra a imagem preocessada
    points = vision_dir.find(screenshot, 0.5 , 'rectangles')

    # msotra o FPS de execução (pode ser melhorado)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key pressesgi
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
