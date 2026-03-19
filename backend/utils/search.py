from configs.db import db
from logs.logger import logger

def tim_only(collection, find_name, variable, find_item):
    try:
        collection_find = db[str(collection)]
        user = collection_find.find_one({str(find_name): str(variable)})
        if not user:
            return {"user not found"}
        res = user.get(str(find_item))
        return res
    except Exception as e:
        logger.error(f"Lỗi ADMIN-ROOT ơi: {e}")
        return None
