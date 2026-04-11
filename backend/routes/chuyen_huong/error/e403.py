from flask import session, Blueprint, send_from_directory
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.rate_limiting import limit_requests

e403 = Blueprint("error403", __name__)


@e403.route("/403", methods=["GET", "POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def e403_user_route():
    return send_from_directory(thu_muc_chinh("frontend/view/error"), "403.html"), 403
