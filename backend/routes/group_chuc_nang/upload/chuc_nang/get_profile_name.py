from flask import session, Blueprint
from controllers.group_chuc_nang.upload.chuc_nang.get_profile_name import (
    get_profile_controller,
)
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

app_route10 = Blueprint("lay_name", __name__)


@app_route10.route("get_profile", methods=["GET"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def get_profile_route():
    return get_profile_controller()
