from requests import Session
from captcha import Captcha
from bs4 import BeautifulSoup as BS
from requests.packages import urllib3
import warnings


urllib3.disable_warnings()
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    
def signUp(name:str, e_mail:str, phone:str, plan_opt: int) -> bool:
    """
    @param: name: Username to account.
    @param: e_mail: Email to receive the confirmation message.
    @param: phone: Ex:. input 2211223311 -> output (22) 1122-3311.
    @param: plan_opt: Plan option ('0' or '1').
    """

    BASE_URL = 'https://149.56.233.36/'
    HOME = 'enqzva'
    CAPTCHA = 'painel/captcha.php'
    SIGN_UP = 'painel/EnviarCadTeste_email.php'
    CAPTCHA_IMAGE_PATH = 'captcha.png'

    payload = {
        "nome": name,
        "email":  e_mail ,
        "EditarCelular": f'({phone[0:2]}) {phone[2:6]}-{phone[6:-1]}',
        "Operadora": "*******" if plan_opt == 0 else "*********",
        "captcha":"" ,
        "r": "nqzva"
    }

    with Session() as session:
        home_page_response = session.get(BASE_URL+HOME, verify=False) 
        soup = BS(home_page_response.content, "html.parser")

        captcha_id = soup.find('div', attrs={'id': 'StatusCaptcha'}).find('img')['src'].split('=')[-1]
        home_cookies = home_page_response.cookies

        
        captcha_response = session.get(BASE_URL+CAPTCHA, data={'c': captcha_id}, cookies=home_cookies)

        with open('captcha.png', 'wb') as cap:
            cap.write(captcha_response.content)

        captcha = Captcha(CAPTCHA_IMAGE_PATH).solve_captcha().lower()
        payload['captcha'] = captcha

        sign_up = session.post(BASE_URL+SIGN_UP, data=payload, cookies=session.cookies)

        response_message = BS(sign_up.content, 'html.parser').find('div', attrs={'class': 'mb-title'}).text.strip().lower()
        
        if response_message == 'sucesso':
            return True
        else:
            return False




if __name__ == "__main__":
    email = "EMAIL"
    name = 'USERNAME'
    phone = 'DDDNUMBER'
    plan_opt = "0"
    
    sign_up  = signUp(
        name=name,
        phone=phone,
        e_mail=email,
        plan_opt=plan_opt
        )

    print(sign_up)
