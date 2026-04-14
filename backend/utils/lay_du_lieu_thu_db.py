from configs.db import db
from utils.nen_anh_cloudinary import nen_anh_cloudinary_url

def lay_tat_ca_file(user_gmail: str, collection: str, limit=40, skip=0) -> dict:
    collection_can_tim = db[str(collection)]
    user_data = list(
        collection_can_tim.find(
            {
                "user_gmail": user_gmail,
                "trang_thai": {"$ne": "xoa_vinh_vien"},
                "loai_file": {"$ne": "avatar"},
            }
        ).sort([("_id", -1)]).skip(skip).limit(limit)
    )
    if not user_data:
        return {"danh_sach_file": [], "danh_sach_file_da_xoa": []}
    res = {"danh_sach_file": [], "danh_sach_file_da_xoa": []}

    for doc in user_data:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
            doc["id"] = doc["_id"]
        t_thai = str(doc.get("trang_thai"))
        if doc.get("loai_file") == "image":
            link_goc = doc.get("duong_dan_file")
            doc["duong_dan_file_nen"] = nen_anh_cloudinary_url(link_goc)
        else:
             doc["duong_dan_file_nen"] = doc.get("duong_dan_file")
        if t_thai == "da_xoa":
            res["danh_sach_file_da_xoa"].append(doc)#
        elif t_thai == "chua_xoa":
            res["danh_sach_file"].append(doc)
    return res
