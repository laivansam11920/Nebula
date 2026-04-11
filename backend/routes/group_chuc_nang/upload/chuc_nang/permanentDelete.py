from flask import session, Blueprint
from middleware.rate_limiting import limit_requests
from controllers.group_chuc_nang.upload.chuc_nang.permanentDelete import (
    permanentdelete_file_controller,
)
from configs.settings import MAX_REQUESTS, PERIOD

app_route14 = Blueprint("xoa vinh vien", __name__)


@app_route14.route("/permanent_delete_user", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def permanentdelete_file_route():
    return permanentdelete_file_controller()
