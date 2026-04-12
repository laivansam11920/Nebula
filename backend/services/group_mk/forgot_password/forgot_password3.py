from configs.db import db
from utils.hash_password import hash_password_v2
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai


def kiem_tra_de_doi_mat_khau(token, gmail, new_password):
    thu_muc_can_kiem_tra = db["token"]
    thu_muc_nguoi_dung = db["users"]
    try:
        ket_qua = thu_muc_can_kiem_tra.find_one(
            {"gmail": str(gmail)},
            {"token_nguoi_dung": 1, "trang_thai1": 1, "trang_thai2": 1},
        )
        if not ket_qua:
            return {"success": False, "message": "Yêu cầu không tồn tại!"}

        token_trong_db = ket_qua.get("token_nguoi_dung")
        trang_thai_token = ket_qua.get("trang_thai1")
        trang_thai_thoi_gian = ket_qua.get("trang_thai2")

        if trang_thai_thoi_gian == "da_het_han":
            return {"success": False, "message": "Token đã hết hạn!"}

        if str(token) != str(token_trong_db):
            return {"success": False, "message": "Token không hợp lệ!"}

        if trang_thai_token != "sap_su_dung":
            return {"success": False, "message": "Token không hợp lệ để đổi mật khẩu!"}

        new_hash_pass = hash_password_v2(new_password)

        ket_qua_up_date = thu_muc_nguoi_dung.update_one(
            {"gmail": gmail}, {"$set": {"password": new_hash_pass}}
        )
        if ket_qua_up_date.modified_count > 0:
            thu_muc_can_kiem_tra.update_one(
                {"gmail": gmail}, {"$set": {"trang_thai1": "da_su_dung"}}
            )
            return {"success": True, "message": "Đổi mật khẩu thành công!"}
        else:
            return {
                "success": False,
                "message": "Mật khẩu mới không được giống mật khẩu cũ!",
            }
    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
        return {"success": False, "message": str(e)}
