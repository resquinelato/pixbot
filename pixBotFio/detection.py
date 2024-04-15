# Evitando variavel global
# Trhead detedction

import cv2 as cv
from threading import Thread, Lock
from vision import Vision


class Detection:

    # Propriedades threading 
    stopped = True
    lock = None
    rectangles = []
    # Propriedades
    cascade = None
    screenshot = None

    def __init__(self, model_file_path):
        # Cria um objeto thread lock 
        self.lock = Lock()
        # load the trained model
        #self.cascade = cv.CascadeClassifier(model_file_path)
        self.cascade = Vision(model_file_path)


    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            if not self.screenshot is None:
                # realiza a detecção do objeto
                #rectangles = self.cascade.detectMultiScale(self.screenshot)
                rectangles = self.cascade.find(self.screenshot, 0.7)

                # lock o thread enquanto os resultados sao atualizados
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()


