import requests
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai
PAGE_ACCESS_TOKEN = "EAAWQ4rWjGfoBQ6LqxaZAR643TLZBUQQCsQrkNQe0RZChhuVM9LfC6IoZB3rDKw8z75ZBm0NKM9jMnCxBWerZAolmnv7uJZAu9beVSTZBpf88nqy24NvVi4QJ54ZAgM6bEjGRcV2Ee9v7cMNUZAEC66S9idXwjddfyBOcloQOZCB0TSjnxUKT0ijH3nGHKZC6ZAjR0GQ8Gum6iPwZDZD"


def send_typing(recipient_id):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    payload = {"recipient": {"id": recipient_id}, "sender_action": "typing_on"}
    requests.post(url, params=params, json=payload)


def send_message(recipient_id, text, reply_to_mid=None):
    url = "https://graph.facebook.com/v12.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    message_data = {"text": text}
    payload = {"recipient": {"id": recipient_id}, "message": message_data}
    response=requests.post(url, params=params, json=payload)


def send_button_message(recipient_id):
    url = "https://graph.facebook.com/v12.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}

    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Og muốn tìm hiểu về gói nào của VAULT? :)",
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://www.vault-storage.me/frontend/view/buy_package/index.html",
                            "title": "Xem Bảng Giá",
                        },
                        {
                            "type": "postback",
                            "title": "Hỗ trợ kỹ thuật",
                            "payload": "SUPPORT_PAYLOAD",
                        },
                    ],
                },
            }
        },
    }
    requests.post(url, params=params, json=payload)
