from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:

    CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")

    @staticmethod
    def get_add_to_cart_button(product_name):
        button_id = product_name.lower().replace(" ", "-")
        return (By.ID, f"add-to-cart-{button_id}")

    @staticmethod
    def get_remove_button(product_name):
        button_id = product_name.lower().replace(" ", "-")
        return (By.ID, f"remove-{button_id}")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_page_load(self):
        self.wait.until(
            EC.presence_of_element_located(self.INVENTORY_LIST)
        )
        return self

    def add_product_to_cart(self, product_name):
        button_locator = self.get_add_to_cart_button(product_name)
        element = self.wait.until(
            EC.element_to_be_clickable(button_locator)
        )
        element.click()
        return self

    def add_products_to_cart(self, product_names):
        for product_name in product_names:
            self.add_product_to_cart(product_name)
        return self

    def go_to_cart(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.CART_BUTTON)
        )
        element.click()
        return self
