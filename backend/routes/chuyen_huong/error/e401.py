from flask import Blueprint, send_from_directory
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.rate_limiting import limit_requests

e401 = Blueprint("error401", __name__)


@e401.route("/401", methods=["GET", "POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def e401_user_route():
    return send_from_directory(thu_muc_chinh("frontend/view/error"), "401.html"), 401
