from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.get("http://the-internet.herokuapp.com/inputs")

input_field = driver.find_element(By.TAG_NAME, "input")

input_field.send_keys("Sky")

input_field.clear()

input_field.send_keys("Pro")

driver.quit()
