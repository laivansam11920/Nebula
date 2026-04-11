from flask import session, request, jsonify
from services.group_chuc_nang.dashboard.permanentDelete import (
    permanentdelete_file_services,
)


def permanentdelete_file_controller():
    trang_thai_dang_nhap = session.get("trang_thai")
    if not trang_thai_dang_nhap or str(trang_thai_dang_nhap) == "chua_dang_nhap":
        return jsonify({"trang_thai": False, "mes": "loi chua dang nhap"}), 401
    data = request.get_json()
    ma_dinh_danh = data.get("ma_dinh_danh_file")
    if not ma_dinh_danh:
        return (
            jsonify({"trang_thai": False, "mes": "Thiếu mã định danh file rồi og ơi!"}),
            400,
        )
    ket_qua = permanentdelete_file_services(ma_dinh_danh, "file_info")
    if not ket_qua:
        return jsonify({"trang_thai": False, "mes": ket_qua}), 404
    return jsonify({"trang_thai": True, "mes": ket_qua}), 200
