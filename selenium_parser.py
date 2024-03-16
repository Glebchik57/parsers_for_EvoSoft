import time
import csv
import os

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

try:
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

    browser.get(link)

    browser.implicitly_wait(15)

    market_data = browser.find_element(By.ID, 'link_2')
    hover = ActionChains(browser).move_to_element(market_data)
    hover.perform()

    preopen_market = browser.find_element(
        By.XPATH, '//a[text()="Pre-Open Market"][1]'
    )
    preopen_market.click()

    titles = [
        title.text for title in browser.find_elements(
            By.CSS_SELECTOR, '.symbol-word-break'
        )
    ]
    costs = [
        cost.text for cost in browser.find_elements(
            By.CSS_SELECTOR, 'tbody .bold.text-right'
        )
    ]

    with open('parcered_data.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['Title', 'Price'])
        for title, cost in zip(titles, costs):
            writer.writerow([title, cost])

    main_page = browser.find_element(
        By.CSS_SELECTOR, '.container.top_logomenu .navbar-brand'
    )
    main_page.click()

    NB_button = browser.find_element(By.ID, 'NIFTY BANK')
    NB_button.click()

    draw = browser.find_element(By.ID, 'tab4_container')
    browser.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
        draw
    )

    viewall = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#tab4_gainers_loosers .link-wrap a')
        )
    )
    browser.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
        viewall
    )
    viewall.click()

    select = Select(browser.find_element(By.ID, "equitieStockSelect"))
    select.select_by_value("NIFTY ALPHA 50")

    table = browser.find_elements(By.CSS_SELECTOR, '.symbol-word-break')
    browser.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
        table[-1]
    )

finally:
    time.sleep(5)
    browser.quit()
