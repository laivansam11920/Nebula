from flask import session, request, jsonify
from services.group_mk.forgot_password.forgot_password1 import kiem_tra_dat_lai_mat_khau


def gui_yeu_cau():
    data = request.get_json()

    if not data or "gmail" not in data:
        return jsonify({"success": False, "message": "Thiếu email rồi bạn ơi!"}), 400

    du_lieu = data.get("gmail")

    if not du_lieu:
        return jsonify({"success": False, "message": "Thiếu email rồi bạn ơi!"}), 400

    ket_qua = kiem_tra_dat_lai_mat_khau(du_lieu)

    if ket_qua["success"]:
        return jsonify({"message": ket_qua}), 200
    if ket_qua.get("type") == "not_exist":
        return jsonify({"success": False, "message": "Người dùng không tồn tại."}), 404
    return (
        jsonify(
            {
                "success": False,
                "message": ket_qua.get("error", "Đã có lỗi xảy ra khi gửi email."),
            }
        ),
        500,
    )
