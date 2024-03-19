import numpy as np
import win32gui, win32ui, win32con  
#import pygetwindow



class WindowCapture:
    #Propriedades
    w = 0
    h = 0
    hwnd = None

    #construtor
    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name) #comentado para testar gerando img
        if not self.hwnd:
            raise Exception('Windown not found: {}', window_name)
        #self.w = 1366
        #self.h = 768
        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        #print(window_rect)
        if window_rect[0] != -32000:
            self.w = window_rect[2] - window_rect[0]
            self.h = window_rect[3] - window_rect[1]
        else:
            #corrige erro full screen mode
            self.w = 1366
            self.h = 768

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y




    def get_screenshot(self):
        # https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows/3586280#3586280

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        #salvar screenshot
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        #captura a tela e grea as variaveis em matrizes
        #https://stackoverflow.com/questions/41785831/how-to-optimize-conversion-from-pycbitmap-to-opencv-image
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h,self.w,4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return img

    # encontrar auma lista dos nome das janelad abertas
    #https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    def list_window_names(self):
        def winEnumHandler( hwnd, ctx ):
            if win32gui.IsWindowVisible( hwnd ):
                print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )

        win32gui.EnumWindows( winEnumHandler, None )


    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

