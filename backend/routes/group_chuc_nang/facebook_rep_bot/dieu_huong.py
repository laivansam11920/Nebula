from flask import session, Blueprint, request
from controllers.group_chuc_nang.chat.chat_main import receive_message

app_route22 = Blueprint("facebook-bot", __name__)

VERIFY_TOKEN = "samvasang1192011"


@app_route22.route("/mes", methods=["GET"])
def verify():
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Sai Verify Token rồi og ơi!", 403


@app_route22.route("/mes", methods=["POST"])
def chat_route():
    return receive_message()
