from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from os.path import dirname, realpath, sep
from keras.models import load_model
from .helpers import resize_to_fit
import cv2 as cv
import numpy as np
import pickle



class AI: 
    __SOURCE_DIR_PATH = dirname(realpath(__file__))
    __AI_PATH = __SOURCE_DIR_PATH + sep + 'AI.hdf5'
    __TRANSLATOR_PATH =  __SOURCE_DIR_PATH + sep +'labelbinarizer_to_letter.dat'

    def __init__(self) -> None:
        self.model = load_model(self.__AI_PATH)



    def predict(self, img_letter:cv.Mat) -> str:
        '''
        @param: img: Letter image the will be read.
        '''
        image = cv.cvtColor(img_letter, cv.COLOR_BGR2GRAY)
        image = resize_to_fit(image, width=20, height=20)
        image = np.expand_dims(image, axis=2)
        image = np.expand_dims(image, axis=0)
        
        response = self.model.predict(image, verbose=0)
        
        with open(self.__TRANSLATOR_PATH, 'rb') as translator:
            lb = pickle.load(translator)
        return lb.inverse_transform(response)[0]


if __name__ == "__main__":
    from helpers import resize_to_fit

    ai = AI()
    img = cv.imread("letter.png")
    print(ai.predict(img))
    