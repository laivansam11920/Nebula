from flask import session, Blueprint
from controllers.group_chuc_nang.upload.setting.update_avt import upload_to_cloud_avt
from middleware.rate_limiting import limit_requests
from configs.settings import MAX_REQUESTS, PERIOD

app_route18 = Blueprint("cap nhat avt", __name__)


@app_route18.route("/setting/avatar", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def get_avt_route():
    return upload_to_cloud_avt()
