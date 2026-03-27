from configs.db import db
from datetime import datetime, timedelta, timezone
from utils.get_ip import get_real_ip
from flask import request


def kiem_tra_db(nguoi_dung, gmail_nguoi_dung, pic, uid):
    collection = db["users"]
    log_login = db["log_login"]

    client_info = {
        "ip_address": get_real_ip(),
        "user_agent_raw": request.headers.get("User-Agent"),
        "device": {
            "os": request.user_agent.platform,
            "browser": request.user_agent.browser,
        },
    }

    ket_qua = collection.find_one({"gmail": str(gmail_nguoi_dung)})
    thoi_gian_hien_tai = datetime.now(timezone.utc)
    thoi_gian_het_han = thoi_gian_hien_tai + timedelta(days=30)

    if ket_qua:
        collection.update_one({"gmail": str(gmail_nguoi_dung)}, {"$set": {"uid": uid}})
        log_login.insert_one(
            {
                "timestamp": thoi_gian_hien_tai,
                "user_info": {
                    "gmail": gmail_nguoi_dung,
                    "username": ket_qua.get("username"),
                },
                "network": client_info,
                "security": {"status": "success", "session_id": "True"},
                "login_with": "google",
            }
        )
        return {"trang_thai": True, "mes": "ban da dang nhap"}

    log_login.insert_one(
        {
            "timestamp": thoi_gian_hien_tai,
            "user_info": {"gmail": gmail_nguoi_dung, "username": str(nguoi_dung)},
            "network": client_info,
            "security": {"status": "success", "session_id": "True"},
            "login_with": "google",
        }
    )
    cap_nhat = {
        "username": str(nguoi_dung),
        "gmail": str(gmail_nguoi_dung),
        "cap_nguoi_dung": "basic",
        "thoi_gian_cap_trang_thai": {
            "bat_dau": thoi_gian_hien_tai,
            "ket_thuc": thoi_gian_het_han,
        },
        "khong_gian_luu_tru": "128",
        "role": "user",
        "bio": "",
        "avatar_google": pic,
        "uid": uid,
    }
    collection.insert_one(cap_nhat)
    return {"trang_thai": True, "mes": "Đăng ký thành công!", "email": gmail_nguoi_dung}
