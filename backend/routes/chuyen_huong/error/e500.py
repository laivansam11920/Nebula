from flask import Blueprint, send_from_directory
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.rate_limiting import limit_requests

e500 = Blueprint("error500", __name__)


@e500.route("/500", methods=["GET", "POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def e500_user_route():
    return send_from_directory(thu_muc_chinh("frontend/view/error"), "500.html"), 500
