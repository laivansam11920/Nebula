from services.group_mk.oauth2_google.verify_google import kiem_tra_db
from flask import session, redirect
import uuid


def kiem_tra_goole(dulieu):
    email = dulieu.get("email")
    full_name = dulieu.get("name")
    avatar = dulieu.get("picture")
    dulieu.get("sub")
    sid = str(uuid.uuid4())
    ket_qua = kiem_tra_db(full_name, email, avatar, sid)
    if ket_qua.get("trang_thai") == True:
        return redirect(f"https://vault-storage.me/auth/login?sid={sid}&gmail={email}")

    return redirect("https://vault-storage.me/500")
