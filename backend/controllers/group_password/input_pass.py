from flask import session, request, jsonify, make_response, session
from services.group_mk.login import kiem_tra
from validators.kiem_tra_cap_bac import kiem_tra_cap_bac
from utils.search import tim_only
from configs.duong_dan_thu_muc import duong_dan_hien_tai
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai
from utils.session import set_session

def kiem_tra1():
    du_lieu = request.get_json()

    nguoi_dung = du_lieu.get("gmail", "")
    mat_khau = du_lieu.get("password", "")

    role = kiem_tra_cap_bac(nguoi_dung, "users")
    role_sach = str(role).strip().lower()

    try:
        if str(role_sach) == "admin-root":
            lenh = {"lenh_thuc_thi": "khong_kiem_tra"}
            res_res_res = jsonify(lenh)
            list = {"role": str(role), "lenh_thuc_thi":"khong_kiem_tra"}
            set_session(**list)
            return res_res_res, 200
    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
        return jsonify({"error": "server error"}), 500

    ket_qua = kiem_tra(nguoi_dung, mat_khau)

    if ket_qua["success"]:
        name = tim_only("users", "gmail", str(nguoi_dung), "username")
        token = ket_qua["token"]
        res = jsonify(ket_qua)

        set_session(user_token=token, user_gmail=nguoi_dung, role=role, lenh_thuc_thi="can_kiem_tra", trang_thai="da_dang_nhap", ten_nguoi_dung=name)
    
        return res, 200
    else:
        res_res = jsonify(ket_qua)

        set_session(lenh_thuc_thi="can_kiem_tra", trang_thai="chua_dang_nhap")

        return res_res, 401
