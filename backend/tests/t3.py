from configs.db import db
from configs.argon2 import ph
from utils.hash_password import hash_password
from utils.make_token import tao_token_10_so
from utils.hash import hash
from datetime import datetime, timezone
from flask import session, request
from utils.get_ip import get_real_ip
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai


def kiem_tra(email_gui_len, pass_gui_len):

    noi_tim_kiem = db["users"]

    log_login = db["log_login"]

    kiem_tra_1 = noi_tim_kiem.find_one({"gmail": email_gui_len}, {"gmail": 1, "role": 1, "salt": 1, "password": 1, "_id": 0})

    if kiem_tra_1 is None:
        return {"success": False, "message": "Sai người dùng hoặc mật khẩu!"}

    role = kiem_tra_1["role"]
    salt = kiem_tra_1.get("salt")

    client_info = {
        "ip_address": get_real_ip(),
        "user_agent_raw": request.headers.get("User-Agent"),
        "device": {
            "os": request.user_agent.platform,
            "browser": request.user_agent.browser,
        },
    }
    pass_user = kiem_tra_1["password"]
    
    login_success = False
    migration_needed = False

    try:
        ph.verify(pass_user, pass_gui_len)

        login_success = True

    except Exception:
        pass_hash = hash_password(pass_gui_len, salt)

        if pass_user == pass_hash:
            login_success = True
            migration_needed = True

    if login_success: 

        token_new = tao_token_10_so()
        token_new_hash = hash(str(token_new))

        noi_tim_kiem.update_one(
            {"gmail": email_gui_len},
            {
                "$set": {
                    "token_nguoi_dung_upload": token_new_hash,
                    "trang_thai": "da_dang_nhap",
                    "blacklist": 0,
                    "password": ph.hash(str(pass_gui_len)) if migration_needed else pass_user
                }
            },
        )
        log_login.insert_one(
            {
                "timestamp": datetime.now(timezone.utc),
                "user_info": {
                    "gmail": email_gui_len,
                    "username": kiem_tra_1.get("username"),
                },
                "network": client_info,
                "security": {"status": "success", "session_id": token_new_hash},
                "login_with": "password",
            }
        )
        return {
            "success": True,
            "message": "Đăng nhập thành công! Chào bạn nhé!",
            "token": token_new,
            "role": role,
        }
    else:
        log_login.insert_one(
            {
                "timestamp": datetime.now(timezone.utc),
                "user_info": {"gmail": email_gui_len},
                "network": client_info,
                "security": {"status": "failed", "reason": "incorrect_password"},
                "login_with": "password",
            }
        )
        return {"success": False, "message": "Sai người dùng hoặc mật khẩu!"}
