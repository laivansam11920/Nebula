from flask import request, jsonify
from services.chat.chuc_nang.bot_web.validate_request_data import validate_request_data
from services.chat.chuc_nang.bot_web.get_user_id import get_user_id
from services.chat.chuc_nang.bot_web.save_message import save_message
from services.chat.chuc_nang.bot_web.generate_ai_res import generate_ai_response
from datetime import datetime


def support_chat():
    try:
        # Get request data
        data = request.get_json()

        # Validate
        is_valid, error_msg = validate_request_data(data)
        if not is_valid:
            return jsonify({"success": False, "error": error_msg}), 400

        # Extract data
        user_message = data.get("message", "").strip()
        files = data.get("files", [])

        # Get user ID
        user_id = get_user_id()

        # Log request
        print(f"[CHAT] User {user_id}: {user_message}")

        # Thêm thông tin về files vào message nếu có
        if files:
            user_message += f"\n\n(User đính kèm {len(files)} file: {', '.join(files)})"

        # Lưu user message
        save_message(user_id, "user", user_message)

        # Generate AI response
        bot_response = generate_ai_response(user_id, user_message)

        # Lưu bot response
        save_message(user_id, "bot", bot_response)

        # Log response
        print(f"[CHAT] Bot: {bot_response[:100]}...")

        # Return response
        return (
            jsonify(
                {
                    "success": True,
                    "message": bot_response,
                    "timestamp": datetime.utcnow().isoformat(),
                    "user_id": user_id,
                }
            ),
            200,
        )

    except Exception as e:
        print(f"[ERROR] Chat endpoint error: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Internal server error",
                    "message": "Xin lỗi, có lỗi xảy ra. Vui lòng thử lại sau.",
                }
            ),
            500,
        )
