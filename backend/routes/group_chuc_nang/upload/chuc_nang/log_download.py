from controllers.group_chuc_nang.upload.chuc_nang.log_download import log_dl_con
from flask import session, Blueprint
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

app_route24 = Blueprint("log file", __name__)


@app_route24.route("/log-download", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def log_file_route():
    return log_dl_con()
