import requests
from flask import Response, Blueprint, send_from_directory
from configs.db import db
from configs.duong_dan_thu_muc import thu_muc_chinh
from validators.kiem_tra_dang_nhap import login_required
from services.upload.chuc_nang.lock_file import lock_file_services

show_html_domain = Blueprint("show html domain",__name__)

@show_html_domain.route("/<username>/site/<path:duong_dan_file>")
@login_required
def hien_thi_trang_ca_nhan(username, duong_dan_file):
    link_github_goc = f"https://gemini-dot.github.io/html_upload/users/{username}/{duong_dan_file}"

    try:
        res, code = lock_file_services()

        if code != 200:
            if code == 401:
                return send_from_directory(thu_muc_chinh("frontend/view/error"), "401.html"), 401
            return send_from_directory(thu_muc_chinh("frontend/view/error"), "500.html"), 500

        with requests.get(link_github_goc, stream=True, timeout=20) as lay_file:
            
            if lay_file.status_code == 404:
                return "Lỗi rách việc: Không tìm thấy trang của ông kẹ này!", 404
            
            kieu_file = lay_file.headers.get('content-type', 'text/html')
            
            def truyen_du_lieu():
                for chunk in lay_file.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk

            return Response(truyen_du_lieu(), mimetype=kieu_file), 200
            
    except requests.exceptions.Timeout:
         return "Lỗi rách việc: Github bên Mỹ xa xôi, tui chờ 20 giây hết nổi rồi!", 504
    except Exception as e:
        return f"Lỗi hệ thống người trung gian: {e}", 500