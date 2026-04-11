import cloudinary
import cloudinary.uploader
from flask import session, request, jsonify
from utils.cloudidary_json_get import make_json_cloud
from utils.luu_du_lieu_vao_db import luu
from utils.scan_img import check_image_sensitivity
import os
import uuid
from configs.db import db
import configs.cloudinary
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR, exist_ok=True)
    logger.log(f"Đã tạo thư mục tạm tại: {TEMP_DIR}", duong_dan_hien_tai())
else:
    logger.log(f"Đã tạo thư mục tạm tại: {TEMP_DIR}", duong_dan_hien_tai())


def upload_to_cloud_avt():
    user_email = session.get("user_gmail")
    trang_thai = session.get("trang_thai")

    if trang_thai != "da_dang_nhap":
        return jsonify({"loi": "nguoi_dung_chua_dang_nhap"}), 401

    if not user_email:
        return jsonify({"loi": "nguoi_dung"}), 401

    folder_name = f"my_project/users/{user_email.replace('@', '_').replace('.', '_')}"

    if "avatar" not in request.files:
        return jsonify({"error": "Không có file"}), 400

    files = request.files.getlist("avatar")
    urls = []
    error = []
    for file in files:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        temp_path = os.path.abspath(os.path.join(TEMP_DIR, unique_filename))
        try:
            file.save(temp_path)
            logger.log(f"Đã lưu tạm: {temp_path}", duong_dan_hien_tai())
            file.seek(0)
            ten_file_goc = file.filename
            if ten_file_goc:
                logger.log("ok, name create", duong_dan_hien_tai())
            else:
                ten_file_goc = "no_name__file"
            res = check_image_sensitivity(temp_path)
            logger.log(res, duong_dan_hien_tai())
            level = res.get("level").upper()
            if level != "SAFE":
                error.append({"file": ten_file_goc, "error": "Nội dung nhạy cảm"})
                os.remove(temp_path)
                continue
            upload_result = cloudinary.uploader.upload(
                file,
                folder=folder_name,
                use_filename=True,
                resource_type="auto",
                unique_filename=True,
            )
            file_info = make_json_cloud(
                upload_result, user_email, ten_file_goc, "avatar"
            )

            db["file_info"].update_many(
                {
                    "user_gmail": user_email,
                    "loai_file": "avatar",
                    "trang_thai": {"$ne": "da_xoa"},
                    "url": {"$ne": file_info.get("secure_url", "")},
                },
                {"$set": {"trang_thai": "da_xoa"}},
            )

            luu(file_info, "file_info")
            urls.append(file_info.get("url"))
        except Exception as e:
            logger.error(f"{e}", duong_dan_hien_tai())
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    return jsonify({"mes": urls, "error": error}), 200
