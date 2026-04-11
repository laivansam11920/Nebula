from flask import session, Blueprint

# import nội bộ
from middleware.rate_limiting import limit_requests
from controllers.group_password.forgot_password.forgot_password import gui_yeu_cau
from configs.settings import MAX_REQUESTS, PERIOD

findpassword_route = Blueprint("auth_tim_mk", __name__)


@findpassword_route.route("/tim-mat-khau1", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def tim_mat_khau1():
    return gui_yeu_cau()
