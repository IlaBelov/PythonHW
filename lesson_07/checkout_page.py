from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
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

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_checkout_info_page(self):
        self.wait.until(
            EC.presence_of_element_located(self.FIRST_NAME_INPUT)
        )
        return self

    def wait_for_checkout_overview_page(self):
        self.wait.until(
            EC.presence_of_element_located(self.FINISH_BUTTON)
        )
        return self

    def fill_checkout_info(self, first_name, last_name, postal_code):
        self.wait_for_checkout_info_page()

        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(
            postal_code)

        return self

    def click_continue(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        )
        element.click()
        return self

    def get_total_amount(self):
        self.wait_for_checkout_overview_page()

        element = self.wait.until(
            EC.presence_of_element_located(self.TOTAL_LABEL)
        )

        total_text = element.text

        amount_str = total_text.replace("Total: $", "").strip()
        return float(amount_str)

    def get_summary_info(self):
        self.wait_for_checkout_overview_page()

        subtotal = self.driver.find_element(*self.SUBTOTAL_LABEL).text
        tax = self.driver.find_element(*self.TAX_LABEL).text
        total = self.driver.find_element(*self.TOTAL_LABEL).text

        return {
            "subtotal": subtotal,
            "tax": tax,
            "total": total
        }

    def click_finish(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.FINISH_BUTTON)
        )
        element.click()
        return self

    def get_complete_message(self):
        element = self.wait.until(
            EC.presence_of_element_located(self.COMPLETE_MESSAGE)
        )
        return element.text
