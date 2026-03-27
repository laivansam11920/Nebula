from controllers.group_chuc_nang.upload.chuc_nang.lock_file import lock_file_controller
from flask import Blueprint
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

app_route25 = Blueprint("lock file", __name__)


@app_route25.route("/lock_file_services", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def lock_file_route():
    return lock_file_controller()
