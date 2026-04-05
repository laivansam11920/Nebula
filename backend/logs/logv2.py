from configs.duong_dan_thu_muc import duong_dan_hien_tai
from datetime import timezone, datetime, timedelta
import inspect
from flask import request
import threading
import os
import uuid
import hashlib

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

    def save_database(self, level, line, path_system, mes, time, user):
        def run_save():
            from configs.db import db

            collection = db["log_error_system"]
            try:
                raw_id = f"{level}{line}{path_system}{mes}{user}"

                collection.insert_one(
                    {
                        "log_level": level,
                        "line": line,
                        "path": path_system,
                        "time": time,
                        "user": user,
                        "mes": mes,
                        "id": hashlib.md5(raw_id.encode()).hexdigest()[:10]
                    }
                )
            except Exception as e:
                print(f"{self.RED} {e}")

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
