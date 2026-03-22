from flask import Blueprint, send_from_directory
from configs.duong_dan_thu_muc import thu_muc_chinh
from configs.settings import MAX_REQUESTS, PERIOD
from middleware.rate_limiting import limit_requests

send_mail_reset_password = Blueprint("send_mail_reset_password route user",__name__)

@send_mail_reset_password.route("/reset_password",methods=['GET','POST'])
@limit_requests(max_requests=MAX_REQUESTS, period=PERIOD)

def send_mail_reset_password_user_route():
    return send_from_directory(thu_muc_chinh("frontend/view/group_password"), "forgot_password.html")