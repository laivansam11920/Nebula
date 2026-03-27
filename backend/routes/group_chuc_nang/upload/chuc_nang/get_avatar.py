from flask import Blueprint
from controllers.group_chuc_nang.upload.chuc_nang.get_avatar import (
    get_avatar_controller,
)
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

app_route28 = Blueprint("lay_avatar", __name__)


@app_route28.route("get_avatar", methods=["GET"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def get_avatar_route():
    return get_avatar_controller()
