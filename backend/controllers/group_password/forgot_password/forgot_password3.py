from flask import session, request, jsonify
from services.group_mk.forgot_password.forgot_password3 import kiem_tra_de_doi_mat_khau


def doi_mat_khau_moi():
    data = request.get_json()
    token = data.get("token")
    gmail = data.get("gmail")
    new_password = data.get("new_password")

    if not all([token, gmail, new_password]):
        return jsonify({"success": False, "message": "Thiếu thông tin cần thiết!"}), 400

    try:
        kiem_tra = kiem_tra_de_doi_mat_khau(token, gmail, new_password)
        if kiem_tra["success"]:
            return jsonify(kiem_tra), 200
        return jsonify(kiem_tra), 400
    except Exception as server_error:
        return jsonify({"success": False, "message": str(server_error)}), 500
