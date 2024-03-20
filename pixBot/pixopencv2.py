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
haystack_img = cv.imread('img/googleTab.png', cv.IMREAD_GRAYSCALE)
needle_img = cv.imread('img/googleG.png', cv.IMREAD_GRAYSCALE)


# Verifique se as imagens foram lidas corretamente
'''
if haystack_img is None:
    print("Erro ao ler a imagem haystack")
if needle_img is None:
    print("Erro ao ler a imagem needle")

print("Dimensões da imagem haystack:", haystack_img.shape)
print("Dimensões da imagem needle:", needle_img.shape)
'''


#needle_img = cv.resize(needle_img, (0, 0), fx=0.5, fy=0.5)

#método de comparação das imagens
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)


threshold = 0.5
locations = np.where(result >= threshold)


print(locations)
#faz o reverço da matriz pra ficar mais legivel e arruanja em tuplas
locations = list(zip(*locations[::-1]))
print(locations)


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

    #cv.imshow('Matches', haystack_img)
    cv.waitKey()
    cv.imwrite('result.jpg', haystack_img)

else:
    print('Needle not found.')

