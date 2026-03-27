DEFAULT_EXTEND_TIME = 15  # p
ip_allow = ["127.0.0.1", "192.168.1.121"]
MAX_REQUESTS = 50
PERIOD = 60
GODMODE_COLLECTION = "godmode_admin"
GODMODE_KEY = "private"
OK = "success"  #
csp = {
    "default-src": "'self'",
    "script-src": [
        "'self'",
        "https://accounts.google.com",
        "https://www.gstatic.com",
        "'unsafe-inline'",  # Cần thiết nếu og có viết JS trực tiếp trong HTML
    ],
    "style-src": ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
    "connect-src": [
        "'self'",
        "ws://*",  # Cho phép SocketIO kết nối
        "wss://*",
        "https://vault-storage.me",
        "https://accounts.google.com",
    ],
    "frame-src": ["'self'", "https://accounts.google.com"],
    "img-src": ["'self'", "data:", "https:"],
}
