from google.genai import Client
import os
from logs.logger import logger

google_api = os.getenv("API_GOOGLE_KEY")

try:
    client = Client(api_key=google_api)
except Exception as e:
    logger.error(e)
