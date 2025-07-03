from pages.login_gw import LoginGwPage
import time
from utils.log_util import close_html_popup


def test_login_success(driver, login):
    login_page = LoginGwPage(driver)
    close_html_popup(driver)  # Đóng popup nếu có sau khi login
    error_msg = login_page.get_error_message()
    log_path = 'tests/login_test_log.txt'
    if error_msg and "Incorrect username or password." in error_msg:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write("Login failed\n")
        print("Login failed")
        assert False, "Login failed: Incorrect username or password."
    else:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write("Login pass\n")
        print("Login pass")
        assert True