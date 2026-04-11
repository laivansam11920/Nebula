from flask import session, jsonify, Blueprint
from datetime import datetime
from controllers.group_chuc_nang.upload.chuc_nang.bot_chat import chat_with_bot

app_route23 = Blueprint("chat_bot", __name__)


@app_route23.route("/support/chat", methods=["POST"])
def chat_bot():
    return chat_with_bot()


@app_route23.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})
