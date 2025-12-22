from selenium import webdriver
from selenium.webdriver.common.by import By

button = webdriver.Chrome()
button.get("http://uitestingplayground.com/dynamicid")

button.find_element(By.CLASS_NAME, "btn-primary").click()
