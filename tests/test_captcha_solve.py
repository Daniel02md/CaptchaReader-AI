import captcha.AI as AI
from os.path import dirname, realpath
from captcha import Captcha

IMAGE_PATH = dirname(realpath(__file__))+'\captcha.png'


cap = Captcha(IMAGE_PATH)

letters = cap.split_letters()
solver_captcha = AI()
solved_captcha = ""

for letter_image in letters:
    literal_letter = solver_captcha.predict(img_letter=letter_image)
    solved_captcha += literal_letter.lower()   


print(solved_captcha)