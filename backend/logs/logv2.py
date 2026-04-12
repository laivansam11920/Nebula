from configs.duong_dan_thu_muc import duong_dan_hien_tai
from datetime import timezone, datetime, timedelta
import inspect
from flask import session, request
import threading
import os
import uuid
import hashlib
import resend
from os import getenv
from pymongo import ReturnDocument
import configs.resend

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
        log_entry = f"[{time}] [{path_system}:{line}] [{level}] {mes}:[{user}\n]"

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
            user = session.get("user_gmail")
            ip = request.remote_addr
            method = request.method
            url = request.path
            return f"{user}:{ip} {method}:{url}"
        except:
            return "System"

    def send_email_alert(self, result_from_mongo):
        try:
            email_data = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Error Report Email</title>
</head>
<body style="margin:0;padding:0;background-color:#f0f0f0;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">

  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f0f0f0;padding:40px 0;">
    <tr>
      <td align="center">

        <!-- Container -->
        <table width="620" cellpadding="0" cellspacing="0" border="0" style="max-width:620px;width:100%;background:#ffffff;border:1px solid #ddd;">

          <!-- HEADER -->
          <tr>
            <td style="background:#111111;padding:28px 36px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td>
                    <span style="font-family:'Courier New',monospace;font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:#999999;">System Monitor</span><br/>
                    <span style="font-family:'Courier New',monospace;font-size:20px;font-weight:700;color:#ffffff;letter-spacing:-0.01em;">{result_from_mongo.get("log_level")} Report</span>
                  </td>
                  <td align="right" valign="middle">
                    <!-- Level Badge — thay giá trị và màu theo level -->
                    <span style="display:inline-block;background:#cc0000;color:#ffffff;font-family:'Courier New',monospace;font-size:11px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:6px 14px;border-radius:2px;">{result_from_mongo.get("log_level")}</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- TIMESTAMP BAR -->
          <tr>
            <td style="background:#1a1a1a;padding:10px 36px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="font-family:'Courier New',monospace;font-size:11px;color:#888888;">
                    <span style="color:#555555;">time_first:</span>&nbsp;
                    <span style="color:#cccccc;">{result_from_mongo.get("time_first")}</span>
                    &nbsp;&nbsp;&nbsp;
                    <span style="color:#555555;">time_last:</span>&nbsp;
                    <span style="color:#cccccc;">{result_from_mongo.get("time_last")}</span>
                  </td>
                  <td align="right" style="font-family:'Courier New',monospace;font-size:11px;color:#888888;">
                    <span style="color:#555555;">occurrences:</span>&nbsp;
                    <span style="color:#ffffff;font-weight:700;">{result_from_mongo.get("count")}</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- BODY -->
          <tr>
            <td style="padding:36px 36px 0 36px;">

              <!-- Error ID -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:24px;">
                <tr>
                  <td style="background:#f7f7f5;border-left:3px solid #111111;padding:14px 18px;">
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:#999999;display:block;margin-bottom:4px;">Error ID</span>
                    <span style="font-family:'Courier New',monospace;font-size:15px;font-weight:700;color:#111111;">{result_from_mongo.get("id")}</span>
                  </td>
                </tr>
              </table>

              <!-- MESSAGE -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:28px;">
                <tr>
                  <td>
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:#999999;display:block;margin-bottom:8px;">Message</span>
                    <div style="background:#111111;color:#f5f5f5;font-family:'Courier New',monospace;font-size:13px;line-height:1.7;padding:18px 20px;border-radius:2px;word-break:break-all;">
                      {result_from_mongo.get("mes")}
                    </div>
                  </td>
                </tr>
              </table>

              <!-- DETAIL GRID -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:28px;">
                <tr>
                  <td>
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:#999999;display:block;margin-bottom:12px;">Detail</span>
                  </td>
                </tr>
              </table>

              <!-- Row 1: path + line -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;margin-bottom:1px;">
                <tr>
                  <td width="50%" style="background:#f7f7f5;border:1px solid #ebebeb;padding:14px 18px;vertical-align:top;">
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#aaaaaa;display:block;margin-bottom:5px;">path</span>
                    <span style="font-family:'Courier New',monospace;font-size:12px;color:#111111;word-break:break-all;">{result_from_mongo.get("path")}</span>
                  </td>
                  <td width="50%" style="background:#f7f7f5;border:1px solid #ebebeb;border-left:none;padding:14px 18px;vertical-align:top;">
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#aaaaaa;display:block;margin-bottom:5px;">line</span>
                    <span style="font-family:'Courier New',monospace;font-size:12px;color:#111111;">{result_from_mongo.get("line")}</span>
                  </td>
                </tr>
              </table>

              <!-- Row 2: user + log_level -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;margin-bottom:1px;">
                <tr>
                  <td width="50%" style="background:#f7f7f5;border:1px solid #ebebeb;border-top:none;padding:14px 18px;vertical-align:top;">
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#aaaaaa;display:block;margin-bottom:5px;">user</span>
                    <span style="font-family:'Courier New',monospace;font-size:12px;color:#111111;">{result_from_mongo.get("user")}</span>
                  </td>
                  <td width="50%" style="background:#f7f7f5;border:1px solid #ebebeb;border-left:none;border-top:none;padding:14px 18px;vertical-align:top;">
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#aaaaaa;display:block;margin-bottom:5px;">log_level</span>
                    <span style="display:inline-block;background:#cc0000;color:#ffffff;font-family:'Courier New',monospace;font-size:10px;font-weight:700;letter-spacing:0.1em;padding:3px 10px;border-radius:2px;">{result_from_mongo.get("log_level")}</span>
                  </td>
                </tr>
              </table>

              <!-- Row 3: time_first + time_last -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;margin-bottom:1px;">
                <tr>
                  <td width="50%" style="background:#f7f7f5;border:1px solid #ebebeb;border-top:none;padding:14px 18px;vertical-align:top;">
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#aaaaaa;display:block;margin-bottom:5px;">time_first <span style="color:#cccccc;font-size:9px;">($setOnInsert)</span></span>
                    <span style="font-family:'Courier New',monospace;font-size:12px;color:#111111;">{result_from_mongo.get("time_first")}</span>
                  </td>
                  <td width="50%" style="background:#f7f7f5;border:1px solid #ebebeb;border-left:none;border-top:none;padding:14px 18px;vertical-align:top;">
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#aaaaaa;display:block;margin-bottom:5px;">time_last <span style="color:#cccccc;font-size:9px;">($set)</span></span>
                    <span style="font-family:'Courier New',monospace;font-size:12px;color:#111111;">{result_from_mongo.get("time_last")}</span>
                  </td>
                </tr>
              </table>

              <!-- Row 4: count -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;margin-bottom:28px;">
                <tr>
                  <td colspan="2" style="background:#f7f7f5;border:1px solid #ebebeb;border-top:none;padding:14px 18px;vertical-align:top;">
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#aaaaaa;display:block;margin-bottom:5px;">count <span style="color:#cccccc;font-size:9px;">($inc +1 mỗi lần xảy ra)</span></span>
                    <span style="font-family:'Courier New',monospace;font-size:18px;font-weight:700;color:#111111;">{result_from_mongo.get("count")}</span>
                    <span style="font-family:'Courier New',monospace;font-size:11px;color:#aaaaaa;margin-left:6px;">occurrences</span>
                  </td>
                </tr>
              </table>

              <!-- MONGODB PAYLOAD -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:36px;">
                <tr>
                  <td>
                    <span style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:#999999;display:block;margin-bottom:8px;">MongoDB Upsert Payload</span>
                    <div style="background:#1a1a1a;font-family:'Courier New',monospace;font-size:11px;line-height:1.8;padding:18px 20px;border-radius:2px;color:#d4d4d4;word-break:break-all;">
<span style="color:#808080;">// filter</span><br/>
{{ <span style="color:#9cdcfe;">"id"</span>: <span style="color:#ce9178;">{result_from_mongo.get("id")}</span> }}<br/>
<br/>
<span style="color:#808080;">// update</span><br/>
{{<br/>  
&nbsp;&nbsp;<span style="color:#dcdcaa;">"$inc"</span>: {{ <span style="color:#9cdcfe;">"count"</span>: <span style="color:#b5cea8;">{result_from_mongo.get("count")}</span> }},<br/>
&nbsp;&nbsp;<span style="color:#dcdcaa;">"$set"</span>: {{<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#9cdcfe;">"log_level"</span>: <span style="color:#ce9178;">{result_from_mongo.get("log_level")}</span>,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#9cdcfe;">"line"</span>: <span style="color:#b5cea8;">{result_from_mongo.get("line")}</span>,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#9cdcfe;">"path"</span>: <span style="color:#ce9178;">{result_from_mongo.get("path")}</span>,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#9cdcfe;">"time_last"</span>: <span style="color:#ce9178;">{result_from_mongo.get("time_last")}</span>,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#9cdcfe;">"user"</span>: <span style="color:#ce9178;">{result_from_mongo.get("user")}</span>,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#9cdcfe;">"mes"</span>: <span style="color:#ce9178;">{result_from_mongo.get("mes")}</span><br/>
&nbsp;&nbsp;}},<br/>
&nbsp;&nbsp;<span style="color:#dcdcaa;">"$setOnInsert"</span>: {{<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#9cdcfe;">"time_first"</span>: <span style="color:#ce9178;">{result_from_mongo.get("time_first")}</span><br/>
&nbsp;&nbsp;}}<br/>
}}<br/>
<br/>
<span style="color:#808080;">// options: upsert=true, return_document=true</span>
                    </div>
                  </td>
                </tr>
              </table>

          <!-- FOOTER -->
          <tr>
            <td style="background:#f7f7f5;border-top:1px solid #ebebeb;padding:20px 36px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="font-family:'Courier New',monospace;font-size:10px;color:#aaaaaa;letter-spacing:0.06em;">
                    Auto-generated by System Monitor &nbsp;·&nbsp; Do not reply to this email
                  </td>
                  <td align="right" style="font-family:'Courier New',monospace;font-size:10px;color:#cccccc;letter-spacing:0.06em;">
                    upsert=True &nbsp;·&nbsp; return_document=True
                  </td>
                </tr>
              </table>
            </td>
          </tr>

        </table>
        <!-- /Container -->

      </td>
    </tr>
  </table>

</body>
</html>
            """

            params = {
                "from": "Vault Monitor <system@vault-storage.me>",
                "to": ["samvasang1192011@gmail.com"],
                "subject": f"[{result_from_mongo.get('log_level')}] New Alert: {result_from_mongo.get('id')}",
                "html": email_data,
            }

            resend.Emails.send(params)
            print(f"{self.GREEN} [Resend] Đã bắn mail báo cáo thành công! {self.RESET}")

        except Exception as e:
            print(f"{self.RED} [Resend] Lỗi khi gửi mail: {e} {self.RESET}")

    def save_database(self, level, line, path_system, mes, time, user):
        def run_save():
            from configs.db import db

            collection = db["log_error_system"]

            raw_id = f"{level}{line}{path_system}{mes}{user}"
            error_id = hashlib.md5(raw_id.encode(), usedforsecurity=False).hexdigest()[:10]

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
                            "mes": mes,
                        },
                        "$setOnInsert": {"time_first": time},
                    },
                    upsert=True,
                    return_document=ReturnDocument.AFTER,
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
        print(f"[{time}] [{path_in}:{line}] [{self.main_info}] {messing_info}:[{user}]")
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
        print(f"[{time}] [{path_in}:{line}] [{self.main_log}] {messing_log}:[{user}]")
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
