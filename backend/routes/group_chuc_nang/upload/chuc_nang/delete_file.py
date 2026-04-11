from flask import session, Blueprint
from middleware.rate_limiting import limit_requests
from controllers.group_chuc_nang.upload.chuc_nang.delete_file import (
    detele_file_controller,
)
from configs.settings import MAX_REQUESTS, PERIOD

app_route12 = Blueprint("delete file", __name__)


@app_route12.route("/deletefile_user", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def delete_file_route():
    return detele_file_controller()
