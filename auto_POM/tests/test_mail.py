import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.menu_mail_page import MenuMailPage
from locators.mail_locators import MailLocator as M
from utils.log_util import Logging

# Fixture này có scope="function", nghĩa là nó sẽ chạy lại cho MỖI test function.
# Nó đảm bảo mỗi test bắt đầu từ một trạng thái giống nhau và độc lập:
# 1. Đã đăng nhập (nhờ `login` fixture)
# 2. Đã vào trang Mail
# 3. Đã vào mục Settings
# Điều này giúp loại bỏ lỗi do các test ảnh hưởng lẫn nhau.
@pytest.fixture(scope="function")
def mail_settings_page(login):
    # `login` fixture trả về `driver` đã đăng nhập
    driver = login
    page = MenuMailPage(driver)
    page.load()
    page.go_to_setting()
    return page

def close_html_popup(driver, timeout=5):
    try:
        close_btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@ng-click, 'cancel(false)') and contains(., 'Close')]"))
        )
        close_btn.click()
    except Exception:
        pass

# Test này kiểm tra việc truy cập vào tab "Signature" thành công.
def test_access_signature_tab(mail_settings_page):
    """
    Kiểm tra xem sau khi vào Settings, có thể click vào tab Signature hay không.
    """
    mail_settings_page.go_to_signature_tab()
    # Assert: Kiểm tra nút "Add" signature có tồn tại không để xác nhận đã vào đúng tab.
    result = mail_settings_page.driver.find_element(*M.BUTTON_SIGNATURE_ADD).is_displayed()
    Logging(f"test_access_signature_tab: {'Pass' if result else 'Fail'}")
    assert result

# Test này kiểm tra chức năng thêm chữ ký mới.
def test_add_new_signature(mail_settings_page):
    """
    Kiểm tra chức năng thêm một chữ ký mới.
    """
    mail_settings_page.go_to_signature_tab()
    count_before = mail_settings_page.get_signature_count()
    signature_text = "Test signature " + str(int(time.time()))
    mail_settings_page.add_text_signature(signature_text)
    count_after = mail_settings_page.get_signature_count()
    # Assert: Kiểm tra số lượng chữ ký đã tăng lên 1.
    result = (count_after == count_before + 1)
    Logging(f"test_add_new_signature: {'Pass' if result else 'Fail'}")
    assert result
