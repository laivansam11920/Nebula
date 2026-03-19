from playwright.sync_api import sync_playwright


def test_web_online():
    with sync_playwright() as p:
        # 1. Mở trình duyệt
        browser = p.chromium.launch(headless=False, slow_mo=800)
        page = browser.new_page()

        # 2. Đi tới link web (Thay bằng link thật của ông)
        logger("Đang mở trang web...")
        page.goto(
            "https://gemini-dot.github.io/learnpythonsever-sm/frontend/view/group_password/input_pass.html",
            wait_until="networkidle",
        )

        # 3. Kiểm tra xem có đúng trang không trước khi điền
        # Đợi cho đến khi ô #firstname xuất hiện trên màn hình
        try:
            page.wait_for_selector("#firstname", timeout=10000)  # Đợi tối đa 10s
            logger("Đã thấy ô nhập tên, bắt đầu điền...")

            page.fill("#firstname", "Sam")
            page.fill("#lastname", "Lai Van")
            # ... các lệnh fill khác ...

        except Exception as e:
            logger("Lỗi rồi: Không tìm thấy ô nhập liệu. Kiểm tra lại link web nhé!")
            page.screenshot(
                path="error_screen.png"
            )  # Chụp ảnh lại xem lúc đó web hiện gì

        page.wait_for_timeout(3000)
        browser.close()


if __name__ == "__main__":
    test_web_online()
