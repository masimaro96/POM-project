import os
import openpyxl
import sys
import datetime
import re
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl.styles import Alignment

def Logging(result: str, log_path: str = 'utils/Log/log_test.txt'):
    """Lưu kết quả test vào file txt."""
    # Sử dụng Path object để xử lý đường dẫn nhất quán hơn
    log_file = Path(log_path)
    # Tạo thư mục cha nếu nó chưa tồn tại
    log_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(result + '\n')
    except IOError as e:
        print(f"Lỗi khi ghi file log {log_file}: {e}")

def export_log_to_excel(
    txt_path: str = 'utils/Log/log_test.txt',
    excel_path: str = 'utils/Log/log_test.xlsx',
    tester: str = 'Quynh',
    menu: str = 'Mail',
    sub_menu: str = 'Signature'
):
    """
    Đọc file txt log, xử lý log đa dòng (stack trace) và xuất ra file Excel.
    Tự động điều chỉnh độ rộng cột và định dạng để dễ đọc.
    """
    log_file = Path(txt_path)
    if not log_file.exists():
        print(f"Không tìm thấy file log: {log_file}")
        return

    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Test Log'

        headers = ["Menu", "Sub-Menu", "Test Case Name", "Status", "Description", "Date", "Tester"]
        ws.append(headers)

        # Đọc toàn bộ nội dung file và tách các khối log
        content = log_file.read_text(encoding='utf-8')
        # Mỗi khối log mới được xác định bằng 'test_' ở đầu dòng.
        # Regex này sẽ tách chuỗi tại mỗi dòng bắt đầu bằng 'test_'.
        log_entries = re.split(r'(?m)^\s*(?=test_)', content)
        # Lọc bỏ các phần tử rỗng có thể được tạo ra từ việc tách chuỗi
        log_entries = [entry.strip() for entry in log_entries if entry.strip()]

        for entry in log_entries:
            # Tách dòng đầu tiên (chứa tên test case và kết quả) khỏi phần còn lại (stack trace)
            parts = entry.split('\n', 1)
            first_line = parts[0].strip()
            stack_trace = parts[1].strip() if len(parts) > 1 else ""

            # Tách tên test case và phần mô tả kết quả
            header_parts = first_line.split(':', 1)
            if len(header_parts) == 2:
                testcase = header_parts[0].strip()
                result_part = header_parts[1].strip()

                if 'Pass' in result_part:
                    status = 'Pass'
                    # Lấy mô tả là phần còn lại sau chữ 'Pass'
                    description = result_part.replace('Pass', '', 1).strip(' -').strip()
                elif 'Fail' in result_part:
                    status = 'Fail'
                    # Kết hợp mô tả từ dòng đầu và toàn bộ stack trace
                    description = result_part.replace('Fail', '', 1).strip(' -').strip()
                    if stack_trace:
                        description = f"{description}\n{stack_trace}"
                else:
                    # Trường hợp không có Pass/Fail rõ ràng
                    status = 'Info'
                    description = f"{result_part}\n{stack_trace}".strip()
            else:
                # Xử lý các dòng không có dấu ':' (ví dụ: chỉ có tên test case)
                testcase = first_line
                status = 'Info'
                description = stack_trace

            ws.append([
                menu,
                sub_menu,
                testcase,
                status,
                description.strip(),
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                tester
            ])

        # Tự động điều chỉnh độ rộng cột và định dạng để dễ đọc
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                # Căn chỉnh văn bản lên trên cùng, sang trái
                cell.alignment = Alignment(vertical='top', horizontal='left')
                if cell.value:
                    # Với cột 'Description' (cột E), bật chế độ wrap text
                    if column == 'E':
                        cell.alignment = Alignment(wrap_text=True, vertical='top', horizontal='left')
                        max_length = 80  # Đặt chiều rộng cố định hợp lý
                        continue

                    # Tính độ dài tối đa cho các cột khác
                    try:
                        cell_max_line_length = max(len(line) for line in str(cell.value).split('\n'))
                        if cell_max_line_length > max_length:
                            max_length = cell_max_line_length
                    except:
                        pass

            # Đặt độ rộng cho cột
            if column == 'E':
                ws.column_dimensions[column].width = max_length
            else:
                adjusted_width = (max_length + 2) if max_length > 0 else 15
                ws.column_dimensions[column].width = adjusted_width

        # Tạo thư mục cha cho file excel nếu chưa tồn tại
        excel_file = Path(excel_path)
        excel_file.parent.mkdir(parents=True, exist_ok=True)
        wb.save(excel_file)
        print(f'Đã xuất log ra file: {excel_file}')
    except Exception as e:
        print(f"Đã xảy ra lỗi khi xuất file Excel: {e}")

def get_paths(date_id):
    platform = sys.platform
    paths = {}
    if platform.startswith("linux"):
        local_path = "/home/oem/groupware-auto-test"
        log_folder = "/Log/"
        log_testcase = "/Log/"
        paths["file_upload"] = os.path.join(local_path, "Attachment", "quynh1@meo.qa.hanbiro.net_2323_1608785342.837046.eml")
        paths["file_zip_upload"] = os.path.join(local_path, "Attachment", "sent_mail.zip")
        paths["execution_log"] = os.path.join(local_path, log_folder.lstrip("/"), f"execution_log_{date_id}.txt")
        paths["testcase_log"] = os.path.join(local_path, log_testcase.lstrip("/"), f"NQuynh_TestcaseAllmenu_{date_id}.xlsx")
    else:
        local_path = os.path.dirname(Path(__file__).absolute())
        log_folder = "Log"
        log_testcase = "Log"
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
