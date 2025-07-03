import pytest
from utils.driver_factory import get_driver
from pages.login_gw import LoginGwPage

# Fixture này sẽ chạy một lần duy nhất cho toàn bộ session test.
# Nó sẽ khởi tạo trình duyệt, sau đó đóng trình duyệt khi tất cả test kết thúc.
@pytest.fixture(scope="session")
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

# Fixture này cũng chạy một lần cho cả session, phụ thuộc vào `driver`.
# Nó sẽ mở trang login, đăng nhập, và sẵn sàng cho các test khác.
# Việc này giúp tiết kiệm thời gian vì không phải đăng nhập lại cho mỗi test.
# Fixture này trả về đối tượng driver đã ở trạng-thái-đăng-nhập.
@pytest.fixture(scope="session")
def login(driver):
    login_page = LoginGwPage(driver)
    login_page.load()
    login_page.login("quynh1", "quynh1!@")
    return driver 