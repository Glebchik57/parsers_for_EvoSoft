import time
import csv
import os

from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
IP_ADRESS = os.getenv('IP_ADRESS')
PORT = os.getenv('PORT')

proxy_options = {
    'proxy': {
        'http': f'http://{LOGIN}:{PASSWORD}@{IP_ADRESS}:{PORT}'
    }
}

try:
    link = 'https://www.nseindia.com/'
    browser = webdriver.Chrome(seleniumwire_options=proxy_options)
    browser.get(link)

    market_data = browser.find_element(By.ID, 'link_2')
    hover = ActionChains(browser).move_to_element(market_data)
    hover.perform()

    preopen_market = browser.find_element(By.CSS_SELECTOR, '#main_navbar > ul > li:nth-child(3) > div > div.container > div > div:nth-child(1) > ul > li:nth-child(1) > a')
    preopen_market.click()

    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.symbol-word-break'))
    )

    titles = [title.text for title in browser.find_elements(By.CSS_SELECTOR, '.symbol-word-break')]
    costs = [cost.text for cost in browser.find_elements(By.CSS_SELECTOR, 'tbody .bold.text-right')]

    data = list(zip(titles, costs))

    print(data)

    with open('parcered_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Имя', 'Цена'])
        for item in data:
            writer.writerow([item[0], item[1]])

finally:
    time.sleep(5)
    browser.quit()
