import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("Il manque la variable d'environnement TELEGRAM_TOKEN !")

app = Flask(__name__)

# Fonction pour envoyer un message à Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

# Route webhook que Telegram va appeler
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/start":
            reply = "Bienvenue Kevin 😎 Ton bot fonctionne sur Render !"
        else:
            reply = f"Tu as dit : {text}"

        send_message(chat_id, reply)

    return "ok"

# Page d'accueil pour tester le serveur
@app.route("/")
def index():
    return "Bot Telegram en ligne ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
