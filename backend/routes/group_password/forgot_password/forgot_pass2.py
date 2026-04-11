from flask import session, Blueprint
from flask_cors import CORS, cross_origin

# import nội bộ
from controllers.group_password.forgot_password.forget_password2 import xac_thuc
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

findpassword_route_2 = Blueprint("auth_xac_thuc_mk", __name__)

CORS(findpassword_route_2)


@findpassword_route_2.route("/tim-mat-khau2", methods=["GET"])
@cross_origin()
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def tim_mat_khau2():
    return xac_thuc()
