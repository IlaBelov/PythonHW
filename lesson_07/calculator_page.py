from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SlowCalculatorPage:

    DELAY_INPUT = (By.CSS_SELECTOR, "#delay")
    RESULT_DISPLAY = (By.CLASS_NAME, "screen")
    BUTTON_7 = (By.XPATH, "//span[text()='7']")
    BUTTON_8 = (By.XPATH, "//span[text()='8']")
    BUTTON_PLUS = (By.XPATH, "//span[text()='+']")
    BUTTON_EQUALS = (By.XPATH, "//span[text()='=']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)

    def open(self):
        self.driver.get(
            "https://bonigarcia.dev"
            "/selenium-webdriver-java/slow-calculator.html"
        )

    def set_delay(self, seconds):
        element = self.wait.until(
            EC.presence_of_element_located(self.DELAY_INPUT)
        )
        element.clear()
        element.send_keys(str(seconds))

    def click_button_7(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.BUTTON_7)
        )
        element.click()

    def click_button_8(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.BUTTON_8)
        )
        element.click()

    def click_button_plus(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.BUTTON_PLUS)
        )
        element.click()

    def click_button_equals(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.BUTTON_EQUALS)
        )
        element.click()

    def calculate_7_plus_8(self):
        self.click_button_7()
        self.click_button_plus()
        self.click_button_8()
        self.click_button_equals()

    def get_result_text(self, timeout=None):
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

    def wait_for_result(self, expected_result, timeout):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            EC.text_to_be_present_in_element(
                self.RESULT_DISPLAY,
                str(expected_result)
            )
        )
