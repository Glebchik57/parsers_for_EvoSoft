import time
import os
from functools import wraps
from random import randint

from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from seleniumwire import webdriver
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

load_dotenv()
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
IP_ADRESS = os.getenv('FR_IP_ADRESS')
PORT = os.getenv('FR_PORT')

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

proxy_options = {
    'proxy': {
        'http': f'http://{LOGIN}:{PASSWORD}@{IP_ADRESS}:{PORT}'
    }
}

link = 'https://twitter.com/elonmusk'
browser = webdriver.Chrome(
    options=options,
    seleniumwire_options=proxy_options
)

stealth(
    browser,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)


def set_browser(func):
    '''Декоратор запускает браузер,
    выполняет функцию, к которой он применен,
    после чего закрывает браузер'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        browser.implicitly_wait(15)
        browser.get(link)
        func()
        time.sleep(5)
        browser.close()
        browser.quit()
    return wrapper()


def wait(how, what):
    WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((how, what))
    )


def wait_loadung_page():
    '''Ожидание загрузки страницы'''
    state = ""
    while state != "complete":
        time.sleep(randint(3, 5))
        state = browser.execute_script("return document.readyState")


def find_elms(how, what):
    '''Находит все элементы на странице
    how - метод "By" для поиска
    what - CSS селектор или Xpath'''
    return browser.find_elements(how, what)


def collector():
    '''Сборщик текста из Твитов'''
    body = browser.find_element(By.CSS_SELECTOR, 'body')
    twits = []
    while len(twits) != 10:
        body.send_keys(Keys.PAGE_DOWN)
        for i in find_elms(
            By.CSS_SELECTOR,
            '[data-testid="tweet"] [data-testid="tweetText"]'
        ):
            if i.text in twits:
                continue
            else:
                try:
                    twits.append(i.text)
                except Exception:
                    continue
        time.sleep(randint(3, 5))
    return twits


def print_tweets(tweets):
    '''Выводит твиты в консоль'''
    for twet in tweets:
        print(twet)


@set_browser
def main():
    wait_loadung_page()
    wait(By.CSS_SELECTOR, '[data-testid="tweet"]')
    print_tweets(collector())


if __name__ == "__main__":
    main()
