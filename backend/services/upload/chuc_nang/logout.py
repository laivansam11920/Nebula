from flask import session, make_response, jsonify
from configs.db import db


def logout():
    res = make_response(
        jsonify({"success": True, "message": "Đã đăng xuất thành công!"})
    )

    usergmail = session.get("user_gmail")

    collection = db["users"]

    session.clear()

    user = collection.update_one(
        {"gmail": usergmail}, {"$set": {"trang_thai": "chua_dang_nhap"}}
    )

    return res, 200
