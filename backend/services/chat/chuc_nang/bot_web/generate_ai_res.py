from services.chat.chuc_nang.bot_web.buid_chat_context import build_chat_context
from google.genai import types
from configs.AI_clinet import client
from services.chat.chuc_nang.bot_web.get_fallback_res import get_fallback_response
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

def generate_ai_response(user_id, user_message):
    try:
        full_prompt = build_chat_context(user_id, user_message)

        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=full_prompt,
            config=types.GenerateContentConfig(temperature=0.7),
        )

        bot_response = response.text.strip()

        return bot_response

    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
        return get_fallback_response(user_message)
