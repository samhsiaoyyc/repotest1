"""Taco Bell menu scraper.

This script uses Selenium to scrape the Taco Bell website for
menu information and saves the result as a json file.

TODO:
    * Add support for running headless.
    * Replace arbitrary time.sleep calls with ExpectedConditions
"""

import time
import json
import os
from typing import Any, Text, Dict, List

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_addon_data(el) -> Dict[Text, Any]:
    """Get an addon data dict from a div[@class=custom-info] element."""
    name_xpath = './/span[@class="custom-name"]'
    name = el.find_element_by_xpath(name_xpath).text
    price_calorie_xpath = './/span[@class="price-calorie"]'
    price_calorie = el.find_element_by_xpath(price_calorie_xpath).text
    return {"name": name,
            "price": price_calorie.split()[1],
            "calorie": price_calorie.split()[-2]}


def get_data_group(driver, group_name) -> List[Dict[Text, Any]]:
    """Get data from the specified data-group div."""
    group_xpath = '//div[@data-group="{}"]'.format(group_name)
    addons_els = driver.find_elements_by_xpath(group_xpath)
    if addons_els:
        addons_el = addons_els[0]
        info_xpath = './/div[@class="custom-info"]'
        return [get_addon_data(info_el)
                for info_el in addons_el.find_elements_by_xpath(info_xpath)]
    else:
        return []


def get_size_data(card_el) -> List[Dict[Text, Any]]:
    """Get size data from a size dropdown menu."""
    size_xpath = './/span[@class="size-name"]'
    size_els = card_el.find_elements_by_xpath(size_xpath)
    retval = []
    if not size_els:
        return retval
    size_els[0].find_element_by_xpath('./..').click()
    time.sleep(0.2)  # TODO use await instead of sleep
    size_option_xpath = './/ul[@class="size-dropdown"]/li'
    size_option_els = card_el.find_elements_by_xpath(size_option_xpath)
    for size_option_el in size_option_els:
        size_name = size_option_el.text or 'Large'
        retval.append({
            size_name: {
                'calorie': size_option_el.get_attribute('data-calories'),
                'price': size_option_el.get_attribute('data-price')}})
    return retval


def get_menu_data(menu_links) -> Dict[Text, Any]:
    """Get menu data from a list of menu links."""
    menu_data = {'menu_categories': {}}
    for menu_link in menu_links:
        driver.get(menu_link)
        menu_name = ' '.join(menu_link.split('/')[-1].split('-'))
        menu_data['menu_categories'][menu_name] = []
        time.sleep(2)
        card_xpath = '//div[@class="product-card"]'
        for card_el in driver.find_elements_by_xpath(card_xpath):
            xstr = './/div[@class="product-{}"]'
            name_els, price_els, calorie_els = [
                card_el.find_elements_by_xpath(xstr.format(item))
                for item in ['name', 'price', 'calorie']
            ]

            if name_els and price_els and calorie_els:
                name = name_els[0].text
                menu_data['menu_categories'][menu_name].append(name)
                menu_data[name] = {
                    "product-price": price_els[0].text,
                    "product-calorie": calorie_els[0].text,
                    'addons': [],
                    'sauces': []
                }

            menu_data[name]['sizes'] = get_size_data(card_el)

            button_xpath = ('.//button[@class="btn '
                            'btn-customize js-customize-btn"]')
            buttons = card_el.find_elements_by_xpath(button_xpath)
            if buttons:
                time.sleep(0.5)  # TODO use await instead of sleep
                buttons[0].click()
                time.sleep(0.5)  # TODO use await instead of sleep
                menu_data[name]['addons'] += get_data_group(driver, 'addons')
                menu_data[name]['sauces'] += get_data_group(driver, 'sauces')
                time.sleep(0.3)
                driver.find_element_by_xpath("/html").send_keys(Keys.ESCAPE)
                time.sleep(2)
    return menu_data


if __name__ == "__main__":
    DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']

    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    url_root = 'http://www.tacobell.com'
    driver.get(url_root + '/food')
    xpath = '//a[@class="cls-category-card-item"]'
    menu_links = [link_el.get_attribute('href')
                  for link_el in driver.find_elements_by_xpath(xpath)][3:-3]

    menu_data = get_menu_data(menu_links)

    with open('scraped_menu.json', 'w') as f:
        json.dump(menu_data, f)
