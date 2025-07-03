from pages.login_gw import LoginGwPage
from utils.log_util import Logging, export_log_to_excel
import time

def test_login_success(driver, login):
    # Nếu login thất bại, không tiếp tục test
    error_msg = login.get_error_message()
    if error_msg and "Incorrect username or password." in error_msg:
        Logging("Login failed")
        assert False, "Login failed: Incorrect username or password."
    else:
        Logging("Login pass")
        assert True