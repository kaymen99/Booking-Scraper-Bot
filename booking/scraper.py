import time, os
from functions import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from selenium.webdriver.chrome.options import Options 

def scrape(currency, city, start, end, adultes, rooms):
	opts = Options()
	opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36")
	opts.add_argument('--lang=en')
	opts.add_argument('--headless')
	driver = webdriver.Chrome(options=opts)
	driver.maximize_window()
	print('Getting the page')
	driver.get(f'https://www.booking.com')
	time.sleep(8)
	change_lang(driver)
	time.sleep(4)
	change_currency(driver, currency)
	time.sleep(4)
	choose_destination(driver, city)
	time.sleep(4)
	choose_date(driver, start, end)
	time.sleep(4)
	choose_persons(driver, adultes, rooms)
	time.sleep(4)
	search(driver)
	time.sleep(8)




	places = driver.find_element_by_id('hotellist_inner').find_elements_by_xpath('//*[@id="hotellist_inner"]/div/div[2]')
	elements = []

	try:
		while True:
			print(f'found {len(places)} properties on this pages')
			for i in range(len(places)):
				try:
					hotel = places[i].find_element_by_class_name('sr-hotel__title-wrap').find_element_by_tag_name('h3').find_element_by_tag_name('span').text
					url = places[i].find_element_by_tag_name('h3').find_element_by_tag_name('a').get_attribute('href')
					try:
						rating = places[i].find_element_by_class_name('sr-hotel__title-wrap').find_element_by_class_name('sr-hotel__title-badges').find_elements_by_tag_name('span')[2].get_attribute('aria-label')
					except IndexError as e:
						rating = ''
					reviews_note = places[i].find_element_by_class_name('sr_item_review_block').find_element_by_css_selector('div[class="sr-review-score"]').get_attribute('data-ugc-review-score')
					n_reviews = places[i].find_element_by_class_name('sr_item_review_block').find_element_by_css_selector('div[class="sr-review-score"]').get_attribute('data-ugc-review-nr')
					location = places[i].find_element_by_class_name('sr_card_address_line').find_element_by_tag_name('a').text[:-21]
					room_details = '|'.join(places[i].find_element_by_class_name('room_details ').find_element_by_class_name('roomNameInner').text.split('\n'))
					orders = [i.text for i in places[i].find_elements_by_class_name('prco-ltr-right-align-helper')]
					price = orders[1].split('\n')[0]
					taxes = orders[2][1:-18]
					elements.append([hotel, url, location, rating, reviews_note, n_reviews, room_details, price, taxes])
				except NoSuchElementException:
					pass
			print('finished page')
			driver.find_element_by_css_selector('a[title="Next page"]').click()
			time.sleep(8)
			places = driver.find_element_by_id('hotellist_inner').find_elements_by_xpath('//*[@id="hotellist_inner"]/div/div[2]')
	except NoSuchElementException:
				pass







	data = pd.DataFrame(elements, columns=['hotel', 'url', 'location', 'rating', 'reviews_note', 'n_reviews', 'room_details', 'price', 'taxes and charges'])
	save_path = os.path.join(os.getcwd(), 'data.csv')
	data.to_csv(save_path)

	print('finished')
	driver.quit()






