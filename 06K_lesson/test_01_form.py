import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService


class TestFormValidation:

    @pytest.fixture(scope="function")
    def driver(self):
        service = EdgeService()
        driver = webdriver.Edge(service=service)

        yield driver

        driver.quit()

    def fill_form(self, driver, wait):
        test_data = {
            "first-name": "Иван",
            "last-name": "Петров",
            "address": "Ленина, 55-3",
            "e-mail": "test@skypro.com",
            "phone": "+7985899998787",
            "zip-code": "",
            "city": "Москва",
            "country": "Россия",
            "job-position": "QA",
            "company": "SkyPro"
        }

        for field_id, value in test_data.items():
            field = wait.until(
                EC.presence_of_element_located((By.NAME, field_id))
            )
            field.clear()
            if value:
                field.send_keys(value)

    def test_form_validation(self, driver):
        driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
        wait = WebDriverWait(driver, 10)

        self.fill_form(driver, wait)

        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Submit']"))
        )
        submit_button.click()

        zip_code_field = wait.until(
            EC.presence_of_element_located((By.ID, "zip-code"))
        )

        zip_code_classes = zip_code_field.get_attribute("class")

        assert any(error_class in zip_code_classes for
                   error_class in ['alert-danger']), \
            f" Классы поля Zip code: {zip_code_classes}"

        green_fields = [
            "first-name", "last-name", "address", "e-mail", "phone",
            "city", "country", "job-position", "company"
        ]

        failed_fields = []

        for field_id in green_fields:
            try:
                field = wait.until(
                    EC.presence_of_element_located((By.ID, field_id))
                )
                field_classes = field.get_attribute("class")

                if 'alert-success' not in field_classes:
                    failed_fields.append(
                        f"{field_id} (классы: {field_classes})"
                        )

            except Exception as e:
                failed_fields.append(f"{field_id} (ошибка: {str(e)})")

        assert len(failed_fields) == 0, \
            "Следующие поля не подсвечены зеленым:\n" + (
                "\n".join(failed_fields))


if __name__ == "__main__":
    pytest.main([__file__])
