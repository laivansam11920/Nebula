from flask import request, jsonify
from services.group_mk.create_a_password import kiem_tra_mat_khau


def kiem_tra2():
    dulieu = request.get_json()
    gmail = dulieu.get("gmail", "")
    mat_khau = dulieu.get("password", "")
    nguoi_dung = dulieu.get("username", "")

    ket_qua = kiem_tra_mat_khau(nguoi_dung, gmail, mat_khau)

    code = 201

    bang_ma_loi = {
        "loi_trung_email": 409,
        "loi_luu_tru_database": 500,
        "loi_do_manh_pass": 400,
        "loi_dinh_dang_gmail": 400,
        "thieu_thong_tin": 400,
    }

    if ket_qua.get("status") == "error":
        loi = ket_qua.get("error_type")
        code = bang_ma_loi.get(loi, 400)
        print(f"Lỗi: {loi} - Trả về code: {code}")
    else:
        print("Gửi lên ok! Tạo tài khoản thành công.")

    return jsonify(ket_qua), code
