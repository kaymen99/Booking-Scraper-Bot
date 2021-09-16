import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

def change_currency(driver, currency='USD'):
    currency_button = driver.find_element_by_css_selector('button[data-modal-aria-label="Select your currency"]')
    currency_button.click()
    time.sleep(3)
    currency = driver.find_element_by_css_selector(
        f'a[data-modal-header-async-url-param="changed_currency=1;selected_currency={currency}"]')
    currency.click()

def change_lang(driver):
    lang_button = driver.find_element_by_css_selector('button[data-modal-id="language-selection"]')
    lang_button.click()
    lang = driver.find_element_by_css_selector('a[data-lang="en-us"]')
    lang.click()

def choose_destination(driver, location):
    destination_search = driver.find_element_by_css_selector('input[aria-label="Type your destination"]')
    destination_search.click()
    destination_search.send_keys(location)
    time.sleep(2)
    first_element = driver.find_element_by_css_selector('li[data-i="0"]')
    first_element.click()

def choose_date(driver, start='2021-09-16', end='2021-10-23'):
    start_date = driver.find_element_by_css_selector(f'td[data-date="{start}"]')
    start_date.click()
    end_date = driver.find_element_by_css_selector(f'td[data-date="{end}"]')
    end_date.click()

def choose_persons(driver, adults=3, rooms=2):
    person_search = driver.find_element_by_css_selector('div[class="xp__input-group xp__guests"]')
    person_search.click()
    adult_reset = driver.find_element_by_css_selector('button[aria-label="Decrease number of Adults"]')
    adult_n = driver.find_element_by_css_selector('input[id="group_adults"]').get_attribute('value')

    while True:
        adult_reset.click()
        adult_n = driver.find_element_by_css_selector('input[id="group_adults"]').get_attribute('value')
        if int(adult_n) == 1:
            break
    adult_increase = driver.find_element_by_css_selector('button[aria-label="Increase number of Adults"]')
    for i in range(adults - 1):
        adult_increase.click()

    """
    children_increase = driver.find_element_by_css_selector('button[aria-label="Increase number of Children"]')
    for _ in range(children):
        children_increase.click()
    for i in range(children):
        select = Select(driver.find_element_by_css_selector(f'select[aria-label="Child {i + 1} age"]'))
        time.sleep(1)
        select.select_by_value('10')
    """
    rooms_increase = driver.find_element_by_css_selector('button[aria-label="Increase number of Rooms"]')
    for _ in range(rooms - 1):
        rooms_increase.click()

    

def search(driver):
    driver.find_element_by_css_selector('button[type="submit"]').click()