from flask import session, request, jsonify
from configs.db import db


def get_avatar():
    gmail_user = session.get("user_gmail")
    if not gmail_user:
        return jsonify({"trang_thai": False, "mes": "Chưa đăng nhập!"}), 401

    collection = db["file_info"]

    query = {
        "user_gmail": gmail_user,
        "loai_file": "avatar",
        "trang_thai": {"$ne": "da_xoa"},
    }

    try:
        ket_qua_tim = collection.find_one(query)

        if not ket_qua_tim:
            url_mac_dinh = "https://res.cloudinary.com/dshgtuy8f/image/upload/v1773481136/avatar-facebook-mac-dinh-6_usxs2v.jpg"
            return (
                jsonify(
                    {
                        "trang_thai": True,
                        "url": url_mac_dinh,
                        "mes": "Sử dụng ảnh mặc định",
                    }
                ),
                200,
            )

        return jsonify({"trang_thai": True, "url": ket_qua_tim.get("url")}), 200

    except Exception as e:
        return jsonify({"trang_thai": False, "mes": f"Lỗi hệ thống: {str(e)}"}), 500
