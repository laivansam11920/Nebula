from flask import session, request, jsonify
from utils.lay_du_lieu_thu_db import lay_tat_ca_file
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai


def get_files_for_dashboard():
    user_email = session.get("user_gmail", "")
    trang_thai = session.get("trang_thai", "")

    if trang_thai != "da_dang_nhap" or not user_email:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        user_files = lay_tat_ca_file(user_email, "file_info")

        return jsonify({"status": "success", "files": user_files}), 200

    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
        return jsonify({"error": "Internal Server Error"}), 500
