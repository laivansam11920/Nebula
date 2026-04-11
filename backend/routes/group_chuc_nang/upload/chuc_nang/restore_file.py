from flask import session, Blueprint
from middleware.rate_limiting import limit_requests
from controllers.group_chuc_nang.upload.chuc_nang.restore_file import (
    restore_file_controller,
)
from configs.settings import MAX_REQUESTS, PERIOD

app_route13 = Blueprint("restore file", __name__)


@app_route13.route("/restorefile_user", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def restore_file_route():
    return restore_file_controller()
