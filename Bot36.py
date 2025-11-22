import os
import requests
from flask import Flask, request
import threading
import time

# Récupère le token depuis Render Environment Variables
TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("Il manque la variable d'environnement TELEGRAM_TOKEN !")

app = Flask(__name__)

# Envoie un message
def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if keyboard:
        payload["reply_markup"] = keyboard

    requests.post(url, json=payload)

# Crée le clavier avec icônes
def menu_keyboard():
    return {
        "keyboard": [
            [
                {"text": "⚙️ Mini-app"},
                {"text": "📞 Contact"}
            ]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

# Route webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        if text == "/start":
            send_message(chat_id, "Bienvenue à la team 🚀", keyboard=menu_keyboard())
        elif text == "⚙️ Mini-app":
            send_message(chat_id, "Voici la mini-app ⚙️ (bientôt disponible).")
        elif text == "📞 Contact":
            send_message(chat_id, "Contact 📞 : https://t.me/ton_contact")
        else:
            send_message(chat_id, f"Message reçu : {text}")

        print(f"Message reçu : {text}")

    return "OK", 200

# Petit serveur pour Render
@app.route("/")
def index():
    return "Bot Telegram en ligne ✅"

# Fonction de polling
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
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"]["text"]

                        if text == "/start":
                            send_message(chat_id, "Bienvenue à la team 🚀", keyboard=menu_keyboard())
                        else:
                            send_message(chat_id, f"Message reçu : {text}")

                        last_update_id = update_id

        except Exception as e:
            print("Erreur polling :", e)

        time.sleep(1)

# Lance le polling dans un thread
threading.Thread(target=telegram_bot_polling).start()

# Lance Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
