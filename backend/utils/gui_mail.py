import requests
from utils.tinh_thoi_gian import thoi_gian_tuong_doi
from datetime import datetime
from utils.kiem_tra_thong_tin import lam_dep_thiet_bi


def gui_mail_reset(email_nguoi_nhan, token, thoi_gian, dia_chi_ip, thiet_bi):

    service_id = "service_xszjius"
    template_id = "template_rahi05h"
    public_key = "Z2nHUm0dY8tFSWlaB"
    pivate_key = "vFQ1PfWU2tFXj7Iq7p1Rk"

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
        response = requests.post(url, json=data)

        print(f"EmailJS Response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            print(f"Gửi mail cho {email_nguoi_nhan} thành công rồi og ơi! 🎉")
            return {"success": True}
        else:
            print(f"EmailJS báo lỗi: {response.text}")
            return {"success": False, "error": response.text}
    except Exception as e:
        print(f"Có lỗi bất ngờ rồi og ơi: {e}")
        return {"success": False, "error": str(e)}
