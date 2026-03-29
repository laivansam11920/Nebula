from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

def parse_size_to_bytes(size_data):
    if not size_data:
        return 0

    if isinstance(size_data, (int, float)):
        return max(0, float(size_data))  # Đảm bảo không âm

    size_str = str(size_data).upper().strip()

    try:
        # Lấy tất cả các ký tự là số hoặc dấu chấm
        number_part = "".join(c for c in size_str if c.isdigit() or c == ".")

        if not number_part:
            return 0

        num = float(number_part)

        # Nhân với hệ số
        if "GB" in size_str:
            return num * 1024 * 1024 * 1024
        if "MB" in size_str:
            return num * 1024 * 1024
        if "KB" in size_str:
            return num * 1024
        return num  # Mặc định Bytes

    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
        return 0
