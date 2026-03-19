import requests

# URL này phải khớp với cái @app_route2 của og trong ảnh
BASE_URL_CREATE = "http://localhost:5000/auth/create-a-pass"


def test_full_signup_flow():
    import random

    # Tạo email ngẫu nhiên để không bị lỗi trùng khi test nhiều lần
    test_email = f"user_{random.randint(1, 9999)}@gmail.com"

    payload = {
        "username": "Hacker Lớp 9",
        "gmail": test_email,
        "password": "SecurePass123!",
    }

    response = requests.post("http://localhost:5000/auth/create-a-pass", json=payload)
    assert response.status_code == 201
    logger(f"\n✅ Đăng ký thành công email: {test_email}")
