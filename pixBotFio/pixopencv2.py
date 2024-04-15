import cv2 as cv
import numpy as np
#import os
#os.chdir(os.path.dirname(os.path.abspath(__file__)))
'''
#opção para ver todos os dados ams usa muita memoria
import sys
np.set_printoptions(threshold=sys.maxsize)
'''

#metodo que a foto será tyratada
haystack_img = cv.imread('img/pos_fogao1.png', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('img/click_to_cook.png', cv.IMREAD_UNCHANGED)
#haystack_img = cv.imread('img\palheiro1.png', cv.IMREAD_REDUCED_COLOR_2)
#needle_img = cv.imread('img\needle1.png', cv.IMREAD_REDUCED_COLOR_2)

#método de comparação das imagens
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

'''
# testando novo metodo pra ver se aparece melhorezs resultados (horrivel)
#nesse metodo o trashgold funciona d emaneira diferente
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_SQDIFF_NORMED)
'''
#print(result)

'''
threshold = 0.85
locations = np.where(result >= threshold)
print(locations)
#peinta 9 localizacoe com limiar acuma de 0.85 em que a primeira coluna eh y e a segunda eh x
#(array([105, 105, 105, 169, 169, 169, 233, 233, 233], dtype=int64), array([168, 232, 296, 168, 232, 296, 168, 232, 296], dtype=int64))
# (168,105), (232,105)... 
'''


threshold = 0.9
locations = np.where(result >= threshold)
'''
#novo tashold pra o novo metodo (horrível)
#threshold = 0.005
#locations = np.where(result <= threshold)
'''
#print(locations)
#faz o reverço da matriz pra ficar mais legivel e arruanja em tuplas
locations = list(zip(*locations[::-1]))
#print(locations)


if locations:
    print('Found needle.')

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    # Loop over all the locations and draw their rectangle
    for loc in locations:
        # Determine the box positions
        top_left = loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        # Draw the box
        cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)

    cv.imshow('Matches', haystack_img)
    cv.waitKey()
    #cv.imwrite('result.jpg', haystack_img)

else:
    print('Needle not found.')
