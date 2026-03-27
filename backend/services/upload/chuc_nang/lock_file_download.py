from flask import request


def lock_file_download_services():
    request.cookies.get("user_gmail")
    request.cookies.get("ten_nguoi_dung")
    request.cookies.get("trang_thai")
