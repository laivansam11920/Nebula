import requests
from utils.tinh_thoi_gian import thoi_gian_tuong_doi
from datetime import datetime
from utils.kiem_tra_thong_tin import lam_dep_thiet_bi
from os import getenv
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai


def gui_mail_reset(email_nguoi_nhan, token, thoi_gian, dia_chi_ip, thiet_bi):

    service_id = str(getenv("SERVICE_ID_EMAILJS"))
    template_id = str(getenv("TEMPLATE_ID_EMAILJS"))
    public_key = str(getenv("PUBLIC_KEY_EMAILJS"))
    pivate_key = str(getenv("PRIVATE_KEY_EMAILJS"))

    link_reset = f"https://vault-storage.me/auth/reset_password?gmail={email_nguoi_nhan}&token={token}"

    try:
        url = "https://api.emailjs.com/api/v1.0/email/send"

        if isinstance(thoi_gian, int):
            thoi_gian_obj = datetime.fromtimestamp(thoi_gian)
            thoi_gian = thoi_gian_tuong_doi(thoi_gian_obj)
        else:
            thoi_gian = thoi_gian_tuong_doi(thoi_gian)

        ket_qua_thiet_bi = lam_dep_thiet_bi(thiet_bi)

        data = {
            "service_id": service_id,
            "template_id": template_id,
            "user_id": public_key,
            "accessToken": pivate_key,
            "template_params": {
                "email": email_nguoi_nhan,
                "LINK_RESET": link_reset,
                "time_now": thoi_gian,
                "ip_user": dia_chi_ip,
                "thiet_bi": ket_qua_thiet_bi,
            },
        }
        #
        response = requests.post(url, json=data, timeout=20)

        if response.status_code == 200:
            logger.log(f"send for {email_nguoi_nhan}!", duong_dan_hien_tai())
            return {"success": True}
        else:
            logger.warring(f"EmailJS error: {response.text}", duong_dan_hien_tai())
            return {"success": False, "error": response.text}
    except Exception as e:
        logger.error(f"error: {e}", duong_dan_hien_tai())
        return {"success": False, "error": str(e)}
