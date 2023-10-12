from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

# Création d'un blueprint contenant les routes ayant le préfixe /auth/...
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Route /auth/register
@auth_bp.route('/register', methods=('GET', 'POST'))
def register():

    # Si des données de formulaire sont envoyées vers la route /register (ce qui est le cas lorsque le formulaire d'inscription est envoyé)
    if request.method == 'POST':

        # On récupère les champs 'username' et 'password' de la requête HTTP
        adresse_mail = request.form['adresse_mail']
        Mot_de_passe = request.form['Mot_de_passe']
        Nom = request.form['Nom']
        Prenom = request.form['Prenom']
        date_de_naisssance = request.form['date_de_naisssance']
        no_de_telephone = request.form['no_de_telephone']

        # On récupère la base de donnée
        db = get_db()

        # Si le nom d'utilisateur et le mot de passe ont bien une valeur
        # on essaie d'insérer l'utilisateur dans la base de données
        if adresse_mail and Mot_de_passe and Nom and Prenom and date_de_naisssance and no_de_telephone:
            try:
                db.execute("INSERT INTO Personne (adresse_mail, Mot_de_passe, Nom, Prenom, date_de_naissance, no_de_telephone) VALUES (?, ?, ?, ?, ?, ?)",(adresse_mail, generate_password_hash(Mot_de_passe), Nom, Prenom, date_de_naisssance, no_de_telephone))
                # db.commit() permet de valider une modification de la base de données
                db.commit()
            except db.IntegrityError:

                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = f"User {adresse_mail} is already registered."
                flash(error)
                return redirect(url_for("auth.register"))
            
            return redirect(url_for("auth.login"))
         
        else:
            error = "adresse_mail or Mot_de_passe invalid"
            flash(error)
            return redirect(url_for("auth.login"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription
        return render_template('auth/register.html')

# Route /auth/login
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    # Si des données de formulaire sont envoyées vers la route /login (ce qui est le cas lorsque le formulaire de login est envoyé)
    if request.method == 'POST':

        # On récupère les champs 'username' et 'password' de la requête HTTP
        adresse_mail = request.form['adresse_mail']
        Mot_de_passe = request.form['Mot_de_passe']

        # On récupère la base de données
        db = get_db()
        
        # On récupère l'utilisateur avec le username spécifié (une contrainte dans la db indique que le nom d'utilisateur est unique)
        # La virgule après username est utilisée pour créer un tuple contenant une valeur unique
        Personne = db.execute('SELECT * FROM Personne WHERE adresse_mail = ?', (adresse_mail,)).fetchone()

        # Si aucun utilisateur n'est trouve ou si le mot de passe est incorrect
        # on crée une variable error 
        error = None
        if Personne is None:
            error = 'Incorrect adresse_mail.'
        elif not check_password_hash(Personne['Mot_de_passe'], Mot_de_passe):
            error = 'Incorrect Mot_de_passe.'

        # S'il n'y pas d'erreur, on ajoute l'id de l'utilisateur dans une variable de session
        # De cette manière, à chaque requête de l'utilisateur, on pourra récupérer l'id dans le cookie session
        if error is None:
            session.clear()
            session['Personne_ID'] = Personne['Personne_ID']
            # On redirige l'utilisateur vers la page principale une fois qu'il s'est connecté
            return redirect("/")
        
        else:
            # En cas d'erreur, on ajoute l'erreur dans la session et on redirige l'utilisateur vers le formulaire de login
            flash(error)
            return redirect(url_for("auth.login"))
    else:
        return render_template('auth/login.html')

# Route /auth/logout
@auth_bp.route('/logout')
def logout():
    # Se déconnecter consiste simplement à supprimer le cookie session
    session.clear()

    # On redirige l'utilisateur vers la page principale une fois qu'il s'est déconnecté
    return redirect("/")


# Fonction automatiquement appelée à chaque requête (avant d'entrer dans la route) sur une route appartenant au blueprint 'auth_bp'
# La fonction permet d'ajouter un attribut 'user' représentant l'utilisateur connecté dans l'objet 'g' 
@auth_bp.before_app_request
def load_logged_in_user():

    # On récupère l'id de l'utilisateur stocké dans le cookie session
    Personne_ID = session.get('Personne_ID')

    # Si l'id de l'utilisateur dans le cookie session est nul, cela signifie que l'utilisateur n'est pas connecté
    # On met donc l'attribut 'user' de l'objet 'g' à None
    if Personne_ID is None:
        g.Personne = None

    # Si l'id de l'utilisateur dans le cookie session n'est pas nul, on récupère l'utilisateur correspondant et on stocke
    # l'utilisateur comme un attribut de l'objet 'g'
    else:
         # On récupère la base de données et on récupère l'utilisateur correspondant à l'id stocké dans le cookie session
        db = get_db()
        g.Personne = db.execute('SELECT * FROM Personne WHERE Personne_ID = ?', (Personne_ID,)).fetchone()



