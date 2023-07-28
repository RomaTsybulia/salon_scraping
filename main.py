import time

from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

def get_all_salons(location: str, category):
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    work_driver = wd.Chrome(service=Service(), options=chrome_options)

    url = 'https://www.yelp.ca'
    work_driver.get(url)
    time.sleep(3)
    category_field = work_driver.find_element(By.ID, "search_description")
    location_field = work_driver.find_element(By.ID, "search_location")

    category_field.send_keys(category)
    location_field.send_keys(location)

    submit_button = work_driver.find_element(By.CSS_SELECTOR, 'button[data-testid="suggest-submit"]')
    submit_button.click()

    elements = work_driver.find_elements(By.CSS_SELECTOR, 'a.css-1idmmu3[role="link"]')

    return elements, work_driver


def get_salon_information(salons, work_driver):
    salons_urls = [salon.get_attribute("href") for salon in salons]
    all_data = []
    for salon_url in set(salons_urls):
        work_driver.get(salon_url)
        data_dict = {}
        print(salon_url)
        name = WebDriverWait(work_driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.css-1se8maq'))
        )
        data_dict["name"] = name.text
        try:
            phone_number_label = work_driver.find_element(By.XPATH,
                                                 '//p[contains(text(), "Phone number")]')
            phone_number_element = phone_number_label.find_element(By.XPATH,
                                                               './following-sibling::p')
            data_dict["phone"] = phone_number_element.text
        except Exception:
            data_dict["phone"] = ""

        try:
            city_elements = work_driver.find_elements(By.CSS_SELECTOR,
                                                       "p.css-1sb02f4 span.raw__09f24__T4Ezm")
            if len(city_elements) > 1:
                city_element = city_elements[1].text
            else:
                city_element = city_elements[0].text
            data_dict["postal_code"] = " ".join(city_element.split(", ")[1].split(" ")[1:])
            desired_elements = work_driver.find_elements(By.CLASS_NAME, 'css-gutk1c')

            data_dict["district"] = desired_elements[2].text
        except Exception:
            data_dict["postal_code"] = ""
            data_dict["district"] = ""
        print(salon_url)
        try:
            parent_div = work_driver.find_element(By.CSS_SELECTOR,
                                                  'div.photo-header-content__09f24__q7rNO')
            all_spans = parent_div.find_elements(By.TAG_NAME, 'span')
            yelp_category = ""
            for i in range(8, len(all_spans)):
                if "$" in all_spans[i].text:
                    continue
                if all_spans[i].text == "Edit":
                    break

                yelp_category += " " + all_spans[i].text
            data_dict["yelp_category"] = yelp_category.lstrip()

            site_url = work_driver.find_element(By.CSS_SELECTOR, 'p.css-1p9ibgf a.css-1idmmu3')
            data_dict["site"] = "https://" + site_url.text

            all_data.append(data_dict)
        except Exception:
            continue
        work_driver.quit()
    return all_data


def excel_performer(data):
    columns_order = ['Name', 'Site', 'Telephone', 'Search category',
                     'yelp_category', 'Search address', 'District', 'City',
                      'Address', 'Postal_code']

    df = pd.DataFrame(data, columns=columns_order)

    output_file = 'eyelash_services.xlsx'
    df.to_excel(output_file, index=False)

    print(f"Data successfully saved to '{output_file}'.")


def main():
    location = input("Enter city: ")
    search_category = input("Enter category: ")
    search_address = input("Enter disctrict: ")
    postal_code = input("Enter postal code: ")

    salons, work_driver = get_all_salons(location, search_category)
    data = get_salon_information(salons, work_driver)

    filtered_data = []
    for salon in data:
        salon["city"] = location.split(", ")[0]
        salon["search search_category"] = search_category
        if salon["district"] == search_address or salon["postal_code"] == postal_code:
            filtered_data.append(salon)

    excel_performer(filtered_data)


if __name__ == "__main__":
    main()
