import cv2 as cv
import numpy as np
import os
from time import time
import win32gui, win32ui, win32con

# encontrar auma lista dos nome das janelad abertas
#https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
def list_window_names():
    def winEnumHandler( hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )

    win32gui.EnumWindows( winEnumHandler, None )


def window_capture():
    # https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows/3586280#3586280
    w = 1366 # set this
    h = 768 # set this

    windowname = 'Ravendawn'
    hwnd = win32gui.FindWindow(None, windowname) #comentado para testar gerando img
    #hwnd = None

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

    #salvar screenshot
    #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
    #captura a tela e grea as variaveis em matrizes
    #https://stackoverflow.com/questions/41785831/how-to-optimize-conversion-from-pycbitmap-to-opencv-image
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h,w,4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return img




# desabilitar loop paraa testar wincapture
loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = window_capture()
    # precisa ser um argumento amtematico no imashow
    screenshot = np.array(screenshot)
    #corrige a coloraçao de troca de RGB
    screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)


    cv.imshow('Computer Vision', screenshot)

    # msotra o FPS de execução (pode ser melhorado)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


#window_capture()
list_window_names()
print('Done.')