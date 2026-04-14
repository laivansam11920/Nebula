import random
import string


def goi_y_username(username_cu: str) -> str:
    # Tạo 3 con số ngẫu nhiên
    so_ngau_nhien = "".join(random.choices(string.digits, k=3))

    # Trả về tên mới kiểu: user123
    return f"{username_cu}{so_ngau_nhien}"
