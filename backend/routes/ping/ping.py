from flask import session, Blueprint

khoi_dong = Blueprint("ping", __name__)


@khoi_dong.route("/khoi-dong")
def ping():
    return "Pong!"
