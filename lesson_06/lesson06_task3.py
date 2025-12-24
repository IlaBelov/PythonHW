from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()
                                                ))
waiter = WebDriverWait(driver, 40)

driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html"
           )

waiter.until(lambda d: len(d.find_elements
                           (By.CSS_SELECTOR, "#image-container img")) >= 4)

print(driver.find_element(By.ID, "award").get_attribute("src"))

driver.quit()
