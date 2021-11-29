from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

#This example requires Selenium WebDriver 3.13 or newer
with webdriver.Chrome() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.facebook.com/profile.php?id=100011366594475")
    first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "h1")))
    print(first_result.get_attribute("textContent"))