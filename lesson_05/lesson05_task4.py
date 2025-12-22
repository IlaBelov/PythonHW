from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Firefox()

driver.get("http://the-internet.herokuapp.com/login")

username_field = driver.find_element(By.ID, "username")
username_field.send_keys("tomsmith")

password_field = driver.find_element(By.ID, "password")
password_field.send_keys("SuperSecretPassword!")

login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login_button.click()

sleep(2)

success_message = driver.find_element(By.ID, "flash")
message_text = success_message.text

print(message_text)

driver.quit()
