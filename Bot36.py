import os
import requests
from flask import Flask, request
import threading
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("Variable d'environnement TELEGRAM_TOKEN manquante !")

app = Flask(__name__)

# --- Envoi du menu avec les boutons ---
def send_main_menu(chat_id):
    menu = {
        "keyboard": [
            [
                {"text": "📱 Mini-App", "web_app": {"url": "https://clope36.42web.io"}},
                {"text": "📞 Contact"}
            ]
        ],
        "resize_keyboard": True
    }

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": "Bienvenue dans la team 🔥\nChoisissez une option :",
            "reply_markup": menu
        }
    )

# --- Webhook ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/start":
            send_main_menu(chat_id)
        elif text == "📞 Contact":
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "📞 Contact de la team : @TeamSupport"
                }
            )
        else:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": f"Message reçu : {text}"}
            )

    return "OK", 200

# --- Polling (secours) ---
def polling():
    last = None
    while True:
        try:
            r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()
            if "result" in r:
                for up in r["result"]:
                    if last != up["update_id"]:
                        webhook_processing(up)
                        last = up["update_id"]
        except:
            pass
        time.sleep(1)

def webhook_processing(update):
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        if text == "/start":
            send_main_menu(chat_id)
        elif text == "📞 Contact":
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "📞 Contact de la team : @TeamSupport"
                }
            )
        else:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": f"Message reçu : {text}"}
            )

threading.Thread(target=polling).start()

@app.route("/")
def index():
    return "Bot Telegram en ligne ⚡"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
