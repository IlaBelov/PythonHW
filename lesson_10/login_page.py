import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class LoginPage:
    """
    Page Object класс для работы со страницей авторизации.
    """

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container")

    URL = "https://www.saucedemo.com/"

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу авторизации.

        Args:
            driver: Экземпляр WebDriver для управления браузером
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть страницу авторизации")
    def open(self) -> 'LoginPage':
        """
        Открывает страницу авторизации в браузере.

        Returns:
            LoginPage: текущий экземпляр класса
        """
        self.driver.get(self.URL)
        return self

    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Вводит указанное имя пользователя в соответствующее поле.

        Args:
            username: str - имя пользователя для авторизации

        Returns:
            LoginPage: текущий экземпляр класса
        """
        element = self.wait.until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )
        element.clear()
        element.send_keys(username)
        return self

    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Вводит указанный пароль в соответствующее поле.

        Args:
            password: str - пароль для авторизации

        Returns:
            LoginPage: текущий экземпляр класса
        """
        element = self.driver.find_element(*self.PASSWORD_INPUT)
        element.clear()
        element.send_keys(password)
        return self

    @allure.step("Нажать кнопку 'Login'")
    def click_login(self) -> 'LoginPage':
        """
        Нажимает кнопку входа (Login).

        Returns:
            LoginPage: текущий экземпляр класса
        """
        element = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        element.click()
        return self

    @allure.step("Выполнить авторизацию под пользователем: {username}")
    def login(self, username: str, password: str) -> 'LoginPage':
        """
        Выполняет полный процесс авторизации.

        Args:
            username: str - имя пользователя для авторизации
            password: str - пароль для авторизации

        Returns:
            LoginPage: текущий экземпляр класса
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
