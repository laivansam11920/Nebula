from flask import request, jsonify
from utils.lay_du_lieu_thu_db import lay_tat_ca_file


def get_files_for_dashboard():
    user_email = request.cookies.get("user_gmail", "")
    trang_thai = request.cookies.get("trang_thai", "")

    if trang_thai != "da_dang_nhap" or not user_email:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        user_files = lay_tat_ca_file(user_email, "file_info")

        return jsonify({"status": "success", "files": user_files}), 200

    except Exception as e:
        print(f"Lỗi khi lấy danh sách file: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
