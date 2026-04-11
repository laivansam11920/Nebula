from flask import session, Blueprint
from configs.oauth2_google import oauth
from controllers.group_password.oauth2_google.sed_data import kiem_tra_goole

app_route20 = Blueprint("receiver", __name__)


@app_route20.route("/google")
def google_login():
    google = oauth.create_client("google")
    google.authorize_access_token()
    user_info = google.get("https://openidconnect.googleapis.com/v1/userinfo").json()
    return kiem_tra_goole(user_info)
