import re
from google.genai import types
from configs.AI_clinet import client
import psutil

from RestrictedPython import compile_restricted, safe_builtins
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Guards import full_write_guard
from RestrictedPython.Eval import (
    default_guarded_getitem,
    default_guarded_getiter,
)  # Đã thêm getiter


# --- TRẠM KIỂM SOÁT THƯ VIỆN ---
def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    allowed_modules = ["math", "datetime", "time", "json", "psutil", "random"]
    if name in allowed_modules:
        return __import__(name, globals, locals, fromlist, level)
    raise ImportError(f"Cảnh báo: Không được phép import module '{name}'!")


# 1. HÀM SANDBOX
def run_ai_code_safely(code):
    my_builtins = safe_builtins.copy()
    my_builtins["__import__"] = safe_import

    safe_globals = {"__builtins__": my_builtins}
    safe_globals["_logger.log_"] = PrintCollector
    safe_globals["_write_"] = full_write_guard
    safe_globals["_getattr_"] = getattr
    safe_globals["_getitem_"] = default_guarded_getitem
    # Vá lỗi vòng lặp for ở đây nè og
    safe_globals["_getiter_"] = default_guarded_getiter

    local_scope = {}
    try:
        byte_code = compile_restricted(code, filename="<string>", mode="exec")
        exec(byte_code, safe_globals, local_scope)

        if "result" in local_scope:
            return str(local_scope["result"])
        else:
            return "Code chạy xong nhưng AI quên gán biến 'result'."
    except Exception as e:
        return f"Lỗi chạy code bên trong Sandbox: {str(e)}"


# 2. HÀM GỌI AI THẬT
def ask_gemini_for_sandbox(system_instruction, user_text, doan_chat_truoc):
    logger.log("\n[Hệ thống] Đang gọi Gemma-3-27b-it...")
    try:
        if doan_chat_truoc is None:
            doan_chat_truoc = []

        clean_history = []
        for chat in doan_chat_truoc:
            role = chat.get("role")
            parts = chat.get("parts", [])
            if parts and isinstance(parts, list):
                t = (
                    parts[0].get("text", "")
                    if isinstance(parts[0], dict)
                    else str(parts[0])
                )
                if t and not t.startswith("loi"):
                    clean_history.append({"role": role, "parts": [{"text": t}]})

        instruction_msg = {
            "role": "user",
            "parts": [{"text": f"SYSTEM INSTRUCTION: {system_instruction}"}],
        }
        current_message = {"role": "user", "parts": [{"text": user_text}]}
        all_contents = [instruction_msg] + clean_history + [current_message]

        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=all_contents,
            config=types.GenerateContentConfig(
                temperature=0.4
            ),  # Tăng xíu nhiệt độ để nó nch tự nhiên hơn
        )
        if response and response.text:
            return response.text.strip()
        return "Tui chưa nghĩ ra câu trả lời, og thử lại sau nha! :)"
    except Exception as e:
        return f"loi{e}"


# 3. LOGIC XỬ LÝ CHÍNH ĐÃ THÔNG MINH HƠN
def handle_ai_code_generation(message_text, history):
    logger.log(f"\n--- KHÁCH NHẮN: {message_text} ---")

    # CÔNG THỨC MỚI: AI tự đánh giá xem có cần viết code không
    system_prompt_smart = (
        "Bạn là trợ lý Vault-Sm hóm hỉnh, luôn dùng icon :) . "
        "LUẬT XỬ LÝ QUAN TRỌNG NHẤT:\n"
        "1. NẾU người dùng CHỈ giao tiếp bình thường (hỏi thăm, tán gẫu, hỏi 'thấy vui không', v.v.), hãy trả lời trực tiếp một cách tự nhiên và KẾT THÚC. TUYỆT ĐỐI KHÔNG VIẾT CODE.\n"
        "2. CHỈ KHI người dùng yêu cầu tính toán toán học, xem ngày giờ, hoặc lấy thông tin hệ thống máy tính, bạn MỚI viết code Python.\n"
        "3. NẾU BẮT BUỘC PHẢI VIẾT CODE: Đặt code trong thẻ ```python. Gán kết quả v��o biến 'result'. KHÔNG dùng logger.log(), KHÔNG import thư viện lạ."
    )

    ai_reply = ask_gemini_for_sandbox(system_prompt_smart, message_text, history)
    code_match = re.search(r"```python\n(.*?)\n```", ai_reply, re.DOTALL)

    # Nếu nó có viết code (Trường hợp B)
    if code_match:
        ai_code = code_match.group(1).strip()
        logger.log(f"\n[1. CODE GEMMA TỰ VIẾT RA]:\n{ai_code}")

        execution_result = run_ai_code_safely(ai_code)
        logger.log(f"\n[2. KẾT QUẢ CHẠY TRÊN UBUNTU]: {execution_result}")

        system_prompt_answer = "Bạn là trợ lý Vault-Sm. Trả lời kết quả tính toán cho khách thật ngắn gọn và thân thiện, dùng icon :)"
        final_answer_prompt = f"Yêu cầu ban đầu: {message_text}. Kết quả tính toán là: {execution_result}. Hãy báo cho khách."

        final_reply = ask_gemini_for_sandbox(
            system_prompt_answer, final_answer_prompt, history
        )
        return final_reply

    # Nếu nó KHÔNG viết code (Trường hợp A - Tán gẫu)
    else:
        logger.log("\n[Hệ thống]: Chế độ tán gẫu. Không cần chạy Sandbox.")
        return ai_reply


# 4. CHẠY TEST
if __name__ == "__main__":
    logger.log("=== BẮT ĐẦU TEST VỚI GEMINI THẬT ===")

    # Test thử câu nói chuyện bình thường
    cau_hoi = "ê thấy vui không?"
    lich_su = []

    cau_tra_loi = handle_ai_code_generation(cau_hoi, lich_su)
    logger.log(f"\n[3. GEMMA TRẢ LỜI KHÁCH]:\n{cau_tra_loi}")
    logger.log("\n=== KẾT THÚC TEST ===")
