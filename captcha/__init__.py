import cv2 as cv
from PIL import Image
import PIL
import numpy as np
from .AI import AI


class Captcha:
    '''
    @methos: solve_captcha -> str -> "SOLVEDCAPTCHA"
    @method: split_letters -> list[cv.Mat]
    '''
    def __init__(self, img_captcha: str) -> None:
        '''
            @param: img_captcha: path to the captcha image
            
        '''
        self.__img_captcha = Image.open(img_captcha)
        self.img_captcha_processed = self.__process_image(self.__img_captcha)
        
    def solve_captcha(self):
        letters = self.split_letters()
        ai = AI()

        captcha_solved = []
        for letter in letters:
            response = ai.predict(letter)
            captcha_solved.append(response)

        return "".join(captcha_solved)


    def split_letters(self) -> list[cv.Mat]:
        '''
        Separate individually letters from the captcha image
        
        '''
        img = np.asarray(self.img_captcha_processed)
        
        result = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        _, img_gray_scale = cv.threshold(result, 127, 255, cv.THRESH_BINARY_INV)
        img_gray_scale = cv.cvtColor(img_gray_scale, cv.COLOR_RGB2GRAY)
        contours, _ = cv.findContours(img_gray_scale, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        letter_contours = []
        
        for contour in contours:
            (x, y, largura, altura) = cv.boundingRect(contour)
            letter_contours.append((x, y, largura, altura))
        
        letter_contours = sorted(letter_contours, key=lambda x: x[0])
        letters_images = []

        for contour in letter_contours:
            x, y, largura, altura = contour
            letter = result[y-2:y+2+altura, x-2:x+2+largura]
            letters_images.append(letter)

        return letters_images


    def __process_image(self, image: cv.Mat) -> PIL.Image.Image:
        COLOR_WHITE = (255, 255, 255)
        COLOR_BLACK = (0, 0, 0)

        image2 = Image.new("RGB", image.size, COLOR_WHITE)

        altura = image.size[1]
        largura = image.size[0]

        for x in range(largura):
            for y in range(altura):
                pixel_color = image.getpixel((x, y))
                if (pixel_color[0] > 100 and  pixel_color[1] > 100 and pixel_color[2] > 100) and (pixel_color[0] <= 110 and  pixel_color[1] <= 110 and pixel_color[2] <= 110):
                    image2.putpixel((x,y), COLOR_BLACK)

        return image2.convert("P")





if __name__ == "__main__":
    cap =  Captcha('captcha/base_captcha/IMG_CAPTCHA_0.jpg')
    print(cap.solve_captcha())
    

