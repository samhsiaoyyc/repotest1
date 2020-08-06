"""Starbucks menu scraper to be used for Starbucks chatbot."""

from typing import List, Text, Dict, Any, Tuple, Optional
import json
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from logging import getLogger

# I suggest not lowering this time, 2 seconds was leaving out a lot of important info
WAIT_TIME = 4

"""
 NOTES:
    - How to tie a default amount of shots to a drink size? For example, if the user orders an americano, it defaults to
      16oz and 3 shots. If the user changes the size to a 12oz, it should automatically change the number of shots. But
      the user should also be able to modify the number of shots.
"""

logger = getLogger(__name__)


def get_selection(driver: webdriver.Chrome, option_elements: Any) -> Dict[Text, Any]:
    """For each possible option, get all possible selections.

    Args:
        driver: chrome driver
        edit_buttons: webelements of the individual options

    Returns:
        Dict[Text, Dict[Text, Any]]: A dictionary of option name, option data pairs
            example: {'cream': {'price': 0, 'cal': 0}, 'room': {'price': 0, 'cal': 0} ... }

    """
    options_dict = {}
    category = selections = None

    for option in option_elements:
        # TODO: special case for quantity (like shots)
        # TODO: add default selections
        # TODO: fix type labeling to a more general label
        raw_selections = option.text.split('\n')
        if len(raw_selections) > 2:
            category = raw_selections[0]
            selections = raw_selections[2:]
        for s in selections:
            selection_info = {}
            selection_info['type'] = category
            selection_info['category'] = True
            selection_info['selected'] = False
            selection_info['quantity'] = None
            selection_info['calories'] = '0'
            selection_info['price'] = '0'
            # TODO: this isn't working, still getting 'with with whipped cream'
            if 'with' in s:
                s.strip('with ')
            options_dict[s] = selection_info
    return options_dict


def get_option_data(driver: webdriver.Chrome, edit_buttons: Any) -> Dict[Text, Dict[Text, Any]]:
    """Open each option field and get option data.

    Args:
        driver: chrome driver
        edit_buttons: webelements of the options 'edit' buttons

    Returns:
        Dict[Text, Dict[Text, Any]]: A dictionary of option name, option data pairs

    """
    wait = WebDriverWait(driver, WAIT_TIME)
    done_xpath = '//button[@data-e2e="doneFrap"]'
    option_elements_xpath = '//div[@class="selectLine___2LyZE"]/div[1]/div[1]'
    options_dict = {}

    for button in edit_buttons:
        button.click()
        wait.until(EC.visibility_of_element_located((By.XPATH, done_xpath)))
        # TODO: fix, not finding headers
        # option_categories = [cat.text for cat in driver.find_elements_by_xpath(option_category_xpath)]
        # logger.error(option_categories)
        options_dict.update(get_selection(driver, driver.find_elements_by_xpath(option_elements_xpath)))
        driver.find_element_by_xpath(done_xpath).click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    return options_dict


def get_options(driver: webdriver.Chrome, item: Text) -> Dict[Text, Dict[Text, Any]]:
    """Get all add-ons/options.

    Args:
        driver (Any): chrome driver
        item (Text): item page url

    Returns:
        Dict[Text, Dict[Text, Any]]: a dictionary of option, option info dict pairs
    """
    wait = WebDriverWait(driver, WAIT_TIME)
    options_dict = {}
    try:
        button_xpath = '//button[@class="sb-editField__button text-bold"]'
        # option_category_xpath = '//div[@class="frapPadding optionsSection__1eeR7"]/div/h2'
        # move down to get all options in view
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        wait.until(EC.visibility_of_all_elements_located((By.XPATH, button_xpath)))
        edit_buttons = driver.find_elements_by_xpath(button_xpath)
        # click into each set of options
        options_dict = get_option_data(driver, edit_buttons)

    except Exception as e:
        logger.error(f"There was a problem getting the options for {item}")
        logger.error(e)
    return options_dict


def get_size_cal_price(driver: webdriver.Chrome, item: Text
                       ) -> Tuple[Optional[Text], Optional[Text], Dict[Text, Dict[Text, Any]], List[Text]]:
    """Get the size info, number of calories, and price.

    Args:
        driver (Any): chrome driver
        item (Text): item page url

    Returns:
        Tuple[Optional[Text], Optional[Text], Dict[Text, Dict]]:
            default cal, default price, size options dict, list of req. slots
    """
    wait = WebDriverWait(driver, WAIT_TIME)
    size_options = {}
    default_size = None
    default_calories = None
    default_price = None
    # TODO: add all required slots, currently only size
    required_slots = []
    try:
        # find default size
        default_xpath = '//span[@class="select__selectedText"]'
        calorie_xpath = '//div[@class="calories___24fAg spaceBetween___9Mcd4 flexRow___1F07M yPadding___1vF3l"]/span'
        """
        add_button_xpath = '//button[@data-e2e="add-to-order-button"]'
        cart_button_xpath = '//button[@data-e2e="open-cart-button"]'
        price_xpath = '//span[@data-e2e="cart-item-price"]'
        decrease_button_xpath = '//button[@data-e2e="decreaseQuantityButton"]'
        """
        wait.until(EC.visibility_of_element_located((By.XPATH, default_xpath)))
        default_elements = driver.find_elements_by_xpath(default_xpath)
        if default_elements:
            default_size = default_elements[0].text
            default_size = default_size.split(" ")[0]
            if default_size:
                required_slots.append("size")
                # This seems to work but the price doesn't appear in the cart???
                """
                add_button = driver.find_element_by_xpath(add_button_xpath)
                cart_button = driver.find_element_by_xpath(cart_button_xpath)
                add_button.click()
                cart_button.click()
                wait.until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
                default_price = driver.find_element_by_xpath(price_xpath).text
                decrease_button = driver.find_element_by_xpath(decrease_button_xpath)
                decrease_button.click()
                driver.back()
                """

        # get default calories
        default_calories = driver.find_elements_by_xpath(calorie_xpath)[0].text.strip("Calories")

        # TODO FIX
        # get default price
        # add_button_xpath = '//button[@data-e2e="add-to-order-button"]'
        # driver.find_elements_by_xpath(add_button_xpath).click()
        # cart_button_xpath = '//button[@data-e2e="open-cart-button"]'
        # driver.find_elements_by_xpath(cart_button_xpath).click()

        # get list of possible sizes
        sizes_xpath = '//select[@id="sizeSelector"]/option'
        sizes = [option.get_attribute("value") for option in driver.find_elements_by_xpath(sizes_xpath)]
        if '' in sizes:
            sizes.remove("")
        for size in sizes:
            size_details = {}
            driver.find_element_by_xpath(sizes_xpath + f'[@value="{size}"]').click()
            size_details['type'] = 'size'
            size_details['category'] = True
            if default_size in size:
                size_details['selected'] = True
            else:
                size_details['selected'] = False
            size_details['quantity'] = None
            size_details['calories'] = str(int(driver.find_elements_by_xpath(calorie_xpath)[0].text.strip("Calories")) -
                                           int(default_calories))
            size_details['price'] = '0'  # TODO FIX PRICE
            size_options[size] = size_details

    except Exception as e:
        logger.error(f"There was a problem when getting size, calorie, and price info for {item}")
        logger.error(e)
    # TODO Fix price
    default_price = '3.00'
    return (default_calories, default_price, size_options, required_slots)


def get_item_ingredients(driver: webdriver.Chrome, item: Text) -> Optional[Text]:
    """Get the list of ingredients in the item.

    Args:
        driver (Any): Chrome driver
        item (Text): url to item page

    Returns:
        Optional[Text]: list of ingredients or none
    """
    wait = WebDriverWait(driver, WAIT_TIME)
    ingredients = None
    try:
        ingr_xpath = '//p[@class="my1"]/span'
        wait.until(EC.visibility_of_element_located((By.XPATH, ingr_xpath)))
        ingr_elements = driver.find_elements_by_xpath(ingr_xpath)
        if ingr_elements:
            ingr_elements = [ingr.text for ingr in ingr_elements]
            ingredients = ''.join(ingr_elements)
    except Exception as e:
        logger.error(f"Could not find ingredients for {item}")
        logger.error(e)
    return ingredients


def get_item_name(driver: webdriver.Chrome, item: Text) -> Optional[Text]:
    """Get the name of the item.

    Args:
        driver: Chrome driver
        item: url to the item page

    Returns:
        Optional[Text]: The item name or none

    """
    wait = WebDriverWait(driver, WAIT_TIME)
    item_name = None
    try:
        # wait for page to load and grab item name
        driver.get(item)
        name_xpath = '//h1[@class="sb-heading sb-heading--large text-bold"]'
        wait.until(EC.visibility_of_element_located((By.XPATH, name_xpath)))
        item_name = driver.find_element_by_xpath(name_xpath).text
    except Exception as e:
        logger.error(f"Could not find name for {item}")
        logger.error(e)

    return item_name


def get_image_url(driver: webdriver.Chrome, item: Text) -> Optional[Text]:
    """Get the url of the item image.

    Args:
        driver: Chrome driver
        item: a url to the item page

    Return:
        Optional[Text]: A url to the item image

    """
    image_url = None
    wait = WebDriverWait(driver, WAIT_TIME)
    try:
        # image url
        image_xpath = '//img[@class="sb-imageFade__imagePositioning sb-imageFade__show"]'
        wait.until(EC.visibility_of_element_located((By.XPATH, image_xpath)))
        image_url = driver.find_element_by_xpath(image_xpath).get_attribute('src')
    except Exception as e:
        logger.error(f"Could not find image for {item}")
        logger.error(e)

    return image_url


def get_item_description(driver: webdriver.Chrome, item: Text) -> Optional[Text]:
    """Get item description.

    Args:
        driver: Chrome driver
        item: a url to the item page

    Return:
        Optional[Text]: A description of the item.

    """
    item_desc = None
    wait = WebDriverWait(driver, WAIT_TIME)
    try:
        # item description
        desc_xpath = '//div[@data-e2e="productDescription"]'
        wait.until(EC.visibility_of_element_located((By.XPATH, desc_xpath)))
        item_desc = driver.find_element_by_xpath(desc_xpath).text
    except Exception as e:
        logger.error(f"Could not find description for {item}")
        logger.error(e)

    return item_desc


def get_item_data(driver: webdriver.Chrome, item: Text, cat_name: Text) -> Optional[Tuple[Text, Dict[Text, Any]]]:
    """Fill a dict with information for a particular item.

    Args:
        driver (Any): Chrome driver
        item (Text): A url to the item page
        cat_name (Text): The name of the item's category on the menu

    Returns:
        Tuple[Text, Dict[Text, Any]]: The item name and it's info as a dict

    """
    item_dict = {}
    item_dict["required_slots"] = []
    item_name = get_item_name(driver, item)
    if item_name:
        item_dict['category'] = cat_name
        item_dict['image'] = get_image_url(driver, item)
        item_dict['description'] = get_item_description(driver, item)
        item_dict['ingredients'] = get_item_ingredients(driver, item)
        cal, price, size_opts, req_slots = get_size_cal_price(driver, item)
        item_dict['calories'] = cal
        item_dict['price'] = price
        item_dict['options'] = size_opts
        item_dict['options'].update(get_options(driver, item))
        item_dict['required_slots'] += req_slots

        return (item_name, item_dict)
    else:
        return None


def get_menu_data(driver: webdriver.Chrome, categories: List[Text]) -> Dict[Text, Any]:
    """Scrape data for each menu item and return a dict of items.

    Args:
        driver (Any): Chrome driver
        categories (List[Text]): a list of urls to menu category pages

    Returns:
        Dict[Text, Any]: item name, item info dict pairs

    """
    wait = WebDriverWait(driver, WAIT_TIME)
    menu_dict = {}
    # loop through each category
    for c in categories:
        try:
            driver.get(c)
            xpath = '//a[@class="block linkOverlay__primary prodTile"]'
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            # grab the links to each item in the category
            item_links = [link.get_attribute('href') for link in driver.find_elements_by_xpath(xpath)]
            cat_name_xpath = '//h1[@class="sb-heading pb4 md-pb5 lg-pb7 text-bold"]'
            cat_name = driver.find_element_by_xpath(cat_name_xpath).text
            # send each link to get item data and get the returned dict key/value
            for item in item_links:
                scrape_result = get_item_data(driver, item, cat_name)
                if scrape_result:
                    item_name, item_data = scrape_result
                    menu_dict[item_name] = item_data
        except Exception as e:
            logger.error(e)
    return menu_dict


def set_store_location(driver: webdriver.Chrome) -> None:
    """Set the store location on the Starbucks website.

    The store location must be set in order for price information to show.
    If location is enabled on Chrome, it will use the user's location and
    pick the closest store, otherwise it will default to downtown Seattle.

    Args:
        driver (Any): Chrome driver

    """
    wait = WebDriverWait(driver, WAIT_TIME)
    store_xpath = '//a[@class="decorativeUnderline pb1 lg-pb2 container___3FzPz"]'
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, store_xpath)))
        logger.error(driver.find_element_by_xpath(store_xpath).get_attribute('href'))
        driver.get(driver.find_element_by_xpath(store_xpath).get_attribute('href'))
        # try to fill location, pass if chrome is already using location data
        try:
            driver.find_element_by_xpath('//input[@name="place"]').send_keys("seattle, wa\n")
        except Exception:
            logger.info("Using location to get closest store")
        button_xpath = '//button[@data-e2e="confirmStoreButton"]'
        wait.until(EC.visibility_of_element_located((By.XPATH, button_xpath)))
        driver.find_element_by_xpath(button_xpath).click()
    except Exception as e:
        logger.error(e)
    return


def main():
    """Scrape starbucks menu."""
    # setup driver and set root to starbucks homepage
    root_url = 'https://www.starbucks.com/'
    driver = webdriver.Chrome('/opt/webdrivers/bin/chromedriver')
    driver.get(root_url + '/menu/')
    wait = WebDriverWait(driver, WAIT_TIME)

    # set store (required to get prices)
    set_store_location(driver)

    # set xpath to grab the urls of all category buttons
    xpath = '//a[@class="block linkOverlay__primary tile___wDvCC"]'
    # create a list of all the paths to each category
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    category_links = [link.get_attribute('href') for link in driver.find_elements_by_xpath(xpath)]

    menu_data = get_menu_data(driver, category_links)
    driver.quit()

    # export to json file
    with open('./bots/starbucks/data/menus/starbucks.json', 'w') as f:
        json.dump(menu_data, f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


if __name__ == '__main__':
    main()
