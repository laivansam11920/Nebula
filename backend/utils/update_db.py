from configs.db import db
from utils.hash256 import get_sha256_hash


def update_config(thu_muc_goc):
    # 1. Chọn collection
    collection = db[str(thu_muc_goc)]
    
    tim_kiem = collection.find_one({"lenh_thuc_thi_bat_buoc": "admin-root"})

    i = get_sha256_hash("samvasang1192011-0")

    if not tim_kiem:
        schema = {
            "lenh_thuc_thi_bat_buoc": "admin-root",
            "lenh_thuc_thi": "samvasang1192011-0",
        }
        # 3. Dùng insert_one nếu là tạo mới lần đầu
        collection.insert_one(schema)
        return schema
    collection.update_one(
        {"lenh_thuc_thi_bat_buoc": "admin-root"}, {"$set": {"lenh_thuc_thi": i}}
    )
    return tim_kiem


update_config("thuc_thi")
