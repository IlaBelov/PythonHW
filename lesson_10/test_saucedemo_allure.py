import pytest
import allure
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
        """
        Фикстура для создания и настройки экземпляра WebDriver.

        Yields:
            webdriver.Firefox: экземпляр Firefox WebDriver
        """
        firefox_options = Options()
        firefox_options.add_argument("--start-maximized")

        service = Service()
        driver_instance = webdriver.Firefox(
            service=service,
            options=firefox_options
        )

        yield driver_instance

        driver_instance.quit()

    @allure.title("Проверка общей суммы заказа при оформлении")
    @allure.description("""
    Тест проверяет полный процесс оформления заказа в интернет-магазине:
    1. Авторизация пользователя
    2. Добавление товаров в корзину
    3. Переход в корзину и проверка содержимого
    4. Заполнение информации о покупателе
    5. Проверка корректности расчета общей суммы заказа

    Ожидаемая сумма заказа: $58.29
    """)
    @allure.feature("Оформление заказа")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("Запуск теста проверки общей суммы заказа")
    def test_checkout_total_amount(self, driver):
        """
        Тест проверяет корректность расчета общей суммы при оформлении заказа.

        Args:
            driver: Экземпляр WebDriver
        """
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

        with allure.step(f"Авторизация пользователя {USERNAME}"):
            login_page = LoginPage(driver)
            login_page.open().login(USERNAME, PASSWORD)
            allure.attach(
                f"Авторизация выполнена под пользователем: {USERNAME}",
                name="Результат авторизации",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step(f"Добавление товаров в корзину: {PRODUCTS_TO_ADD}"):
            main_page = MainPage(driver)
            main_page.wait_for_page_load()
            main_page.add_products_to_cart(PRODUCTS_TO_ADD)
            allure.attach(
                f"Добавлено товаров: {len(
                    PRODUCTS_TO_ADD)}\nСписок: {', '.join(PRODUCTS_TO_ADD)}",
                name="Добавленные товары",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Переход в корзину"):
            main_page.go_to_cart()

        with allure.step("Проверка содержимого корзины"):
            cart_page = CartPage(driver)
            cart_page.wait_for_page_load()

            verification_result, message = cart_page.verify_cart_contains(
                PRODUCTS_TO_ADD)

            with allure.step("Верификация товаров в корзине"):
                assert verification_result, message
                allure.attach(
                    f"Проверка корзины успешна: {message}",
                    name="Результат проверки корзины",
                    attachment_type=allure.attachment_type.TEXT
                )

        with allure.step("Начало оформления заказа"):
            cart_page.click_checkout()

        with allure.step("Заполнение информации о покупателе"):
            checkout_page = CheckoutPage(driver)
            checkout_page.fill_checkout_info(
                CUSTOMER_DATA["first_name"],
                CUSTOMER_DATA["last_name"],
                CUSTOMER_DATA["postal_code"]
            ).click_continue()

            allure.attach(
                f"Заполнены данные покупателя:\n"
                f"Имя: {CUSTOMER_DATA['first_name']}\n"
                f"Фамилия: {CUSTOMER_DATA['last_name']}\n"
                f"Почтовый индекс: {CUSTOMER_DATA['postal_code']}",
                name="Данные покупателя",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Получение общей суммы заказа"):
            total_amount = checkout_page.get_total_amount()
            allure.attach(
                f"Получена общая сумма заказа: ${total_amount:.2f}",
                name="Общая сумма заказа",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step(
                f"Проверка суммы заказа: ожидается ${EXPECTED_TOTAL}"):
            assert total_amount == EXPECTED_TOTAL, (
                f"Ожидалась сумма ${EXPECTED_TOTAL}, "
                f"но получено ${total_amount}"
            )

            allure.attach(
                f"Сумма заказа корректна: ${total_amount:.2f}",
                name="Результат проверки суммы",
                attachment_type=allure.attachment_type.TEXT
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
