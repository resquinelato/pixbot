import cv2 as cv
import numpy as np
#import os
#os.chdir(os.path.dirname(os.path.abspath(__file__)))



def findClickPositions(needle_img_path, haystack_img_path, threshold=0.25, debug_mode=None):

    #metodo que a foto será tyratada
    haystack_img = cv.imread(haystack_img_path, cv.IMREAD_GRAYSCALE)
    needle_img = cv.imread(needle_img_path, cv.IMREAD_GRAYSCALE)

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    #método de comparação das imagens
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(haystack_img, needle_img, method)

    locations = np.where(result >= threshold)
    #faz o reverço da matriz pra ficar mais legivel e arruanja em tuplas
    locations = list(zip(*locations[::-1]))

    #agrupando os retangulos criando lista de [x,y,w,h]
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)
        #para que retangulos unico tambewm sejam escolhidos
        rectangles.append(rect)

    #no metodo rectangles  1 eh o tento que se repete, 0.5 eha  distancia tolerada
    rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

    #sem o metodo anterior funciona como a função de antes(se tirar o len)
    points = []
    if len(rectangles):
    #if rectangles:
        print('Found needle.')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (0, 0, 225)
        marker_type =  cv.MARKER_CROSS

        # Loop over all the locations and draw their rectangle
        for (x, y, w, h) in rectangles:
            # Determine centro das posicoes
            center_x = x+int(w/2)
            center_y = y+int(h/2)
            # salvando pontos
            points.append((center_x, center_y))

            if debug_mode == 'rectangles':
                # Determine the box position
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # Draw the box
                cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                             lineType=line_type, thickness=2)

            elif debug_mode == 'points':
                # Draw the center point
                cv.drawMarker(haystack_img, (center_x, center_y), 
                              color=marker_color, markerType=marker_type, 
                              markerSize=40, thickness=2)

        if debug_mode:
            cv.imshow('Matches', haystack_img)
            cv.waitKey()
            #cv.imwrite('result_click_point.jpg', haystack_img)

    return points



pontos = findClickPositions('img/googleG.png','img/googleTab.png', threshold=0.3, debug_mode='points')
print(pontos)