import requests
from os import getenv

PAGE_ACCESS_TOKEN = str(getenv("PAGE_ACCESS_TOKEN"))


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
    response = requests.post(url, params=params, json=payload)


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
