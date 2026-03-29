from validators.kiem_tra_dinh_dang_gmail import kiem_tra_dinh_dang_gmail
from validators.kiem_tra_do_bao_mat_pass import check_password_strength
from configs.db import db
from utils.hash_password import hash_password, make_salt
from datetime import datetime, timedelta
from configs.duong_dan_thu_muc import duong_dan_hien_tai
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

def kiem_tra_mat_khau(user_name_input, gmail_input, password_input):

    luu_tru = db["users"]

    try:
        db.command("ping")
        logger.log("system: find to connect mongodb", duong_dan_hien_tai())
    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())

    if luu_tru.find_one({"gmail": gmail_input}):
        logger.warring(f"Email {gmail_input} đã tồn tại.", duong_dan_hien_tai())
        return {
            "status": "error",
            "error_type": "loi_trung_email",
            "message": "Email này đã được sử dụng rồi!",
        }

    if not kiem_tra_dinh_dang_gmail(gmail_input):
        return {
            "status": "error",
            "error_type": "loi_dinh_dang_gmail",
            "message": "Định dạng Gmail không hợp lệ!",
        }

    is_valid, message = check_password_strength(password_input)

    if not is_valid:
        return {"status": "error", "error_type": "loi_do_manh_pass", "message": message}

    try:
        thoi_gian_hien_tai = datetime.now()
        thoi_gian_het_han = thoi_gian_hien_tai + timedelta(days=30)
        salt = make_salt()
        hashed = hash_password(password_input, salt)

        user_data = {
            "username": user_name_input,
            "gmail": gmail_input,
            "password": hashed,
            "salt": salt,
            "cap_nguoi_dung": "basic",
            "thoi_gian_cap_trang_thai": {
                "bat_dau": thoi_gian_het_han,
                "ket_thuc": thoi_gian_het_han,
            },
            "luu_tru": {"khong_gian_luu_tru": "128", "don_vi": "mb"},
            "role": "user",
            "trang_thai": "chua_dang_nhap",
        }

        luu_tru.insert_one(user_data)

        return {"status": "good", "message": "Tạo tài khoản thành công rồi nhé!"}
    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
        return {
            "status": "error",
            "error_type": "loi_luu_tru_database",
            "message": "Lỗi hệ thống, vui lòng thử lại sau!",
        }
