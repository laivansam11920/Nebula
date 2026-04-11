from controllers.group_chuc_nang.upload.chuc_nang.logout import logout_controller
from flask import session, Blueprint
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

app_route27 = Blueprint("logout", __name__)


@app_route27.route("/logout", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def logout_route():
    return logout_controller()
