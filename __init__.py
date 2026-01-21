from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# ---------------------------
# Fonction d'authentification
# ---------------------------
def est_authentifie():
    return session.get('authentifie')


# ---------------------------
# Route accueil
# ---------------------------
@app.route('/')
def home():
    return render_template('hello.html')


# ---------------------------
# Route lecture / dashboard
# ---------------------------
@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    return render_template(
        'lecture.html',
        username=session.get('username'),
        role=session.get('role')
    )


# ---------------------------
# Route authentification
# ---------------------------
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    error = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Admin
        if username == 'admin' and password == 'password':
            session['authentifie'] = True
            session['username'] = 'admin'
            session['role'] = 'admin'
            return redirect(url_for('lecture'))

        # User simple
        elif username == 'user' and password == '12345':
            session['authentifie'] = True
            session['username'] = 'user'
            session['role'] = 'user'
            return redirect(url_for('lecture'))

        else:
            error = "Nom d'utilisateur ou mot de passe incorrect."

    return render_template('formulaire_authentification.html', error=error)


# ---------------------------
# Route consultation d'un livre par titre
# ---------------------------
@app.route('/fiche_livre/<titre>')
def fiche_livre(titre):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM livres WHERE titre LIKE ?', ('%' + titre + '%',))
        data = cursor.fetchall()

    return render_template('read_data.html', data=data)


# ---------------------------
# Route consultation de toute la bibliothèque
# ---------------------------
@app.route('/consultation/')
def ReadBDD():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM livres')
        data = cursor.fetchall()

    return render_template('read_data.html', data=data)


# ---------------------------
# Route pour ajouter un livre
# ---------------------------
@app.route('/enregistrer_livre', methods=['GET', 'POST'])
def enregistrer_livre():
    # Protection : seul admin
    if not est_authentifie() or session.get('role') != 'admin':
        return "Accès refusé : Seul l'administrateur peut ajouter des livres.", 403

    error = None

    if request.method == 'POST':
        titre = request.form.get('titre', '').strip()
        auteur = request.form.get('auteur', '').strip()
        annee = request.form.get('annee', '').strip()

        # Validation
        if not titre or not auteur:
            error = "Titre et auteur sont obligatoires."
            return render_template('formulaire_livre.html', error=error)

        # Conversion année
        try:
            annee = int(annee) if annee else None
        except ValueError:
            error = "Année invalide."
            return render_template('formulaire_livre.html', error=error)

        # Insertion dans la DB
        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO livres (titre, auteur, annee_publication) VALUES (?, ?, ?)',
                    (titre, auteur, annee)
                )
        except Exception as e:
            error = f"Erreur lors de l'enregistrement : {e}"
            return render_template('formulaire_livre.html', error=error)

        return redirect(url_for('ReadBDD'))

    return render_template('formulaire_livre.html', error=error)


# ---------------------------
# Route de déconnexion
# ---------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# ---------------------------
# Lancement de l'application
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
