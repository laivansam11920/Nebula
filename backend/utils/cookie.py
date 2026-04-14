from datetime import timedelta
from flask import session, make_response, jsonify


def cookie(dict_cookies, so_ngay_toi_da: int, ket_qua_tra_ve: dict) -> any:
    so_ngay = int(timedelta(days=so_ngay_toi_da).total_seconds())
    response = make_response(jsonify(ket_qua_tra_ve))

    for ten, gia_tri in dict_cookies.items():
        response.set_cookie(
            key=ten,
            value=gia_tri,
            max_age=so_ngay,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )

    return response
