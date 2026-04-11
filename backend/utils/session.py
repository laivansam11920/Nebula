from flask import session, session
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai
def set_session(**list):
    try:
        session.clear()
        session.permanent = True
        for key, value in list.items():
            session[str(key)] = value
    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
