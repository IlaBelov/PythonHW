import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_saucedemo_checkout():

    driver = webdriver.Firefox()

    try:
        driver.get("https://www.saucedemo.com/")
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "inventory_list")))

        items = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        for item in items:
            item_id = item.lower().replace(" ", "-")
            button_id = f"add-to-cart-{item_id}"

            add_button = wait.until(
                EC.element_to_be_clickable((By.ID, button_id))
            )
            add_button.click()
            print(f"Добавлен: {item}")

        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.ID, "checkout").click()

        driver.find_element(By.ID, "first-name").send_keys("Илья")
        driver.find_element(By.ID, "last-name").send_keys("Белов")
        driver.find_element(By.ID, "postal-code").send_keys("160033")
        driver.find_element(By.ID, "continue").click()

        total_element = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "summary_total_label"))
        )

        total_text = total_element.text
        total_amount = float(total_text.split("$")[1])

        assert total_amount == 58.29, f"Ожидалось $58.29, ${total_amount}"

    finally:
        driver.quit()


if __name__ == "__main__":
    pytest.main([__file__])
