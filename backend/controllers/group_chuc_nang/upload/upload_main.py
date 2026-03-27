import cloudinary
import cloudinary.uploader
from flask import request, jsonify
from utils.cloudidary_json_get import make_json_cloud
from utils.luu_du_lieu_vao_db import luu
from utils.scan_img import check_image_sensitivity
from services.upload.chuc_nang.upload_html import upload_html_to_github
from services.upload.chuc_nang.save_metadata import save_metadata_html
from services.upload.chuc_nang.kiem_tra_gioi_han_dung_luong_user import (
    check_storage_user_services,
)
import os
import uuid
import concurrent.futures
import configs.cloudinary

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR, exist_ok=True)
    print(f"📁 Đã tạo thư mục tạm tại: {TEMP_DIR}")
else:
    print(f"📁 Thư mục tạm đã sẵn sàng: {TEMP_DIR}")


def process_single_file(file_data, user_email, folder_name):
    file_bytes, ten_file_goc, content_type = file_data

    unique_filename = f"{uuid.uuid4()}_{ten_file_goc}"
    temp_path = os.path.abspath(os.path.join(TEMP_DIR, unique_filename))

    result = {"url": None, "error": None}

    try:
        with open(temp_path, "wb") as f:
            f.write(file_bytes)

        print(f"--- Đã lưu tạm: {temp_path} ---")

        if not ten_file_goc:
            ten_file_goc = "no_name_file"

        if ten_file_goc.lower().endswith(".html") or content_type == "text/html":
            print(f"Da phat hien ra file html {ten_file_goc}")
            link_github = upload_html_to_github(temp_path, ten_file_goc, user_email)
            if link_github:
                file_info_html = save_metadata_html(
                    temp_path, user_email, ten_file_goc, link_github
                )
                luu(file_info_html, "file_info")
                result["url"] = link_github
            else:
                result["error"] = {"file": ten_file_goc, "error": "Lỗi upload GitHub"}
            return result

        is_document = ten_file_goc.lower().endswith(
            (".pptx", ".ppt", ".pdf", ".docx", ".xlsx", ".txt")
        )
        if not is_document:
            res = check_image_sensitivity(temp_path)
            level = res.get("level", "UNKNOWN").upper()
            if level != "SAFE":
                result["error"] = {"file": ten_file_goc, "error": "Nội dung nhạy cảm"}
                return result

        ### Upload lên Cloudinary
        print(f"--- Bắt đầu upload Cloudinary: {ten_file_goc} ---")
        upload_result = cloudinary.uploader.upload(
            temp_path,
            folder=folder_name,
            use_filename=True,
            resource_type="auto",
            unique_filename=True,
        )
        print(f"--- Upload Cloudinary xong: {ten_file_goc} ---")

        file_info = make_json_cloud(upload_result, user_email, ten_file_goc, "upload")
        luu(file_info, "file_info")

        result["url"] = file_info["url"]

    except Exception as e:
        print(f"Lỗi khi xử lý file {ten_file_goc}: {e}")
        result["error"] = {"file": ten_file_goc, "error": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return result


def upload_to_cloud():
    user_email = request.cookies.get("user_gmail")
    trang_thai = request.cookies.get("trang_thai")

    if trang_thai != "da_dang_nhap":
        return jsonify({"loi": "nguoi_dung_chua_dang_nhap"}), 401

    if not user_email:
        return jsonify({"loi": "nguoi_dung"}), 401

    hop_le, loi_nhan = check_storage_user_services(user_email)
    if not hop_le:
        return jsonify({"error": loi_nhan}), 507

    folder_name = f"my_project/users/{user_email.replace('@', '_').replace('.', '_')}"

    if "files[]" not in request.files:
        return jsonify({"error": "Không có file"}), 400

    files_list = request.files.getlist("files[]")
    if not files_list or all(f.filename == "" for f in files_list):
        return jsonify({"error": "Danh sách file rỗng"}), 400

    print("--- KIỂM TRA ĐẦU VÀO ---")
    print(f"Content-Length: {request.content_length}")

    urls = []
    errors = []

    prepared_files = []
    for file in files_list:
        if file.filename:
            file_bytes = file.read()
            prepared_files.append((file_bytes, file.filename, file.content_type))

    max_workers = min(5, len(prepared_files))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single_file, file_data, user_email, folder_name)
            for file_data in prepared_files
        ]

        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res.get("url"):
                urls.append(res["url"])
            if res.get("error"):
                errors.append(res["error"])

    return jsonify({"links": urls, "error": errors}), 200
