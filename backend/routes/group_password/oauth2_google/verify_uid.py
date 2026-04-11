from flask import session, Blueprint
from controllers.group_password.oauth2_google.verify_uid import verify_uid_controller
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

app_route21 = Blueprint("kiem tra uid", __name__)


@app_route21.route("/google/verify_uid", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def verify_uid_route():
    return verify_uid_controller()
