# Privacy Policy
from flask import Blueprint, send_from_directory
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.rate_limiting import limit_requests

privacy_policy = Blueprint("Privacy Policy", __name__)


@privacy_policy.route("/privacy_policy", methods=["GET", "POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def privacy_policy_user_route():
    return send_from_directory(
        thu_muc_chinh("frontend/view/dieu_khoan&chinh_sach"), "index.html"
    )
