import os
import requests
from flask import Flask
import threading
import time

TOKEN = os.environ.get("8532082529:AAG76DFBL3V9JYcdTHd5XbgReDhuBCOalbEc")

# Vérifie que le token est présent
if not TOKEN:
    raise ValueError("Il manque la variable d'environnement TELEGRAM_TOKEN !")

# Petit serveur Flask pour Render
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot Telegram en ligne ✅"

# Fonction de polling Telegram
def telegram_bot():
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
                            reply = "Bienvenue Kevin 😎 Ton bot fonctionne sur Render !"
                        else:
                            reply = f"Tu as dit : {text}"
                        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={reply}")
                        last_update_id = update_id
        except Exception as e:
            print("Erreur:", e)
        time.sleep(1)

# Lance le bot en thread
threading.Thread(target=telegram_bot).start()

# Lance Flask pour Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
