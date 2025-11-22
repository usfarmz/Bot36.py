import requests
import time
import os

TOKEN = os.environ.get("8532082529:AAG76DFBL3V9JYcdTHd5XbgReDhuBCOalbEc")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

OFFSET = 0

def get_updates(offset):
    url = BASE_URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    resp = requests.get(url, params=params)
    return resp.json()

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

while True:
    updates = get_updates(OFFSET)
    for update in updates.get("result", []):
        OFFSET = update["update_id"] + 1
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text")
        if text:
            if text == "/start":
                send_message(chat_id, "Bienvenue Kevin 😎 Ton bot Python fonctionne sur Render !")
            else:
                send_message(chat_id, f"Tu as dit : {text}")
    time.sleep(1)
