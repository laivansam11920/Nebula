from configs.db import db
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

def tim_only(collection, find_name, variable, find_item):
    try:
        collection_find = db[str(collection)]
        user = collection_find.find_one({str(find_name): str(variable)})
        if not user:
            return {"user not found"}
        res = user.get(str(find_item))
        return res
    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
        return None
