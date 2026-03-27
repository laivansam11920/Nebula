from configs.db import db


def tim_only(collection, find_name, variable, find_item):
    try:
        collection_find = db[str(collection)]
        user = collection_find.find_one({str(find_name): str(variable)})
        if not user:
            return {"user not found"}
        res = user.get(str(find_item))
        return res
    except Exception as e:
        print(f"Lỗi ADMIN-ROOT ơi: {e}")
        return None
