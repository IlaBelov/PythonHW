from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:

    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_page_load(self):
        self.wait.until(
            EC.presence_of_element_located(self.CHECKOUT_BUTTON)
        )
        return self

    def click_checkout(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        element.click()
        return self

    def get_cart_items(self):
        items = self.driver.find_elements(*self.CART_ITEMS)
        return items

    def get_cart_items_names(self):
        items = self.get_cart_items()
        names = []
        for item in items:
            name_element = item.find_element(*self.ITEM_NAME)
            names.append(name_element.text)
        return names

    def verify_cart_contains(self, expected_items):
        actual_items = self.get_cart_items_names()
        for item in expected_items:
            if item not in actual_items:
                return False, f"Товар '{item}' отсутствует в корзине"
        return True, "Все товары присутствуют в корзине"
