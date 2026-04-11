from flask import session, request, jsonify
from services.group_chuc_nang.dashboard.setting.get_bio import get_bio_services


def get_bio_controller():
    user = session.get("user_gmail")
    if not user:
        jsonify({"trang_thai": False, "mes": "chua dang nhap"}), 401
    ket_qua = get_bio_services(user)
    if not ket_qua["trang_thai"]:
        return jsonify({"trang_thai": False, "mes": ket_qua["mes"]}), 400
    return jsonify({"trang_thai": True, "mes": ket_qua["mes"]}), 200
