import eventlet

eventlet.monkey_patch()
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
from routes import register_routes
from whitenoise import WhiteNoise
from configs.duong_dan_thu_muc import thu_muc_chinh, duong_dan_hien_tai
from logs import logger
from routes.render_subdomain import render_subdomain
from flask_session import Session
import redis
from flask_compress import Compress
from configs.config_app import Config
from configs.settings import error_codes

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

sentry_sdk.init(
    dsn=str(os.getenv("SENTRY_KEY")),
    send_default_pii=True,
    traces_sample_rate=1.0,
)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

app = Flask(__name__)

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BACKEND_DIR), "frontend")

app.wsgi_app = WhiteNoise(app.wsgi_app, root=FRONTEND_DIR, prefix="frontend/")

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

redis_url_socket = os.environ.get("REDIS_URL", "redis://localhost:6379/1")

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet",
    engineio_logger=True,
    logger=True,
    always_connect=True,
    message_queue=redis_url_socket,
)

app.config.from_object(Config)

Session(app)
Compress(app)

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


def handle_error(e):
    code = getattr(e, "code", 500)

    folder = "frontend/view/error" if code != 404 else ""

    return send_from_directory(thu_muc_chinh(folder), f"{code}.html"), code


for code in error_codes:
    app.register_error_handler(code, handle_error)


@socketio.on("admin_broadcast")
def handle_broadcast(data):
    logger.log(f"{data['msg']}", duong_dan_file)
    emit("global_notification", {"message": data["msg"]}, broadcast=True)


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


if __name__ == "__main__":
    try:
        db.command("ping")
        port = int(os.environ.get("PORT", 8000))
        socketio.run(app, host="0.0.0.0", port=port, threaded=True, debug=True)
    except Exception as e:
        logger.critical(f"{e}", duong_dan_file)
