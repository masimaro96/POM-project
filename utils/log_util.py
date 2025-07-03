import os
import openpyxl
import sys
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Logging(result: str, log_path: str = 'utils/Log/log_test.txt'):
    """Lưu kết quả test vào file txt."""
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(result + '\n')

def export_log_to_excel(txt_path: str = 'utils/Log/login_test_log.txt', excel_path: str = 'utils/Log/log_test.xlsx'):
    """Đọc file txt log và xuất ra file Excel."""
    if not os.path.exists(txt_path):
        print(f"Không tìm thấy file log: {txt_path}")
        return
    wb = openpyxl.Workbook()
    ws = wb.active
    if ws is None:
        ws = wb.create_sheet(title='Login Test Log')
    else:
        ws.title = 'Login Test Log'
    ws.append(['STT', 'Kết quả'])
    with open(txt_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            ws.append([idx, line.strip()])
    wb.save(excel_path)
    print(f'Đã xuất log ra file: {excel_path}')

def get_paths(date_id):
    platform = sys.platform
    paths = {}
    if platform.startswith("linux"):
        local_path = "/home/oem/groupware-auto-test"
        log_folder = "/Log/"
        log_testcase = "/Log/"
        paths["json_file"] = os.path.join(local_path, "NQ_selenium.json")
        paths["file_upload"] = os.path.join(local_path, "Attachment", "quynh1@meo.qa.hanbiro.net_2323_1608785342.837046.eml")
        paths["file_zip_upload"] = os.path.join(local_path, "Attachment", "sent_mail.zip")
        paths["execution_log"] = os.path.join(local_path, log_folder.lstrip("/"), f"execution_log_{date_id}.txt")
        paths["testcase_log"] = os.path.join(local_path, log_testcase.lstrip("/"), f"NQuynh_TestcaseAllmenu_{date_id}.xlsx")
    else:
        local_path = os.path.dirname(Path(__file__).absolute())
        log_folder = "Log"
        log_testcase = "Log"
        paths["json_file"] = os.path.join(local_path, "NQ_selenium.json")
        paths["file_upload"] = os.path.join(local_path, "Attachment", "quynh1@meo.qa.hanbiro.net_2323_1608785342.837046.eml")
        paths["file_zip_upload"] = os.path.join(local_path, "Attachment", "sent_mail.zip")
        paths["execution_log"] = os.path.join(local_path, log_folder, f"execution_log_{date_id}.txt")
        paths["testcase_log"] = os.path.join(local_path, log_testcase, f"NQuynh_TestcaseAllmenu_{date_id}.xlsx")
    return paths

def close_html_popup(driver, timeout=10):
    # Chờ popup xuất hiện rồi mới bấm nút Close, không reload page
    try:
        close_btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@ng-click, 'cancel(false)') and contains(., 'Close')]") )
        )
        driver.execute_script("arguments[0].click();", close_btn)  # Dùng JS click để tránh reload hoặc sự kiện phụ
    except Exception:
        pass


