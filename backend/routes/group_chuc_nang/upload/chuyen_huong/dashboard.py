from flask import session, Blueprint, send_from_directory, render_template
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.rate_limiting import limit_requests
from controllers.group_chuc_nang.kiem_tra_dang_nhap.upload_fist_login import (
    kiem_tra_token,
)

user_dashboard = Blueprint("user dashboard route", __name__)


@user_dashboard.route("/dashboard", methods=["GET", "POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def user_dashboard_user_route():
    res, ma_loi = kiem_tra_token()
    if ma_loi != 200:
        if ma_loi == 401:
            return (
                send_from_directory(thu_muc_chinh("frontend/view/error"), "401.html"),
                401,
            )
        return (
            send_from_directory(thu_muc_chinh("frontend/view/error"), "500.html"),
            500,
        )
    return render_template('test.html', name='lvs', user_email=session.get("user_gmail", "User"))
