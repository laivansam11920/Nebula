from configs.db import db
import datetime
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

def delete_file_services(ma_dinh_danh_file, collection):
    try:
        collection_can_tim = db[str(collection)]
        res = collection_can_tim.update_one(
            {"ma_dinh_danh_file": ma_dinh_danh_file},
            {"$set": {"trang_thai": "da_xoa", "ngay_xoa": datetime.datetime.now()}},
        )
        if res.matched_count == 0:
            logger.log(f"Không tìm thấy file có ID: {ma_dinh_danh_file}", duong_dan_hien_tai())
            return {"trang_thai": False, "mes": "khong tim thay id"}
        return {"trang_thai": True, "mes": "ok"}
    except Exception as e:
        return {"trang_thai": False, "mes": f"loi {e}"}
