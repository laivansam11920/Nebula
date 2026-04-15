import eventlet

eventlet.monkey_patch()
import newrelic.agent

newrelic.agent.initialize()
from flask import session, Flask, abort, request, send_from_directory
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
from whitenoise import WhiteNoise
import secrets
from configs.duong_dan_thu_muc import thu_muc_chinh, duong_dan_hien_tai
from __about__ import (
    __title__,
    __author_email__,
    __copyright__,
    __version__,
    __author__,
)
from logs import logger
from routes.render_subdomain import render_subdomain
from flask_session import Session
import redis

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

sentry_sdk.init(
    dsn=str(os.getenv("SENTRY_KEY")),
    send_default_pii=True,
    traces_sample_rate=1.0,
)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

app = Flask(__name__)

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BACKEND_DIR), 'frontend')

app.wsgi_app = WhiteNoise(app.wsgi_app, root=FRONTEND_DIR, prefix='frontend/')

app.secret_key = str(os.getenv("SERVER_SECRET_KEY"))

app.config.update(
    SESSION_COOKIE_DOMAIN=".vault-storage.me",
    SESSION_COOKIE_NAME="vault-storage-session",
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_PATH="/",
)

CORS(
    app,
    supports_credentials=True,
    origins=[
        "https://gemini-dot.github.io",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://www.vault-storage.me",
        "https://vault-storage.me",
        "https://dashboard.vault-storage.me",
        "https://api.vault-storage.me",
    ],
)

redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet",
    engineio_logger=True,
    logger=True,
    always_connect=True,
    message_queue=redis_url
)

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True 
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url(redis_url)

Session(app)

oauth.init_app(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

register_routes(app)

duong_dan_file = duong_dan_hien_tai()


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
    logger.log(f"{data['msg']}", duong_dan_file)
    emit("global_notification", {"message": data["msg"]}, broadcast=True)


last_check_time = 0
cached_maintenance_status = None

@app.before_request
def check_for_maintenance():
    global last_check_time, cached_maintenance_status
    import time
    current_time = time.time()
    client_ip = request.remote_addr
    if cached_maintenance_status is None or (current_time - last_check_time > 10):
        try:
            new_status = get_maintenance_status()
            if new_status:
                cached_maintenance_status = new_status
                last_check_time = current_time
        except Exception as e:
            logger.error(f"{e}", duong_dan_file)
    allowed_routes = ["/unlock-server", "/check-status", "/lock-server"]
    if cached_maintenance_status == "website_off" and request.path not in allowed_routes:
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

    user_agent = request.headers.get("User-Agent", "")

    if any(bot in user_agent for bot in blacklisted_bots):
        abort(403)


@app.route("/")
def home():
    try:
        res = render_subdomain()

        if res:
            return res

        thu_muc = thu_muc_chinh()
        return send_from_directory(thu_muc, "trang_chu.html")
    except Exception as e:
        logger.error(f"{e}", duong_dan_file)
        return f"Lỗi rách việc rồi og ơi, thư mục này không tồn tại: {e}", 404


port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    try:
        db.command("ping")
        socketio.run(app, host="0.0.0.0", port=port, threaded=True)
    except Exception as e:
        logger.critical(f"{e}", duong_dan_file)
