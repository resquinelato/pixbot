#copia de pixopencv3_2.py
import cv2 as cv
import numpy as np


class Vision:

    #propriedades
    needle_img = None
    needle_h = 0
    needle_W = 0
    method = None

    #construtor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        if needle_img_path:
            #metodo que a foto será tratada
            self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
            
            #salva as dimensoes das imgs needle
            self.needle_w = self.needle_img.shape[1]
            self.needle_h = self.needle_img.shape[0]

        #método de comparação das imagens
        self.method = method

    def find(self, haystack_img, threshold=0.25):
        #aplica metodo de comparacao com needle e haystack
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        locations = np.where(result >= threshold)
        #faz o reverço da matriz pra ficar mais legivel e arruanja em tuplas
        locations = list(zip(*locations[::-1]))

        #agrupando os retangulos criando lista de [x,y,w,h]
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            #para que retangulos unico tambewm sejam escolhidos
            rectangles.append(rect)

        #no metodo rectangles  1 eh o tento que se repete, 0.5 eha  distancia tolerada
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        return rectangles

    def get_click_points(self, rectangles):
        points = []

        # Loop over all the locations and draw their rectangle
        for (x, y, w, h) in rectangles:
            # Determine centro das posicoes
            center_x = x+int(w/2)
            center_y = y+int(h/2)
            # salvando pontos
            points.append((center_x, center_y))
        
        return points
    

    def draw_rectangles(self,haystack_img,rectangles):
        line_color = (0,255,0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # Determine the box position
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # Draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                        lineType=line_type, thickness=2)
        
        return haystack_img
    

    def draw_croshair(self, haystack_img, points):
        marker_color = (255,0,255)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            # Draw the center point
            cv.drawMarker(haystack_img, (center_x, center_y), 
                        color=marker_color, markerType=marker_type, 
                        markerSize=40, thickness=2)
            
        return haystack_img