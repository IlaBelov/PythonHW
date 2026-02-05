import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Dict


class CheckoutPage:
    """
    Page Object класс для работы со страницами оформления заказа.
    """

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container")

    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON_OVERVIEW = (By.ID, "cancel")

    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    COMPLETE_MESSAGE = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу оформления заказа.

        Args:
            driver: Экземпляр WebDriver для управления браузером
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Ожидание загрузки страницы информации о покупателе")
    def wait_for_checkout_info_page(self) -> 'CheckoutPage':
        """
        Ожидает загрузки страницы с информацией о покупателе.

        Returns:
            CheckoutPage: текущий экземпляр класса
        """
        self.wait.until(
            EC.presence_of_element_located(self.FIRST_NAME_INPUT)
        )
        return self

    @allure.step("Ожидание загрузки страницы обзора заказа")
    def wait_for_checkout_overview_page(self) -> 'CheckoutPage':
        """
        Ожидает загрузки страницы обзора заказа.

        Returns:
            CheckoutPage: текущий экземпляр класса
        """
        self.wait.until(
            EC.presence_of_element_located(self.FINISH_BUTTON)
        )
        return self

    @allure.step(
            "Заполнить информацию о покупателе:"
            " {first_name} {last_name}, индекс: {postal_code}")
    def fill_checkout_info(
            self, first_name: str,
            last_name: str, postal_code: str) -> 'CheckoutPage':
        """
        Заполняет поля информации о покупателе.

        Args:
            first_name: str - имя покупателя
            last_name: str - фамилия покупателя
            postal_code: str - почтовый индекс

        Returns:
            CheckoutPage: текущий экземпляр класса
        """
        self.wait_for_checkout_info_page()

        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(
            *self.POSTAL_CODE_INPUT).send_keys(postal_code)

        return self

    @allure.step("Нажать кнопку 'Continue'")
    def click_continue(self) -> 'CheckoutPage':
        """
        Нажимает кнопку продолжения оформления заказа.

        Returns:
            CheckoutPage: текущий экземпляр класса
        """
        element = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        )
        element.click()
        return self

    @allure.step("Получить общую сумму заказа")
    def get_total_amount(self) -> float:
        """
        Извлекает и парсит общую сумму заказа.

        Returns:
            float: общая сумма заказа
        """
        self.wait_for_checkout_overview_page()

        element = self.wait.until(
            EC.presence_of_element_located(self.TOTAL_LABEL)
        )

        total_text = element.text
        amount_str = total_text.replace("Total: $", "").strip()

        return float(amount_str)

    @allure.step("Получить полную сводку по заказу")
    def get_summary_info(self) -> Dict[str, str]:
        """
        Получает всю финансовую информацию о заказе.

        Returns:
            Dict[str, str]: словарь с ключами subtotal, tax, total
        """
        self.wait_for_checkout_overview_page()

        subtotal = self.driver.find_element(*self.SUBTOTAL_LABEL).text
        tax = self.driver.find_element(*self.TAX_LABEL).text
        total = self.driver.find_element(*self.TOTAL_LABEL).text

        return {
            "subtotal": subtotal,
            "tax": tax,
            "total": total
        }

    @allure.step("Нажать кнопку 'Finish'")
    def click_finish(self) -> 'CheckoutPage':
        """
        Нажимает кнопку завершения заказа.

        Returns:
            CheckoutPage: текущий экземпляр класса
        """
        element = self.wait.until(
            EC.element_to_be_clickable(self.FINISH_BUTTON)
        )
        element.click()
        return self

    @allure.step("Получить сообщение о завершении заказа")
    def get_complete_message(self) -> str:
        """
        Извлекает сообщение об успешном оформлении заказа.

        Returns:
            str: текст сообщения о завершении заказа
        """
        element = self.wait.until(
            EC.presence_of_element_located(self.COMPLETE_MESSAGE)
        )
        return element.text
