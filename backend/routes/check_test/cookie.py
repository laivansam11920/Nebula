from flask import Blueprint, request, jsonify

check_status_auth_cookie = Blueprint("auth_cookie", __name__)


@check_status_auth_cookie.route("check-status")
def check_status():
    token = request.cookies.get("user_token")
    if token:
        return jsonify({"exists": True, "user": token}), 200
    return jsonify({"exists": False}), 401
