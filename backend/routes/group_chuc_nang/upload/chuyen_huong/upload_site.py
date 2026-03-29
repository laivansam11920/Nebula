from flask import Blueprint, send_from_directory
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.rate_limiting import limit_requests
from controllers.group_chuc_nang.kiem_tra_dang_nhap.upload_fist_login import (
    kiem_tra_token,
)

user_upload_site = Blueprint("user upload site route", __name__)


@user_upload_site.route("/upload", methods=["GET", "POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def user_upload_user_route():
    res, ma_loi  = kiem_tra_token()
    if ma_loi != 200:
        if ma_loi == 401:
            return send_from_directory(thu_muc_chinh("frontend/view/error"), "401.html"), 401
        return send_from_directory(thu_muc_chinh("frontend/view/error"), "500.html"), 500
    return send_from_directory(
        thu_muc_chinh("frontend/view/upload/web_upload"), "index.html"
    )
