from flask import session, request, jsonify
from services.group_mk.forgot_password.forgot_password2 import kiem_tra_xac_nhan


def xac_thuc():
    gmail = request.args.get("gmail")
    token = request.args.get("token")

    kiem_tra = kiem_tra_xac_nhan(gmail, token)

    if kiem_tra["success"]:
        return jsonify(kiem_tra), 200
    return jsonify(kiem_tra), 400
