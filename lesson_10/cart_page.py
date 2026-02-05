import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple


class CartPage:
    """
    Page Object класс для работы со страницей корзины покупок.
    """

    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу корзины.

        Args:
            driver: Экземпляр WebDriver для управления браузером
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Ожидание загрузки страницы корзины")
    def wait_for_page_load(self) -> 'CartPage':
        """
        Ожидает полной загрузки страницы корзины.

        Returns:
            CartPage: текущий экземпляр класса
        """
        self.wait.until(
            EC.presence_of_element_located(self.CHECKOUT_BUTTON)
        )
        return self

    @allure.step("Нажать кнопку 'Checkout'")
    def click_checkout(self) -> 'CartPage':
        """
        Нажимает кнопку оформления заказа.

        Returns:
            CartPage: текущий экземпляр класса
        """
        element = self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        element.click()
        return self

    @allure.step("Получить все товары из корзины")
    def get_cart_items(self) -> List[WebElement]:
        """
        Находит все товары, добавленные в корзину.

        Returns:
            List[WebElement]: список веб-элементов товаров
        """
        items = self.driver.find_elements(*self.CART_ITEMS)
        return items

    @allure.step("Получить названия всех товаров в корзине")
    def get_cart_items_names(self) -> List[str]:
        """
        Извлекает текстовые названия всех товаров в корзине.

        Returns:
            List[str]: список названий товаров
        """
        items = self.get_cart_items()
        names = []
        for item in items:
            name_element = item.find_element(*self.ITEM_NAME)
            names.append(name_element.text)
        return names

    @allure.step("Проверить наличие товаров в корзине: {expected_items}")
    def verify_cart_contains(self, expected_items: List[str]) -> Tuple[
            bool, str]:
        """
        Проверяет наличие ожидаемых товаров в корзине.

        Args:
            expected_items: List[str] - список ожидаемых названий товаров

        Returns:
            Tuple[bool, str]: (результат проверки, сообщение)
        """
        actual_items = self.get_cart_items_names()

        for item in expected_items:
            if item not in actual_items:
                error_msg = f"Товар '{item}' отсутствует в корзине"
                allure.attach(
                    f"Ожидалось: {expected_items}\nФактически: {actual_items}",
                    name="Детали проверки корзины",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False, error_msg

        success_msg = "Все товары присутствуют в корзине"
        allure.attach(
            f"Проверка пройдена успешно\nОжидаемые товары: {expected_items}",
            name="Успешная проверка корзины",
            attachment_type=allure.attachment_type.TEXT
        )
        return True, success_msg
