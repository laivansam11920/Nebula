from flask import Blueprint
import requests
from configs.db import db
import os
from utils.hash256 import get_sha256_hash
from logs.logger import logger

lenh_tu_huy = Blueprint("lenh_tu_huy", __name__)

RENDER_API_KEY = os.getenv("RENDER_API_KEY")
SERVICE_ID = os.getenv("SERVICE_ID1")


@lenh_tu_huy.route("/nuclear-shutdown/<passphrase>", methods=["GET"])
def kill_switch(passphrase):
    security_check = db["thuc_thi"].find_one({"lenh_thuc_thi_bat_buoc": "admin-root"})
    env_pass = os.getenv("DATABASE_0")

    api_key = os.getenv("RENDER_API_KEY")
    service_id = os.getenv("SERVICE_ID1")

    if security_check and env_pass:
        db_hash = security_check.get("lenh_thuc_thi")
        if passphrase == env_pass and str(db_hash) == str(get_sha256_hash(env_pass)):
            if not api_key or not service_id:
                return "Thiếu biến môi trường RENDER_API_KEY hoặc SERVICE_ID1", 500

            logger.warning(f"\n☢️ [SECURITY ALERT] Đang đình chỉ dịch vụ: {service_id}")

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            }
            url = f"https://api.render.com/v1/services/{service_id}/suspend"

            try:
                response = requests.post(url, headers=headers, timeout=15)
                if response.status_code == 204:
                    return "☢️ [SUCCESS] Render Service Suspended.", 200
                else:
                    return (
                        f"Render trả về lỗi: {response.status_code} - {response.text}",
                        500,
                    )
            except Exception as e:
                return f"Lỗi kết nối API: {str(e)}", 500

    return "Access Denied", 403
