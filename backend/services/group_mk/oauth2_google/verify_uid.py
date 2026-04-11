from configs.db import db
import hmac


def verify_uid(user_gmail, uid):
    collection = db["users"]
    user = collection.find_one({"gmail": user_gmail}, {"gmail": 1, "_id": 0})
    if not user:
        return {"trang_thai": False, "mes": "khong tin thay nguoi dung"}
    uid_db = str(user.get("uid"))
    if hmac.compare_digest(str(uid), uid_db):
        collection.update_one({"gmail": user_gmail}, {"$set": {"uid": "0"}})
        return {"trang_thai": True, "mes": "dang nhap thanh cong"}
    return {"trang_thai": False, "mes": "sai uid roi kia"}
