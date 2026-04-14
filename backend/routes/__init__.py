# import file nội bộ
from configs.duong_dan_thu_muc import duong_dan_hien_tai
from routes.group_password.input_pass import login_route
from routes.group_password.create_a_password import signup_route
from routes.group_password.forgot_password.forgot_password import findpassword_route
from routes.group_password.forgot_password.forgot_pass2 import findpassword_route_2
from routes.group_password.forgot_password.forgot_password3 import findpassword_route_3
from routes.check_test.cookie import check_status_auth_cookie
from routes.group_chuc_nang.kiem_tra_dang_nhap.upload_fist_login import app_route7
from routes.group_chuc_nang.upload.upload_main import app_route8
from routes.group_chuc_nang.upload.chuc_nang.lay_file import app_route9
from routes.group_chuc_nang.upload.chuc_nang.get_profile_name import app_route10
from routes.group_chuc_nang.upload.chuc_nang.get_profile_power import app_route11
from routes.group_chuc_nang.upload.chuc_nang.delete_file import app_route12
from routes.group_chuc_nang.upload.chuc_nang.restore_file import app_route13
from routes.group_chuc_nang.upload.chuc_nang.permanentDelete import app_route14
from routes.scan_malware.scan_malware_link import app_route15
from routes.group_chuc_nang.upload.setting.bio import app_route16
from routes.group_chuc_nang.upload.setting.get_bio import app_route17
from routes.group_chuc_nang.upload.setting.update_avatar import app_route18
from routes.group_password.oauth2_google.login_frontend import app_route19
from routes.group_password.oauth2_google.sed_data import app_route20
from routes.group_password.oauth2_google.verify_uid import app_route21
from routes.group_chuc_nang.facebook_rep_bot.dieu_huong import app_route22
from routes.group_chuc_nang.upload.chuc_nang.rep_bot import app_route23
from routes.group_chuc_nang.upload.chuc_nang.log_download import app_route24
from routes.group_chuc_nang.upload.chuc_nang.lock_file import app_route25
from routes.group_chuc_nang.upload.chuc_nang.log_share_14031432026 import app_route26
from routes.group_chuc_nang.upload.chuc_nang.logout import app_route27
from routes.group_chuc_nang.upload.chuc_nang.get_avatar import app_route28
from routes.group_chuc_nang.upload.chuc_nang.check_storage import check_storage
from routes.ping.ping import khoi_dong
from routes.group_admin.group_chuc_nang.kill_switch import lenh_tu_huy
from routes.group_password.chuyen_huong.login import login
from routes.group_password.chuyen_huong.signup import signup
from routes.group_password.chuyen_huong.reset_password.send_mail import (
    send_mail_reset_password,
)
from routes.group_password.chuyen_huong.reset_password.repass import (
    send_mail_reset_password_main,
)
from routes.group_chuc_nang.upload.chuyen_huong.dashboard import user_dashboard
from routes.chuyen_huong.error.e401 import e401
from routes.chuyen_huong.error.e403 import e403
from routes.chuyen_huong.error.e500 import e500
from routes.chuyen_huong.error.e503 import e503
from routes.chuyen_huong.dieukhoan_dichvu.dieukhoandichvu import privacy_policy
from routes.group_chuc_nang.upload.chuyen_huong.upload_site import user_upload_site
from routes.chuyen_huong.robot.robot import robot_site
from routes.chuyen_huong.robot.sitemap import sitemap_site
from routes.group_chuc_nang.upload.chuc_nang.show_html_domain import show_html_domain
from routes.check_test.dash_board import dash_board

blueprint_groups = {
    "/auth": [
        login_route,  # tiến trình 1
        signup_route,
        findpassword_route_2,
        findpassword_route,
        findpassword_route_3,
        check_status_auth_cookie,
        app_route19,
        app_route20,
        app_route21,
        app_route27,
        login,
        signup,
        send_mail_reset_password,
        send_mail_reset_password_main,
    ],
    "/profile": [
        app_route10,
        app_route11,
        app_route12,
        app_route13,
        app_route14,
        app_route16,
        app_route17,
        app_route18,
        app_route28,
    ],
    "/security": [app_route7, app_route15, app_route25],
    "/upload_sv": [app_route8, app_route9, app_route24, app_route26, check_storage],
    "/ping": [khoi_dong],
    "/admin": [lenh_tu_huy],
    "/fac": [app_route22],
    "/api": [app_route23],
    "": [
        user_dashboard,
        e401,
        e403,
        e500,
        e503,
        privacy_policy,
        robot_site,
        sitemap_site,
        show_html_domain,
    ],
    "/app": [user_upload_site],
    '/test': [dash_board],
}


def register_routes(app):
    try:
        for prefix, blueprints in blueprint_groups.items():
            if not isinstance(blueprints, list):
                blueprints = [blueprints]

            for bp in blueprints:
                if prefix == "":
                    app.register_blueprint(bp)
                else:
                    app.register_blueprint(bp, url_prefix=prefix)
        print("[SUCCESS]: Đã đăng ký toàn bộ route thành công! :)")
    except Exception as e:
        print(f"[ERROR] Lỗi khi đăng ký Blueprint: {e}")
