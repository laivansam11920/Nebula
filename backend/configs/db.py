import os
from pymongo import MongoClient
from dotenv import load_dotenv
from logs.logger import logger
from pathlib import Path
from logs.logger import logger

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)


def get_database():
    uri = os.getenv("MONGO_URI")
    if not uri:
        logger.error("system: not found file .env")
        return None
    try:
        client = MongoClient(uri)
        client.admin.command("ping")
        db_admin = client["myDatabase"]
        return db_admin
    except Exception as e:
        logger.error(f"system: connet error {e}")


db = get_database()

if db is not None:
    try:
        db["users"].drop_index("key_1")
        logger.log("Đã xóa Index lỗi 'key_1' thành công!")
    except Exception as e:
        pass
