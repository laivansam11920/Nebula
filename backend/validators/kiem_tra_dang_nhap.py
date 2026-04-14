from flask import session, send_from_directory
from functools import wraps
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.db import db
from logs import logger

def login_required(f) -> any:
    @wraps(f)
    def decorated_function(*args, **kwargs) -> any:
        try:
            s_user = session.get("user_gmail")
            s_trang_thai = session.get("trang_thai")

            if not s_trang_thai or not s_user:
                return (
                    send_from_directory(thu_muc_chinh("frontend/view/error"), "401.html"),
                    401,
                )
            collection = db['users']
            
            trang_thai = collection.find_one({'gmail': s_user}, {'trang_thai': 1, '_id': 0})

            if not trang_thai:
                return (
                    send_from_directory(thu_muc_chinh("frontend/view/error"), "401.html"),
                    401,
                )

            if str(s_trang_thai) != "da_dang_nhap" or str(trang_thai.get("trang_thai")) != 'da_dang_nhap':
                return (
                    send_from_directory(thu_muc_chinh("frontend/view/error"), "401.html"),
                    401,
                )

            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Lỗi kiểm tra đăng nhập: {str(e)}", thu_muc_chinh())
            return (
                send_from_directory(thu_muc_chinh("frontend/view/error"), "500.html"),
                500,
            )
    return decorated_function
