from utils.gui_mail import gui_mail_reset
from configs.db import db
from utils.make_token import tao_token_10_so
from time import time
from flask import session, request
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai
from utils.session import set_session


def kiem_tra_dat_lai_mat_khau(gmail):

    cho_luu_token = db["token"]
    user = db["users"]

    kiem_tra_ton_tai = user.find_one({"gmail": str(gmail)})

    if kiem_tra_ton_tai is None:
        return {
            "success": False,
            "error": "Người dùng không tồn tại.",
            "type": "not_exist",
        }
    else:
        tao_token = tao_token_10_so()
        thoi_gian_tao = int(time())

        dieu_kien = {"gmail": gmail}

        noi_dung_thay_doi = {
            "$set": {
                "token_nguoi_dung": tao_token,
                "thoi_gian_tao": thoi_gian_tao,
                "thoi_gian_het_han": thoi_gian_tao
                + 15 * 60,  # Token hết hạn sau 15 phút
                "trang_thai1": "chua_su_dung",
                "trang_thai2": "chua_het_han",
            }
        }

        set_session(gmail=gmail, token=tao_token)

        cho_luu_token.update_one(dieu_kien, noi_dung_thay_doi, upsert=True)

        ip_nguoi_dung = request.remote_addr
        user_agent = request.headers.get("User-Agent")

        ket_qua = gui_mail_reset(
            gmail, tao_token, thoi_gian_tao, ip_nguoi_dung, user_agent
        )

        if isinstance(ket_qua, dict) and ket_qua.get("success"):
            return {
                "success": True,
                "message": "Đã gửi email thành công! Vui lòng kiểm tra hộp thư.",
            }
        else:
            logger.error(
                f"Lỗi gửi email: {ket_qua.get('error', 'Không rõ lỗi')}",
                duong_dan_hien_tai(),
            )
            return {
                "success": False,
                "error": ket_qua.get("error", "Đã có lỗi xảy ra khi gửi email."),
                "type": "send_fail",
            }
