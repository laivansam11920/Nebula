from flask import session, request, jsonify
from services.group_chuc_nang.dashboard.get_profile_name import get_profile


def get_profile_controller():
    try:
        gmail = session.get("user_gmail")
        if not gmail:
            return jsonify({"trang_thai": False, "mes": "Cookie gmail trống"}), 401
        ket_qua = get_profile(gmail)
        if not ket_qua["trang_thai"]:
            return jsonify(ket_qua), 404
        return ket_qua, 200
    except Exception as e:
        return jsonify({"trang_thai": False, "mes": f"error{e}"}), 500
