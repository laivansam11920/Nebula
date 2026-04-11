from flask import session, Blueprint, url_for
from configs.oauth2_google import oauth

app_route19 = Blueprint("dang-nhap-bang-google", __name__)


@app_route19.route("/login_google")
def login():
    google = oauth.create_client("google")
    redirect_uri = url_for("receiver.google_login", _external=True)
    return google.authorize_redirect(redirect_uri)
