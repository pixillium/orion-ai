from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils import mprint


def chrome():
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    options.add_experimental_option("debuggerAddress", "localhost:9111")
    driver = webdriver.Chrome(service=service, options=options)
    mprint("Chrome driver initialized")
    return driver
