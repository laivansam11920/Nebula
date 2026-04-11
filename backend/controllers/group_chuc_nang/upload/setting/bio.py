from flask import session, request, jsonify
from services.group_chuc_nang.dashboard.setting.bio import cap_nhat_bio


def cap_nhat_bio_controller():
    try:
        ket_qua_gui_tu_frontend = request.get_json()
        user = session.get("user_gmail")
        bio = ket_qua_gui_tu_frontend.get("bio")
        ket_qua = cap_nhat_bio(str(bio), str(user))
        if not ket_qua["trang_thai"]:
            return jsonify(ket_qua), 401
        return jsonify(ket_qua), 200
    except Exception:
        return jsonify({"trang_thai": False, "mes": "loi tu phia server"}), 500
