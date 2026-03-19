from services.upload.chuc_nang.check_storage import get_user_storage_info

def check_storage_user_services(user_gmail):
    if not user_gmail:
        return False, "Không tìm thấy người dùng"
    
    storage_info = get_user_storage_info(user_gmail)

    if isinstance(storage_info, tuple):
        return False, "Lỗi máy chủ khi kiểm tra dung lượng"

    try:
        percent = storage_info.get("storage", {}).get("percent_used", 0)
        
        if percent >= 100:
            return False, "Bạn đã sử dụng hết không gian lưu trữ cho phép. Vui lòng nâng cấp gói!"
        
    except Exception as e:
        return False, f"Lỗi tính toán dung lượng: {str(e)}"
        
    return True, "ok"