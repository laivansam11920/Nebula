from flask import session, Blueprint
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD
from controllers.group_chuc_nang.upload.chuc_nang.lay_file import (
    get_files_for_dashboard,
)

app_route9 = Blueprint("upload_lay_file", __name__)


@app_route9.route("/upload_get_file", methods=["GET"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def get_file_route():
    return get_files_for_dashboard()
