from selenium.webdriver.common.by import By
from locators.mail_locators import MailLocator as M
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MenuMailPage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    def load(self):
        self.driver.get(M.URL)
        # Chờ cho menu bên trái load xong
        self.wait.until(EC.presence_of_element_located(M.BUTTON_SETTING))

    def go_to_setting(self):
        setting_button = self.wait.until(EC.element_to_be_clickable(M.BUTTON_SETTING))
        setting_button.click()

    def go_to_signature_tab(self):
        signature_tab = self.wait.until(EC.element_to_be_clickable(M.BUTTON_SIGNATURE))
        signature_tab.click()

    def add_text_signature(self, signature_content):
        self.wait.until(EC.element_to_be_clickable(M.BUTTON_SIGNATURE_ADD)).click()
        self.wait.until(EC.element_to_be_clickable(M.SIGNATURE_TYPE)).click()

        # Chuyển vào iframe để nhập text
        frame = self.wait.until(EC.presence_of_element_located(M.FRAME_TEXT))
        self.driver.switch_to.frame(frame)
        self.wait.until(EC.element_to_be_clickable(M.SIGNATURE_INPUT)).send_keys(signature_content)
        
        # Chuyển về context mặc định
        self.driver.switch_to.default_content()
        self.driver.find_element(*M.SIGNATURE_SAVE).click()

    def get_signature_count(self):
        # Chờ một chút để danh sách cập nhật sau khi lưu
        self.wait.until(EC.presence_of_element_located(M.SIGNATURE_LIST_ITEMS))
        return len(self.driver.find_elements(*M.SIGNATURE_LIST_ITEMS))

    def auto_sort(self):
        self.driver.find_element(*M.BUTTON_AUTO_SORT).click()
        self.driver.implicitly_wait(10)