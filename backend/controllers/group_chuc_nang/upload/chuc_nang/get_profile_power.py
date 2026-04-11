from flask import session, request, jsonify
from services.group_chuc_nang.dashboard.get_profile_power import get_power_services


def get_power_controller():
    user_gmail = session.get("user_gmail")
    if not user_gmail:
        return jsonify({"ket_qua": "loi lay cookies roi"}), 401
    ket_qua = get_power_services(user_gmail)
    if not ket_qua:
        return jsonify({"ket_qua": "loi roi"}), 404
    return jsonify({"power": ket_qua}), 200
