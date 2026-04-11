from flask import session, Blueprint, render_template, make_response
from datetime import datetime

sitemap_site = Blueprint("sitemap_site", __name__)


@sitemap_site.route("/sitemap.xml")
def sitemap():
    pages = [
        {"loc": "/", "lastmod": datetime.now().strftime("%Y-%m-%d"), "priority": "1.0"},
        {
            "loc": "/app/upload",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "priority": "0.8",
        },
    ]

    sitemap_xml = render_template(
        "sitemap_template.xml", pages=pages, base_url="https://vault-storage.me"
    )

    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response
