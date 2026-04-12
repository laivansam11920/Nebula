from flask import Blueprint, request
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai
from os import getenv

app_fac = Blueprint("face", __name__)

MY_VERIFY_TOKEN = str(getenv("MY_VERIFY_TOKEN"))
PAGE_ACCESS_TOKEN = str(getenv("PAGE_ACCESS_TOKEN"))

@app_fac.route("/mes", methods=["GET"])
def verify():
    # Facebook gửi yêu cầu GET để kiểm tra Webhook
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == MY_VERIFY_TOKEN:
        logger.log("WEBHOOK_VERIFIED", duong_dan_hien_tai())
        return challenge, 200  # BẮT BUỘC trả về challenge này

    return "Verification failed", 403
