import eventlet

eventlet.monkey_patch()  # debug
import newrelic.agent

newrelic.agent.initialize()
from flask import Flask, abort, request, send_from_directory
from flask_cors import CORS
import os
import sys
import io
import sentry_sdk
from flask_socketio import SocketIO, emit
from configs.oauth2_google import oauth
from configs.db import db
from configs.settings import ip_allow
from utils.trang_thai_db_503 import get_maintenance_status
from routes import register_routes
import secrets
from configs.duong_dan_thu_muc import thu_muc_chinh, duong_dan_hien_tai
from __about__ import __title__, __author_email__, __copyright__, __version__, __author__
from logs import logger

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

sentry_sdk.init(
    dsn=str(os.getenv("SENTRY_KEY")),
    send_default_pii=True,
    traces_sample_rate=1.0,
)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

app = Flask(__name__)

app.secret_key = str(os.getenv("SERVER_SECRET_KEY"))

app.config.update(
    SESSION_COOKIE_NAME="google-auth-session",
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="None",
)

CORS(
    app,
    supports_credentials=True,
    origins=[
        "https://gemini-dot.github.io",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://www.vault-storage.me",
        "https://vault-storage.me/",
    ],
)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet",
    engineio_logger=True,
    logger=True,
    always_connect=True,
)

oauth.init_app(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

register_routes(app)


@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory(thu_muc_chinh(), "404.html")


@app.errorhandler(500)
def internal_server_error(e):
    return send_from_directory(thu_muc_chinh("frontend/view/error"), "500.html"), 500


@app.errorhandler(401)
def unauthorized_error(e):
    return send_from_directory(thu_muc_chinh("frontend/view/error"), "401.html"), 401


@app.errorhandler(503)
def service_unavailable_error(e):
    return send_from_directory(thu_muc_chinh("frontend/view/error"), "503.html"), 503

@app.errorhandler(405)
def method_not_allowed(error):
    return send_from_directory(thu_muc_chinh("frontend/view/error"), "405.html"), 405

tim_kiem = db["trang_thai_web"]

admin_pass_on, admin_pass_off = str(os.getenv("BAOTRI_KEY_ON")), str(
    os.getenv("BAOTRI_KEY_OFF")
)


@socketio.on("admin_broadcast")
def handle_broadcast(data):
    logger.log(f"{data['msg']}", duong_dan_hien_tai())
    emit("global_notification", {"message": data["msg"]}, broadcast=True)


@app.before_request
def check_for_maintenance():
    client_ip = request.remote_addr
    IS_MAINTENANCE = get_maintenance_status()
    allowed_routes = ["/unlock-server", "/check-status", "/lock-server"]
    if IS_MAINTENANCE == "website_off" and request.path not in allowed_routes:
        if client_ip in ip_allow:
            return None
        else:
            abort(503)


@app.route("/lock-server")
def lock():
    pw = request.args.get("key", "")
    if admin_pass_on and secrets.compare_digest(pw, admin_pass_on):
        tim_kiem.update_one({"id": "config"}, {"$set": {"status": "website_off"}})
        return "Đã bật chế độ bảo trì!", 200
    return "Sai mật khẩu!", 403


@app.route("/unlock-server")
def unlock():
    pw = request.args.get("key", "")
    if admin_pass_off and secrets.compare_digest(pw, admin_pass_off):
        tim_kiem.update_one({"id": "config"}, {"$set": {"status": "website_on"}})
        return "Đã mở cửa server!", 200
    return "Sai mật khẩu!", 403

@app.before_request
def block_bad_bots():
    blacklisted_bots = ["GPTBot", "CCBot", "ClaudeBot", "Bytespider"]
    
    user_agent = request.headers.get('User-Agent', '')
    
    if any(bot in user_agent for bot in blacklisted_bots):
        abort(403)

@app.route("/")
def home():
    thu_muc = thu_muc_chinh()
    try:
        return send_from_directory(thu_muc, "index.html")
    except Exception as e:
        logger.error(f"{e}",duong_dan_hien_tai())
        return f"Lỗi rách việc rồi og ơi, thư mục này không tồn tại: {e}",401


port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    try:
        db.command("ping")
        socketio.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        logger.critical(f"{e}",duong_dan_hien_tai())

# hỡi người anh em
# nếu bro gặp lỗi và đang cố gắng fix lỗi(90% là vậy)
# thì xin lỗi...
# chỉ có chúa với tui là hiểu nó chạy thế nào
# và giờ chỉ còn chúa thôi
