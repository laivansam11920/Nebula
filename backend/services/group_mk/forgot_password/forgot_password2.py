from configs.db import db
from utils.token_het_han import kiem_tra_het_han_token
from time import time
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

def kiem_tra_xac_nhan(gmail, token_nguoi_dung_gui_len):
    thu_muc_can_kiem_tra = db["token"]

    try:
        ban_ghi = thu_muc_can_kiem_tra.find_one({"gmail": gmail})

        if ban_ghi is None:
            return {
                "success": False,
                "message": "Yêu cầu không tồn tại hoặc đã hết hạn!",
            }

        token_trong_db = ban_ghi.get("token_nguoi_dung")

        if str(token_nguoi_dung_gui_len) != str(token_trong_db):
            return {"success": False, "message": "Mã xác thực không chính xác!"}

        thoi_gian_tao_token = ban_ghi.get("thoi_gian_tao")
        thoi_gian_het_han = ban_ghi.get("thoi_gian_het_han")
        da_su_dung = ban_ghi.get("trang_thai1")

        if da_su_dung == "da_su_dung":
            return {"success": False, "message": "Mã xác thực đã được sử dụng!"}

        thoi_gian_hien_tai = int(time())

        kiem_tra_token_het_han = kiem_tra_het_han_token(
            gmail, thoi_gian_tao_token, thoi_gian_hien_tai, thoi_gian_het_han
        )

        if not kiem_tra_token_het_han["success"]:
            return {"success": False, "message": "Token đã hết hạn sử dụng"}

        thu_muc_can_kiem_tra.update_one(
            {"gmail": gmail}, {"$set": {"trang_thai1": "sap_su_dung"}}
        )

        return {"success": True, "message": "Xác thực thành công!"}

    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
        return {"success": False, "message": "Có lỗi xảy ra phía server!"}
