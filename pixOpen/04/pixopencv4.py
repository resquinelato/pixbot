import cv2 as cv
import numpy as np
import os
from time import time
#from windowcapture import WindowCapture
import pyautogui

#os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
#wincap = WindowCapture('Albion Online Client')

loop_time = time()
while(True):

    # get an updated image of the game
    #screenshot = None
    screenshot = pyautogui.screenshot()
    # precisa ser um argumento amtematico no imashow
    screenshot = np.array(screenshot)
    #corrige a coloraçao de troca de RGB
    screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)
    #screenshot = wincap.get_screenshot()

    cv.imshow('Computer Vision', screenshot)

    # msotra o FPS de execução (pode ser melhorado)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


print('Done.')