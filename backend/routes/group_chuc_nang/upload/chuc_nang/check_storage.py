from flask import session, Blueprint
from middleware.rate_limiting import limit_requests
from controllers.group_chuc_nang.upload.chuc_nang.check_storage import (
    check_storage_controller,
)
from configs.settings import MAX_REQUESTS, PERIOD

check_storage = Blueprint("check storage", __name__)


@check_storage.route("/check_storage_user", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def check_storage_route():
    return check_storage_controller()
