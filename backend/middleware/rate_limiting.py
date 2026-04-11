from flask import session, request, jsonify
from functools import wraps
import time
from configs.settings import ip_allow, MAX_REQUESTS, PERIOD
from utils.tim_kiem_db import tim_kiem
from utils.kiem_tra_het_han_toan_cuc import kiem_tra_het_han

ip_history = {}


def limit_requests(max_requests=MAX_REQUESTS, period=PERIOD):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            WHITELIST_IPS = ip_allow
            ket_qua = tim_kiem("godmode_admin", "trang_thai")
            now_n = time.time()
            ket_qua_thoi_gian = kiem_tra_het_han(
                now_n,
                "godmode_admin",
                "godmode",
                "private",
                "thoi_gian_het_han",
                "trang_thai_thoi_gian",
                "da_het_han",
            )
            ket_qua_thoi_gian_tra_ve = ket_qua_thoi_gian["trang_thai"]
            ip = request.remote_addr
            if (
                ip in WHITELIST_IPS
                and str(ket_qua) == "on"
                and str(ket_qua_thoi_gian_tra_ve) == "chua_het_han"
            ):
                return f(*args, **kwargs)
            now = time.time()
            if ip not in ip_history:
                ip_history[ip] = []
            ip_history[ip] = [t for t in ip_history[ip] if now - t < period]
            if len(ip_history[ip]) >= max_requests:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": f"Quá nhiều yêu cầu! Thử lại sau {period} giây.",
                        }
                    ),
                    429,
                )
            ip_history[ip].append(now)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
