from flask import session, Blueprint
from controllers.group_chuc_nang.upload.setting.bio import cap_nhat_bio_controller
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

app_route16 = Blueprint("setting bio", __name__)


@app_route16.route("/setting/bio", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def cap_nhat_bio_route():
    return cap_nhat_bio_controller()
