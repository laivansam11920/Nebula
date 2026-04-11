from flask import session, request


def lock_file_download_services():
    session.get("user_gmail")
    session.get("ten_nguoi_dung")
    session.get("trang_thai")
