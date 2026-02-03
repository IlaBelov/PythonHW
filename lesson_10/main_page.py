import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from typing import List, Tuple


class MainPage:
    """
    Page Object класс для работы с главной страницей интернет-магазина.
    """

    CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")

    @staticmethod
    @allure.step(
        "Получить локатор кнопки 'Add to cart' для товара: {product_name}")
    def get_add_to_cart_button(product_name: str) -> Tuple[str, str]:
        """
        Генерирует локатор для кнопки добавления товара в корзину.

        Args:
            product_name: str - название товара

        Returns:
            Tuple[str, str]: кортеж (By.ID, значение) для локатора кнопки
        """
        button_id = product_name.lower().replace(" ", "-")
        return (By.ID, f"add-to-cart-{button_id}")

    @staticmethod
    @allure.step("Получить локатор кнопки 'Remove' для товара: {product_name}")
    def get_remove_button(product_name: str) -> Tuple[str, str]:
        """
        Генерирует локатор для кнопки удаления товара из корзины.

        Args:
            product_name: str - название товара

        Returns:
            Tuple[str, str]: кортеж (By.ID, значение) для локатора кнопки
        """
        button_id = product_name.lower().replace(" ", "-")
        return (By.ID, f"remove-{button_id}")

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует главную страницу магазина.

        Args:
            driver: Экземпляр WebDriver для управления браузером
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Ожидание загрузки главной страницы")
    def wait_for_page_load(self) -> 'MainPage':
        """
        Ожидает полной загрузки главной страницы магазина.

        Returns:
            MainPage: текущий экземпляр класса
        """
        self.wait.until(
            EC.presence_of_element_located(self.INVENTORY_LIST)
        )
        return self

    @allure.step("Добавить товар '{product_name}' в корзину")
    def add_product_to_cart(self, product_name: str) -> 'MainPage':
        """
        Добавляет указанный товар в корзину.

        Args:
            product_name: str - название товара для добавления в корзину

        Returns:
            MainPage: текущий экземпляр класса
        """
        button_locator = self.get_add_to_cart_button(product_name)

        element = self.wait.until(
            EC.element_to_be_clickable(button_locator)
        )
        element.click()

        return self

    @allure.step("Добавить несколько товаров в корзину: {product_names}")
    def add_products_to_cart(self, product_names: List[str]) -> 'MainPage':
        """
        Добавляет несколько товаров в корзину.

        Args:
            product_names: List[str] - список названий товаров для добавления

        Returns:
            MainPage: текущий экземпляр класса
        """
        for product_name in product_names:
            self.add_product_to_cart(product_name)
        return self

    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> 'MainPage':
        """
        Нажимает на иконку корзины для перехода на страницу корзины.

        Returns:
            MainPage: текущий экземпляр класса
        """
        element = self.wait.until(
            EC.element_to_be_clickable(self.CART_BUTTON)
        )
        element.click()
        return self
