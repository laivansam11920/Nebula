from configs.db import db
from services.chat.chuc_nang.AI_core import ask_gemini
from services.chat.chuc_nang.search_duck import get_realtime_info
from services.chat.chuc_nang.send_mes import (
    send_message,
    send_typing,
    send_button_message,
)
from services.chat.chuc_nang.AI_core import find_relevant_doc
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai
limits_col = db["user_limits"]


def handle_ai_logic(sender_id, message_text, message_id=None):

    send_typing(sender_id)

    user_data = limits_col.find_one({"sender_id": sender_id})
    history = user_data.get("history", []) if user_data else []
    
    keywords = ["tin tức", "thời tiết", "giá", "hôm nay", "ngày mấy", "mấy giờ"]
    search_context = ""

    if any(word in message_text.lower() for word in keywords):
        logger.log(f"Đang tìm tin tức cho: {message_text}", duong_dan_hien_tai())
        search_context = get_realtime_info(message_text)
        message_text = (
            f"(Bối cảnh thực tế: {search_context})\nCâu hỏi khách: {message_text}"
        )

    prompt_gop = f"{message_text}\n(System Note: Nếu cần trích dẫn lại để làm rõ, hãy bắt đầu câu trả lời bằng chữ [QUOTE])"

    ai_reply = ask_gemini(prompt_gop, history)
    if isinstance(ai_reply, str) and ai_reply.startswith("loi"):
        if "429" in ai_reply or "RESOURCE_EXHAUSTED" in ai_reply:
            send_message(sender_id, "Tui đang nghẹn kẹo (quá tải xíu), og đợi tui khoảng 1 phút rồi nhắn lại nha :)", message_id)
        else:
            send_message(sender_id, "Não tui đang bị lag, og đợi xíu nha :)", message_id)
        
        logger.warring(f"Bỏ qua lưu vì lỗi API: {ai_reply}", duong_dan_hien_tai())
        return
    
    is_quote = False
    if ai_reply.startswith("[QUOTE]"):
        ai_reply = ai_reply.replace("[QUOTE]", "").strip()
        is_quote = True
    mid_to_send = message_id if is_quote else None

    has_sent = False

    if "||| SHOW_PRICING" in ai_reply:
        clean_msg = ai_reply.replace("||| SHOW_PRICING", "").strip()
        send_message(sender_id, clean_msg, reply_to_mid=mid_to_send)
        send_button_message(sender_id)
        ai_reply = clean_msg
        has_sent = True

    if "||| find_info:" in ai_reply:
        parts = ai_reply.split("||| find_info:")
        wait_message = parts[0].strip() 
        search_query = parts[1].strip()  

        send_message(sender_id, wait_message, reply_to_mid=None)

        context_doc = find_relevant_doc(search_query)
        final_prompt = f"(Thông tin từ hệ thống: {context_doc})\nDựa vào thông tin trên, trả lời khách: {message_text}"
        
        final_ai_reply = ask_gemini(final_prompt, history)
        
        if isinstance(final_ai_reply, str) and not final_ai_reply.startswith("loi"):
            send_message(sender_id, final_ai_reply)
            ai_reply = final_ai_reply
        else:
            send_message(sender_id, "Tui đang tra tài liệu thì bị lag xíu, og hỏi lại nha :)")
            
        has_sent = True

    if not has_sent:
        if ai_reply.startswith("loi"):
            send_message(
                sender_id,
                "Tui đang 'reset' lại não xíu, og nhắn lại câu vừa nãy nha!",
            )
            logger.warring(f"Bỏ qua lưu vì lỗi API: {ai_reply}", duong_dan_hien_tai())
            return
        msg_to_send = (
            ai_reply.split("|||")[0].strip() if "|||" in ai_reply else ai_reply
        )
        send_message(sender_id, msg_to_send, reply_to_mid=mid_to_send)

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
