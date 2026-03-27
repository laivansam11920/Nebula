from flask import request, jsonify
from services.upload.chuc_nang.check_storage import get_user_storage_info


def check_storage_controller():
    try:
        user_gmail = request.cookies.get("user_gmail")
        res = get_user_storage_info(user_gmail)
        return jsonify(res), 200
    except Exception as e:
        print(f"[DEBUG]error {e}", flush=True)
