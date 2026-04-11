from flask import session, Blueprint, send_from_directory
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.rate_limiting import limit_requests

e503 = Blueprint("error503", __name__)


@e503.route("/503", methods=["GET", "POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def e501_user_route():
    return send_from_directory(thu_muc_chinh("frontend/view/error"), "503.html"), 503
