import os

#compila os arquivos negativos e positivo em uma lsita.txt
def generate_negative_description_file():
    # open the output file for writing. will overwrite all existing data in there
    with open('neg.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir('negative'):
            f.write('C:/Users/Acer/Documents/Progamacao/pixbot/pixOpen/negative/' + filename + '\n')

def generate_positive_description_file():
    # open the output file for writing. will overwrite all existing data in there
    with open('pos.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir('pixOpen/08/positive'):
            f.write('positive/' + filename + '\n')

generate_negative_description_file()
#anotar as regioes positivas das imagens
#C:/Users/Acer/Documents/Progamacao/openCV/opencv/build/x64/vc15/bin/opencv_annotation.exe --anotations='pos.txt' --images='positive'

#transformar as anotacoes em vetores
#C:/Users/Acer/Documents/Progamacao/openCV/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 300 -vec pos.vec

#treinar as informaçoes

#C:/Users/Acer/Documents/Progamacao/openCV/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -numPos 12 -numNeg 1 -numStages 10



