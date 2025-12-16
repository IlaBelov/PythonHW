from selenium import webdriver
from selenium.webdriver.common.by import By

blue_button = webdriver.Chrome()
blue_button.get("http://uitestingplayground.com/classattr")

blue_button.find_element(By.CLASS_NAME, "btn-primary").click()
