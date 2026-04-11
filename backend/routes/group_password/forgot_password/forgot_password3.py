from flask import session, Blueprint

# import nội bộ
from middleware.rate_limiting import limit_requests
from controllers.group_password.forgot_password.forgot_password3 import doi_mat_khau_moi
from configs.settings import MAX_REQUESTS, PERIOD

findpassword_route_3 = Blueprint("auth_xac_nhan_token", __name__)


@findpassword_route_3.route("/tim-mat-khau3", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def xac_nhan_token():
    return doi_mat_khau_moi()
