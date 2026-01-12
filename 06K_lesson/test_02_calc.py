import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_slow_calculator():
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get(
            "https://bonigarcia.dev"
            "/selenium-webdriver-java/slow-calculator.html")
        wait = WebDriverWait(driver, 50)
        delay_field = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#delay"))
        )
        delay_field.clear()
        delay_field.send_keys("45")
        buttons_to_click = ["7", "+", "8", "="]
        for button_text in buttons_to_click:
            button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//span[text()='{button_text}']"))
            )
            button.click()

        wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15")
        )
        result_element = driver.find_element(By.CLASS_NAME, "screen")
        actual_result = result_element.text
        assert actual_result == "15", f"Получено: {actual_result}"

    finally:
        driver.quit()


if __name__ == "__main__":
    pytest.main([__file__])
