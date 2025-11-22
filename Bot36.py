import os
import requests
from flask import Flask, request
import threading
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("Variable d'environnement TELEGRAM_TOKEN manquante !")

app = Flask(__name__)

# --- Menu principal avec boutons ---
def send_main_menu(chat_id):
    menu = {
        "inline_keyboard": [
            [
                {
                    "text": "📱 Mini-App",
                    "web_app": {"url": "https://clope36.42web.io"}
                },
                {
                    "text": "📞 Contact",
                    "callback_data": "contact"
                }
            ]
        ]
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
        else:
            reply = f"Message reçu : {text}"
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={reply}")
            print(f"Message reçu : {text} → {reply}")
    elif "callback_query" in update:
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        data = update["callback_query"]["data"]
        if data == "contact":
            reply = "📞 Contact de la team : @TeamSupport"
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={reply}")
            print(f"Callback reçu : {data} → {reply}")
    return "OK", 200

# --- Serveur Flask ---
@app.route("/")
def index():
    return "Bot Telegram en ligne ✅"

# --- Polling (secours) ---
def telegram_bot_polling():
    last_update_id = None
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            r = requests.get(url).json()
            if "result" in r:
                for update in r["result"]:
                    update_id = update["update_id"]
                    if last_update_id != update_id:
                        webhook_processing(update)
                        last_update_id = update_id
        except Exception as e:
            print("Erreur polling:", e)
        time.sleep(1)

def webhook_processing(update):
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        if text == "/start":
            send_main_menu(chat_id)
        else:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": f"Message reçu : {text}"}
            )
    elif "callback_query" in update:
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        data = update["callback_query"]["data"]
        if data == "contact":
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": "📞 Contact de la team : @TeamSupport"}
            )

# Lance le polling dans un thread
threading.Thread(target=telegram_bot_polling).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
