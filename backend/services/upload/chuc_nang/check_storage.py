from configs.db import db
from utils.tinh_toan_file import parse_size_to_bytes
import traceback
from logs.logger import logger

def get_user_storage_info(user_gmail):
    try:
        col_file_info = db['file_info']
        col_users = db['users']

        user = col_users.find_one({"gmail": user_gmail})
        
        if not user:
            return {"error": "Người dùng không tồn tại!"}, 404

        files = col_file_info.find(
            {
                "user_gmail": user_gmail,
                "trang_thai": {"$ne": "xoa_vinh_vien"} 
            },
            {"size": 1, "_id": 0} 
        )

        total_used_bytes = 0
        for f in files:
            size_str = f.get("size", "0 KB")
            total_used_bytes += parse_size_to_bytes(size_str)

        user_storage = user.get("luu_tru") or {}
        
        don_vi_tinh = user_storage.get("khong_gian_luu_tru", 128) 
        user_plan = str(user.get("cap_nguoi_dung", "BASIC"))

        try:
            max_storage_mb = float(don_vi_tinh)
        except (ValueError, TypeError):
            max_storage_mb = 128.0

        max_storage_bytes = max_storage_mb * 1024 * 1024

        percent_used = 0
        if max_storage_bytes > 0:
            percent_used = round((total_used_bytes / max_storage_bytes) * 100, 1)

        return {
            "user_email": user_gmail,
            "plan": user_plan,
            "storage": {
                "used_bytes": total_used_bytes,
                "used_mb": round(total_used_bytes / (1024 * 1024), 2),
                "max_bytes": max_storage_bytes,
                "max_mb": max_storage_mb,
                "percent_used": percent_used
            }
        }
    except Exception as e:
        logger.debug("[DEBUG] CHI TIẾT LỖI:", flush=True)
        logger.log(traceback.format_exc(), flush=True) 
        return {"error": f"Lỗi máy chủ: {str(e)}"}, 500