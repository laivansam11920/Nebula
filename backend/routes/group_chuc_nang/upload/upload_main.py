from flask import session, Blueprint

# import noi bo
from middleware.rate_limiting import limit_requests
from controllers.group_chuc_nang.upload.upload_main import upload_to_cloud
from configs.settings import MAX_REQUESTS, PERIOD

app_route8 = Blueprint("upload_api", __name__)


@app_route8.route("/upload", methods=["POST"])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)
def up_load_route():
    return upload_to_cloud()
