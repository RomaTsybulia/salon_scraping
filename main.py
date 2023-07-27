import time
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_all_salons(location: str, categories):
    firefox_options = Options()
    firefox_options.add_argument('-headless')
    work_driver = wd.Firefox(service=Service(), options=firefox_options)
    url = 'https://www.yelp.ca'
    work_driver.get(url)

    category_field = work_driver.find_element(By.ID, "search_description")
    location_field = work_driver.find_element(By.ID, "search_location")
    category_field.send_keys(categories)
    location_field.send_keys(location)
    submit_button = work_driver.find_element(By.CSS_SELECTOR, 'button[data-testid="suggest-submit"]')
    submit_button.click()

    elements = work_driver.find_elements(By.CSS_SELECTOR, 'a.css-1idmmu3[role="link"]')

    return elements, work_driver

def get_salon_information(salons, driver):
    for salon in salons:
        url = salon.get_attribute("href")
        driver.get(url)



salons, driver = get_all_salons("Kamloops, BC", "Eyelash Services")
get_salon_information(salons, driver)



