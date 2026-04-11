from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai
import configs.resend
import resend
def send_mail(user_gmail, file, time, location, level):
    try:
        email_data = f"""pass"""

        params = {
            "from": "Vault Monitor <system@vault-storage.me>",
            "to": [str(user_gmail)],
            "subject": f"[{level}] File bạn upload lên Vault có nghi ngờ chứa mã độc!!!",
            "html":email_data
        }
        resend.Emails.send(params)
    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())