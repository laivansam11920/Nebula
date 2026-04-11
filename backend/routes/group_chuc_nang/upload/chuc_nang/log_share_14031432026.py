from controllers.group_chuc_nang.upload.chuc_nang.log_share_135914032026 import (
    log_sh_con,
)
from flask import session, Blueprint
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

app_route26 = Blueprint("log file share", __name__)


@app_route26.route("/log-share", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def log_share_route():
    return log_sh_con()
