from flask import session, Blueprint

# import nội bộ
from middleware.rate_limiting import limit_requests
from controllers.group_password.input_pass import kiem_tra1
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.limit_content_length import limit_content_length

login_route = Blueprint("auth_input", __name__)


@login_route.route("/input-pass", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
@limit_content_length(100 * 1024 * 1024)
def input_pass():
    return kiem_tra1()
