import cv2 as cv
import numpy as np


#metodo que a foto será tyratada
haystack_img = cv.imread('palheiro1.png', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('needle1.png', cv.IMREAD_UNCHANGED)
haystack_img = cv.imread('palheiro1.png', cv.IMREAD_REDUCED_COLOR_2)
needle_img = cv.imread('needle1.png', cv.IMREAD_REDUCED_COLOR_2)

#método de comparação das imagens
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
'''
cv.imshow('Resultado', result)
cv.waitKey() #impede o fechamento imediato
'''

#get best match position
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % max_val)

# em funão de um limiar de análise dizer se agulha foi encontrada
threshold = 0.8
if max_val >= threshold:
    print('Found needle.')

    #pega as dimensoes da imagem
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, 
                    top_left[1] + needle_h)

    #gera um retanglulo no match encontrado
    cv.rectangle(haystack_img, top_left, bottom_right, 
                color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    cv.imshow('Resultado', haystack_img)
    cv.waitKey() #impede o fechamento imediato
else:
    print('Needle not found.')
