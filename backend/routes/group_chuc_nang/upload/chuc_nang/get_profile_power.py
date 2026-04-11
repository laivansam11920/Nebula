from flask import session, Blueprint
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD
from controllers.group_chuc_nang.upload.chuc_nang.get_profile_power import (
    get_power_controller,
)

app_route11 = Blueprint("lay_quyen_han_nguoi_dung", __name__)


@app_route11.route("/get_power", methods=["GET"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def get_power_route():
    return get_power_controller()
