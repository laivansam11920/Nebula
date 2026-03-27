from flask import Blueprint, send_from_directory
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.rate_limiting import limit_requests

user_dashboard = Blueprint("user dashboard route", __name__)


@user_dashboard.route("/dashboard", methods=["GET", "POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def user_dashboard_user_route():
    return send_from_directory(
        thu_muc_chinh("frontend/view/upload/dashboard"), "index.html"
    )
