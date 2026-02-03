import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional, Union
from selenium.webdriver.remote.webdriver import WebDriver


class SlowCalculatorPage:

    DELAY_INPUT = (By.CSS_SELECTOR, "#delay")
    RESULT_DISPLAY = (By.CLASS_NAME, "screen")
    BUTTON_7 = (By.XPATH, "//span[text()='7']")
    BUTTON_8 = (By.XPATH, "//span[text()='8']")
    BUTTON_PLUS = (By.XPATH, "//span[text()='+']")
    BUTTON_EQUALS = (By.XPATH, "//span[text()='=']")

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу калькулятора.

        Args:
            driver: Экземпляр WebDriver для управления браузером
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)

    @allure.step("Открыть страницу калькулятора")
    def open(self) -> None:
        """Открывает страницу медленного калькулятора."""
        self.driver.get(
            "https://bonigarcia.dev"
            "/selenium-webdriver-java/slow-calculator.html"
        )

    @allure.step("Установить задержку вычислений: {seconds} секунд")
    def set_delay(self, seconds: Union[str, int]) -> None:
        """
        Устанавливает время задержки вычислений.

        Args:
            seconds: Количество секунд задержки
        """
        element = self.wait.until(
            EC.presence_of_element_located(self.DELAY_INPUT)
        )
        element.clear()
        element.send_keys(str(seconds))

    @allure.step("Нажать кнопку '7'")
    def click_button_7(self) -> None:
        """Нажимает кнопку с цифрой 7."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.BUTTON_7)
        )
        element.click()

    @allure.step("Нажать кнопку '8'")
    def click_button_8(self) -> None:
        """Нажимает кнопку с цифрой 8."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.BUTTON_8)
        )
        element.click()

    @allure.step("Нажать кнопку '+'")
    def click_button_plus(self) -> None:
        """Нажимает кнопку сложения."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.BUTTON_PLUS)
        )
        element.click()

    @allure.step("Нажать кнопку '='")
    def click_button_equals(self) -> None:
        """Нажимает кнопку равенства."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.BUTTON_EQUALS)
        )
        element.click()

    @allure.step("Выполнить операцию 7 + 8")
    def calculate_7_plus_8(self) -> None:
        """Выполняет операцию сложения 7 + 8."""
        self.click_button_7()
        self.click_button_plus()
        self.click_button_8()
        self.click_button_equals()

    @allure.step("Получить результат вычислений")
    def get_result_text(self, timeout: Optional[int] = None) -> str:
        """
        Получает текст результата с дисплея калькулятора.

        Args:
            timeout: Необязательный таймаут ожидания в секундах

        Returns:
            Текст результата вычислений
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                EC.text_to_be_present_in_element(self.RESULT_DISPLAY, "15")
            )
        else:
            self.wait.until(
                EC.text_to_be_present_in_element(self.RESULT_DISPLAY, "15")
            )

        element = self.driver.find_element(*self.RESULT_DISPLAY)
        return element.text

    @allure.step("Ожидать результат: {expected_result} (таймаут: {timeout}с)")
    def wait_for_result(
            self, expected_result: Union[str, int], timeout: int) -> None:
        """
        Ожидает появления определенного результата на дисплее.

        Args:
            expected_result: Ожидаемый результат вычислений
            timeout: Максимальное время ожидания в секундах
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            EC.text_to_be_present_in_element(
                self.RESULT_DISPLAY,
                str(expected_result)
            )
        )
