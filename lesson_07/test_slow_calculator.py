import pytest
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

    def test_calculator_with_45_second_delay(self, calculator_page):
        calculator_page.set_delay(45)
        calculator_page.calculate_7_plus_8()
        calculator_page.wait_for_result("15", 46)
        result = calculator_page.get_result_text()
        assert result == "15", (
            f"Ожидался результат 15, но получено: {result}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
