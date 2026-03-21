from flask import Blueprint, send_from_directory
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.rate_limiting import limit_requests

login = Blueprint("login route user",__name__)

@login.route("/login",methods=['GET','POST'])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)

def login_user_route():
    return send_from_directory(thu_muc_chinh("frontend/view/group_password"), "input_pass.html")