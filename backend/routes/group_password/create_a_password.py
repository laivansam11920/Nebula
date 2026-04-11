from flask import session, Blueprint
from middleware.rate_limiting import limit_requests
from controllers.group_password.create_a_password import kiem_tra2
from configs.settings import MAX_REQUESTS, PERIOD

signup_route = Blueprint("auth_create", __name__)


@signup_route.route("/create-a-pass", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def create_a_pass():
    return kiem_tra2()
