import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from calculator_page import SlowCalculatorPage


class TestSlowCalculator:

    @pytest.fixture
    def driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")

        service = Service()
        driver_instance = webdriver.Chrome(
            service=service,
            options=chrome_options
        )

        yield driver_instance

        driver_instance.quit()

    @pytest.fixture
    def calculator_page(self, driver):
        page = SlowCalculatorPage(driver)
        page.open()
        return page

    @allure.title("Тест калькулятора с задержкой 45 секунд")
    @allure.description("""Проверяет корректность работы калькулятора
                         с установленной задержкой вычислений""")
    @allure.feature("Медленный калькулятор")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_calculator_with_45_second_delay(self, calculator_page):

        @allure.step("Установка задержки 45 секунд")
        def set_delay():
            calculator_page.set_delay(45)

        @allure.step("Выполнение операции 7 + 8")
        def calculate():
            calculator_page.calculate_7_plus_8()

        @allure.step("Ожидание результата")
        def wait_result():
            calculator_page.wait_for_result("15", 46)

        @allure.step("Проверка результата вычислений")
        def check_result():
            result = calculator_page.get_result_text()
            assert result == "15", (
                f"Ожидался результат 15, но получено: {result}"
            )

        set_delay()
        calculate()
        wait_result()
        check_result()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
