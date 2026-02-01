from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def create_driver(chromedriver="chromedriver.exe"):
    service = Service(chromedriver)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver
