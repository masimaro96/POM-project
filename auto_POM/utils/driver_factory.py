from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)
