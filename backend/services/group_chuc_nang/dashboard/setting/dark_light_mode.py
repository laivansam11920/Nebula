from flask import session, request, jsonify
from configs.db import db


def dark_m_services():
    data_res = request.get_json()

    nguoi_dung = data_res.get("gmail")
    du_lieu_nen = data_res.get("dark_light_m")

    collection = db["users"]
    user = collection.find_one({"gmail": nguoi_dung})
    if not user:
        return jsonify({"ket_qua": False, "mes": "khong tim thay nguoi dung"}), 401

    query = {"gmail": nguoi_dung}
    new_values = {"$set": {"trang_thai_hinh_nen": du_lieu_nen}}

    collection.update_one(query, new_values)

    return jsonify({"ket_qua": True, "mes": "Cap nhat thanh cong"}), 200
