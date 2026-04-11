from flask import session, Blueprint
from controllers.group_chuc_nang.upload.setting.get_bio import get_bio_controller
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

app_route17 = Blueprint("cap nhat bio", __name__)


@app_route17.route("/setting/get_bio", methods=["GET"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def get_bio_route():
    return get_bio_controller()
