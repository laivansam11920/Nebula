from flask import make_response, jsonify, request
from configs.db import db


def logout():
    res = make_response(
        jsonify({"success": True, "message": "Đã đăng xuất thành công!"})
    )

    usergmail = request.cookies.get("user_gmail")

    collection = db["users"]

    cookie_keys = [
        "user_token",
        "user_gmail",
        "role",
        "lenh_thuc_thi",
        "trang_thai",
        "ten_nguoi_dung",
    ]

    for key in cookie_keys:
        res.set_cookie(
            key,
            "",
            max_age=0,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
        )

    user = collection.update_one(
        {"gmail": usergmail}, {"$set": {"trang_thai": "chua_dang_nhap"}}
    )

    return res, 200
