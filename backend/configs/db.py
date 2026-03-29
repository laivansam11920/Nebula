import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)


def get_database():
    uri = os.getenv("MONGO_URI")
    if not uri:
        logger.warring("system: not found file .env",duong_dan_hien_tai())
        return None
    try:
        client = MongoClient(uri)
        client.admin.command("ping")
        db_admin = client["myDatabase"]
        return db_admin
    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())


db = get_database()

if db is not None:
    try:
        db["users"].drop_index("key_1")
        logger.log("Đã xóa Index lỗi 'key_1' thành công!", duong_dan_hien_tai())
    except Exception as e:
        pass
