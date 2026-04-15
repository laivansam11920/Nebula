from configs.db import db

tim_kiem = db["trang_thai_web"]


def get_maintenance_status():
    data = tim_kiem.find_one({"id": "config"}, {"_id": 0, "status": 1})
    if not data:
        tim_kiem.insert_one(
            {"id": "config", "status": "website_on", "status_admin": "allways_on"}
        )
        return "website_on"
    return data["status"]
