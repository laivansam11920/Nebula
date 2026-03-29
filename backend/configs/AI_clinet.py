from google.genai import Client
import os

google_api = os.getenv("API_GOOGLE_KEY")

try:
    client = Client(api_key=google_api)
except Exception as e:
    logger.log(e)
