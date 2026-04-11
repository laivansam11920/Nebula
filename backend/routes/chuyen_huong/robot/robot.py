from flask import session, Blueprint

robot_site = Blueprint("robot_txt", __name__)


@robot_site.route("/robots.txt")
def robots_txt():
    content = """User-agent: *
        Content-Signal: search=yes,ai-train=no
        Allow: /

        User-agent: GPTBot
        Disallow: /
"""
    return content, 200, {"Content-Type": "text/plain"}
