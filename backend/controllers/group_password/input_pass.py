from flask import request, jsonify, make_response
from services.group_mk.login import kiem_tra
from validators.kiem_tra_cap_bac import kiem_tra_cap_bac
from utils.search import tim_only
from configs.duong_dan_thu_muc import duong_dan_hien_tai
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

def kiem_tra1():
    du_lieu = request.get_json()

    nguoi_dung = du_lieu.get("gmail", "")
    mat_khau = du_lieu.get("password", "")

    role = kiem_tra_cap_bac(nguoi_dung, "users")
    role_sach = str(role).strip().lower()

    try:
        if str(role_sach) == "admin-root":
            lenh = {"lenh_thuc_thi": "khong_kiem_tra"}
            res_res_res = make_response(jsonify(lenh))
            res_res_res.set_cookie(
                "role",
                str(role),
                max_age=86400 * 30,
                httponly=True,
                samesite="None",
                secure=True,
                path="/",
            )
            res_res_res.set_cookie(
                "lenh_thuc_thi",
                "khong_kiem_tra",
                max_age=86400 * 30,
                httponly=True,
                samesite="None",
                secure=True,
                path="/",
            )
            return res_res_res, 200
    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
        return jsonify({"error": "server error"}), 500

    ket_qua = kiem_tra(nguoi_dung, mat_khau)

    if ket_qua["success"]:
        name = tim_only("users", "gmail", str(nguoi_dung), "username")
        token = ket_qua["token"]
        res = make_response(jsonify(ket_qua))
        res.set_cookie(
            "user_token",
            token,
            max_age=86400 * 30,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )
        res.set_cookie(
            "user_gmail",
            nguoi_dung,
            max_age=86400 * 30,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )
        res.set_cookie(
            "role",
            role,
            max_age=86400 * 30,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )
        res.set_cookie(
            "lenh_thuc_thi",
            "can_kiem_tra",
            max_age=86400 * 30,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )
        res.set_cookie(
            "trang_thai",
            "da_dang_nhap",
            max_age=86400 * 30,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )
        res.set_cookie(
            "ten_nguoi_dung",
            name,
            max_age=86400 * 30,
            httponly=False,
            samesite="None",
            secure=True,
            path="/",
        )
        return res, 200
    else:
        res_res = make_response(jsonify(ket_qua))
        res_res.set_cookie(
            "user_token",
            "",
            max_age=0,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )
        res_res.set_cookie(
            "user_gmail",
            "",
            max_age=0,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )
        res_res.set_cookie(
            "role",
            role,
            max_age=86400 * 30,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )
        res_res.set_cookie(
            "lenh_thuc_thi",
            "can_kiem_tra",
            max_age=86400 * 30,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )
        res_res.set_cookie(
            "trang_thai",
            "chua_dang_nhap",
            max_age=86400 * 30,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )
        return res_res, 401
