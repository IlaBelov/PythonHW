import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from login_page import LoginPage
from main_page import MainPage
from cart_page import CartPage
from checkout_page import CheckoutPage


class TestSauceDemo:

    @pytest.fixture
    def driver(self):
        firefox_options = Options()
        firefox_options.add_argument("--start-maximized")

        service = Service()
        driver_instance = webdriver.Firefox(
            service=service,
            options=firefox_options
        )

        yield driver_instance

        driver_instance.quit()

    def test_checkout_total_amount(self, driver):
        USERNAME = "standard_user"
        PASSWORD = "secret_sauce"
        PRODUCTS_TO_ADD = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]
        CUSTOMER_DATA = {
            "first_name": "Илья",
            "last_name": "Белов",
            "postal_code": "160033"
        }
        EXPECTED_TOTAL = 58.29

        login_page = LoginPage(driver)
        login_page.open().login(USERNAME, PASSWORD)

        main_page = MainPage(driver)
        main_page.wait_for_page_load()
        main_page.add_products_to_cart(PRODUCTS_TO_ADD)

        main_page.go_to_cart()

        cart_page = CartPage(driver)
        cart_page.wait_for_page_load()

        verification_result, message = cart_page.verify_cart_contains(
            PRODUCTS_TO_ADD
        )
        assert verification_result, message

        cart_page.click_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_checkout_info(
            CUSTOMER_DATA["first_name"],
            CUSTOMER_DATA["last_name"],
            CUSTOMER_DATA["postal_code"]
        ).click_continue()

        total_amount = checkout_page.get_total_amount()

        assert total_amount == EXPECTED_TOTAL, (
            f"Ожидалась сумма ${EXPECTED_TOTAL}, "
            f"но получено ${total_amount}"
        )
