from flask import Blueprint, render_template, session
from utils.lay_du_lieu_thu_db import lay_tat_ca_file
from utils.viet_hoa_ten_user import xu_ly_ten_cho_logo
from services.group_chuc_nang.dashboard.get_du_lieu import get_du_lieu_dashboard
from utils.xu_ly_ten_cho_logo import xu_ly_ten_cho_logo, xu_ly_avatar

dash_board = Blueprint('dash_board', __name__)

@dash_board.route('/dash_board_test')

def dash_board_test():

    user_email = session.get("user_gmail", "")

    du_lieu = lay_tat_ca_file(user_email, "file_info")
    user_info = get_du_lieu_dashboard(user_email)
    username = user_info.get('username', 'User')
    user_power = user_info.get('cap_nguoi_dung', 'basic')
    luu_tru_dict = user_info.get('luu_tru') or {}
    storage_plan = luu_tru_dict.get("khong_gian_luu_tru", "128")
    logo_name = xu_ly_ten_cho_logo(username)
    avatar_char = xu_ly_avatar(username)

    return render_template(
        'test.html', 
        username=username, 
        user_email=user_email, 
        quyen_han=user_power, 
        goi_luu_tru=storage_plan, 
        danh_sach_file=du_lieu["danh_sach_file"], 
        danh_sach_file_da_xoa=du_lieu["danh_sach_file_da_xoa"],
        logo_name=logo_name,    
        avatar_char=avatar_char    
    )