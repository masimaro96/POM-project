from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.login_locators import LoginLocator as L

class LoginGwPage:
    def __init__(self, driver):
        self.driver = driver
    
    def load(self):
        self.driver.get(L.URL) 

    def login(self, username, password):
        wait = WebDriverWait(self.driver, 10)
        # Chờ ô username xuất hiện
        wait.until(EC.presence_of_element_located(L.USERNAME_INPUT))
        self.driver.find_element(*L.USERNAME_INPUT).send_keys(username)
        # Chờ frame password xuất hiện
        wait.until(EC.frame_to_be_available_and_switch_to_it(L.FRAME_PASSWORD))
        wait.until(EC.presence_of_element_located(L.PASSWORD_INPUT))
        self.driver.find_element(*L.PASSWORD_INPUT).send_keys(password)
        self.driver.switch_to.default_content()
        wait.until(EC.element_to_be_clickable(L.LOGIN_BUTTON))
        self.driver.find_element(*L.LOGIN_BUTTON).click()

    def get_error_message(self):
        wait = WebDriverWait(self.driver, 5)
        from locators.login_locators import LoginLocator as L
        try:
            error_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.login-error')))
            return error_elem.text
        except Exception:
            return None
