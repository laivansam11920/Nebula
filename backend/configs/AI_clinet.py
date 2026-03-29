from google.genai import Client
import os
from configs.duong_dan_thu_muc import duong_dan_hien_tai
from logs import logger
google_api = os.getenv("API_GOOGLE_KEY")

try:
    client = Client(api_key=google_api)
except Exception as e:
    logger.error(f"{e}", duong_dan_hien_tai())
