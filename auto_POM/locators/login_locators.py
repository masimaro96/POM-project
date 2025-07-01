from selenium.webdriver.common.by import By

class LoginLocator:
    URL = "https://vndev.hanbiro.com/ngw/app"
    USERNAME_INPUT = (By.ID, "log-userid")
    FRAME_PASSWORD = (By.ID, "iframeLoginPassword")
    PASSWORD_INPUT = (By.ID, "p")
    LOGIN_BUTTON = (By.ID, "btn-log")