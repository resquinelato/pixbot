import cv2 as cv
import numpy as np
#import os
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

#metodo que a foto será tyratada
haystack_img = cv.imread('img/palheiro2.png', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('img/needle5.png', cv.IMREAD_UNCHANGED)

needle_w = needle_img.shape[1]
needle_h = needle_img.shape[0]

#método de comparação das imagens
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

print(result)


threshold = 0.25
locations = np.where(result >= threshold)

print(locations)
#faz o reverço da matriz pra ficar mais legivel e arruanja em tuplas
locations = list(zip(*locations[::-1]))
print(locations)



#agrupando os retangulos criando lista de [x,y,w,h]
rectangles = []
for loc in locations:
    rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
    rectangles.append(rect)
    rectangles.append(rect)

#no metodo rectangles  1 eh o tento que se repete, 0.5 eha  distancia tolerada
rectangles, weights = cv.groupRectangles(rectangles, 1, 0.08)
print(rectangles)

#sem o metodo anterior funciona como a função de antes(se tirar o len)
if len(rectangles):
#if rectangles:
    print('Found needle.')

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    # Loop over all the locations and draw their rectangle
    for (x, y, w, h) in rectangles:
        # Determine the box positions
        top_left = (x,y)
        bottom_right = (x+w,y+h)
        # Draw the box
        cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)

    #cv.imshow('Matches', haystack_img)
    cv.waitKey()
    cv.imwrite('result3.jpg', haystack_img)

else:
    print('Needle not found.')
