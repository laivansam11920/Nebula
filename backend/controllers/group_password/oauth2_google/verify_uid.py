from flask import session, request, jsonify
from services.group_mk.oauth2_google.verify_uid import verify_uid


def verify_uid_controller():
    data = request.get_json()
    uid = data.get("uid")
    user_gmail = data.get("gmail")
    ket_qua = verify_uid(user_gmail, uid)
    if ket_qua["mes"]:
        return jsonify({"trang_thai": True, "mes": ket_qua["mes"]}), 200
    return jsonify({"trang_thai": False, "mes": ket_qua["mes"]}), 401
