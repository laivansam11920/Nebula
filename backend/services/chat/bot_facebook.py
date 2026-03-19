from configs.db import db
from services.chat.chuc_nang.AI_core import ask_gemini
from services.chat.chuc_nang.search_duck import get_realtime_info
from services.chat.chuc_nang.send_mes import (
    send_message,
    send_typing,
    send_button_message,
)
from services.chat.chuc_nang.AI_core import find_relevant_doc
from logs.logger import logger

limits_col = db["user_limits"]


def handle_ai_logic(sender_id, message_text):

    send_typing(sender_id)

    user_data = limits_col.find_one({"sender_id": sender_id})
    history = user_data.get("history", []) if user_data else []

    keywords = ["tin tức", "thời tiết", "giá", "hôm nay", "ngày mấy", "mấy giờ"]
    search_context = ""

    if any(word in message_text.lower() for word in keywords):
        logger.log(f"--- Đang tìm tin tức cho: {message_text} ---")
        search_context = get_realtime_info(message_text)
        message_text = (
            f"(Bối cảnh thực tế: {search_context})\nCâu hỏi khách: {message_text}"
        )

    ai_reply = ask_gemini(message_text, history)

    has_sent = False

    if "||| SHOW_PRICING" in ai_reply:
        clean_msg = ai_reply.replace("||| SHOW_PRICING", "").strip()
        send_message(sender_id, clean_msg)
        send_button_message(sender_id)
        ai_reply = clean_msg
        has_sent = True

    if "||| find_info:" in ai_reply:
        search_query = ai_reply.split("||| find_info:")[1].strip()
        context_doc = find_relevant_doc(search_query)
        final_prompt = f"(Thông tin từ hệ thống: {context_doc})\nDựa vào thông tin trên, trả lời khách: {message_text}"
        ai_reply = ask_gemini(final_prompt, history)

    if not has_sent:
        if ai_reply.startswith("loi"):
            send_message(
                sender_id,
                "Tui đang 'reset' lại não xíu, og nhắn lại câu vừa nãy nha! 🧠",
            )
            logger.warning(f"Bỏ qua lưu vì lỗi API: {ai_reply}", flush=True)
            return
        msg_to_send = (
            ai_reply.split("|||")[0].strip() if "|||" in ai_reply else ai_reply
        )
        send_message(sender_id, msg_to_send)

    limits_col.update_one(
        {"sender_id": sender_id},
        {
            "$push": {
                "history": {
                    "$each": [
                        {"role": "user", "parts": [{"text": message_text}]},
                        {"role": "model", "parts": [{"text": ai_reply}]},
                    ],
                    "$slice": -20,
                }
            }
        },
    )
