def get_fallback_response(user_message):
    msg = user_message.lower()
    if "upload" in msg:
        return """Để upload file, bạn có thể:
1. Click nút "Upload" ở góc trên bên phải
2. Hoặc kéo thả file trực tiếp vào dashboard

📤 Hỗ trợ mọi định dạng file
💾 Tối đa 2GB/file (gói PRO)."""

    elif "mật khẩu" in msg or "password" in msg:
        return """Để reset mật khẩu:
1. Click "Quên mật khẩu" ở trang đăng nhập
2. Nhập email đã đăng ký
3. Kiểm tra email và làm theo hướng dẫn

📧 Nếu không nhận được email, kiểm tra mục Spam nhé!"""

    elif "nâng cấp" in msg or "upgrade" in msg or "gói" in msg:
        return """VAULT có 3 gói lưu trữ:

🆓 FREE: 2GB, 100MB/file
⭐ PRO: 50GB, 2GB/file - 99.000đ/tháng
💎 PREMIUM: 500GB, 10GB/file - 249.000đ/tháng

Click "Nâng cấp" trong Settings để xem chi tiết!"""

    elif "chia sẻ" in msg or "share" in msg:
        return """Để chia sẻ file:
1. Click vào file muốn chia sẻ
2. Click nút "Chia sẻ" ở panel bên phải
3. Chọn quyền truy cập (View/Edit)
4. Copy link và gửi cho người khác

🔒 Link có thể đặt mật khẩu (gói PREMIUM)"""

    elif "lỗi" in msg or "bug" in msg or "error" in msg:
        return """Rất tiếc về sự cố này! Vui lòng cung cấp:
1. Mô tả lỗi chi tiết
2. Thời gian xảy ra
3. Screenshot (nếu có)

📧 Email: support@vault.com
⏰ Team support sẽ xử lý trong 24h"""

    elif "xin chào" in msg or "hello" in msg or "hi" in msg:
        return "Xin chào! 👋 Tôi có thể giúp gì cho bạn hôm nay?"

    elif "cảm ơn" in msg or "thanks" in msg:
        return "Không có gì! Nếu cần hỗ trợ thêm, cứ nhắn nhé 😊"

    else:
        return """Tôi đã ghi nhận câu hỏi của bạn. Một chuyên viên sẽ phản hồi sớm nhất.

Hoặc bạn có thể:
📧 Email: support@vault.com
📞 Hotline: 1900-xxxx
⏰ 8h - 22h hàng ngày"""
