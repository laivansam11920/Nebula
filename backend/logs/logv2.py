from configs.duong_dan_thu_muc import duong_dan_hien_tai
from datetime import timezone, datetime, timedelta
import inspect
from flask import request
import threading
import os
import uuid
import hashlib
from configs.db import db
import resend
from os import getenv
from pymongo import ReturnDocument

resend.api_key = str(getenv("RESEND_API_KEY"))

mui_gio_vn = timezone(timedelta(hours=7))
bay_gio = datetime.now(mui_gio_vn)
thoi_gian_dep = bay_gio.strftime("%H:%M:%S %d/%m/%Y")


class Log_system:
    
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    def __init__(
        self, main_log, main_error, main_warring, main_info, main_debug, main_CRITICAL
    ):
        self.main_log = main_log
        self.main_error = main_error
        self.main_warring = main_warring
        self.main_info = main_info
        self.main_debug = main_debug
        self.main_critical = main_CRITICAL
        self.mui_gio_vn = timezone(timedelta(hours=7))

    def save_to_file(self, level, line, path_system, mes, time, user):
        log_entry = (
            f"[{time}] [{path_system}:{line}] [{level}] {mes}:[{user}\n]"
        )

        def run_main():
            try:
                thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
                duong_dan_log = os.path.join(thu_muc_hien_tai, "server.log")

                with open(duong_dan_log, "a", encoding="utf-8") as f:
                    f.write(log_entry)
            except Exception as e:
                print(f"{self.RED} Lỗi ghi file log: {e}{self.RESET}")

        threading.Thread(target=run_main).start()

    def get_time(self):
        return datetime.now(self.mui_gio_vn).strftime("%H:%M:%S %d/%m/%Y")

    def get_user(self):
        try:
            user = request.cookies.get("user_gmail")
            ip = request.remote_addr
            method = request.method
            url = request.path
            return f"{user}:{ip} {method}:{url}"
        except:
            return "System"

    def send_email_alert(self, result_from_mongo):
        try:
            email_data = {
                "type": result_from_mongo.get("log_level"),
                "time-first": result_from_mongo.get("time_first"),
                "time-last": result_from_mongo.get("time_last"),
                "count": result_from_mongo.get("count"),
                "id_log": result_from_mongo.get("id"),
                "mes": result_from_mongo.get("mes"),
                "path": result_from_mongo.get("path"),
                "line": result_from_mongo.get("line"),
                "user": result_from_mongo.get("user"),
                "time": result_from_mongo.get("time_last")
            }

            params = {
                "from": "Vault Monitor <system@vault-storage.me>",
                "to": ["samvasang1192011@gmail.com"],
                "subject": f"[{email_data['type']}] New Alert: {email_data['id_log']}",
                "template_id": "system-monitor-report",
                "data": email_data
            }

            resend.Emails.send(params)
            print(f"{self.GREEN} [Resend] Đã bắn mail báo cáo thành công! {self.RESET}")

        except Exception as e:
            print(f"{self.RED} [Resend] Lỗi khi gửi mail: {e} {self.RESET}")

    def save_database(self, level, line, path_system, mes, time, user):
        def run_save():
           
            collection = db["log_error_system"]
            
            raw_id = f"{level}{line}{path_system}{mes}{user}"
            error_id = hashlib.md5(raw_id.encode()).hexdigest()[:10]

            try:
                result = collection.find_one_and_update(
                    {"id": error_id},
                    {
                        "$inc": {"count": 1},
                        "$set": {
                            "log_level": level,
                            "line": line,
                            "path": path_system,
                            "time_last": time,
                            "user": user,
                            "mes": mes
                        },
                        "$setOnInsert": {"time_first": time}
                    },
                    upsert=True,
                    return_document=ReturnDocument.AFTER
                )
                count = result.get("count")
                if count == 1 or (count > 1 and count % 100 == 0):
                    self.send_email_alert(result) 
                    
            except Exception as e:
                print(f"{self.RED} {e}{self.RESET}")

        threading.Thread(target=run_save).start()

    def info(self, messing_info, path_in=None):
        line = inspect.stack()[1][2]
        time = self.get_time()
        user = self.get_user()
        print(
            f"[{time}] [{path_in}:{line}] [{self.main_info}] {messing_info}:[{user}]"
        )
        self.save_to_file(self.main_info, line, path_in, messing_info, time, user)

    def warring(self, messing_warring, path_in=None):
        line = inspect.stack()[1][2]
        user = self.get_user()
        time = self.get_time()
        print(
            f"[{time}] [{path_in}:{line}] [{self.main_warring}] {messing_warring}:[{user}]"
        )
        self.save_database(
            self.main_warring,
            line,
            path_in,
            messing_warring,
            time,
            user,
        )
        self.save_to_file(self.main_warring, line, path_in, messing_warring, time, user)

    def error(self, messing_error, path_in=None):
        line = inspect.stack()[1][2]
        user = self.get_user()
        time = self.get_time()
        print(
           f"[{time}] [{path_in}:{line}] [{self.main_error}] {messing_error}:[{user}]"
        )
        self.save_database(
            self.main_error,
            line,
            path_in,
            messing_error,
            time,
            user,
        )
        self.save_to_file(self.main_error, line, path_in, messing_error, time, user)

    def log(self, messing_log, path_in=None):
        line = inspect.stack()[1][2]
        time = self.get_time()
        user = self.get_user()
        print(
           f"[{time}] [{path_in}:{line}] [{self.main_log}] {messing_log}:[{user}]"
        )
        self.save_to_file(self.main_log, line, path_in, messing_log, time, user)

    def debug(self, messing_debug, path_in=None):
        line = inspect.stack()[1][2]
        time = self.get_time()
        user = self.get_user()
        print(
            f"[{time}] [{path_in}:{line}] [{self.main_debug}] {messing_debug}:[{user}]"
        )
        self.save_to_file(self.main_debug, line, path_in, messing_debug, time, user)

    def critical(self, messing_critical, path_in=None):
        line = inspect.stack()[1][2]
        user = self.get_user()
        time = self.get_time()
        print(
           f"[{time}] [{path_in}:{line}] [{self.main_critical}] {messing_critical}:[{user}]"
        )
        self.save_database(
            self.main_critical,
            line,
            path_in,
            messing_critical,
            time,
            user,
        )
        self.save_to_file(
            self.main_critical, line, path_in, messing_critical, time, user
        )
