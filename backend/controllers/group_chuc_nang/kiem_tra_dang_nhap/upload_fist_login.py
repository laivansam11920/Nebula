from flask import session, request, session
from services.group_chuc_nang.kiem_tra_dang_nhap.up_load_fist_login import (
    kiem_tra_token_link,
)
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai


def kiem_tra_token():
    try:
        nguoi_dung = session.get("user_gmail", "")
        token_nguoi_dung = session.get("user_token", "")
        role = session.get("role", "")
        lenh_thuc_thi = session.get("lenh_thuc_thi", "")

        if str(role) == "admin-root" and str(lenh_thuc_thi) == "khong_kiem_tra":
            return {"success": True, "message": "ok, admin-root"}, 200

        ket_qua = kiem_tra_token_link(
            nguoi_dung, token_nguoi_dung, "users", "token_nguoi_dung_upload"
        )

        if ket_qua["success"]:
            return ket_qua, 200
        return ket_qua, 401
    except Exception as e:
        logger.log(f"{e}", duong_dan_hien_tai())
        return {"success": False, "message": "Lỗi hệ thống nghiêm trọng!"}, 500
