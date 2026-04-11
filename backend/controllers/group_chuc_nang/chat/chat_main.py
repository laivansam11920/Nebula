from flask import session, request
import time
import threading
from configs.db import db
from services.chat.chuc_nang.send_mes import send_message
from services.chat.bot_facebook import handle_ai_logic

limits_col = db["user_limits"]

processed_mids = {}


def receive_message():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"].get("text")
                    mid = messaging_event["message"].get("mid")

                    current_time = time.time()

                    mids_to_delete = [
                        k for k, v in processed_mids.items() if current_time - v > 300
                    ]
                    for k in mids_to_delete:
                        del processed_mids[k]

                    if mid in processed_mids:
                        return "ok", 200

                    processed_mids[mid] = current_time

                    if not message_text:
                        send_message(
                            sender_id, "thử gửi lại mà không dùng icon đi bạn:)"
                        )  # Trường hợp khách gửi ảnh/sticker
                        continue

                    user_data = limits_col.find_one({"sender_id": sender_id})

                    if not user_data:
                        new_user = {
                            "sender_id": sender_id,
                            "count": 1,
                            "reset_time": current_time + 86400,
                        }
                        limits_col.insert_one(new_user)
                    else:
                        if current_time > user_data["reset_time"]:
                            limits_col.update_one(
                                {"sender_id": sender_id},
                                {
                                    "$set": {
                                        "count": 1,
                                        "reset_time": current_time + 86400,
                                    }
                                },
                            )
                        else:
                            if user_data["count"] >= 20:
                                send_message(
                                    sender_id,
                                    "Câu hỏi của bạn sẽ được chúng tôi hỗ trợ sớm nhất có thể!",
                                )
                                return "ok", 200
                            limits_col.update_one(
                                {"sender_id": sender_id}, {"$inc": {"count": 1}}
                            )
                    thread = threading.Thread(
                        target=handle_ai_logic, args=(sender_id, message_text, mid)
                    )
                    thread.start()

    return "ok", 200
