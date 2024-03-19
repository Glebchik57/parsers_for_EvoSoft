import time
import csv
import os
from functools import wraps

from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv

load_dotenv()
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
IP_ADRESS = os.getenv('IP_ADRESS')
PORT = os.getenv('PORT')

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

proxy_options = {
    'proxy': {
        'http': f'http://{LOGIN}:{PASSWORD}@{IP_ADRESS}:{PORT}'
    }
}

link = 'https://www.nseindia.com/'
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


def find_el(how, what):
    '''Находит конкретный элемент на странице
    how - метод "By" для поиска
    what - CSS селектор или Xpath'''
    element = browser.find_element(how, what)
    return element


def find_elms(how, what):
    '''Находит все элементы на странице
    how - метод "By" для поиска
    what - CSS селектор или Xpath'''
    elements = browser.find_elements(how, what)
    return elements


def hover_to_point(elm):
    '''наводится на выбранный элемент'''
    hover = ActionChains(browser).move_to_element(elm)
    hover.perform()


def write_to_csv(titles, costs):
    '''Создает csv файл и записывает туда переданные значния'''
    data1 = [
        title.text for title in titles
    ]
    data2 = [
        cost.text for cost in costs
    ]
    with open('parcered_data.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['Title', 'Price'])
        for title, cost in zip(data1, data2):
            writer.writerow([title, cost])


def scroll(target):
    '''Скролит до выбранного элемента'''
    time.sleep(1)
    browser.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
        target
    )
    time.sleep(3)


def wait(target):
    '''Ждет пока выбраный элемент станет кликабельным'''
    waiting = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (target)
        )
    )
    return waiting


def sel(slct, value):
    '''Выбирает элемент из выподающего списка'''
    Select(slct).select_by_value(value)


def common_move():
    '''Имитация пользовательского сценария'''
    find_el(By.CSS_SELECTOR, '.container.top_logomenu .navbar-brand').click()
    find_el(By.ID, 'NIFTY BANK').click()
    scroll(find_el(By.ID, 'tab4_container'))
    wait(find_el(By.CSS_SELECTOR, '#tab4_gainers_loosers .link-wrap a'))
    scroll(find_el(By.CSS_SELECTOR, '#tab4_gainers_loosers .link-wrap a'))
    find_el(By.CSS_SELECTOR, '#tab4_gainers_loosers .link-wrap a').click()
    sel(find_el(By.ID, "equitieStockSelect"), "NIFTY ALPHA 50")
    scroll(find_elms(By.CSS_SELECTOR, '.symbol-word-break')[-1])


@set_browser
def main():
    try:
        hover_to_point(find_el(By.ID, 'link_2'))
        find_el(By.XPATH, '//a[text()="Pre-Open Market"][1]').click()
        scroll(find_elms(By.CSS_SELECTOR, '.symbol-word-break')[-1])
        scroll(find_el(By.CSS_SELECTOR, '.container.top_logomenu .navbar-brand'))
        write_to_csv(
            find_elms(By.CSS_SELECTOR, '.symbol-word-break'),
            find_elms(By.CSS_SELECTOR, 'tbody .bold.text-right')
        )
        common_move()
    except Exception as error:
        return f'что-то пошло не так:{error}'
    return 'Успешно'


if __name__ == "__main__":
    main()
